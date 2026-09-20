"""Model router: which DeepSeek model answers which question, and what it cost.

Two models, one rule (docs/RESOURCE_PACK.md §1): the strong model does the work
that has to be *right* — corrective edits and reading a stack trace — and the
cheap model does the work that only has to be *labelled* — classification and
summaries. Routing every call to the strong model is the easiest way to lose
M3 for no M1 gain.

The key comes from the environment, never from code (golden rule 2, and
CONFIGURATION.md §2). With no key the router is simply unavailable: callers
check :attr:`Router.available` and skip the live path rather than crashing, so
the suite runs without a paid account.

Temperature is pinned low (NFR-6) because a migration that produces a different
patch on every run is not reproducible, and reproducibility is the deliverable.
"""

from __future__ import annotations

import os
from typing import Any, Literal

from dotenv import load_dotenv

from mra.state import Tokens, new_tokens

load_dotenv()

#: What a call is *for*. The task, not the model, is what callers name.
Task = Literal["edit", "trace", "classify", "summary"]

#: Task -> tier. Edits and trace reasoning are the accuracy-critical half.
TIER: dict[Task, str] = {
    "edit": "pro",
    "trace": "pro",
    "classify": "flash",
    "summary": "flash",
}

#: Off-peak DeepSeek list price, USD per million tokens, (input, output).
#: An estimate for reporting M3 cost, not a billing record — rates move, and
#: docs/05 §2.4 says to verify them at run time.
PRICES_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    "pro": (0.66, 1.98),
    "flash": (0.22, 0.66),
}

DEFAULT_BASE_URL = "https://api.deepseek.com"


def model_id(task: Task) -> str:
    """The configured model name for a task class."""
    if TIER[task] == "pro":
        return os.getenv("MRA_EDIT_MODEL", "deepseek-v4-pro")
    return os.getenv("MRA_UTILITY_MODEL", "deepseek-v4-flash")


def cost_usd(tokens: Tokens | dict[str, int]) -> float:
    """M3 cost from the token counters, per docs/05 §2.4."""
    total = 0.0
    for tier, (price_in, price_out) in PRICES_USD_PER_MTOK.items():
        total += tokens.get(f"{tier}_in", 0) * price_in / 1e6
        total += tokens.get(f"{tier}_out", 0) * price_out / 1e6
    return total


def total_tokens(tokens: Tokens | dict[str, int]) -> int:
    """Every token in and out, across both tiers — the M3 headline number."""
    return sum(tokens.get(key, 0) for key in
               ("pro_in", "pro_out", "flash_in", "flash_out"))


class Router:
    """Routes a task to its model and bills the result to a token ledger.

    ``tokens`` is the live ``MigrationState.tokens`` mapping (SRS §4.1); the
    router mutates it in place so that M3 is accumulated at the point of spend
    rather than reconstructed afterwards from logs.
    """

    def __init__(
        self,
        tokens: Tokens | None = None,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float | None = None,
        client: Any = None,
    ) -> None:
        self.tokens: Tokens = tokens if tokens is not None else new_tokens()
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or ""
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
        self.temperature = (
            temperature if temperature is not None
            else float(os.getenv("MRA_LLM_TEMPERATURE", "0.1"))
        )
        self._client = client
        #: (task, model, in, out) per call, for the trajectory.
        self.calls: list[dict[str, Any]] = []

    @property
    def available(self) -> bool:
        """True when a live call can be made. False means: skip, do not fail."""
        return bool(self._client or self.api_key)

    @property
    def client(self) -> Any:
        if self._client is None:
            from openai import OpenAI  # imported lazily: no key, no client, no import cost

            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def complete(self, task: Task, system: str, user: str, *, max_tokens: int = 4096) -> str:
        """One chat completion for ``task``; bills its tokens and returns the text."""
        if not self.available:
            raise RuntimeError("DEEPSEEK_API_KEY is not set; check Router.available first")
        model = model_id(task)
        response = self.client.chat.completions.create(
            model=model,
            temperature=self.temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        usage = getattr(response, "usage", None)
        tokens_in = int(getattr(usage, "prompt_tokens", 0) or 0)
        tokens_out = int(getattr(usage, "completion_tokens", 0) or 0)
        self._bill(task, model, tokens_in, tokens_out)
        return response.choices[0].message.content or ""

    def _bill(self, task: Task, model: str, tokens_in: int, tokens_out: int) -> None:
        tier = TIER[task]
        self.tokens[f"{tier}_in"] = self.tokens.get(f"{tier}_in", 0) + tokens_in  # type: ignore[literal-required]
        self.tokens[f"{tier}_out"] = self.tokens.get(f"{tier}_out", 0) + tokens_out  # type: ignore[literal-required]
        self.tokens["tool_calls"] = self.tokens.get("tool_calls", 0) + 1
        # The model ID and the counts are loggable; the key never is (CONFIGURATION.md §6).
        self.calls.append(
            {"task": task, "model": model, "tokens_in": tokens_in, "tokens_out": tokens_out}
        )

    def cost_usd(self) -> float:
        return cost_usd(self.tokens)
