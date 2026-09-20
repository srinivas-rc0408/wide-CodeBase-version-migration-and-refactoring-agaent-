# Configuration & Secrets

How to configure the MRA and manage API keys **securely**. This document contains no secrets — real keys live only in your local, gitignored `.env` file.

> **Why there is no `api_keys.md`:** putting API keys in a markdown (or any tracked) file is how secrets get committed to git and leaked publicly. Once a key is in git history it is compromised even after deletion. Keys go in environment variables, loaded from a `.env` file that git ignores. This is the standard, non-negotiable pattern.

## 1. First-time setup

```bash
cp .env.example .env      # create your local, private config
$EDITOR .env              # fill in real values
```

`.env` is listed in `.gitignore`. Verify it is ignored before your first commit:

```bash
git check-ignore .env     # should print: .env
git status                # .env must NOT appear as a tracked/staged file
```

## 2. Required keys

| Variable | What it is | Where to get it |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek API key (edits + recovery + summaries) | Sign up at `platform.deepseek.com`; new accounts get 5M free tokens. |

## 3. Optional keys

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Only if you route some calls to Groq. |
| `OPENROUTER_API_KEY` | Only if you route via OpenRouter. |

## 4. Configuration variables (non-secret)

These tune the agent and mirror the non-functional constraints in `docs/03_SRS.md §6`. Defaults are in `.env.example`.

| Variable | Meaning | Default |
|---|---|---|
| `MRA_EDIT_MODEL` | Strong model for edits/trace reasoning | `deepseek-v4-pro` |
| `MRA_UTILITY_MODEL` | Cheap model for summaries/classification | `deepseek-v4-flash` |
| `MRA_MAX_FIX_ATTEMPTS` | Recovery retry ceiling per failure signature | `3` |
| `MRA_TOKEN_BUDGET` | Hard per-task token ceiling (abort + flag if exceeded) | `2000000` |
| `MRA_RUN_TIMEOUT_SEC` | Per-run wall-clock timeout | `1800` |
| `MRA_PYTEST_TIMEOUT_SEC` | Per-`pytest` invocation timeout (in sandbox) | `120` |
| `MRA_EDIT_BATCH_SIZE` | Files per EDIT batch (ablation variable) | `3` |
| `MRA_LLM_TEMPERATURE` | Edit temperature (determinism) | `0.1` |
| `MRA_SANDBOX_IMAGE` | Docker image tag for the sandbox | `mra-sandbox:py312` |
| `MRA_CONTAINER_RUNTIME` | `docker` or `podman` | `docker` |

## 5. Loading config in code

Use `python-dotenv` (add to `pyproject.toml`) and read from the environment. Never hard-code a key.

```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env in development; in CI/containers use real env vars

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]   # KeyError early if missing — good
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
EDIT_MODEL = os.getenv("MRA_EDIT_MODEL", "deepseek-v4-pro")
```

Pass the key to the OpenAI-compatible client:

```python
from openai import OpenAI
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)
```

## 6. Security rules

- **Never** commit `.env`, a key, or a token. If `git status` ever shows `.env`, stop and fix `.gitignore`.
- **Never** print a key to logs or the trajectory. Log the *model ID* and *token counts*, not credentials.
- **Never** pass secrets in URL query strings.
- **If a key is exposed** (pushed to a public repo, pasted in an issue), **rotate it immediately** at the provider and purge git history if needed.
- Inside the sandbox, the agent runs with `--network none` at execution time; the key is used only by the host-side orchestrator that calls the LLM API, not inside the code-execution container.
- Keep `.env.example` in sync with `.env` **keys** (names only, placeholder values) so collaborators know what to set.

## 7. CI / grading environments

For CI or a shared grading machine, set the same variables as real environment secrets (e.g. repository secrets), not a committed file. The code reads `os.environ` either way, so no code changes are needed.
