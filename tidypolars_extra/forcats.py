import polars as pl
from .utils import _col_expr

__all__ = [
    "fct_collapse",
    "fct_infreq",
    "fct_lump",
    "fct_recode",
    "fct_rev",
]


def fct_infreq(df, col_name):
    """
    Reorder factor levels by frequency (most common first)

    Parameters
    ----------
    df : tibble
        The DataFrame containing the column
    col_name : str
        Name of the column to reorder

    Returns
    -------
    tibble
        DataFrame with column cast to Enum with levels ordered by frequency.

    Examples
    --------
    >>> df = tp.tibble(x=['a', 'b', 'a', 'a', 'b', 'c'])
    >>> df = tp.fct_infreq(df, 'x')
    """
    counts = (df.to_polars()
              .get_column(col_name)
              .cast(pl.Utf8)
              .value_counts(sort=True))
    levels = counts.get_column(col_name).to_list()
    dtype = pl.Enum(levels)
    return df.mutate(pl.col(col_name).cast(pl.Utf8).cast(dtype).alias(col_name))


def fct_rev(df, col_name):
    """
    Reverse factor level order

    Parameters
    ----------
    df : tibble
        The DataFrame containing the column
    col_name : str
        Name of the column to reverse

    Returns
    -------
    tibble
        DataFrame with column cast to Enum with reversed level order.

    Examples
    --------
    >>> df = tp.tibble(x=['a', 'b', 'c'])
    >>> df = tp.fct_rev(df, 'x')
    """
    col_series = df.to_polars().get_column(col_name)
    dtype = col_series.dtype
    if isinstance(dtype, pl.Enum):
        levels = list(reversed(dtype.categories.to_list()))
    elif dtype == pl.Categorical:
        levels = list(reversed(col_series.cast(pl.Utf8).unique().sort().to_list()))
    else:
        levels = list(reversed(col_series.cast(pl.Utf8).unique().sort().to_list()))
    new_dtype = pl.Enum(levels)
    return df.mutate(pl.col(col_name).cast(pl.Utf8).cast(new_dtype).alias(col_name))


def fct_lump(x, n=None, prop=None, other_level='Other'):
    """
    Collapse least frequent factor levels into 'Other'

    Uses a ranking approach: for each value, computes its frequency rank
    and replaces values outside the top n with other_level.

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column
    n : int, optional
        Number of most frequent levels to keep
    prop : float, optional
        Minimum proportion to keep a level (0 to 1)
    other_level : str
        Label for collapsed levels (default: 'Other')

    Returns
    -------
    Expr
        Expression with infrequent levels replaced.

    Examples
    --------
    >>> df.mutate(x_lumped = tp.fct_lump('x', n=3))
    """
    x = _col_expr(x)
    x_str = x.cast(pl.Utf8)

    if n is not None:
        # Rank by frequency; keep levels where rank <= n
        freq = x_str.len().over(x_str)
        freq_rank = freq.rank(method='dense', descending=True)
        return pl.when(freq_rank <= n).then(x_str).otherwise(pl.lit(other_level))
    elif prop is not None:
        # Keep levels that appear in at least prop fraction of rows
        freq = x_str.len().over(x_str)
        return pl.when(freq >= pl.len() * prop).then(x_str).otherwise(pl.lit(other_level))
    else:
        return x_str


def fct_recode(x, **kwargs):
    """
    Manually recode factor levels

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column
    **kwargs
        Mapping of new_level = 'old_level' or new_level = ['old1', 'old2']

    Returns
    -------
    Expr
        Expression with recoded levels.

    Examples
    --------
    >>> df.mutate(x_recoded = tp.fct_recode('x', good='a', bad='b'))
    """
    x = _col_expr(x)
    result = x.cast(pl.Utf8)
    for new_level, old_levels in kwargs.items():
        if isinstance(old_levels, str):
            old_levels = [old_levels]
        for old_level in old_levels:
            result = pl.when(result == old_level).then(pl.lit(new_level)).otherwise(result)
    return result


def fct_collapse(x, **kwargs):
    """
    Collapse multiple factor levels into one

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column
    **kwargs
        Mapping of new_level = ['old1', 'old2', ...]

    Returns
    -------
    Expr
        Expression with collapsed levels.

    Examples
    --------
    >>> df.mutate(x_collapsed = tp.fct_collapse('x', ab=['a', 'b'], cd=['c', 'd']))
    """
    x = _col_expr(x)
    result = x.cast(pl.Utf8)
    for new_level, old_levels in kwargs.items():
        if isinstance(old_levels, str):
            old_levels = [old_levels]
        result = pl.when(result.is_in(old_levels)).then(pl.lit(new_level)).otherwise(result)
    return result
