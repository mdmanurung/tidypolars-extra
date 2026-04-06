"""
Extended tibble class for tidypolars4sci.

Subclasses the upstream ``tidypolars4sci.tibble_df.tibble`` to add
new methods (joins, slicing, set operations, tidyr verbs, etc.) and
apply compatibility fixes for the current Polars API.
"""
import polars as pl
import polars.selectors as cs
import copy
from operator import not_

from tidypolars4sci.tibble_df import (
    tibble as _BaseTibble,
    TibbleGroupBy as _BaseTibbleGroupBy,
    from_polars as _base_from_polars,
    from_pandas as _base_from_pandas,
    _polars_methods,
    _allowed_methods,
    __get_accepted_output_formats__,
)
from tidypolars4sci.utils import (
    _as_list,
    _col_expr,
    _col_exprs,
    _kwargs_as_exprs,
    _uses_by,
)
from tidypolars4sci.helpers import desc, DescCol, everything, where
from tidypolars4sci.reexports import col

__all__ = [
    "tibble",
    "TibbleGroupBy",
    "from_polars",
    "from_pandas",
    "__get_accepted_output_formats__",
]


# ---------------------------------------------------------------------------
# Conversion helpers — always return the *extended* tibble
# ---------------------------------------------------------------------------

def from_polars(df):
    """
    Convert from polars DataFrame to the extended tibble.

    Parameters
    ----------
    df : DataFrame
        pl.DataFrame to convert to a tibble

    Returns
    -------
    tibble

    Examples
    --------
    >>> tp.from_polars(df)
    """
    return tibble(df)


def from_pandas(df):
    """
    Convert from pandas DataFrame to the extended tibble.

    Parameters
    ----------
    df : DataFrame
        pd.DataFrame to convert to a tibble

    Returns
    -------
    tibble

    Examples
    --------
    >>> tp.from_pandas(df)
    """
    import pandas as pd

    if isinstance(df, pd.DataFrame):
        try:
            df = from_polars(pl.from_pandas(df))
        except Exception as e:
            print(f"Error during conversion: {e}")
            print("Identifying problematic columns...")
            problematic_columns = []
            for column in df.columns:
                try:
                    pl.from_pandas(df[[column]])
                except Exception as col_error:
                    print(f"Column '{column}' caused an error: {col_error}")
                    problematic_columns.append(column)
            for column in problematic_columns:
                df[column] = df[column].astype(str)
    elif isinstance(df, tibble):
        pass
    elif isinstance(df, pl.DataFrame):
        df = from_polars(df)
    else:
        df = None
    return df


class tibble(_BaseTibble):
    """
    Extended tibble — adds methods missing from the upstream tidypolars4sci.

    Inherits all upstream methods (arrange, filter, mutate, …) and adds:
      * Joins: right_join, semi_join, anti_join, cross_join
      * Slicing: slice_min, slice_max, slice_sample
      * Set ops: union, union_all, intersect, setdiff
      * dplyr verbs: transmute, rename_with, add_count, tally, uncount, ungroup
      * tidyr: complete, expand, separate_rows, extract, drop_na, replace_na
    """

    def __init__(self, *args, **kwargs):
        # Allow tibble(x=[1,2], y=[3,4]) syntax like R's tibble()
        if len(args) == 0 and len(kwargs) > 0:
            _df_params = {
                'data', 'schema', 'schema_overrides', 'orient',
                'infer_schema_length', 'strict', 'nan_to_null',
            }
            if not any(k in _df_params for k in kwargs):
                super(_BaseTibble, self).__init__(kwargs)
                return
        super(_BaseTibble, self).__init__(*args, **kwargs)

    # ------------------------------------------------------------------
    # Override upstream helpers so they produce *our* tibble type
    # ------------------------------------------------------------------
    @property
    def _constructor(self):
        return self.__class__

    def to_polars(self):
        """Convert to a polars DataFrame"""
        self = copy.copy(self)
        self.__class__ = pl.DataFrame
        return self

    def __dir__(self):
        base = list(super().__dir__())
        ext = [
            'add_count',
            'anti_join',
            'complete', 'cross_join',
            'drop_na',
            'expand', 'extract',
            'intersect',
            'rename_with', 'replace_na', 'right_join',
            'semi_join', 'separate_rows', 'setdiff',
            'slice_max', 'slice_min', 'slice_sample',
            'tally', 'transmute',
            'uncount', 'ungroup', 'union', 'union_all',
        ]
        return sorted(set(base + ext))

    # ------------------------------------------------------------------
    # Override group_by to return *our* TibbleGroupBy
    # ------------------------------------------------------------------

    def group_by(self, group, *args, **kwargs):
        """
        Takes an existing tibble and converts it into a grouped tibble
        where operations are performed "by group".

        Parameters
        ----------
        group : str, list
            Variable names to group by.

        Returns
        -------
        TibbleGroupBy
        """
        return TibbleGroupBy(self, group, maintain_order=True)

    # ------------------------------------------------------------------
    # Compatibility overrides — fixes for current Polars API
    # ------------------------------------------------------------------

    def full_join(self, df, left_on=None, right_on=None, on=None, suffix='_right'):
        """Perform a full join (fixes upstream ``'outer'`` → ``'full'``)."""
        if (left_on is None) and (right_on is None) and (on is None):
            on = list(set(self.names) & set(df.names))
        return super(_BaseTibble, self).join(
            df, on, 'full',
            left_on=left_on, right_on=right_on,
            suffix=suffix, coalesce=True,
        ).pipe(from_polars)

    def pivot_longer(self, cols=None, names_to="name", values_to="value"):
        """Pivot data from wide to long (uses ``unpivot`` instead of deprecated ``melt``)."""
        if cols is None:
            cols = everything()
        if isinstance(cols, dict):
            cols = list(cols.keys())
        value_vars = self.select(cols).names
        id_vars = [c for c in self.names if c not in value_vars]
        out = self.to_polars().unpivot(
            on=value_vars, index=id_vars,
            variable_name=names_to, value_name=values_to,
        )
        return out.pipe(from_polars)

    def pivot_wider(self, names_from='name', values_from='value',
                    id_cols=None, values_fn='first', values_fill=None):
        """Pivot data from long to wide (uses list-comprehension filtering)."""
        if id_cols is None:
            from_col_names = self.select(names_from, values_from).names
            id_cols = [c for c in self.names if c not in from_col_names]

        no_id = len(id_cols) == 0
        if no_id:
            id_cols = '___id__'
            self = self.mutate(___id__=pl.lit(1))

        out = (
            self.to_polars()
            .pivot(index=id_cols, on=names_from, values=values_from,
                   aggregate_function=values_fn)
            .pipe(from_polars)
        )

        if values_fill is not None:
            id_col_set = set(_as_list(id_cols))
            new_cols = [c for c in out.names if c not in id_col_set]
            fill_exprs = [col(new_col).fill_null(values_fill) for new_col in new_cols]
            out = out.mutate(*fill_exprs)

        if no_id:
            out = out.drop('___id__')
        return out

    def relocate(self, *args, before=None, after=None):
        """Move columns (fixes ``is_in`` compatibility)."""
        cols_all = pl.Series(self.names)
        locs_all = pl.Series(range(len(cols_all)))
        locs_dict = {k: v for k, v in zip(cols_all, locs_all)}
        locs_df = pl.DataFrame(locs_dict, orient="row")

        cols_relocate = _as_list(args)
        locs_relocate = pl.Series(locs_df.select(cols_relocate).row(0))

        if len(locs_relocate) == 0:
            return self

        uses_before = before is not None
        uses_after = after is not None

        if uses_before and uses_after:
            raise ValueError("Cannot provide both before and after")
        elif (not uses_before) and (not uses_after):
            before = cols_all[0]
            uses_before = True

        if uses_before:
            before_val = locs_df.select(before).get_column(before)
            locs_start = locs_all.filter(locs_all < before_val)
        else:
            after_val = locs_df.select(after).get_column(after)
            locs_start = locs_all.filter(locs_all <= after_val)

        locs_start = locs_start.filter(~locs_start.is_in(locs_relocate.implode()))
        final_order = pl.concat([locs_start, locs_relocate, locs_all]).unique(maintain_order=True)
        final_order = cols_all[final_order].to_list()
        return self.select(final_order)

    def replace(self, rep, regex=False):
        """Replace values (avoids pandas for regex replacement)."""
        is_column_specific = all(isinstance(value, dict) for value in rep.values())

        if is_column_specific and not regex:
            out = self.to_polars()
            for var, mapping in rep.items():
                try:
                    out = out.with_columns(**{var: pl.col(var).replace(mapping)})
                except Exception:
                    out = out.with_columns(**{var: pl.col(var).replace_strict(mapping)})
            return out.pipe(from_polars)

        if regex:
            out = self.to_polars()
            str_cols = [c for c, dt in zip(out.columns, out.dtypes)
                        if dt == pl.Utf8 or dt == pl.Categorical or dt == pl.String]
            for pattern, replacement in rep.items():
                exprs = [pl.col(c).str.replace_all(str(pattern), str(replacement))
                         for c in str_cols]
                if exprs:
                    out = out.with_columns(exprs)
            return out.pipe(from_polars)

        out = self.to_polars()
        for old_val, new_val in rep.items():
            exprs = [
                pl.when(pl.col(c) == old_val)
                .then(pl.lit(new_val))
                .otherwise(pl.col(c))
                .alias(c)
                for c in out.columns
            ]
            out = out.with_columns(exprs)
        return out.pipe(from_polars)

    # ------------------------------------------------------------------
    # NEW joins
    # ------------------------------------------------------------------

    def right_join(self, df, left_on=None, right_on=None, on=None, suffix='_right'):
        """
        Perform a right join

        Parameters
        ----------
        df : tibble
            DataFrame to join with.
        left_on : str, list
            Join column(s) of the left DataFrame.
        right_on : str, list
            Join column(s) of the right DataFrame.
        on: str, list
            Join column(s) of both DataFrames.
        suffix : str
            Suffix to append to columns with a duplicate name.

        Examples
        --------
        >>> df1.right_join(df2, on = 'x')
        """
        if (left_on is None) and (right_on is None) and (on is None):
            on = list(set(self.names) & set(df.names))
        return super(_BaseTibble, self).join(
            df, on, 'right',
            left_on=left_on, right_on=right_on, suffix=suffix,
        ).pipe(from_polars)

    def semi_join(self, df, left_on=None, right_on=None, on=None):
        """
        Perform a semi join (keep rows from left with matches in right)

        Parameters
        ----------
        df : tibble
            DataFrame to join with.
        left_on : str, list
            Join column(s) of the left DataFrame.
        right_on : str, list
            Join column(s) of the right DataFrame.
        on: str, list
            Join column(s) of both DataFrames.

        Examples
        --------
        >>> df1.semi_join(df2, on = 'x')
        """
        if (left_on is None) and (right_on is None) and (on is None):
            on = list(set(self.names) & set(df.names))
        return super(_BaseTibble, self).join(
            df, on, 'semi',
            left_on=left_on, right_on=right_on,
        ).pipe(from_polars)

    def anti_join(self, df, left_on=None, right_on=None, on=None):
        """
        Perform an anti join (keep rows from left without matches in right)

        Parameters
        ----------
        df : tibble
            DataFrame to join with.
        left_on : str, list
            Join column(s) of the left DataFrame.
        right_on : str, list
            Join column(s) of the right DataFrame.
        on: str, list
            Join column(s) of both DataFrames.

        Examples
        --------
        >>> df1.anti_join(df2, on = 'x')
        """
        if (left_on is None) and (right_on is None) and (on is None):
            on = list(set(self.names) & set(df.names))
        return super(_BaseTibble, self).join(
            df, on, 'anti',
            left_on=left_on, right_on=right_on,
        ).pipe(from_polars)

    def cross_join(self, df, suffix='_right'):
        """
        Perform a cross join (Cartesian product)

        Parameters
        ----------
        df : tibble
            DataFrame to join with.
        suffix : str
            Suffix to append to columns with a duplicate name.

        Examples
        --------
        >>> df1.cross_join(df2)
        """
        return super(_BaseTibble, self).join(
            df, how='cross', suffix=suffix,
        ).pipe(from_polars)

    # ------------------------------------------------------------------
    # NEW slicing variants
    # ------------------------------------------------------------------

    def slice_min(self, order_by, n=1, *, by=None, with_ties=True):
        """
        Select rows with the smallest values of a column

        Parameters
        ----------
        order_by : str, Expr
            Column to order by
        n : int
            Number of rows to return
        by : str, list
            Columns to group by
        with_ties : bool
            If True, return all rows with ties

        Examples
        --------
        >>> df.slice_min('x', n = 1)
        >>> df.slice_min('x', n = 1, by = 'g')
        """
        order_col = _col_expr(order_by)
        if with_ties:
            rank_expr = order_col.rank('dense')
            if _uses_by(by):
                return super(_BaseTibble, self).group_by(by).map_groups(
                    lambda x: x.filter(x.select(rank_expr).to_series() <= n)
                ).pipe(from_polars)
            else:
                return self.filter(rank_expr <= n)
        else:
            return self.arrange(order_by).slice_head(n=n, by=by)

    def slice_max(self, order_by, n=1, *, by=None, with_ties=True):
        """
        Select rows with the largest values of a column

        Parameters
        ----------
        order_by : str, Expr
            Column to order by
        n : int
            Number of rows to return
        by : str, list
            Columns to group by
        with_ties : bool
            If True, return all rows with ties

        Examples
        --------
        >>> df.slice_max('x', n = 1)
        >>> df.slice_max('x', n = 1, by = 'g')
        """
        order_col = _col_expr(order_by)
        if with_ties:
            rank_expr = order_col.rank('dense', descending=True)
            if _uses_by(by):
                return super(_BaseTibble, self).group_by(by).map_groups(
                    lambda x: x.filter(x.select(rank_expr).to_series() <= n)
                ).pipe(from_polars)
            else:
                return self.filter(rank_expr <= n)
        else:
            return self.arrange(desc(order_by)).slice_head(n=n, by=by)

    def slice_sample(self, n=None, prop=None, *, by=None, replace=False, seed=None):
        """
        Randomly sample rows

        Parameters
        ----------
        n : int
            Number of rows to sample
        prop : float
            Fraction of rows to sample (0 to 1)
        by : str, list
            Columns to group by
        replace : bool
            Sample with replacement
        seed : int
            Random seed

        Examples
        --------
        >>> df.slice_sample(n = 5)
        >>> df.slice_sample(prop = 0.5)
        """
        if _uses_by(by):
            return super(_BaseTibble, self).group_by(by).map_groups(
                lambda x: x.sample(
                    n=n, fraction=prop,
                    with_replacement=replace, seed=seed,
                )
            ).pipe(from_polars)
        else:
            return super(_BaseTibble, self).sample(
                n=n, fraction=prop,
                with_replacement=replace, seed=seed,
            ).pipe(from_polars)

    # ------------------------------------------------------------------
    # Set Operations
    # ------------------------------------------------------------------

    def union(self, df):
        """
        Rows in either table, deduplicated

        Parameters
        ----------
        df : tibble
            DataFrame to combine with

        Examples
        --------
        >>> df1.union(df2)
        """
        return self.bind_rows(df).distinct()

    def union_all(self, df):
        """
        Rows in either table, keeping duplicates

        Parameters
        ----------
        df : tibble
            DataFrame to combine with

        Examples
        --------
        >>> df1.union_all(df2)
        """
        return self.bind_rows(df)

    def intersect(self, df):
        """
        Rows that appear in both tables

        Parameters
        ----------
        df : tibble
            DataFrame to intersect with

        Examples
        --------
        >>> df1.intersect(df2)
        """
        common_cols = list(set(self.names) & set(df.names))
        return self.semi_join(df, on=common_cols).distinct()

    def setdiff(self, df):
        """
        Rows in first table but not in second

        Parameters
        ----------
        df : tibble
            DataFrame to compare against

        Examples
        --------
        >>> df1.setdiff(df2)
        """
        common_cols = list(set(self.names) & set(df.names))
        return self.anti_join(df, on=common_cols)

    # ------------------------------------------------------------------
    # Additional dplyr verbs
    # ------------------------------------------------------------------

    def transmute(self, *args, by=None, **kwargs):
        """
        Mutate and keep only the new columns (plus grouping columns)

        Parameters
        ----------
        *args : Expr
            Column expressions to add
        by : str, list
            Columns to group by
        **kwargs : Expr
            Column expressions to add

        Examples
        --------
        >>> df.transmute(double_x = col('x') * 2)
        """
        new_cols = list(kwargs.keys())
        for arg in _as_list(args):
            if hasattr(arg, 'meta'):
                try:
                    new_cols.append(arg.meta.output_name())
                except Exception:
                    pass
        keep_cols = (_as_list(by) if _uses_by(by) else []) + new_cols
        return self.mutate(*args, by=by, **kwargs).select(keep_cols)

    def rename_with(self, fn, cols=None):
        """
        Rename columns using a function

        Parameters
        ----------
        fn : callable
            Function to apply to column names
        cols : list, optional
            Columns to rename. If None, rename all columns.

        Examples
        --------
        >>> df.rename_with(str.upper)
        >>> df.rename_with(str.lower, cols = ['X', 'Y'])
        """
        if cols is None:
            target_cols = self.names
        else:
            target_cols = _as_list(cols)
        rename_dict = {c: fn(c) for c in target_cols}
        return self.rename(rename_dict)

    def add_count(self, *args, name='n'):
        """
        Add a count column without collapsing rows

        Parameters
        ----------
        *args : str
            Columns to group by for counting
        name : str
            Name of the count column

        Examples
        --------
        >>> df.add_count('group')
        """
        by = list(args) if len(args) > 0 else None
        if _uses_by(by):
            return self.mutate(**{name: pl.len()}, by=by)
        else:
            return self.mutate(**{name: pl.len()})

    def tally(self, name='n'):
        """
        Count observations (simple count)

        Parameters
        ----------
        name : str
            Name of the count column

        Examples
        --------
        >>> df.tally()
        """
        return self.summarize(**{name: pl.len()})

    def uncount(self, weights, remove=True):
        """
        Inverse of count: duplicate rows based on a weight column

        Parameters
        ----------
        weights : str
            Column containing the number of times to repeat each row
        remove : bool
            If True, remove the weights column

        Examples
        --------
        >>> df = tp.tibble(x = ['a', 'b'], n = [2, 3])
        >>> df.uncount('n')
        """
        out = (
            self.to_polars()
            .filter(pl.col(weights) > 0)
            .with_columns(pl.col(weights).cast(pl.UInt32))
            .select(pl.all().repeat_by(pl.col(weights)))
            .explode(pl.all())
        )
        if remove:
            out = out.drop(weights)
        return out.pipe(from_polars)

    def ungroup(self):
        """
        Remove grouping (returns self for ungrouped tibble)

        Examples
        --------
        >>> df.ungroup()
        """
        return self

    # ------------------------------------------------------------------
    # tidyr functions
    # ------------------------------------------------------------------

    def complete(self, *args, fill=None):
        """
        Complete a data frame with all combinations of specified columns,
        filling missing values with NA (or specified fill values)

        Parameters
        ----------
        *args : str
            Columns to expand into all combinations
        fill : dict, optional
            Dictionary of {column_name: fill_value} for filling NAs

        Examples
        --------
        >>> df.complete('x', 'y')
        """
        expand_cols = list(args)
        unique_frames = [self.distinct(c).select(c) for c in expand_cols]
        grid = unique_frames[0]
        for frame in unique_frames[1:]:
            grid = grid.cross_join(frame)
        out = grid.left_join(self, on=expand_cols)
        if fill is not None:
            out = out.replace_null(fill)
        out = out.select([c for c in self.names if c in out.names])
        return out

    def expand(self, *args):
        """
        Create a tibble of all unique combinations of specified columns

        Parameters
        ----------
        *args : str
            Columns to expand

        Examples
        --------
        >>> df.expand('x', 'y')
        """
        expand_cols = list(args)
        unique_frames = [self.distinct(c).select(c) for c in expand_cols]
        grid = unique_frames[0]
        for frame in unique_frames[1:]:
            grid = grid.cross_join(frame)
        return grid

    def separate_rows(self, col, sep=','):
        """
        Separate a column into rows by splitting on a separator

        Parameters
        ----------
        col : str
            Column to separate
        sep : str
            Separator pattern to split on

        Examples
        --------
        >>> df.separate_rows('x', sep = ',')
        """
        return (
            self.to_polars()
            .with_columns(pl.col(col).str.split(sep))
            .explode(col)
            .pipe(from_polars)
        )

    def extract(self, col, into, regex, remove=True):
        """
        Extract capture groups from a string column into new columns

        Parameters
        ----------
        col : str
            Column to extract from
        into : list
            Names for the new columns
        regex : str
            Regular expression with capture groups
        remove : bool
            If True, remove the input column

        Examples
        --------
        >>> df.extract('x', into=['letter', 'number'], regex=r'(\\w)-(\\d)')
        """
        extracted = self.to_polars().select(
            pl.col(col).str.extract_groups(regex)
        ).unnest(col)
        old_names = extracted.columns
        rename_map = {old: new for old, new in zip(old_names, into)}
        extracted = extracted.rename(rename_map)
        out = self.bind_cols(from_polars(extracted))
        if remove:
            out = out.drop(col)
        return out

    def drop_na(self, *args):
        """
        Drop rows with missing values (alias for drop_null)

        Parameters
        ----------
        *args : str
            Columns to check for missing values. If empty, checks all columns.

        Examples
        --------
        >>> df.drop_na()
        """
        return self.drop_null(*args)

    def replace_na(self, replace=None):
        """
        Replace missing values (alias for replace_null)

        Parameters
        ----------
        replace : dict, scalar
            Values to replace NAs with

        Examples
        --------
        >>> df.replace_na({'x': 0, 'y': 'missing'})
        """
        return self.replace_null(replace)


# ---------------------------------------------------------------------------
# Extended TibbleGroupBy
# ---------------------------------------------------------------------------

class TibbleGroupBy(_BaseTibbleGroupBy):
    """Extended GroupBy with ungroup, n_groups, group_keys, group_split."""

    def __init__(self, df, by, *args, **kwargs):
        assert isinstance(by, str) or isinstance(by, list), \
            "Use list or string to group by."
        kwargs.setdefault('predicates', None)
        super().__init__(df, by, *args, **kwargs)
        self.df = df
        self.by = by if isinstance(by, list) else [by]

    @property
    def _constructor(self):
        return TibbleGroupBy

    def mutate(self, *args, **kwargs):
        return self.map_groups(
            lambda x: from_polars(x).mutate(*args, **kwargs)
        )

    def filter(self, *args, **kwargs):
        return self.map_groups(
            lambda x: from_polars(x).filter(*args, **kwargs)
        )

    def summarize(self, *args, **kwargs):
        return self.map_groups(
            lambda x: from_polars(x).summarise(by=self.by, *args, **kwargs)
        )

    def ungroup(self):
        """Remove grouping and return a regular tibble"""
        return from_polars(self.df)

    def n_groups(self):
        """Return the number of groups"""
        return self.df.distinct(*self.by).select(self.by).nrow

    def group_keys(self):
        """Return a tibble of unique group combinations"""
        return self.df.distinct(*self.by).select(self.by)

    def group_split(self):
        """Split into a list of tibbles, one per group"""
        return [from_polars(df) for df in self.df.to_polars().partition_by(self.by)]
