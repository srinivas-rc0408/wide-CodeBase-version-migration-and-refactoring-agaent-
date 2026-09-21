"""Start-up bookkeeping. Both of its constants are computed at *import* time.

That is what makes this module the fixture's tripwire. :data:`STARTED_AT` is
this module's own clock reading and :data:`STARTUP_LAG_S` hands it straight
back to :mod:`pkg.timebase`. Migrate this file while ``timebase`` has not
moved and the aware stamp meets a naive clock, :func:`~pkg.timebase.aligned`
refuses to downgrade it, and :func:`~pkg.timebase.elapsed_since` raises a
named ``TypeError`` *while the module is being imported* — so every test
module that reaches this package errors during collection, not at test time.
"""

from datetime import datetime

from pkg.timebase import elapsed_since

#: This process's start, stamped as the module is first imported.
STARTED_AT = datetime.utcnow()

#: How long the package took to reach this line. Evaluated at import time.
STARTUP_LAG_S = elapsed_since(STARTED_AT)


def uptime_s() -> float:
    """Seconds since :data:`STARTED_AT`."""
    return elapsed_since(STARTED_AT)
