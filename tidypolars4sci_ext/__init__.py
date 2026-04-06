"""
tidypolars4sci_ext — Extension package for tidypolars4sci.

Re-exports everything from the original ``tidypolars4sci`` and layers on
additional functions and an extended ``tibble`` class with new methods.

Usage::

    import tidypolars4sci_ext as tp

    # All original tidypolars4sci symbols are available
    df = tp.tibble(x=[1, 2, 3], y=['a', 'b', 'c'])

    # Plus new functions such as:
    df.mutate(label=tp.case_match(tp.col('x'), 1, 'one', _default='other'))
    df.slice_min('x', n=2)
    df.right_join(other_df, on='x')
"""

try:
    from importlib.metadata import version
    __version__ = version("tidypolars4sci_ext")
except Exception:
    __version__ = ""

# ── Step 1: Re-export everything from the upstream package ─────────────
from tidypolars4sci import *           # noqa: F401,F403
from tidypolars4sci import (           # noqa: F401
    API_labels,
)

# Re-export upstream functions that exist but are not included in __all__
from tidypolars4sci.funs import (      # noqa: F401
    between, coalesce, if_else, lead, rep, replace_null, row_number,
)

# Re-export lubridate functions (upstream has the module but doesn't import it)
from tidypolars4sci.lubridate import * # noqa: F401,F403

# Re-export log, log10, sqrt which exist in upstream stats but not in its __all__
from tidypolars4sci.stats import log, log10, sqrt  # noqa: F401

# ── Step 2: Monkey-patch upstream from_polars / from_pandas ────────────
#
# The upstream tibble methods (arrange, filter, mutate, …) all call
#   ``.pipe(from_polars)``
# internally.  If we don't patch that function, every inherited method
# will return the *base* tibble — losing our extension methods.
#
# By replacing ``tidypolars4sci.tibble_df.from_polars`` (and from_pandas)
# with our versions, every existing method will transparently return the
# *extended* tibble.

import tidypolars4sci.tibble_df as _upstream_tdf
from .ext_tibble import (             # noqa: F401
    tibble,
    TibbleGroupBy,
    from_polars,
    from_pandas,
    __get_accepted_output_formats__,
)

# Patch the module-level conversion helpers so inherited methods return our type.
# IMPORTANT: Do NOT patch _upstream_tdf.tibble or _upstream_tdf.TibbleGroupBy —
# the upstream code uses ``super(tibble, self)`` calls that depend on ``tibble``
# referring to the *upstream* class in the MRO, not the extension class.
_upstream_tdf.from_polars = from_polars
_upstream_tdf.from_pandas = from_pandas

# ── Step 3: Import new standalone functions ─────────────────────────────
from .ext_funs import *               # noqa: F401,F403
from .ext_helpers import *            # noqa: F401,F403
from .ext_stats import *              # noqa: F401,F403
