"""
Extension functions for tidypolars4sci.

New standalone functions not present in the upstream package:
- case_match: switch-like pattern matching on values
- na_if: replace a specific value with null
- consecutive_id: generate consecutive group IDs on value changes
- expand_grid: standalone Cartesian product of named lists
- nesting: tibble of observed (existing) combinations only
"""
import polars as pl
from tidypolars4sci.utils import (
    _col_expr,
    _is_constant,
    _is_iterable,
    _is_list,
    _is_series,
    _str_to_lit,
)

__all__ = [
    "case_match",
    "na_if",
    "consecutive_id",
    "expand_grid",
    "nesting",
    "rep",  # override upstream version to fix tibble isinstance check
]


def case_match(x, *args, _default=None):
    """
    Pattern matching (switch-like): match values and return corresponding results

    Parameters
    ----------
    x : Expr, str
        Column to match against
    *args : pairs of (match_value(s), result)
        Alternating match values and results. Match values can be
        a single value or a list of values.
    _default : optional
        Default value if no match

    Examples
    --------
    >>> df.mutate(
    >>>    label = tp.case_match(col('x'),
    >>>                          1, 'one',
    >>>                          [2, 3], 'two_or_three',
    >>>                          _default = 'other')
    >>> )
    """
    if len(args) == 0 or len(args) % 2 != 0:
        raise ValueError("case_match requires pairs of (match_value, result) arguments")
    x = _col_expr(x)
    match_vals = [args[i] for i in range(0, len(args), 2)]
    results = [args[i] for i in range(1, len(args), 2)]
    results = [_str_to_lit(r) for r in results]
    for i in range(len(match_vals)):
        if isinstance(match_vals[i], list):
            cond = x.is_in(match_vals[i])
        else:
            cond = x == _str_to_lit(match_vals[i])
        if i == 0:
            expr = pl.when(cond).then(results[i])
        else:
            expr = expr.when(cond).then(results[i])
    _default = _str_to_lit(_default)
    expr = expr.otherwise(_default)
    return expr


def na_if(x, value):
    """
    Replace a specific value with null/NA

    Parameters
    ----------
    x : Expr, str
        Column to operate on
    value :
        Value to replace with null

    Examples
    --------
    >>> df.mutate(x = tp.na_if(col('x'), 0))
    """
    x = _col_expr(x)
    return pl.when(x == value).then(None).otherwise(x)


def consecutive_id(*args):
    """
    Generate consecutive group IDs based on changes in one or more columns

    Parameters
    ----------
    *args : str, Expr
        Columns to track changes in

    Examples
    --------
    >>> df = tp.tibble(x = ['a', 'a', 'b', 'b', 'a'])
    >>> df.mutate(id = tp.consecutive_id('x'))
    """
    import functools
    cols = [_col_expr(x) for x in args]
    changes = [c != c.shift(1) for c in cols]
    combined = functools.reduce(lambda a, b: a | b, changes)
    return combined.fill_null(True).cast(pl.Int64).cum_sum()


def expand_grid(**kwargs):
    """
    Create a tibble of all combinations of provided values (standalone function)

    Parameters
    ----------
    **kwargs :
        Named lists of values to expand

    Examples
    --------
    >>> tp.expand_grid(x = [1, 2], y = ['a', 'b'])
    """
    from .ext_tibble import tibble
    items = list(kwargs.items())
    result = tibble({items[0][0]: items[0][1]})
    for name, values in items[1:]:
        right = tibble({name: values})
        result = result.cross_join(right)
    return result


def nesting(*args, **kwargs):
    """
    Create a tibble of existing (observed) combinations only.
    Used with complete() and expand() to specify columns that
    should only include combinations that appear in the data.

    Parameters
    ----------
    *args : tibble
        A tibble to extract unique combinations from
    **kwargs :
        Named columns with values

    Examples
    --------
    >>> tp.nesting(x = [1, 1, 2], y = ['a', 'b', 'a'])
    """
    from .ext_tibble import tibble
    if len(kwargs) > 0:
        df = tibble(kwargs)
        return df.distinct()
    elif len(args) == 1:
        return args[0].distinct()
    else:
        raise ValueError("Provide either a tibble or keyword arguments")


def rep(x, times=1):
    """
    Replicate the values in x

    Parameters
    ----------
    x : const, Series
        Value or Series to repeat
    times : int
        Number of times to repeat

    Examples
    --------
    >>> tp.rep(1, 3)
    >>> tp.rep(pl.Series(range(3)), 3)
    """
    if _is_constant(x):
        out = [x]
    elif _is_series(x):
        out = x.to_list()
    elif _is_list(x):
        out = x
    elif hasattr(x, 'bind_rows'):  # tibble-like
        from .ext_tibble import from_polars
        out = pl.concat([x for _ in range(times)]).pipe(from_polars)
    elif _is_iterable(x):
        out = list(x)
    else:
        raise ValueError("Incompatible type")
    if _is_list(out):
        out = pl.Series(out * times)
    return out
