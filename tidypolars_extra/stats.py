import polars as pl
from .utils import (
    _col_expr,
)

__all__ = [
    # Agg stats
    "abs", "cor", "cov", "count", "first", "last", "length",
    "log", "log10",
    "max", "mean", "median", "min", "n",
     "quantile", "sd", "sqrt", "sum", "var", "rank",
    "floor", 'scale',
    # Cumulative
    "cumsum", "cumprod", "cummax", "cummin",
    # Ranking
    "percent_rank", "cume_dist", "ntile",
    # Extra stats
    "weighted_mean", "mode", "iqr", "mad", "zscore",
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
        raise ValueError("`method` must be either 'pearson' or 'spearman'")
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
    Number of observations in each group.

    Alias for :func:`count`.

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(length = tp.length(col('x')))
    """
    return count(x)

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
    >>> rank([10, 20, 20, 30])
    [1, 2, 2, 3]
    >>> rank([3, 1, 2])
    [3, 1, 2]  # since sorted order is 1,2,3 => ranks are assigned as per their order
    >>> rank(["b", "a", "a", "c"])
    [2, 1, 1, 3]
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

def zscore(x):
    """
    Standardize to z-scores (alias for scale)

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(z = tp.zscore('x'))
    """
    return scale(x)

def cumsum(x):
    """
    Cumulative sum

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(csum = tp.cumsum('x'))
    """
    x = _col_expr(x)
    return x.cum_sum()

def cumprod(x):
    """
    Cumulative product

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(cprod = tp.cumprod('x'))
    """
    x = _col_expr(x)
    return x.cum_prod()

def cummax(x):
    """
    Cumulative maximum

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(cmax = tp.cummax('x'))
    """
    x = _col_expr(x)
    return x.cum_max()

def cummin(x):
    """
    Cumulative minimum

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(cmin = tp.cummin('x'))
    """
    x = _col_expr(x)
    return x.cum_min()

def percent_rank(x):
    """
    Compute percent rank (values between 0 and 1)

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(prank = tp.percent_rank('x'))
    """
    x = _col_expr(x)
    r = x.rank(method='min')
    return (r - 1) / (pl.len() - 1)

def cume_dist(x):
    """
    Compute cumulative distribution (proportion of values <= current value)

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(cd = tp.cume_dist('x'))
    """
    x = _col_expr(x)
    r = x.rank(method='max')
    return r / pl.len()

def ntile(x, n):
    """
    Divide values into n roughly equal groups

    Parameters
    ----------
    x : Expr, Series
        Column to operate on
    n : int
        Number of groups

    Examples
    --------
    >>> df.mutate(quartile = tp.ntile('x', 4))
    """
    x = _col_expr(x)
    r = x.rank(method='ordinal')
    return ((r - 1) * n / pl.len()).cast(pl.Int64) + 1

def weighted_mean(x, w):
    """
    Compute weighted mean

    Parameters
    ----------
    x : Expr, Series
        Column of values
    w : Expr, Series
        Column of weights

    Examples
    --------
    >>> df.summarize(wm = tp.weighted_mean('x', 'w'))
    """
    x = _col_expr(x)
    w = _col_expr(w)
    return (x * w).sum() / w.sum()

def mode(x):
    """
    Compute the statistical mode (most frequent value)

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(m = tp.mode('x'))
    """
    x = _col_expr(x)
    return x.mode().first()

def iqr(x):
    """
    Compute the interquartile range (Q3 - Q1)

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.summarize(iqr_val = tp.iqr('x'))
    """
    x = _col_expr(x)
    return x.quantile(0.75) - x.quantile(0.25)

def mad(x):
    """
    Compute the median absolute deviation

    Parameters
    ----------
    x : Expr, Series
        Column to operate on

    Examples
    --------
    >>> df.mutate(mad_val = tp.mad('x'))
    """
    x = _col_expr(x)
    return (x - x.median()).abs().median()
