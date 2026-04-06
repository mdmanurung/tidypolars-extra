# Getting Started

## Installation

Install tidypolars-extra from PyPI:

```bash
pip install tidypolars-extra
```

### Requirements

- Python 3.9 or later
- Polars ≥ 1.0, NumPy, Pandas, PyArrow

## Your First Analysis

```python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, sd, n, desc

# Create a tibble (enhanced DataFrame)
df = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"],
    dept=["Eng", "Sales", "Eng", "Sales", "Eng", "Sales"],
    salary=[95000, 72000, 88000, 65000, 102000, 78000],
    years=[5, 3, 7, 2, 10, 4]
)
df
```

```text
shape: (6, 4)
┌───────┬───────┬────────┬───────┐
│ name  ┆ dept  ┆ salary ┆ years │
│ ---   ┆ ---   ┆ ---    ┆ ---   │
│ str   ┆ str   ┆ i64    ┆ i64   │
╞═══════╪═══════╪════════╪═══════╡
│ Alice ┆ Eng   ┆ 95000  ┆ 5     │
│ Bob   ┆ Sales ┆ 72000  ┆ 3     │
│ Carol ┆ Eng   ┆ 88000  ┆ 7     │
│ Dave  ┆ Sales ┆ 65000  ┆ 2     │
│ Eve   ┆ Eng   ┆ 102000 ┆ 10    │
│ Frank ┆ Sales ┆ 78000  ┆ 4     │
└───────┴───────┴────────┴───────┘
```

### Filter rows

```python
# Keep only engineers with salary above 90k
df.filter(col("dept") == "Eng", col("salary") > 90000)
```

```text
shape: (2, 4)
┌───────┬──────┬────────┬───────┐
│ name  ┆ dept ┆ salary ┆ years │
│ ---   ┆ ---  ┆ ---    ┆ ---   │
│ str   ┆ str  ┆ i64    ┆ i64   │
╞═══════╪══════╪════════╪═══════╡
│ Alice ┆ Eng  ┆ 95000  ┆ 5     │
│ Eve   ┆ Eng  ┆ 102000 ┆ 10    │
└───────┴──────┴────────┴───────┘
```

### Add new columns with mutate

```python
from tidypolars_extra import if_else

df.mutate(
    salary_k=col("salary") / 1000,
    senior=if_else(col("years") >= 5, "Yes", "No")
)
```

### Summarize by group

```python
df.summarize(
    avg_salary=mean("salary"),
    headcount=n(),
    by="dept"
)
```

```text
shape: (2, 3)
┌───────┬────────────┬───────────┐
│ dept  ┆ avg_salary ┆ headcount │
│ ---   ┆ ---        ┆ ---       │
│ str   ┆ f64        ┆ u32       │
╞═══════╪════════════╪═══════════╡
│ Eng   ┆ 95000.0    ┆ 3         │
│ Sales ┆ 71666.67   ┆ 3         │
└───────┴────────────┴───────────┘
```

### Chain it all together

```python
result = (
    df
    .filter(col("salary") > 60000)
    .mutate(salary_k=col("salary") / 1000)
    .summarize(
        avg_salary_k=mean("salary_k"),
        headcount=n(),
        by="dept"
    )
    .arrange(desc("avg_salary_k"))
)
```

## Converting Between Formats

tidypolars-extra interoperates smoothly with Pandas and Polars:

```python
import pandas as pd
import polars as pl

# From pandas
pandas_df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
df = tp.from_pandas(pandas_df)

# From polars
polars_df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
df = tp.from_polars(polars_df)

# Back to pandas or polars
df.to_pandas()
df.to_polars()
```

## What's Next?

- **{doc}`Syntax Comparisons <comparisons/index>`** — See how tidypolars-extra compares to pandas and siuba
- **{doc}`User Guide <guide/index>`** — In-depth tutorials on every verb and feature
- **{doc}`API Reference <api/index>`** — Complete reference for all functions and methods
