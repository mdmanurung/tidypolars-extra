"""
Extension statistics functions for tidypolars4sci.

New ranking, cumulative, and math functions not present in the upstream package:
- dense_rank, min_rank, percent_rank, cume_dist, ntile
- nth
- cumall, cumany, cummean
"""
import polars as pl
from tidypolars4sci.utils import _col_expr

__all__ = [
    # Ranking functions
    "dense_rank",
    "min_rank",
    "percent_rank",
    "cume_dist",
    "ntile",
    # Positional
    "nth",
    # Cumulative
    "cumall",
    "cumany",
    "cummean",
]


def dense_rank(x):
    """
    Rank with no gaps between consecutive ranks for tied values

    Parameters
    ----------
    x : Expr, str
        Column to rank

    Examples
    --------
    >>> df.mutate(r = tp.dense_rank('x'))
    """
    x = _col_expr(x)
    return x.rank('dense')


def min_rank(x):
    """
    Rank with gaps: tied values get the minimum rank

    Parameters
    ----------
    x : Expr, str
        Column to rank

    Examples
    --------
    >>> df.mutate(r = tp.min_rank('x'))
    """
    x = _col_expr(x)
    return x.rank('min')


def percent_rank(x):
    """
    Rescale ranks to [0, 1] range: (rank - 1) / (n - 1)

    Parameters
    ----------
    x : Expr, str
        Column to rank

    Examples
    --------
    >>> df.mutate(r = tp.percent_rank('x'))
    """
    x = _col_expr(x)
    return (x.rank('min').cast(pl.Float64) - 1) / (pl.len().cast(pl.Float64) - 1)


def cume_dist(x):
    """
    Cumulative distribution: proportion of values <= current value

    Parameters
    ----------
    x : Expr, str
        Column to compute cumulative distribution for

    Examples
    --------
    >>> df.mutate(cd = tp.cume_dist('x'))
    """
    x = _col_expr(x)
    return x.rank('max').cast(pl.Float64) / pl.len().cast(pl.Float64)


def ntile(x, n):
    """
    Divide values into n roughly equal-sized buckets

    Parameters
    ----------
    x : Expr, str
        Column to divide
    n : int
        Number of buckets

    Examples
    --------
    >>> df.mutate(q = tp.ntile('x', 4))
    """
    x = _col_expr(x)
    return ((x.rank('ordinal') - 1) * n / pl.len()).cast(pl.Int64) + 1


def nth(x, idx, default=None):
    """
    Get the nth value from a column

    Parameters
    ----------
    x : Expr, str
        Column to operate on
    idx : int
        Index to get (0-based)
    default : optional
        Value to return if index is out of bounds

    Examples
    --------
    >>> df.summarize(second = tp.nth('x', 1))
    """
    x = _col_expr(x)
    if default is not None:
        return x.get(idx, null_on_oob=True).fill_null(default)
    return x.gather(idx)


def cumall(x):
    """
    Cumulative all: True as long as all preceding values are True

    Parameters
    ----------
    x : Expr, str
        Boolean column

    Examples
    --------
    >>> df.mutate(ca = tp.cumall('flag'))
    """
    x = _col_expr(x)
    return x.cast(pl.Int8).cum_min().cast(pl.Boolean)


def cumany(x):
    """
    Cumulative any: True once any preceding value is True

    Parameters
    ----------
    x : Expr, str
        Boolean column

    Examples
    --------
    >>> df.mutate(ca = tp.cumany('flag'))
    """
    x = _col_expr(x)
    return x.cast(pl.Int8).cum_max().cast(pl.Boolean)


def cummean(x):
    """
    Cumulative mean

    Parameters
    ----------
    x : Expr, str
        Column to operate on

    Examples
    --------
    >>> df.mutate(cm = tp.cummean('x'))
    """
    x = _col_expr(x)
    return x.cum_sum() / (pl.int_range(pl.len()) + 1)
