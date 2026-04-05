import polars as pl
import numpy as np
from .utils import (
    _col_expr,
)

__all__ = [
    # Agg stats
    "abs", "cor", "cov", "count", "first", "last", "length",
    "max", "mean", "median", "min", "n",
     "quantile", "sd", "sum", "var", "rank",
    "floor", 'scale',
    # Ranking functions
    "dense_rank", "min_rank", "percent_rank", "cume_dist", "ntile",
    # Positional
    "nth",
    # Cumulative
    "cumall", "cumany", "cummean",
    # Math
    "log", "log10", "sqrt",
]


def abs(x):
    """
    Absolute value

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(abs_x = tp.abs('x'))
    >>> df.mutate(abs_x = tp.abs(col('x')))
    """
    x = _col_expr(x)
    return x.abs()

def cor(x, y, method = 'pearson'):
    """
    Find the correlation of two columns

    Parameters
    ----------
    x : Expr
        A column
    y : Expr
        A column
    method : str
        Type of correlation to find. Either 'pearson' or 'spearman'.

    Examples
    --------
    >>> df.summarize(cor = tp.cor(col('x'), col('y')))
    """
    if pl.Series([method]).is_in(['pearson', 'spearman']).not_().item():
        ValueError("`method` must be either 'pearson' or 'spearman'")
    return pl.corr(x, y, method = method)

def cov(x, y):
    """
    Find the covariance of two columns

    Parameters
    ----------
    x : Expr
        A column
    y : Expr
        A column

    Examples
    --------
    >>> df.summarize(cor = tp.cov(col('x'), col('y')))
    """
    return pl.cov(x, y)

def count(x):
    """
    Number of observations in each group

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(count = tp.count(col('x')))
    """
    x = _col_expr(x)
    return x.count()

def first(x):
    """
    Get first value

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(first_x = tp.first('x'))
    >>> df.summarize(first_x = tp.first(col('x')))
    """
    x = _col_expr(x)
    return x.first()

def last(x):
    """
    Get last value

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(last_x = tp.last('x'))
    >>> df.summarize(last_x = tp.last(col('x')))
    """
    x = _col_expr(x)
    return x.last()

def length(x):
    """
    Number of observations in each group

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(length = tp.length(col('x')))
    """
    x = _col_expr(x)
    return x.count()

def floor(x):
    """
    Round numbers down to the lower integer

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(floor_x = tp.floor(col('x')))
    """
    x = _col_expr(x)
    return x.floor()

def log(x):
    """
    Compute the natural logarithm of a column

    Parameters
    ----------
    x : Expr
        Column to operate on

    Examples
    --------
    >>> df.mutate(log = tp.log('x'))
    """
    x = _col_expr(x)
    return x.log()

def log10(x):
    """
    Compute the base 10 logarithm of a column

    Parameters
    ----------
    x : Expr
        Column to operate on

    Examples
    --------
    >>> df.mutate(log = tp.log10('x'))
    """
    x = _col_expr(x)
    return x.log10()

def max(x):
    """
    Get column max

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(max_x = tp.max('x'))
    >>> df.summarize(max_x = tp.max(col('x')))
    """
    x = _col_expr(x)
    return x.max()

def mean(x):
    """
    Get column mean

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(mean_x = tp.mean('x'))
    >>> df.summarize(mean_x = tp.mean(col('x')))
    """
    x = _col_expr(x)
    return x.mean()

def median(x):
    """
    Get column median

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(median_x = tp.median('x'))
    >>> df.summarize(median_x = tp.median(col('x')))
    """
    x = _col_expr(x)
    return x.median()

def min(x):
    """
    Get column minimum

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(min_x = tp.min('x'))
    >>> df.summarize(min_x = tp.min(col('x')))
    """
    x = _col_expr(x)
    return x.min()

def n():
    """
    Number of observations in each group

    Examples
    --------
    >>> df.summarize(count = tp.n())
    """
    return pl.len()

def quantile(x, quantile = .5):
    """
    Get number of distinct values in a column

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    quantile : float
        Quantile to return

    Examples
    --------
    >>> df.summarize(quantile_x = tp.quantile('x', .25))
    """
    x = _col_expr(x)
    return x.quantile(quantile)

def sd(x):
    """
    Get column standard deviation

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(sd_x = tp.sd('x'))
    >>> df.summarize(sd_x = tp.sd(col('x')))
    """
    x = _col_expr(x)
    return x.std()

def sqrt(x):
    """
    Get column square root

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(sqrt_x = tp.sqrt('x'))
    """
    x = _col_expr(x)
    return x.sqrt()

def sum(x):
    """
    Get column sum

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(sum_x = tp.sum('x'))
    >>> df.summarize(sum_x = tp.sum(col('x')))
    """
    x = _col_expr(x)
    return x.sum()

def var(x):
    """
    Get column variance

    Parameters
    ----------
    x : Expr
        Column to operate on

    Examples
    --------
    >>> df.summarize(sum_x = tp.var('x'))
    >>> df.summarize(sum_x = tp.var(col('x')))
    """
    x = _col_expr(x)
    return x.var()

def rank(x, method='dense'):
    """
    Assigns a minimum rank to each element in the input list, handling ties by
    assigning the same (lowest) rank to tied values. The next distinct value's rank
    is increased by the number of tied values before it.

    Parameters
    ----------
    x : str
        Column to operate on

    method : str
        dense (default): Assigns ranks in a consecutive manner, without gaps, even for ties.
        average : Assigns the average rank to tied values.
        min: Assigns the minimum rank to tied values.
        max: Assigns the maximum rank to tied values.
        ordinal: Assigns a distinct rank to each value based on its order of appearance.

    Returns
    -------
    list of int
        A list of ranks corresponding to the elements of `x`.

    Examples
    --------
    >>> min_rank([10, 20, 20, 30])
    [1, 2, 2, 4]
    >>> min_rank([3, 1, 2])
    [3, 1, 2]  # since sorted order is 1,2,3 => ranks are assigned as per their order
    >>> min_rank(["b", "a", "a", "c"])
    [2, 1, 1, 4]
    """

    x = _col_expr(x)
    return x.rank(method=method)

def scale(x):
    """
    Standardize the input by scaling it to a mean of 0 and a standard deviation of 1.

    Parameters
    ----------
    x : Expr
        Column to operate on

    Returns
    -------
    array-like
        The standardized version of the input data.
    """
    x = _col_expr(x)
    return (x - x.mean()) / x.std()


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
        # Use get() which returns null for out-of-bounds, then fill_null
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


