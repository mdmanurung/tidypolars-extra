![](docs/_css/tidypolars4sci.png)

# TidyPolars $^{4sci}$ — Extension Package

**tidypolars4sci_ext** is an **extension package** for the original
[tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci). It
re-exports everything from the upstream package and layers on additional
dplyr/tidyr verbs, joins, ranking functions, set operations, and more.

## How it works

- **Imports and re-exports** every symbol from the original `tidypolars4sci`.
- **Adds new functions and tibble methods** that are not yet in the upstream.
- **Monkey-patches `from_polars` / `from_pandas`** at import time so that
  inherited upstream methods transparently return the extended `tibble`.
- Uses the upstream package as its only runtime dependency — no code is
  duplicated.

## Installation

```bash
pip install git+https://github.com/mdmanurung/tidypolars4sci.git
```

This will automatically install the upstream `tidypolars4sci>=0.0.1.22` as a
dependency.

## Basic usage

```python
import tidypolars4sci_ext as tp

# All original tidypolars4sci features are available
df = tp.tibble(x=range(3), y=range(3, 6), z=['a', 'a', 'b'])

(
    df
    .select('x', 'y', 'z')
    .filter(tp.col('x') < 4, tp.col('y') > 1)
    .arrange(tp.desc('z'), 'x')
    .mutate(double_x=tp.col('x') * 2,
            x_plus_y=tp.col('x') + tp.col('y'))
)

# Plus new extension features:
df.slice_min('x', n=2)
df.right_join(other_df, on='x')
df.mutate(label=tp.case_match(tp.col('x'), 1, 'one', _default='other'))
```

## Converting to/from pandas data frames

```python
# convert to pandas or polars
df = df.to_pandas()
df = df.to_polars()

# convert from pandas or polars
df = tp.from_pandas(df)
df = tp.from_polars(df)
```

## Similar projects

- [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci) — the upstream package this extends
- [tidypolars](https://pypi.org/project/tidypolars/) — tidypolars was the starting point of tidypolars4sci

## Features added by this extension

### New dplyr verbs

| Function | Description |
|----------|-------------|
| `right_join()` | Keep all rows from the right table |
| `semi_join()` | Keep rows from left with matches in right |
| `anti_join()` | Keep rows from left without matches in right |
| `cross_join()` | Cartesian product of two tables |
| `slice_min()` | Select rows with smallest values (with ties support) |
| `slice_max()` | Select rows with largest values (with ties support) |
| `slice_sample()` | Randomly sample rows (with `n`, `prop`, `by`) |
| `transmute()` | Mutate and keep only new columns |
| `rename_with()` | Rename columns using a function |
| `add_count()` | Add count column without collapsing rows |
| `tally()` | Simple observation count |
| `uncount()` | Inverse of count: duplicate rows by weight |
| `ungroup()` | Remove grouping from grouped tibble |

### New tidyr functions

| Function | Description |
|----------|-------------|
| `complete()` | Complete all combinations of columns, filling missing with NA |
| `expand()` | Create tibble of all unique column combinations |
| `expand_grid()` | Standalone Cartesian product of named lists |
| `nesting()` | Create tibble of observed (existing) combinations only |
| `separate_rows()` | Separate a column into rows by splitting on a delimiter |
| `extract()` | Extract regex capture groups into new columns |
| `drop_na()` | Alias for `drop_null()` (tidyr naming) |
| `replace_na()` | Alias for `replace_null()` (tidyr naming) |

### Set operations

| Function | Description |
|----------|-------------|
| `union()` | Rows in either table, deduplicated |
| `union_all()` | Rows in either table, keeping duplicates |
| `intersect()` | Rows that appear in both tables |
| `setdiff()` | Rows in first table but not in second |

### Window and ranking functions

| Function | Description |
|----------|-------------|
| `dense_rank()` | Rank with no gaps for ties |
| `min_rank()` | Rank with gaps at ties |
| `percent_rank()` | Rescale ranks to [0, 1] |
| `cume_dist()` | Cumulative distribution (proportion of values <= current) |
| `ntile()` | Divide into n roughly equal buckets |
| `nth()` | Get the nth value (with out-of-bounds default) |
| `cumall()` | Cumulative all (boolean) |
| `cumany()` | Cumulative any (boolean) |
| `cummean()` | Cumulative mean |

### Conditional and grouping functions

| Function | Description |
|----------|-------------|
| `case_match()` | Switch-like pattern matching on values |
| `na_if()` | Replace a specific value with null |
| `consecutive_id()` | Generate consecutive group IDs on value changes |
| `if_all()` | Check if all conditions are true across columns |
| `if_any()` | Check if any condition is true across columns |

### GroupBy enhancements

| Function | Description |
|----------|-------------|
| `n_groups()` | Return the number of groups |
| `group_keys()` | Return tibble of unique group combinations |
| `group_split()` | Split into a list of tibbles, one per group |

### Science-oriented features (from tidypolars4sci)

- `freq()` — Frequency tables with confidence intervals
- `tab()` — Cross-tabulation / contingency tables
- `descriptive_statistics()` — Descriptive statistics summary
- `to_latex()` — Publication-ready LaTeX table output
- `read_data()` — Universal reader for CSV, Excel, Stata, SPSS, R, and Google Sheets
- `save_data()` — Auto-detect format and save
- `to_dta()` — Export to Stata format
- Date/time functions via lubridate-style API
- Type conversion with R-style naming (`as_factor`, `as_character`, etc.)
- Column selection helpers (`matches()`, `where()`, `across()`, etc.)
- String manipulation via stringr-style API
