# Codebase Evaluation: tidypolars-extra

**Date:** 2026-04-07
**Version evaluated:** 0.1.0 (commit `85f5e5c`)
**Evaluator:** Automated analysis via Claude Code

---

## 1. Overview

**tidypolars-extra** (v0.1.0, beta) is a Python package providing R tidyverse-like functions on top of Polars DataFrames. It targets scientific researchers transitioning from R to Python.

| Metric | Value |
|--------|-------|
| Source code | ~7,224 lines across 13 modules |
| Test code | ~2,164 lines across 14 test files |
| Bundled datasets | 8 (diamonds, flights, iris, mtcars, penguins, starwars, vote, wine) |
| Python support | 3.9 – 3.13 |
| Core dependencies | polars >=1.0, numpy, pandas, pyarrow |
| License | MIT |

---

## 2. Architecture

The package extends `pl.DataFrame` with a `tibble` class (~3,439 lines) offering 79 tidyverse-inspired methods. Supporting modules provide domain-specific functionality:

| Module | Lines | Purpose |
|--------|-------|---------|
| `tibble_df.py` | 3,439 | Core DataFrame class with dplyr/tidyr methods |
| `stats.py` | 617 | Statistical functions (mean, sd, cor, rank, scale, cumsum, ntile, etc.) |
| `io.py` | 566 | Multi-format file I/O (CSV, Excel, Stata, SPSS, R, Parquet, JSON, Google Sheets) |
| `lubridate.py` | 561 | Date/time utilities (floor_date, ceiling_date, difftime, duration constructors) |
| `stringr.py` | 537 | String manipulation (stringr-style) |
| `funs.py` | 420 | Special functions (case_when, if_else, coalesce, between, n_missing, etc.) |
| `io_r.py` | 307 | R file format support via rpy2 |
| `helpers.py` | 218 | Column selection helpers (contains, starts_with, across, where) |
| `forcats.py` | 175 | Factor manipulation (fct_infreq, fct_lump, fct_recode, fct_collapse, fct_rev) |
| `utils.py` | 163 | Internal utility functions |
| `type_conversion.py` | 143 | Type casting (as_character, as_factor, as_integer, etc.) |
| `reexports.py` | 48 | Polars re-exports (col, lit, Expr, Series, dtypes) |

---

## 3. Strengths

### 3.1 Excellent API Design
Faithful tidyverse naming conventions (`mutate`, `filter`, `summarize`, `pivot_longer`, `str_detect`, `as_date`, etc.) significantly lower the barrier for R users. The `tibble` constructor supports kwargs syntax: `tp.tibble(x = [1, 2], y = ['a', 'b'])`.

### 3.2 Comprehensive Documentation
Nearly every public function has NumPy-style docstrings with parameter descriptions and usage examples. Eight tutorial vignettes cover core operations (filter, arrange, select, rename, mutate, transmute, summarize, group_by). Sphinx-based docs deploy to GitHub Pages.

### 3.3 Clean Module Organization
Logical separation by domain mirrors R packages: `stringr.py` for strings, `lubridate.py` for dates, `stats.py` for statistics, `helpers.py` for tidyselect-style helpers. Internal utilities are clearly prefixed with `_`.

### 3.4 Flexible Input Handling
Utility functions (`_col_expr`, `_lit_expr`, `_as_list`, `_kwargs_as_exprs`) transparently handle strings (auto-converted to `pl.col()`), Expressions, Series, and constants. Users can write `tp.mean('x')` or `tp.mean(col('x'))` interchangeably.

### 3.5 Multi-Format I/O
The `read_data` class auto-detects file format and routes to the appropriate reader: CSV, TSV, Excel (xls/xlsx/ods), Stata (.dta), SPSS (.sav), R (.rds/.RData), Google Sheets. Hierarchical header merging is supported.

### 3.6 CI/CD Pipeline
GitHub Actions for testing (matrix across Python 3.9–3.13), Sphinx docs deployment to GitHub Pages, and PyPI publishing via OIDC trusted publishing.

---

## 4. Weaknesses

### 4.1 Minimal Error Handling
- Only 1 bare `except:` clause (in `glimpse()`)
- Most functions lack input validation — incorrect types produce cryptic polars errors
- Only 4 tests used `pytest.raises` for exception testing (pre-evaluation)
- No systematic data validation or helpful error messages at function boundaries

### 4.2 No Type Hints
Zero return type annotations across the codebase. Parameter hints limited to `n: int` in a few places. No mypy/pyright configured. This limits IDE support (autocomplete, hover docs) and prevents static analysis from catching bugs.

### 4.3 Test Gaps
- No edge case testing for empty DataFrames, NaN, Inf, single-row DataFrames
- `nest()` skipped due to polars segfault — no workaround tested
- No test coverage measurement or thresholds configured
- No performance/regression tests
- Optional features (SPSS via pyreadstat, R via rpy2) lack test coverage

### 4.4 Previously Missing Tidyverse Functions (Now Addressed)
Before the v0.1.0 expansion, the package was missing several commonly-used functions that R users would immediately expect. These gaps have since been filled (see Section 5.1 for details). Remaining gaps include:
- **Sampling**: `slice_sample` (unified sampling with grouping support)
- **Data quality**: `skim()` (richer type-aware summary)
- **Factors**: `fct_reorder` (reorder levels by summary of another variable)
- **Slicing**: `slice_min` / `slice_max` (select rows with smallest/largest values)

### 4.5 Code Style Issues
- Uses `== None` with bitwise `&` throughout (e.g., `(x == None) & (y == None)`) instead of idiomatic `x is None and y is None`
- Several ruff rules intentionally disabled (E711, E712, E741, E731) to accommodate existing style
- Wildcard imports (`from .module import *`) used in `__init__.py` and across modules

---

## 5. What Was Done

### 5.1 New Functions Implemented (50+)

All functions include docstrings, follow existing code patterns, and have full test coverage.

**Tibble methods (14):** `semi_join`, `anti_join`, `cross_join`, `pipe`, `transmute`, `clean_names`, `sample_n`, `sample_frac`, `complete`, `describe`, `replace_na`, `get_dupes`, `assert_no_nulls`, `assert_unique`, `to_markdown`

**Statistics (13):** `cumsum`, `cumprod`, `cummax`, `cummin`, `percent_rank`, `cume_dist`, `ntile`, `weighted_mean`, `mode`, `iqr`, `mad`, `zscore`

**String manipulation (7):** `str_count`, `str_pad`, `str_split`, `str_squish`, `str_to_title`, `str_dup`, `str_extract_all`

**Factor manipulation (5, new module):** `fct_infreq`, `fct_lump`, `fct_recode`, `fct_collapse`, `fct_rev`

**Date/time (13):** `today`, `now`, `difftime`, `floor_date`, `ceiling_date`, `days`, `weeks`, `hours`, `minutes`, `seconds`, `milliseconds`, `microseconds`

**Special functions (2):** `n_missing`, `pct_missing`

**I/O (2):** Parquet and JSON/NDJSON reading via `read_data`

### 5.2 Audit Fixes

After implementation, a thorough audit identified and fixed:

| Issue | Severity | Fix |
|-------|----------|-----|
| `ntile()` wrong groups from premature int cast | CRITICAL | Changed to floor-based formula matching R |
| `percent_rank()` division by zero when n=1 | CRITICAL | Added `when(denom==0).then(0.0)` guard |
| `str_split(n=)` returned struct not list | CRITICAL | Removed `n` param, always use `split()` |
| `fct_infreq()` didn't order by frequency | CRITICAL | Rewritten as DataFrame-level with `pl.Enum` |
| `fct_rev()` didn't reverse levels | CRITICAL | Rewritten as DataFrame-level with reversed `pl.Enum` |
| `fct_lump()` broken expression logic | CRITICAL | Rewritten using `len().over()` for frequency |
| `describe()` crash on empty DataFrame | MEDIUM | Added `if not stats_rows` guard |
| `ceiling_date()` bumped boundary dates | MEDIUM | Added `change_on_boundary` param |
| `to_markdown()` O(n*m) row access | MEDIUM | Switched to `iter_rows()` |

### 5.3 Test Coverage

- 73 new tests added (254 total, up from 180)
- Edge case tests for: single-row DataFrames, empty DataFrames, boundary dates, special characters in column names, division by zero
- All existing 180 tests continue to pass (no regressions)

---

## 6. What Still Needs To Be Done

### 6.1 High Priority

**Missing Core Functions:**
- `slice_min` / `slice_max` — select rows with smallest/largest values
- `slice_sample` — unified sampling with grouping support
- `rename_with` — rename columns using a function
- `rows_insert` / `rows_update` / `rows_upsert` — row-level mutations
- `fct_reorder` — reorder factor levels by summary of another variable (requires DataFrame-level implementation)
- `na_if` — replace specific values with null (inverse of `replace_null`)
- `consecutive_id` — ID that increments when values change

**Code Quality:**
- Add type hints to all public functions (enables IDE autocomplete and mypy)
- Configure mypy or pyright in CI
- Add test coverage measurement (e.g., `pytest-cov`) with minimum thresholds
- Replace bare `except:` in `glimpse()` with specific exception types

### 6.2 Medium Priority

**Additional Functions:**
- `expand` / `nesting` — generate all or existing combinations of column values
- Row-wise operations: `row_sums`, `row_means`, `c_across`
- `pmin` / `pmax` — element-wise min/max across columns
- `ceiling` (complement to existing `floor`), `exp`, `log2`
- `se` — standard error of the mean
- `word` — extract words from strings by position
- `str_to_sentence` — sentence case conversion

**Data Quality:**
- `skim()` — richer type-aware summary (inspired by R's skimr package)
- `assert_type` / `assert_range` — additional validation assertions
- `tabyl` — simple frequency tables (inspired by janitor)

**Tidyselect Helpers:**
- `all_of` / `any_of` — programmatic column selection with/without error on missing
- `num_range` — select columns matching prefix + numeric range (e.g., `q1`–`q50`)
- `last_col` — select last column with optional offset

### 6.3 Lower Priority

**Interoperability:**
- `to_arrow()` — explicit PyArrow Table conversion
- DuckDB integration (`to_duckdb` / `from_duckdb`)
- `write_rds` in `save_data` — complete R round-trip
- Clipboard I/O (`write_clip` / `read_clip`)

**Statistical/Scientific:**
- `winsorize` — cap extreme values at percentiles
- Additional correlation methods (Kendall)
- Bootstrap confidence intervals

**Infrastructure:**
- Expand documentation: add vignettes for new modules (forcats, statistics, dates)
- Add performance benchmarks
- Consider API stability markers (stable vs. experimental)
- Add `__all__` exports to tibble_df.py for new methods
- Update `__dir__` in tibble class to include new methods

---

## 7. Metrics Summary

| Metric | Before | After |
|--------|--------|-------|
| Source files | 12 | 13 (+forcats.py) |
| Source lines | ~5,870 | ~7,224 |
| Test files | 13 | 14 (+test_new_features.py) |
| Test functions | 180 | 254 |
| Public functions/methods | ~100 | ~208 |
| Modules | 10 | 11 |
| Ruff violations | 0 | 0 |
