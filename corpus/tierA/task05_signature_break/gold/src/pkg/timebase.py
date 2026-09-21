"""The package clock, and the one place its contract is enforced.

Every module reads the time through :func:`utc_now`, and every module that
compares a stamp it was *handed* against that reading goes through
:func:`elapsed_since`. That makes this module the contract owner: when
``utc_now`` stops returning naive UTC and starts returning an aware datetime,
the shape of every stamp in the package moves with it.

:func:`aligned` is the migration shim, and it is deliberately one-way. A
*naive* stamp from a module that has not been migrated yet can be read as UTC,
because naive-UTC is exactly what the old contract promised it was. An *aware*
stamp handed to a clock that is still naive cannot be repaired the same way:
dropping a ``tzinfo`` would silently reinterpret the value, so the stamp is
passed through untouched and :func:`elapsed_since` raises ``TypeError``.

The asymmetry is the fixture. A caller may be migrated *after* this module —
that window is safe. A caller migrated *before* it is a hard error.
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """The current UTC time, in whatever shape the package contract is in."""
    return datetime.now(timezone.utc)


def aligned(stamp: datetime, reference: datetime) -> datetime:
    """Read ``stamp`` in the shape ``reference`` is in. Upgrades only, never downgrades."""
    if stamp.tzinfo is None and reference.tzinfo is not None:
        return stamp.replace(tzinfo=timezone.utc)
    return stamp


def elapsed_since(stamp: datetime) -> float:
    """Seconds between ``stamp`` and now, for a stamp this package produced.

    The contract is checked before the arithmetic, so a caller that ran ahead
    of this module gets a named, deterministic ``TypeError`` naming the
    ordering violation rather than the stdlib's generic subtraction error.
    """
    reference = utc_now()
    stamp = aligned(stamp, reference)
    if (stamp.tzinfo is None) != (reference.tzinfo is None):
        raise TypeError(
            "pkg.timebase clock contract violated: the stamp is timezone-aware "
            "and the package clock is still naive. A caller was migrated before "
            "pkg/timebase.py; migrate the contract owner first."
        )
    return (reference - stamp).total_seconds()
