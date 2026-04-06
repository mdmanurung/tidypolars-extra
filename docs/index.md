# tidypolars-extra

**Tidyverse-style data manipulation for Python, powered by Polars.**

tidypolars-extra provides functions that closely match R's
[Tidyverse](https://www.tidyverse.org/) for manipulating data frames in Python,
using the fast [Polars](https://docs.pola.rs/) engine as backend.

## Key Features

- **Fast** — Built on [Polars](https://docs.pola.rs/) for high-performance data
  manipulation with parallel execution.
- **Familiar syntax** — API mirrors R's Tidyverse (`filter`, `mutate`, `select`,
  `summarize`, etc.).
- **Type conversions** — R-style type coercion functions (`as_integer`,
  `as_factor`, `as_character`, etc.).
- **String operations** — `stringr`-style string manipulation (`str_detect`,
  `str_replace`, `paste`, etc.).
- **Date/time handling** — `lubridate`-style date functions (`year`, `month`,
  `mday`, `as_date`, etc.).
- **Statistics** — Common statistical functions (`mean`, `sd`, `cor`,
  `quantile`, `scale`, etc.).
- **I/O support** — Read CSV, Excel, Stata, SPSS, R (RDS/Rdata), and Google
  Sheets.
- **LaTeX output** — Export publication-ready LaTeX tables directly from your
  data.

## Quick Example

```python
import tidypolars_extra as tp

df = tp.tibble(
    name=["Alice", "Bob", "Charlie", "Diana"],
    age=[30, 25, 35, 28],
    score=[85, 92, 78, 95],
)

result = (
    df
    .filter(tp.col("age") > 26)
    .mutate(grade=tp.case_when(
        tp.col("score") >= 90, "A",
        tp.col("score") >= 80, "B",
        _default="C",
    ))
    .arrange(tp.desc("score"))
    .select("name", "age", "grade")
)
```

```{toctree}
:maxdepth: 2
:caption: Contents

installation
```

```{toctree}
:maxdepth: 2
:caption: Guide

vignettes/01_filter
vignettes/02_arrange
vignettes/03_select
vignettes/04_rename
vignettes/05_mutate
vignettes/06_transmute
vignettes/07_summarize
vignettes/08_group_by
```

```{toctree}
:maxdepth: 3
:caption: API Reference

autoapi/index
```
