"""T1 codemod: ``datetime.utcnow()`` -> ``datetime.now(timezone.utc)``.

Deterministic, so it is a codemod and not an LLM call (golden rule 5): exact,
reproducible, and zero tokens against M3.

The edit is not one rewrite but two, and picking the wrong one costs precision:

    from datetime import datetime   datetime.utcnow()
                                 -> datetime.now(timezone.utc)      + import
    import datetime                datetime.datetime.utcnow()
                                 -> datetime.datetime.now(datetime.timezone.utc)
    import datetime as dt          dt.datetime.utcnow()
                                 -> dt.datetime.now(dt.timezone.utc)

Only the from-import form needs a new import. Under a module import the
timezone is already reachable through the same binding, so adding
``from datetime import timezone`` there is an unnecessary edit — exactly what
task02 was built to catch.
"""

from __future__ import annotations

import libcst as cst
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

from mra.analysis.call_sites import bindings_of, dotted_path

#: The symbol this codemod migrates, as the analyzer resolves it.
TARGET = "datetime.datetime.utcnow"

#: What each binding form resolves to, and what it implies about imports.
_CLASS_BINDING = "datetime.datetime"  # from datetime import datetime [as d]
_MODULE_BINDING = "datetime"  # import datetime [as dt]


class ConvertUtcnowCommand(VisitorBasedCodemodCommand):
    """Rewrite every resolved ``datetime.utcnow()`` call, whatever its spelling."""

    DESCRIPTION = "Replace datetime.utcnow() with datetime.now(timezone.utc)."

    def __init__(self, context) -> None:
        super().__init__(context)
        self.bindings: dict[str, str] = {}
        #: repo-facing record of what changed, for the trajectory.
        self.edits: list[str] = []

    def transform_module_impl(self, tree: cst.Module) -> cst.Module:
        # Bindings are collected up front rather than during traversal, so a
        # call inside a function defined above the import still resolves.
        self.bindings = bindings_of(tree)
        return super().transform_module_impl(tree)

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        flattened = dotted_path(updated_node.func)
        if flattened is None or updated_node.args:
            # utcnow() takes no arguments; anything with args is not our target.
            return updated_node
        head, attributes = flattened
        base = self.bindings.get(head.value)
        if base is None:
            return updated_node
        if ".".join([base, *attributes]) != TARGET:
            return updated_node

        # `.with_changes(attr=...)` keeps the receiver node untouched, so
        # whitespace, comments and the original spelling all survive (FR-5).
        new_func = updated_node.func.with_changes(attr=cst.Name("now"))

        if base == _CLASS_BINDING:
            # `datetime` here is the class; timezone has to be imported.
            AddImportsVisitor.add_needed_import(self.context, "datetime", "timezone")
            timezone = cst.Attribute(value=cst.Name("timezone"), attr=cst.Name("utc"))
        elif base == _MODULE_BINDING:
            # `dt.timezone` rides the import that is already there.
            timezone = cst.Attribute(
                value=cst.Attribute(value=cst.Name(head.value), attr=cst.Name("timezone")),
                attr=cst.Name("utc"),
            )
        else:  # pragma: no cover - TARGET only resolves through the two above
            return updated_node

        self.edits.append(f"{head.value}.{'.'.join(attributes)} -> now(...)")
        return updated_node.with_changes(func=new_func, args=[cst.Arg(value=timezone)])
