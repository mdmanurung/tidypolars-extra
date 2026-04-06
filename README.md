# tidypolars-extra

**tidypolars-extra** is an extension of [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci), which provides Tidyverse-like functions for data manipulation and analysis in Python using [Polars](https://github.com/pola-rs/polars) as the backend.

This project builds upon the original [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci) by adding extra functionalities and improvements while maintaining the same familiar API.

## Features

- Tidyverse-style API for [Polars](https://github.com/pola-rs/polars) DataFrames
- Scientific research utilities including LaTeX table generation
- Fast data manipulation powered by Polars
- Familiar R-like syntax for Python users
- **Joins**: `inner_join`, `left_join`, `full_join`, `semi_join`, `anti_join`, `cross_join`
- **Data reshaping**: `pivot_longer`, `pivot_wider`, `separate`, `unite`, `complete`, `nest`, `unnest`
- **String manipulation** (stringr-style): `str_detect`, `str_extract`, `str_replace`, `str_count`, `str_split`, `str_pad`, `str_squish`, `str_to_title`, and more
- **Date/time utilities** (lubridate-style): `year`, `month`, `floor_date`, `ceiling_date`, `difftime`, `today`, `now`, duration constructors
- **Statistics**: `mean`, `sd`, `cor`, `rank`, `scale`, `cumsum`, `ntile`, `weighted_mean`, `iqr`, `mad`, and more
- **Factor manipulation** (forcats-style): `fct_infreq`, `fct_lump`, `fct_recode`, `fct_collapse`, `fct_rev`
- **Data quality**: `describe`, `glimpse`, `get_dupes`, `assert_no_nulls`, `assert_unique`, `clean_names`
- **Multi-format I/O**: CSV, Excel, Stata, SPSS, RDS/RData, Parquet, JSON, Google Sheets

## Installation

You can install tidypolars-extra with `pip`:

```bash
pip install tidypolars-extra
```

## Basic usage

tidypolars-extra methods are designed to work like tidyverse functions:

```python
import tidypolars_extra as tp

# create tibble data frame
df = tp.tibble(x = range(3),
               y = range(3, 6),
               z = ['a', 'a', 'b'])

(
    df
    .select('x', 'y', 'z')
    .filter(tp.col('x') < 4, tp.col('y') > 1)
    .arrange(tp.desc('z'), 'x')
    .mutate(double_x = tp.col('x') * 2,
            x_plus_y = tp.col('x') + tp.col('y')
            )
)
┌─────┬─────┬─────┬──────────┬──────────┐
│ x   ┆ y   ┆ z   ┆ double_x ┆ x_plus_y │
│ --- ┆ --- ┆ --- ┆ ---      ┆ ---      │
│ i64 ┆ i64 ┆ str ┆ i64      ┆ i64      │
╞═════╪═════╪═════╪══════════╪══════════╡
│ 2   ┆ 5   ┆ b   ┆ 4        ┆ 7        │
├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤
│ 0   ┆ 3   ┆ a   ┆ 0        ┆ 3        │
├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤
│ 1   ┆ 4   ┆ a   ┆ 2        ┆ 5        │
└─────┴─────┴─────┴──────────┴──────────┘

```

## Converting to/from pandas data frames

If you need to use a package that requires pandas or polars data frames, you can convert from a tidypolars_extra `tibble` to either of those `DataFrame` formats.

```python
# convert to pandas...
df = df.to_pandas()
# ... or convert to polars
df = df.to_polars()
```

To convert from a pandas or polars `DataFrame` to a tidypolars `tibble`:

```python
# convert from pandas...
df = tp.from_pandas(df)
# or covert from polars
df = tp.from_polars(df)
```

## Roadmap

The following features are planned for future releases:

### Missing Tidyverse Functions
- **dplyr**: `slice_min`/`slice_max`, `rows_insert`/`rows_update`/`rows_upsert`, `consecutive_id`, `rename_with`, `expand`/`nesting`, `rowwise` operations (`c_across`, `row_sums`, `row_means`)
- **tidyr**: `expand`, `nesting`
- **stringr**: `word`, `str_to_sentence`
- **forcats**: `fct_reorder` (reorder levels by summary statistic of another variable)
- **purrr-style**: `map`/`map2`/`pmap` equivalents for list columns

### Statistical & Scientific Computing
- `ceiling` (complement to existing `floor`), `exp`, `log2`
- `se` (standard error of the mean)
- `pmin`/`pmax` (parallel min/max across columns)
- `winsorize` (cap extreme values at percentiles)

### Data Quality & Exploration
- `skim()` (richer type-aware summary inspired by R's skimr)
- `assert_type` / `assert_range` (additional data validation assertions)
- Type hints across all public functions for IDE support and static analysis

### Interoperability
- `to_arrow()` (explicit PyArrow Table export)
- DuckDB integration (`to_duckdb`/`from_duckdb`)
- `write_rds` in `save_data` (complete R round-trip)

### Code Quality
- Add comprehensive type hints throughout codebase
- Configure mypy/pyright for static type checking in CI
- Add test coverage measurement and thresholds
- Expand edge case testing (empty DataFrames, NaN, Inf)

## Acknowledgments

This project is an extension of:
- [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci) by Diogo Ferrari
- [tidypolars](https://pypi.org/project/tidypolars/) — the original starting point
