# Filter

The `.filter()` method keeps rows of data that meet all specified conditions.

At its core, it follows these rules:

* If each condition is true for a row, then it keeps that row.
* It does not keep a row when a condition results in null values.
* It supports grouped filtering via the `by` parameter.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))
```

## Filter basics

A row must meet all conditions to be kept. You can verbalize the conditions below as,
"`cyl` is equal to four **and** `gear` is equal to five".

```python
mtcars.filter(tp.col("cyl") == 4, tp.col("gear") == 5)
```

```
shape: (2, 12)
┌───────────────┬──────┬─────┬───────┬───┬─────┬─────┬──────┬──────┐
│ name          ┆ mpg  ┆ cyl ┆ disp  ┆ … ┆ vs  ┆ am  ┆ gear ┆ carb │
╞═══════════════╪══════╪═════╪═══════╪═══╪═════╪═════╪══════╪══════╡
│ Porsche 914-2 ┆ 26.0 ┆ 4   ┆ 120.3 ┆ … ┆ 0   ┆ 1   ┆ 5    ┆ 2    │
│ Lotus Europa  ┆ 30.4 ┆ 4   ┆ 95.1  ┆ … ┆ 1   ┆ 1   ┆ 5    ┆ 2    │
└───────────────┴──────┴─────┴───────┴───┴─────┴─────┴──────┴──────┘
```

## Filters with OR conditions

To keep a row when **one of several** conditions is met, use the bar (`|`) operator.

```python
mtcars.filter((tp.col("cyl") == 4) | (tp.col("gear") == 5))
```

The code above keeps rows where `cyl` is equal to 4 **or** `gear` is equal to 5.

Be sure to put parentheses around both sides of the `|`. Otherwise, Python
will group the operation unexpectedly due to operator precedence.

## Dropping nulls

When a condition evaluates to a `null` value, the row is automatically excluded
from the result. This makes `filter` safe to use on data that contains missing values.

```python
df = tp.tibble(x=[True, False, None])

df
# shape: (3, 1)
# ┌───────┐
# │ x     │
# │ bool  │
# ╞═══════╡
# │ true  │
# │ false │
# │ null  │
# └───────┘

df.filter(tp.col("x"))
# shape: (1, 1)
# ┌──────┐
# │ x    │
# │ bool │
# ╞══════╡
# │ true │
# └──────┘
```

## Grouped filters

The `by` parameter enables grouped filtering. In the example below, we keep
rows where the horsepower (`hp`) is above the **median** horsepower within each
cylinder group.

```python
(
    mtcars
    .filter(tp.col("hp") > tp.col("hp").median(), by="cyl")
)
```

This performs the following steps:

1. Calculates the median `hp` for each `cyl` group.
2. For each row, based on its `cyl` group, tests whether `hp` is greater than that median.
3. Keeps only the rows where the test passes.

## Filter with helper functions

tidypolars-extra includes helper functions for common operations inside
filters.

### Keeping the two lowest horsepower rows per cylinder

Sort the data by ascending horsepower, add a row number within each group,
and keep only the first two entries per group.

```python
(
    mtcars
    .select("name", "cyl", "hp")
    .arrange("hp")
    .mutate(row_num=tp.row_number(), by="cyl")
    .filter(tp.col("row_num") <= 2)
    .drop("row_num")
)
```

Since there are 3 `cyl` groups (4, 6, or 8 cylinders), this returns 6 rows.

### Comparing shifts in hp across rows

Sort the data by ascending horsepower, then filter to keep rows where it
increases by more than 50 from the previous row.

```python
(
    mtcars
    .select("name", "cyl", "hp")
    .arrange("hp")
    .filter(tp.col("hp") - tp.lag(tp.col("hp")) > 50)
)
```
