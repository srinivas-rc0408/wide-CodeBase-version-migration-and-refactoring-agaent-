"""EDIT node: apply the migration codemod to the files the analyzer flagged.

A plain function for now; LangGraph wiring arrives in P4. It edits only files
that hold a reported call site — never the whole tree — so a file the analyzer
did not flag cannot be touched by accident (NB-2).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import libcst as cst
from libcst.codemod import CodemodContext

from mra.codemods.datetime_utcnow import ConvertUtcnowCommand


def apply_codemod(
    repo: Path | str,
    call_sites: dict[str, list[dict[str, Any]]],
    command_type: type[ConvertUtcnowCommand] = ConvertUtcnowCommand,
) -> list[str]:
    """Run the codemod over every file in ``call_sites``; return the ones that changed.

    Writes in place, so ``repo`` must already be the writable copy — never the
    corpus source.
    """
    repo = Path(repo)
    changed: list[str] = []
    for relative in sorted(call_sites):
        path = repo / relative
        source = path.read_text()
        command = command_type(CodemodContext(filename=str(path)))
        # transform_module (not _impl) also runs the scheduled AddImportsVisitor.
        migrated = command.transform_module(cst.parse_module(source)).code
        if migrated != source:
            path.write_text(migrated)
            changed.append(relative)
    return changed
