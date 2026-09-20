"""EDIT node: apply the migration codemod to the files the analyzer flagged.

It edits only files that hold a reported call site — never the whole tree — so
a file the analyzer did not flag cannot be touched by accident (NB-2).
:func:`apply_codemod` is the transform; :func:`make_edit_node` wraps it as the
LangGraph node, which consumes one batch of ``edit_batches`` per visit.
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


def make_edit_node(runs_dir_unused: Any = None):
    """Bind nothing and return the node LangGraph calls.

    The node edits ``edit_batches[current_batch]`` and then advances the index,
    so ``current_batch`` always names the batch that is *next*. docs/04 §2.3
    increments it inside ``route_after_test`` instead, which cannot work: a
    LangGraph router is handed a read-only view and its mutations are never
    written back as channel updates. The routing *decision* is unchanged; only
    the place the counter moves is.
    """

    def edit_node(state: dict[str, Any]) -> dict[str, Any]:
        from mra.sandbox import snapshot

        batches: list[list[str]] = state.get("edit_batches") or []
        index = int(state.get("current_batch", 0))
        if index >= len(batches):
            return {"note": {"action": "no batch left to edit", "detail": {"batch": index}}}

        batch = batches[index]
        repo = Path(state["repo_path"])
        sha = snapshot(repo, f"pre-edit snapshot for batch {index}")
        call_sites = state.get("call_sites") or {}
        changed = apply_codemod(repo, {file: call_sites.get(file, []) for file in batch})

        status = dict(state.get("file_status") or {})
        for file in batch:
            # A file the codemod did not touch was already migrated — by an
            # earlier recovery round, typically — not skipped.
            status[file] = "migrated"
        return {
            "current_batch": index + 1,
            "file_status": status,
            "note": {
                "action": f"batch {index}: codemod changed {len(changed)} of "
                          f"{len(batch)} file(s)",
                "detail": {"batch": index, "files": batch, "changed": changed, "sha": sha},
            },
        }

    return edit_node
