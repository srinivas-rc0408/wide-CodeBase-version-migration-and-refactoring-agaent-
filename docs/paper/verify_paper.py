"""Check paper.md against the artefacts it cites. Run after any benchmark rerun.

The paper's provenance rule (see its header comment) is that a `<!-- SOURCE: -->`
comment covers every line above it back to the previous SOURCE or the nearest
heading. This script enforces that rule mechanically for §7, re-diffs the §7.1
grid against results.md, and re-derives the §8 counts from failure-analysis.md
and results.json. It exists because the §7.1 grid has silently gone stale once.

    python docs/paper/verify_paper.py      # exit 0 = every check passes
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs/paper/paper.md"
RESULTS_MD = ROOT / "runs/benchmark/results.md"
RESULTS_JSON = ROOT / "runs/benchmark/results.json"
FAILURES_MD = ROOT / "runs/benchmark/failure-analysis.md"

GRID_HEADER = (
    "| task / config | outcome | M1 recall | M1 prec | M1 F1 | M2 % "
    "| regr | corr | steps | tokens | cost $ | wall s |"
)
# `task05` is an identifier, not a figure; don't treat its digits as a claim.
IDENTIFIER_DIGITS = re.compile(r"task0\d|V4-|c-i{1,3}\b|§\d|FR-\d|NB-\d|NFR-\d|M[123]\b")
# Padding words cut from §1 by hand; a later pass must not reintroduce them.
INTENSIFIERS = r"\b(?:completely|absolutely|merely|significantly)\b"

results: list[tuple[bool, str]] = []


def check(condition: bool, message: str) -> None:
    results.append((bool(condition), message))


def table_after(lines: list[str], header: str) -> list[str]:
    i = lines.index(header)
    out = []
    while i < len(lines) and lines[i].startswith("|"):
        out.append(lines[i])
        i += 1
    return out


def carries_a_figure(line: str) -> bool:
    """True if the line states a number, ignoring identifiers that contain digits."""
    return bool(re.search(r"\d", IDENTIFIER_DIGITS.sub("", line)))


def section(lines: list[str], start: str, end: str) -> tuple[int, int]:
    s = next(i for i, line in enumerate(lines) if line.startswith(start))
    e = next(i for i, line in enumerate(lines) if line.startswith(end))
    return s, e


def main() -> int:
    paper = PAPER.read_text()
    lines = paper.split("\n")

    # 1. §7.1 is spliced from results.md §1, not transcribed. Prove it.
    src_grid = table_after(RESULTS_MD.read_text().split("\n"), GRID_HEADER)
    paper_grid = table_after(lines, GRID_HEADER)
    check(
        src_grid == paper_grid,
        f"§7.1 grid is byte-identical to results.md §1 ({len(src_grid) - 2} data rows)",
    )

    # 2. Provenance: no numeric span in §7 may close without a SOURCE pointer.
    s, e = section(lines, "# 7. Results", "# 8. Failure")
    pending: int | None = None
    pointers = 0
    gaps: list[str] = []
    in_comment = False
    for k in range(s + 1, e):
        line = lines[k]
        if in_comment:
            in_comment = "-->" not in line
            continue
        if line.lstrip().startswith("<!--"):
            in_comment = "-->" not in line
            pointers += 1
            pending = None
            continue
        if line.startswith("#"):
            if pending is not None:
                gaps.append(f"line {pending + 1}: {lines[pending][:60]!r}")
            pending = None
            continue
        if not line.startswith(">") and carries_a_figure(line) and pending is None:
            pending = k
    if pending is not None:
        gaps.append(f"line {pending + 1}: {lines[pending][:60]!r}")
    check(not gaps, f"§7: every numeric span closed by a SOURCE pointer ({pointers} pointers)")
    for gap in gaps:
        print(f"    uncovered -> {gap}")

    # 3. §8 counts are re-derived, never typed.
    failures = FAILURES_MD.read_text()
    pairs = failures.count("\n## `")
    behaviour = failures.count("**behaviour** break")
    disabled = failures.count("why it was not recovered:** recovery disabled")
    check(
        "42 of 165 runs failed" in failures and "42 did not reach green" in paper,
        "§8: 42 of 165 runs failed",
    )
    check(pairs == 14 and "14 distinct" in paper, f"§8: {pairs} distinct (config, task) pairs")
    check(
        behaviour == 26 and "all 26 surviving failures" in paper,
        f"§8: {behaviour}/{behaviour} surviving failures classify as behaviour",
    )
    check(disabled == pairs, f"§8: all {pairs} pairs cite a disabled loop, not an exhausted one")

    # 4. The retry-cap claim, straight from the run records.
    data = json.loads(RESULTS_JSON.read_text())
    rows = data["rows"]
    peak = lambda r: max((r.get("fix_attempts") or {"_": 0}).values())  # noqa: E731
    at_cap = sorted({(r["config"], r["task_id"], r["outcome"]) for r in rows if peak(r) == 3})
    exhausted = [r for r in rows if r["outcome"] == "gave_up" and peak(r) >= 3]
    check(
        max(peak(r) for r in rows) == 3 and not exhausted,
        "§8: no run gave up by exhausting MAX_FIX_ATTEMPTS = 3",
    )
    check(
        len(at_cap) == 2 and all(o == "success" for _, _, o in at_cap),
        f"§8: the cap is reached only by {', '.join(c for c, _, _ in at_cap)} — both green",
    )
    check(
        len(rows) == 165 and len(data["skipped"]) == 10,
        "§6/§7.6: 165 offline rows, 10 pairs skipped for want of a key",
    )

    # 5. The prose sections stay stubs, and §2 invents no citation.
    # §1 is written, so it is checked for what it must NOT contain instead.
    for heading in (
        "# Abstract",
        "# 2. Related Work",
        "# 10. Conclusion",
        "# References",
    ):
        body = "\n".join(lines[lines.index(heading) : lines.index(heading) + 6])
        check("STUB" in body, f"stub preserved: {heading.lstrip('# ')}")
    intro_start, intro_end = section(lines, "# 1. Introduction", "# 2. Related Work")
    intro = "\n".join(lines[intro_start:intro_end])
    check("STUB" not in intro, "§1: written — the stub outline is gone")
    padding = sorted(set(re.findall(INTENSIFIERS, intro, re.IGNORECASE)))
    check(
        not padding,
        f"§1: no intensifier padding{' — found ' + ', '.join(padding)}"
        if padding
        else "§1: no intensifier padding",
    )
    lit_start, lit_end = section(lines, "# 2. Related Work", "# 3. System")
    related = "\n".join(lines[lit_start:lit_end])
    check(
        related.count("[CITE:") == 9,
        f"§2: {related.count('[CITE:')} unresolved [CITE:] placeholders",
    )
    check(
        not re.search(r"\n\[\d+\]\s|\n- [A-Z][a-z]+,\s+[A-Z]\.", paper),
        "§2/References: no reference filled in yet, so none can be fabricated",
    )

    width = max(len(m) for _, m in results)
    for passed, message in results:
        print(f"{'PASS' if passed else 'FAIL'}  {message.ljust(width)}")
    failed = sum(1 for passed, _ in results if not passed)
    print(f"\n{len(results) - failed}/{len(results)} checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
