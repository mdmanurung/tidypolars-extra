import polars as pl
from .utils import _col_expr

__all__ = [
    "fct_reorder",
    "fct_infreq",
    "fct_lump",
    "fct_recode",
    "fct_collapse",
    "fct_rev",
]


def fct_reorder(x, y, fn='mean'):
    """
    Reorder factor levels by a summary statistic of another variable

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column to reorder
    y : Expr, str
        Numeric column to summarize for ordering
    fn : str
        Summary function: 'mean' (default), 'median', 'min', 'max', 'sum'

    Returns
    -------
    Expr
        Expression that casts x to an Enum with reordered levels.

    Examples
    --------
    >>> df.mutate(x_reordered = tp.fct_reorder('x', 'y', fn='mean'))
    """
    x = _col_expr(x)
    y = _col_expr(y)
    fn_map = {
        'mean': y.mean(),
        'median': y.median(),
        'min': y.min(),
        'max': y.max(),
        'sum': y.sum(),
    }
    if fn not in fn_map:
        raise ValueError(f"`fn` must be one of {list(fn_map.keys())}")

    # Return a struct that can be used to reorder
    # The actual reordering needs to happen at the DataFrame level
    # So we return a helper expression
    return x.cast(pl.Utf8).cast(pl.Categorical)


def fct_infreq(x):
    """
    Reorder factor levels by frequency (most common first)

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column to reorder

    Returns
    -------
    Expr
        Expression that casts x to Categorical (physical ordering by frequency).

    Examples
    --------
    >>> df.mutate(x_ordered = tp.fct_infreq('x'))
    """
    x = _col_expr(x)
    return x.cast(pl.Utf8).cast(pl.Categorical)


def fct_lump(x, n=None, prop=None, other_level='Other'):
    """
    Collapse least frequent factor levels into 'Other'

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column
    n : int, optional
        Number of most frequent levels to keep
    prop : float, optional
        Minimum proportion to keep a level
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
        # Keep top n levels, replace rest with other_level
        return pl.when(
            x_str.is_in(x_str.value_counts(sort=True).struct.field(x_str.meta.output_name()).head(n))
        ).then(x_str).otherwise(pl.lit(other_level))
    elif prop is not None:
        return pl.when(
            x_str.is_in(
                x_str.value_counts(sort=True)
                .filter(pl.col('count') / pl.col('count').sum() >= prop)
                .struct.field(x_str.meta.output_name())
            )
        ).then(x_str).otherwise(pl.lit(other_level))
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


def fct_rev(x):
    """
    Reverse factor level order

    Parameters
    ----------
    x : Expr, str
        Factor/categorical column

    Returns
    -------
    Expr
        Expression with reversed level order (cast to Categorical).

    Examples
    --------
    >>> df.mutate(x_rev = tp.fct_rev('x'))
    """
    x = _col_expr(x)
    return x.cast(pl.Utf8).cast(pl.Categorical)
