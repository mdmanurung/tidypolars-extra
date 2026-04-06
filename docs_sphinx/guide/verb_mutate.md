# mutate — Create & Transform Columns

`mutate()` adds new columns or modifies existing ones. The original DataFrame is
never modified — a new tibble is returned.

## Basic Usage

```python
import tidypolars_extra as tp
from tidypolars_extra import col

df = tp.tibble(
    name=["Alice", "Bob", "Carol"],
    height=[165, 180, 155],
    weight=[60, 85, 52]
)

# Add a new column
df.mutate(bmi=col("weight") / (col("height") / 100) ** 2)
```

```text
shape: (3, 4)
┌───────┬────────┬────────┬───────────┐
│ name  ┆ height ┆ weight ┆ bmi       │
│ ---   ┆ ---    ┆ ---    ┆ ---       │
│ str   ┆ i64    ┆ i64    ┆ f64       │
╞═══════╪════════╪════════╪═══════════╡
│ Alice ┆ 165    ┆ 60     ┆ 22.038567 │
│ Bob   ┆ 180    ┆ 85     ┆ 26.234568 │
│ Carol ┆ 155    ┆ 52     ┆ 21.640542 │
└───────┴────────┴────────┴───────────┘
```

## Multiple Columns at Once

```python
df.mutate(
    height_m=col("height") / 100,
    weight_lbs=col("weight") * 2.205,
    bmi=col("weight") / (col("height") / 100) ** 2
)
```

## Conditional Logic with if_else

```python
from tidypolars_extra import if_else

df.mutate(
    category=if_else(col("height") > 170, "tall", "short")
)
```

## Complex Conditions with case_when

```python
from tidypolars_extra import case_when

df.mutate(
    size=case_when(
        (col("height") < 160, "small"),
        (col("height") < 175, "medium"),
        (True, "large")  # default
    )
)
```

## Using Aggregate Functions

```python
from tidypolars_extra import mean, sd

# Compare each value to the group mean
df.mutate(
    height_centered=col("height") - mean("height"),
    height_zscore=(col("height") - mean("height")) / sd("height")
)
```

## Row-wise Operations with map

```python
from tidypolars_extra import map

# Apply a custom function to each row
df.mutate(
    description=map(
        lambda row: f"{row['name']} is {row['height']}cm",
        returns=str
    )
)
```

## Bulk Transformations with across

```python
from tidypolars_extra import across, matches, scale

# Standardize multiple numeric columns
df.mutate(
    across(matches("height|weight"), scale, names_suffix="_std")
)
```

## Grouped Mutate

Use `by=` for within-group transformations:

```python
df = tp.tibble(
    dept=["Eng", "Eng", "Sales", "Sales"],
    name=["Alice", "Bob", "Carol", "Dave"],
    salary=[95000, 88000, 72000, 65000]
)

# Compute each person's salary as a share of their department total
df.mutate(
    dept_share=col("salary") / col("salary").sum(),
    by="dept"
)
```

## Overwriting Existing Columns

```python
# Replace height in cm with height in meters
df.mutate(height=col("height") / 100)
```
