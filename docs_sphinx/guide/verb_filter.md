# filter — Pick Rows

`filter()` keeps rows that match one or more conditions. It's the tidypolars-extra
equivalent of SQL's `WHERE` clause.

## Basic Usage

```python
import tidypolars_extra as tp
from tidypolars_extra import col

df = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave", "Eve"],
    age=[32, 45, 28, 52, 38],
    dept=["Eng", "Sales", "Eng", "HR", "Sales"],
    salary=[95000, 72000, 88000, 65000, 78000]
)

# Keep rows where age > 30
df.filter(col("age") > 30)
```

```text
shape: (3, 4)
┌───────┬─────┬───────┬────────┐
│ name  ┆ age ┆ dept  ┆ salary │
│ ---   ┆ --- ┆ ---   ┆ ---    │
│ str   ┆ i64 ┆ str   ┆ i64    │
╞═══════╪═════╪═══════╪════════╡
│ Alice ┆ 32  ┆ Eng   ┆ 95000  │
│ Bob   ┆ 45  ┆ Sales ┆ 72000  │
│ Dave  ┆ 52  ┆ HR    ┆ 65000  │
└───────┴─────┴───────┴────────┘
```

## Multiple Conditions (AND)

Pass multiple arguments — they are combined with logical AND:

```python
df.filter(col("age") > 30, col("salary") > 70000)
```

```text
shape: (2, 4)
┌───────┬─────┬───────┬────────┐
│ name  ┆ age ┆ dept  ┆ salary │
│ ---   ┆ --- ┆ ---   ┆ ---    │
│ str   ┆ i64 ┆ str   ┆ i64    │
╞═══════╪═════╪═══════╪════════╡
│ Alice ┆ 32  ┆ Eng   ┆ 95000  │
│ Bob   ┆ 45  ┆ Sales ┆ 72000  │
└───────┴─────┴───────┴────────┘
```

## OR Conditions

Use `|` for logical OR:

```python
df.filter((col("dept") == "Eng") | (col("dept") == "HR"))
```

## Using Helper Functions

```python
from tidypolars_extra import is_in, is_not_null, between

# Check membership
df.filter(is_in("dept", ["Eng", "HR"]))

# Range check
df.filter(between("age", 30, 50))

# Not null
df.filter(is_not_null("salary"))
```

## Grouped Filtering

Use `by=` to filter within groups:

```python
# Keep only the highest-paid person per department
df.filter(
    col("salary") == col("salary").max(),
    by="dept"
)
```

## Comparison Operators

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `&` | And |
| `\|` | Or |
| `~` | Not |
