# summarize — Aggregate Data

`summarize()` (or `summarise()`) collapses multiple rows into summary statistics.
It works hand-in-hand with grouping to compute per-group aggregations.

## Basic Usage

```python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, sd, min, max, n

df = tp.tibble(
    dept=["Eng", "Eng", "Sales", "Sales", "HR"],
    name=["Alice", "Bob", "Carol", "Dave", "Eve"],
    salary=[95000, 88000, 72000, 65000, 58000]
)

# Overall summary
df.summarize(
    avg_salary=mean("salary"),
    sd_salary=sd("salary"),
    min_salary=min("salary"),
    max_salary=max("salary"),
    count=n()
)
```

```text
shape: (1, 5)
┌────────────┬──────────────┬────────────┬────────────┬───────┐
│ avg_salary ┆ sd_salary    ┆ min_salary ┆ max_salary ┆ count │
│ ---        ┆ ---          ┆ ---        ┆ ---        ┆ ---   │
│ f64        ┆ f64          ┆ i64        ┆ i64        ┆ u32   │
╞════════════╪══════════════╪════════════╪════════════╪═══════╡
│ 75600.0    ┆ 15373.863...  ┆ 58000      ┆ 95000      ┆ 5     │
└────────────┴──────────────┴────────────┴────────────┴───────┘
```

## Grouped Summarize with `by=`

The `by=` parameter is the most convenient way to compute per-group summaries:

```python
df.summarize(
    avg_salary=mean("salary"),
    headcount=n(),
    by="dept"
)
```

```text
shape: (3, 3)
┌───────┬────────────┬───────────┐
│ dept  ┆ avg_salary ┆ headcount │
│ ---   ┆ ---        ┆ ---       │
│ str   ┆ f64        ┆ u32       │
╞═══════╪════════════╪═══════════╡
│ Eng   ┆ 91500.0    ┆ 2         │
│ Sales ┆ 68500.0    ┆ 2         │
│ HR    ┆ 58000.0    ┆ 1         │
└───────┴────────────┴───────────┘
```

## Multiple Grouping Columns

```python
df = tp.tibble(
    region=["East", "East", "West", "West", "East"],
    dept=["Eng", "Sales", "Eng", "Sales", "Eng"],
    salary=[95000, 72000, 88000, 65000, 102000]
)

df.summarize(
    avg=mean("salary"),
    count=n(),
    by=["region", "dept"]
)
```

## Available Aggregate Functions

| Function | Description |
|----------|-------------|
| `mean("col")` | Arithmetic mean |
| `median("col")` | Median value |
| `sd("col")` | Standard deviation |
| `var("col")` | Variance |
| `min("col")` | Minimum value |
| `max("col")` | Maximum value |
| `sum("col")` | Sum of values |
| `n()` | Count of rows |
| `n_distinct("col")` | Count of unique values |
| `first("col")` | First value |
| `last("col")` | Last value |
| `quantile("col", q)` | Quantile value |

## Using count()

A shorthand for `group_by` + count:

```python
df = tp.tibble(
    dept=["Eng", "Eng", "Sales", "Sales", "HR"],
    name=["Alice", "Bob", "Carol", "Dave", "Eve"]
)

df.count("dept", sort=True)
```

```text
shape: (3, 2)
┌───────┬─────┐
│ dept  ┆ n   │
│ ---   ┆ --- │
│ str   ┆ u32 │
╞═══════╪═════╡
│ Eng   ┆ 2   │
│ Sales ┆ 2   │
│ HR    ┆ 1   │
└───────┴─────┘
```

## Descriptive Statistics

For a comprehensive statistical summary, use `descriptive_statistics()`:

```python
df = tp.tibble(
    group=["A", "A", "B", "B"],
    x=[10, 20, 30, 40],
    y=[1.5, 2.5, 3.5, 4.5]
)

df.descriptive_statistics(vars=["x", "y"])
```

## Frequency Tables

```python
df.freq(vars=["dept"])
```

Produces relative frequency tables with counts, percentages, standard deviations,
and 95% confidence intervals.
