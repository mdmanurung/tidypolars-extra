# select — Pick Columns

`select()` keeps, drops, or renames columns. It supports column names, lists,
slices, and tidy-select helper functions.

## Basic Usage

```python
import tidypolars_extra as tp
from tidypolars_extra import col

df = tp.tibble(
    name=["Alice", "Bob", "Carol"],
    age=[32, 45, 28],
    dept=["Eng", "Sales", "Eng"],
    salary=[95000, 72000, 88000],
    score=[88, 92, 75]
)

# Select specific columns
df.select("name", "salary")
```

```text
shape: (3, 2)
┌───────┬────────┐
│ name  ┆ salary │
│ ---   ┆ ---    │
│ str   ┆ i64    │
╞═══════╪════════╡
│ Alice ┆ 95000  │
│ Bob   ┆ 72000  │
│ Carol ┆ 88000  │
└───────┴────────┘
```

## Using Selection Helpers

tidypolars-extra provides several helper functions for flexible column selection:

```python
from tidypolars_extra import starts_with, ends_with, contains, matches, everything

# Columns that start with "s"
df.select(starts_with("s"))       # salary, score

# Columns that end with "e"
df.select(ends_with("e"))         # name, age, score

# Columns containing "al"
df.select(contains("al"))         # salary

# Regex match
df.select(matches("^s[a-z]+e$"))  # score

# All columns
df.select(everything())
```

## Renaming While Selecting

Pass a dictionary to rename columns during selection:

```python
df.select({"name": "employee", "salary": "pay"})
```

## Dropping Columns

Use `drop()` to remove specific columns:

```python
df.drop("score", "dept")
```

## Reordering Columns with relocate

```python
# Move salary before name
df.relocate("salary", before="name")

# Move score after name
df.relocate("score", after="name")
```

## Type-Based Selection with where

```python
from tidypolars_extra import where, is_numeric, is_string

# Select only numeric columns
df.select(where(is_numeric))

# Select only string columns
df.select(where(is_string))
```

## In a Pipeline

```python
from tidypolars_extra import desc

(df
 .select("name", "dept", "salary")
 .filter(col("salary") > 80000)
 .arrange(desc("salary")))
```
