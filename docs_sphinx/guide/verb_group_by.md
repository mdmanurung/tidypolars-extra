# group_by — Group Operations

`group_by()` splits a tibble into groups, so that subsequent operations (like
`mutate` or `summarize`) are applied within each group.

## Using `by=` (Recommended)

The simplest way to group is with the `by=` parameter available on `filter`,
`mutate`, `summarize`, `slice`, and other verbs:

```python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, n

df = tp.tibble(
    dept=["Eng", "Eng", "Sales", "Sales", "HR"],
    name=["Alice", "Bob", "Carol", "Dave", "Eve"],
    salary=[95000, 88000, 72000, 65000, 58000]
)

# Summarize by group, no separate group_by needed
df.summarize(
    avg_salary=mean("salary"),
    count=n(),
    by="dept"
)
```

## Explicit group_by()

For multiple grouped operations, use `group_by()` which returns a `TibbleGroupBy`:

```python
grouped = df.group_by("dept")

# Summarize
grouped.summarize(avg=mean("salary"))

# Mutate (adds group-level calculations to each row)
grouped.mutate(dept_avg=mean("salary"))
```

## Multiple Grouping Columns

```python
df.summarize(
    avg=mean("salary"),
    by=["dept", "region"]
)

# Or with explicit group_by
df.group_by("dept", "region").summarize(avg=mean("salary"))
```

## Grouped Filter

Keep rows that meet a condition within each group:

```python
# Keep only the highest salary per department
df.filter(
    col("salary") == col("salary").max(),
    by="dept"
)
```

## Grouped Mutate

Add group-level information to each row:

```python
df.mutate(
    dept_avg=mean("salary"),
    pct_of_dept=col("salary") / col("salary").sum() * 100,
    by="dept"
)
```

## Grouped Slice

Take the top N rows per group:

```python
# Top 2 highest-paid per department
df.arrange(col("salary").sort(descending=True)).slice_head(n=2, by="dept")
```

## count() — Group and Count

A convenient shorthand:

```python
df.count("dept")
df.count("dept", "region", sort=True)
```
