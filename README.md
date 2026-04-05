![](docs/_css/tidypolars4sci.png)

# TidyPolars $^{4sci}$

**tidypolars4sci** provides functions that match as closely as possible to R's [Tidyverse](https://www.tidyverse.org/) functions for manipulating data frames and conducting data analysis in Python using the blazingly fast [Polars](https://github.com/pola-rs/polars) as backend.

The name **tidypolars4sci** reflects the module's main features:

1. Matches the function names and functionalities of R's [Tidyverse](https://tidyverse.org/).
2. Leverages the performance and efficiency of [Polars](https://github.com/pola-rs/polars) under the hood.
3. Tailored for scientific research, extending the default functionalities of both Polars and Tidyverse.

## Details

**tidypolars4sci** is an **extended** API for [Polars](https://github.com/pola-rs/polars). One of the **main advantages** of using Polars as a data manipulation engine is its exceptional speed when compared to other alternatives (see [here](https://pola.rs/posts/benchmarks/)).

The primary distinction between **tidypolars4sci** and Polars lies in user interaction. The frontend functions are designed to closely resemble those available in R's [Tidyverse](https://tidyverse.org/), making it easier for users familiar with that ecosystem to transition to this library.

Another useful feature of **tidypolars4sci** is its extensive functionality aimed at facilitating data analysis and reporting for scientific research and academic publications. This includes the creation of LaTeX tables, which enhances the presentation of results.

Note: Due to the additional functionalities provided, **tidypolars4sci** may operate slightly slower than using Polars directly.


## Documentation

Available [here](https://diogoferrari.com/tidypolars4sci/).

## Installation

You can install tidypolars4sci with `pip`:

```bash
$ pip3 install tidypolars4sci
```

Or through `conda`:
```bash
$ conda install -c conda-forge tidypolars4sci
```

## Basic usage

tidypolars4sci methods are designed to work like tidyverse functions:

```python
import tidypolars4sci as tp

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

<!-- ## General syntax comparing with tidyverse -->


## Converting to/from pandas data frames

If you need to use a package that requires pandas or polars data frames, you can convert from a tidypolars4sci `tibble` to either of those `DataFrame` formats.

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

## Similar projects

- [tidypolars](https://pypi.org/project/tidypolars/): tidypolars was the starting point of tidypolars4sci

## Additional implementations compared to the original tidypolars

**tidypolars4sci** extends the original [tidypolars](https://github.com/markfairbanks/tidypolars) with the following additional features:

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
