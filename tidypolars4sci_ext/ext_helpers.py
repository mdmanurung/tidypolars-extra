"""
Extension helper functions for tidypolars4sci.

New helper functions not present in the upstream package:
- if_all: check if all conditions are true across columns
- if_any: check if any condition is true across columns
"""
import functools
from tidypolars4sci.utils import (
    _as_list,
    _col_exprs,
)

__all__ = [
    "if_all",
    "if_any",
]


def if_all(cols, fn=lambda x: x.is_not_null()):
    """
    Check if all conditions are true across columns

    Parameters
    ----------
    cols : list
        Columns to check
    fn : callable
        Function returning a boolean expression for each column

    Examples
    --------
    >>> df.filter(tp.if_all(['x', 'y'], lambda c: c > 0))
    """
    _cols = _col_exprs(_as_list(cols))
    exprs = [fn(c) for c in _cols]
    return functools.reduce(lambda a, b: a & b, exprs)


def if_any(cols, fn=lambda x: x.is_not_null()):
    """
    Check if any condition is true across columns

    Parameters
    ----------
    cols : list
        Columns to check
    fn : callable
        Function returning a boolean expression for each column

    Examples
    --------
    >>> df.filter(tp.if_any(['x', 'y'], lambda c: c > 0))
    """
    _cols = _col_exprs(_as_list(cols))
    exprs = [fn(c) for c in _cols]
    return functools.reduce(lambda a, b: a | b, exprs)
