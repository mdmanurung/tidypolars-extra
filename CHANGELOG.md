## [Unreleased]

### Added

#### Tibble Methods (14 new)
* `semi_join()` - keep rows with a match in another DataFrame (no columns added)
* `anti_join()` - keep rows without a match in another DataFrame
* `cross_join()` - Cartesian product of two DataFrames
* `pipe()` - apply a function to the entire DataFrame for functional composition
* `transmute()` - mutate and keep only the new columns
* `clean_names()` - standardize column names (snake_case, lower, upper)
* `sample_n()` / `sample_frac()` - random sampling by count or fraction
* `complete()` - expand all combinations of columns, fill missing with NA or specified values
* `describe()` - summary statistics per column (type, nulls, mean, std, quantiles)
* `replace_na()` - replace null values per column via a dictionary
* `get_dupes()` - find and count duplicate rows
* `assert_no_nulls()` / `assert_unique()` - inline data validation assertions
* `to_markdown()` - render DataFrame as a Markdown table string

#### Statistics (13 new in `stats.py`)
* Cumulative functions: `cumsum()`, `cumprod()`, `cummax()`, `cummin()`
* Ranking functions: `percent_rank()`, `cume_dist()`, `ntile()`
* Descriptive stats: `weighted_mean()`, `mode()`, `iqr()`, `mad()`
* Alias: `zscore()` (alias for `scale()`)

#### String Manipulation (7 new in `stringr.py`)
* `str_count()` - count pattern occurrences
* `str_pad()` - pad strings to a fixed width (left, right, both)
* `str_split()` - split strings by pattern into list column
* `str_squish()` - trim and collapse internal whitespace
* `str_to_title()` - convert to Title Case
* `str_dup()` - repeat/duplicate strings
* `str_extract_all()` - extract all pattern matches as list column

#### Factor Manipulation (new `forcats.py` module, 5 functions)
* `fct_infreq()` - reorder factor levels by frequency (most common first)
* `fct_lump()` - collapse least frequent levels into "Other" (by count or proportion)
* `fct_recode()` - manually recode factor levels
* `fct_collapse()` - collapse multiple levels into one
* `fct_rev()` - reverse factor level order

#### Date/Time (13 new in `lubridate.py`)
* `today()` / `now()` - current date/datetime as literals
* `difftime()` - time differences in specified units (days, hours, minutes, etc.)
* `floor_date()` / `ceiling_date()` - round dates down/up to unit boundary
* Duration constructors: `days()`, `weeks()`, `hours()`, `minutes()`, `seconds()`, `milliseconds()`, `microseconds()`

#### Special Functions (2 new in `funs.py`)
* `n_missing()` - count null values in a column
* `pct_missing()` - percentage of null values in a column

#### I/O (2 new readers in `io.py`)
* `read_parquet` support via `read_data(fn='file.parquet')`
* `read_json` / `read_ndjson` support via `read_data(fn='file.json')`

### Known Limitations
* `fct_infreq()` and `fct_rev()` operate at the DataFrame level (not expression level)
* `mode()`, `iqr()`, `mad()` are aggregation functions — use in `summarize()`, not `mutate()`
* `complete()` uses `itertools.product` — can be memory-intensive for high-cardinality columns

---

## [0.1.0]

* First stable release of `tidypolars-extra`
* Renamed package from `tidypolars4sci` to `tidypolars-extra` (import as `tidypolars_extra`)
* Updated all imports and test suite for the new package name
* Full compatibility with Polars 1.39+
* Trusted publishing (OIDC) via GitHub Actions for PyPI and TestPyPI
* CI testing on Python 3.9–3.13

## [0.0.1.22] 

* Minor corrections to create latex tables using tibble.to_latex()

## [0.0.1] 

* First release of `tidypolars_extra`
