"""Find every call to a target symbol, whatever spelling the file uses.

This is FR-1, and the import resolution is the whole point. The same function
reaches the source three ways:

    from datetime import datetime  ->  datetime.utcnow()
    import datetime               ->  datetime.datetime.utcnow()
    import datetime as dt         ->  dt.datetime.utcnow()

A matcher written against one spelling scores zero on the others, and a regex
scores zero on all but the first. So every call is flattened to a dotted path,
its head is resolved through the module's own import bindings, and the result
is compared against one fully-qualified target. All three spellings above
resolve to ``datetime.datetime.utcnow``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import libcst as cst
from libcst.metadata import ImportAssignment, MetadataWrapper, PositionProvider, ScopeProvider

from mra.analysis.dep_graph import python_files


@dataclass(frozen=True)
class CallSite:
    """One located call, in the ``mra:call_site`` shape (SRS §4.2)."""

    file: str
    line: int
    col: int
    symbol: str
    kind: str = "call"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _dotted(node: cst.BaseExpression) -> tuple[cst.Name, list[str]] | None:
    """Flatten ``a.b.c`` into its head ``Name`` node and the attribute names after it.

    Returns None for anything that is not a plain dotted path — ``f().g()``,
    ``obj[0].g()``, a call on a literal — because those cannot be resolved
    statically through imports and must not be guessed at.
    """
    attributes: list[str] = []
    current = node
    while isinstance(current, cst.Attribute):
        attributes.append(current.attr.value)
        current = current.value
    if not isinstance(current, cst.Name):
        return None
    return current, list(reversed(attributes))


def _module_name(node: cst.BaseExpression) -> str:
    """Dotted text of an import's module expression (``a.b.c``)."""
    if isinstance(node, cst.Name):
        return node.value
    if isinstance(node, cst.Attribute):
        return f"{_module_name(node.value)}.{node.attr.value}"
    return ""


class _CallSiteVisitor(cst.CSTVisitor):
    """Collects import bindings, then resolves every dotted call against them."""

    METADATA_DEPENDENCIES = (PositionProvider, ScopeProvider)

    def __init__(self, target: str, file: str) -> None:
        self.target = target
        self.file = file
        #: local name -> fully-qualified thing it is bound to
        self.bindings: dict[str, str] = {}
        self.sites: list[CallSite] = []

    # -- binding collection -------------------------------------------------

    def visit_Import(self, node: cst.Import) -> None:
        for alias in node.names:
            dotted = _module_name(alias.name)
            if not dotted:
                continue
            if alias.asname is not None:
                # `import a.b as x` binds x -> a.b
                self.bindings[str(alias.evaluated_alias)] = dotted
            else:
                # `import a.b` binds only the head package, a -> a
                head = dotted.split(".")[0]
                self.bindings[head] = head

    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
        if isinstance(node.names, cst.ImportStar):
            # A star import binds names we cannot see without importing the
            # module. Resolving it is out of scope; skipping it costs recall,
            # inventing bindings would cost precision.
            return
        module = _module_name(node.module) if node.module is not None else ""
        for alias in node.names:
            name = str(alias.evaluated_name)
            binding = str(alias.evaluated_alias) if alias.asname is not None else name
            self.bindings[binding] = f"{module}.{name}" if module else name

    # -- resolution ---------------------------------------------------------

    def _shadowed(self, head: cst.Name) -> bool:
        """True if ``head`` is bound by anything other than an import here.

        Guards precision: a local ``datetime = FakeClock()`` makes
        ``datetime.utcnow()`` a different function entirely, and editing it
        would be a wrong edit, not a missed one.
        """
        try:
            scope = self.get_metadata(ScopeProvider, head)
        except KeyError:
            return False  # no scope info; fall back to the binding pass
        if scope is None:
            return False
        assignments = list(scope[head.value])
        if not assignments:
            return False
        return not all(isinstance(a, ImportAssignment) for a in assignments)

    def visit_Call(self, node: cst.Call) -> None:
        flattened = _dotted(node.func)
        if flattened is None:
            return
        head, attributes = flattened
        base = self.bindings.get(head.value)
        if base is None or self._shadowed(head):
            return
        resolved = ".".join([base, *attributes]) if attributes else base
        if resolved != self.target:
            return
        position = self.get_metadata(PositionProvider, node).start
        self.sites.append(
            CallSite(file=self.file, line=position.line, col=position.column, symbol=resolved)
        )


def find_in_source(source: str, target: str, file: str) -> list[CallSite]:
    """Locate every call to ``target`` in one module's source text."""
    wrapper = MetadataWrapper(cst.parse_module(source))
    visitor = _CallSiteVisitor(target=target, file=file)
    wrapper.visit(visitor)
    return visitor.sites


def find_in_repo(
    repo: Path | str, target: str, files: list[Path] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """Scan a repo for ``target`` and return the ``MigrationState.call_sites`` map.

    Shape is ``{repo-relative file: [call_site, ...]}`` (SRS §4.1). Files with
    no hit are omitted, so ``|A|`` is the sum of the list lengths.
    """
    repo = Path(repo)
    found: dict[str, list[dict[str, Any]]] = {}
    for path in files if files is not None else python_files(repo):
        relative = path.relative_to(repo).as_posix()
        sites = find_in_source(path.read_text(), target, relative)
        if sites:
            found[relative] = [site.to_dict() for site in sites]
    return found
