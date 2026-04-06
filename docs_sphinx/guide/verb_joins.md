# Joins — Combining Tables

tidypolars-extra provides three join verbs for combining tables by matching rows
on shared columns.

## Setup

```python
import tidypolars_extra as tp
from tidypolars_extra import col

employees = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave"],
    dept_id=[1, 2, 1, 3]
)

departments = tp.tibble(
    dept_id=[1, 2, 4],
    dept_name=["Engineering", "Sales", "Marketing"]
)
```

## left_join — Keep All Left Rows

Keeps every row from the left table, adding columns from the right table where
keys match. Unmatched rows get `null`.

```python
employees.left_join(departments, on="dept_id")
```

```text
shape: (4, 3)
┌───────┬─────────┬─────────────┐
│ name  ┆ dept_id ┆ dept_name   │
│ ---   ┆ ---     ┆ ---         │
│ str   ┆ i64     ┆ str         │
╞═══════╪═════════╪═════════════╡
│ Alice ┆ 1       ┆ Engineering │
│ Bob   ┆ 2       ┆ Sales       │
│ Carol ┆ 1       ┆ Engineering │
│ Dave  ┆ 3       ┆ null        │
└───────┴─────────┴─────────────┘
```

## inner_join — Keep Only Matches

Keeps only rows that have a match in both tables:

```python
employees.inner_join(departments, on="dept_id")
```

```text
shape: (3, 3)
┌───────┬─────────┬─────────────┐
│ name  ┆ dept_id ┆ dept_name   │
│ ---   ┆ ---     ┆ ---         │
│ str   ┆ i64     ┆ str         │
╞═══════╪═════════╪═════════════╡
│ Alice ┆ 1       ┆ Engineering │
│ Bob   ┆ 2       ┆ Sales       │
│ Carol ┆ 1       ┆ Engineering │
└───────┴─────────┴─────────────┘
```

## full_join — Keep Everything

Keeps all rows from both tables, filling `null` where there is no match:

```python
employees.full_join(departments, on="dept_id")
```

```text
shape: (5, 3)
┌───────┬─────────┬─────────────┐
│ name  ┆ dept_id ┆ dept_name   │
│ ---   ┆ ---     ┆ ---         │
│ str   ┆ i64     ┆ str         │
╞═══════╪═════════╪═════════════╡
│ Alice ┆ 1       ┆ Engineering │
│ Bob   ┆ 2       ┆ Sales       │
│ Carol ┆ 1       ┆ Engineering │
│ Dave  ┆ 3       ┆ null        │
│ null  ┆ 4       ┆ Marketing   │
└───────┴─────────┴─────────────┘
```

## Different Column Names

When the join key has different names in each table, use `left_on` and `right_on`:

```python
employees2 = tp.tibble(
    name=["Alice", "Bob"],
    department=[1, 2]
)

departments2 = tp.tibble(
    id=[1, 2],
    dept_name=["Engineering", "Sales"]
)

employees2.left_join(departments2, left_on="department", right_on="id")
```

## Suffix for Duplicate Columns

When both tables have columns with the same name (besides the key), use `suffix`:

```python
df1 = tp.tibble(id=[1, 2], value=[10, 20])
df2 = tp.tibble(id=[1, 2], value=[100, 200])

df1.left_join(df2, on="id", suffix="_other")
```

```text
shape: (2, 3)
┌─────┬───────┬─────────────┐
│ id  ┆ value ┆ value_other │
│ --- ┆ ---   ┆ ---         │
│ i64 ┆ i64   ┆ i64         │
╞═════╪═══════╪═════════════╡
│ 1   ┆ 10    ┆ 100         │
│ 2   ┆ 20    ┆ 200         │
└─────┴───────┴─────────────┘
```

## Binding Rows and Columns

For simple stacking (not key-based joining):

```python
# Stack rows
df1 = tp.tibble(x=[1, 2], y=[3, 4])
df2 = tp.tibble(x=[5, 6], y=[7, 8])
df1.bind_rows(df2)

# Stack columns
a = tp.tibble(x=[1, 2])
b = tp.tibble(y=[3, 4])
a.bind_cols(b)
```
