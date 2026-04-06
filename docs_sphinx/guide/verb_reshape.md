# Reshaping — Pivot, Separate, Unite, Nest

tidypolars-extra provides verbs for transforming the shape of your data between
wide and long formats, splitting and combining columns, and nesting DataFrames.

## pivot_longer — Wide to Long

Collapse multiple columns into key-value pairs:

```python
import tidypolars_extra as tp
from tidypolars_extra import col

df = tp.tibble(
    name=["Alice", "Bob"],
    math=[90, 85],
    science=[88, 92],
    english=[78, 95]
)

df.pivot_longer(
    cols=["math", "science", "english"],
    names_to="subject",
    values_to="score"
)
```

```text
shape: (6, 3)
┌───────┬─────────┬───────┐
│ name  ┆ subject ┆ score │
│ ---   ┆ ---     ┆ ---   │
│ str   ┆ str     ┆ i64   │
╞═══════╪═════════╪═══════╡
│ Alice ┆ math    ┆ 90    │
│ Alice ┆ science ┆ 88    │
│ Alice ┆ english ┆ 78    │
│ Bob   ┆ math    ┆ 85    │
│ Bob   ┆ science ┆ 92    │
│ Bob   ┆ english ┆ 95    │
└───────┴─────────┴───────┘
```

## pivot_wider — Long to Wide

Spread key-value pairs across multiple columns:

```python
long_df = tp.tibble(
    name=["Alice", "Alice", "Bob", "Bob"],
    metric=["height", "weight", "height", "weight"],
    value=[165, 60, 180, 85]
)

long_df.pivot_wider(
    names_from="metric",
    values_from="value"
)
```

```text
shape: (2, 3)
┌───────┬────────┬────────┐
│ name  ┆ height ┆ weight │
│ ---   ┆ ---    ┆ ---    │
│ str   ┆ i64    ┆ i64    │
╞═══════╪════════╪════════╡
│ Alice ┆ 165    ┆ 60     │
│ Bob   ┆ 180    ┆ 85     │
└───────┴────────┴────────┘
```

### Aggregation in pivot_wider

When there are duplicate entries, specify an aggregation function:

```python
df = tp.tibble(
    group=["A", "A", "A", "B", "B"],
    metric=["x", "x", "y", "x", "y"],
    value=[1, 2, 3, 4, 5]
)

df.pivot_wider(
    names_from="metric",
    values_from="value",
    values_fn="mean"
)
```

## separate — Split a Column

Split one column into multiple columns by a separator:

```python
df = tp.tibble(
    date_str=["2024-01-15", "2024-02-20", "2024-03-25"]
)

df.separate("date_str", into=["year", "month", "day"], sep="-")
```

```text
shape: (3, 3)
┌──────┬───────┬─────┐
│ year ┆ month ┆ day │
│ ---  ┆ ---   ┆ --- │
│ str  ┆ str   ┆ str │
╞══════╪═══════╪═════╡
│ 2024 ┆ 01    ┆ 15  │
│ 2024 ┆ 02    ┆ 20  │
│ 2024 ┆ 03    ┆ 25  │
└──────┴───────┴─────┘
```

## unite — Combine Columns

Combine multiple columns into one:

```python
df = tp.tibble(
    first=["Alice", "Bob"],
    last=["Smith", "Jones"]
)

df.unite(col="full_name", unite_cols=["first", "last"], sep=" ")
```

## nest — Nest Data

Create a column of sub-DataFrames grouped by key columns:

```python
df = tp.tibble(
    dept=["Eng", "Eng", "Sales", "Sales"],
    name=["Alice", "Bob", "Carol", "Dave"],
    salary=[95000, 88000, 72000, 65000]
)

nested = df.nest(by="dept")
nested
```

```text
shape: (2, 2)
┌───────┬──────────────────────┐
│ dept  ┆ data                 │
│ ---   ┆ ---                  │
│ str   ┆ struct               │
╞═══════╪══════════════════════╡
│ Eng   ┆ {["Alice","Bob"],..} │
│ Sales ┆ {["Carol","Dave"],.. │
└───────┴──────────────────────┘
```

## unnest — Unnest Data

Expand a nested column back into regular columns:

```python
nested.unnest("data")
```

## crossing — All Combinations

Generate all combinations of values:

```python
df = tp.tibble(x=[1, 2])
df.crossing(y=["a", "b", "c"])
```

```text
shape: (6, 2)
┌─────┬─────┐
│ x   ┆ y   │
│ --- ┆ --- │
│ i64 ┆ str │
╞═════╪═════╡
│ 1   ┆ a   │
│ 1   ┆ b   │
│ 1   ┆ c   │
│ 2   ┆ a   │
│ 2   ┆ b   │
│ 2   ┆ c   │
└─────┴─────┘
```
