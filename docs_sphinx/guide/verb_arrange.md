# arrange — Sort Rows

`arrange()` reorders rows by one or more columns. By default, sorting is ascending.
Use `desc()` for descending order.

## Basic Usage

```python
import tidypolars_extra as tp
from tidypolars_extra import col, desc

df = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave"],
    age=[32, 45, 28, 52],
    salary=[95000, 72000, 88000, 65000]
)

# Sort by age (ascending)
df.arrange("age")
```

```text
shape: (4, 3)
┌───────┬─────┬────────┐
│ name  ┆ age ┆ salary │
│ ---   ┆ --- ┆ ---    │
│ str   ┆ i64 ┆ i64    │
╞═══════╪═════╪════════╡
│ Carol ┆ 28  ┆ 88000  │
│ Alice ┆ 32  ┆ 95000  │
│ Bob   ┆ 45  ┆ 72000  │
│ Dave  ┆ 52  ┆ 65000  │
└───────┴─────┴────────┘
```

## Descending Order

```python
# Sort by salary, highest first
df.arrange(desc("salary"))
```

```text
shape: (4, 3)
┌───────┬─────┬────────┐
│ name  ┆ age ┆ salary │
│ ---   ┆ --- ┆ ---    │
│ str   ┆ i64 ┆ i64    │
╞═══════╪═════╪════════╡
│ Alice ┆ 32  ┆ 95000  │
│ Carol ┆ 28  ┆ 88000  │
│ Bob   ┆ 45  ┆ 72000  │
│ Dave  ┆ 52  ┆ 65000  │
└───────┴─────┴────────┘
```

## Multiple Sort Keys

Sort by multiple columns — left-to-right priority:

```python
df = tp.tibble(
    dept=["Eng", "Sales", "Eng", "Sales"],
    name=["Alice", "Bob", "Carol", "Dave"],
    salary=[95000, 72000, 88000, 65000]
)

# Sort by department (asc), then by salary (desc)
df.arrange("dept", desc("salary"))
```

```text
shape: (4, 3)
┌───────┬───────┬────────┐
│ dept  ┆ name  ┆ salary │
│ ---   ┆ ---   ┆ ---    │
│ str   ┆ str   ┆ i64    │
╞═══════╪═══════╪════════╡
│ Eng   ┆ Alice ┆ 95000  │
│ Eng   ┆ Carol ┆ 88000  │
│ Sales ┆ Bob   ┆ 72000  │
│ Sales ┆ Dave  ┆ 65000  │
└───────┴───────┴────────┘
```

## In a Pipeline

```python
from tidypolars_extra import mean

# Filter, compute, then sort
(df
 .filter(col("salary") > 60000)
 .mutate(salary_k=col("salary") / 1000)
 .arrange(desc("salary_k")))
```
