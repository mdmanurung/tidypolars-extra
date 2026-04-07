# CLAUDE.md

## Project Overview

**tidypolars-extra** is a Python package that extends Polars DataFrames with R tidyverse-like APIs. It targets scientific researchers transitioning from R to Python, providing familiar function names (`mutate`, `filter`, `summarize`, `str_detect`, `as_date`, etc.) on top of Polars' high-performance engine.

## Development Setup

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Optional: SPSS file support
pip install -e ".[sav]"

# Optional: R file interop via rpy2
pip install -e ".[r]"
```

## Commands

```bash
# Run tests
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_tibble.py -v

# Lint
ruff check tidypolars_extra/

# Build docs (requires docs/requirements.txt)
sphinx-build -b html docs docs/_build/html -W
```

CI runs tests across Python 3.9–3.13 and lints with ruff on every push/PR.

## Module Structure

| Module | Lines | Purpose |
|--------|-------|---------|
| `tibble_df.py` | 3,439 | Core `tibble` class extending `pl.DataFrame` — 79 dplyr/tidyr methods |
| `stats.py` | 617 | Statistical functions (mean, sd, cor, rank, scale, cumsum, ntile, etc.) |
| `io.py` | 566 | Multi-format file I/O (CSV, Excel, Stata, SPSS, R, Parquet, JSON, Google Sheets) |
| `lubridate.py` | 561 | Date/time utilities (floor_date, ceiling_date, difftime, duration constructors) |
| `stringr.py` | 537 | String manipulation (str_detect, str_extract, str_replace, str_pad, etc.) |
| `funs.py` | 420 | Special functions (case_when, if_else, coalesce, between, n_missing, etc.) |
| `io_r.py` | 307 | R file format support via rpy2 |
| `helpers.py` | 218 | Tidyselect helpers (contains, starts_with, ends_with, matches, where, across) |
| `forcats.py` | 175 | Factor manipulation (fct_infreq, fct_lump, fct_recode, fct_collapse, fct_rev) |
| `utils.py` | 163 | Internal utility functions (_col_expr, _kwargs_as_exprs, _as_list, etc.) |
| `type_conversion.py` | 143 | Type casting (as_character, as_factor, as_integer, as_numeric, as_date, etc.) |
| `reexports.py` | 48 | Polars re-exports (col, lit, Expr, Series, dtypes) |

Bundled datasets (diamonds, flights, iris, mtcars, penguins, starwars, vote, wine) live in `tidypolars_extra/data/`.

## Code Conventions

- **Docstrings**: NumPy-style on all public functions with parameter descriptions and examples
- **Internal utilities**: Prefixed with `_` (e.g., `_col_expr`, `_lit_expr`, `_as_list`)
- **Null comparisons**: Uses `== None` with bitwise `&` operators throughout — this is an intentional codebase convention (ruff rules E711/E712 are disabled)
- **Wildcard imports**: `__init__.py` uses `from .module import *` intentionally to expose a flat tidyverse-like API
- **Line length**: 120 characters max
- **Lambda assignments**: Used for concise aliases (E731 disabled)
- **Bare except**: Exists in `glimpse()` (E722 disabled) — should be replaced with specific exceptions
- **Disabled ruff rules**: E501, E711, E712, E741, F401, F811, E731, E722 — see `pyproject.toml [tool.ruff.lint]` for rationale

## Key Patterns

- **`tibble` class** extends `pl.DataFrame` directly — all Polars methods are available alongside tidyverse methods
- **Flexible input handling**: `_col_expr()` converts strings to `pl.col()` automatically, so `tp.mean('x')` and `tp.mean(col('x'))` both work
- **Factor functions** in `forcats.py` operate at the DataFrame level using `pl.Enum` types (not expression level)
- **`read_data` class** auto-detects file format from extension and routes to the appropriate reader
- **kwargs constructors**: `tp.tibble(x=[1, 2], y=['a', 'b'])` matches R's tibble syntax
- **`API_labels` dict** in `__init__.py` maps module names to display labels for documentation

## Testing

- 254 test functions across 14 test files (~2,164 lines)
- Tests use `tp.tibble()` directly for fixture data (no shared fixtures)
- `test_new_features.py` uses class-based test organization; other files use module-level functions
- No coverage measurement configured yet

## Build and Publish

- **Build system**: hatchling (pyproject.toml-based)
- **CI**: GitHub Actions — `ci.yml` (tests + lint), `docs.yml` (Sphinx → GitHub Pages), `publish.yml` (PyPI via OIDC)
- **Package name**: `tidypolars-extra` (import as `tidypolars_extra`)
