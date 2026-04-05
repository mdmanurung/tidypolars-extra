# Reshaping & Tidying

tidypolars4sci provides several tidyr-inspired functions for reshaping data:
`complete`, `expand`, `expand_grid`, `nesting`, `separate_rows`, and `uncount`.

## Setup

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci as tp
from tidypolars4sci.data import mtcars as df
import polars as pl
```

## Complete

`complete()` fills in missing combinations of columns. This is useful when
your data has implicit missing values that should be made explicit.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Sales data with a missing quarter for product B
sales = tp.tibble(
    product=["A", "A", "B"],
    quarter=[1, 2, 1],
    revenue=[100, 150, 200]
)
sales.print()
```

``` python
shape: (3, 3)
┌─────────┬─────────┬─────────┐
│ product ┆ quarter ┆ revenue │
│ ---     ┆ ---     ┆ ---     │
│ str     ┆ i64     ┆ i64     │
╞═════════╪═════════╪═════════╡
│ A       ┆ 1       ┆ 100     │
│ A       ┆ 2       ┆ 150     │
│ B       ┆ 1       ┆ 200     │
└─────────┴─────────┴─────────┘
```

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Complete all product-quarter combinations (missing revenue becomes null)
sales.complete('product', 'quarter').print()
```

``` python
shape: (4, 3)
┌─────────┬─────────┬─────────┐
│ product ┆ quarter ┆ revenue │
│ ---     ┆ ---     ┆ ---     │
│ str     ┆ i64     ┆ i64     │
╞═════════╪═════════╪═════════╡
│ A       ┆ 2       ┆ 150     │
│ A       ┆ 1       ┆ 100     │
│ B       ┆ 2       ┆ null    │
│ B       ┆ 1       ┆ 200     │
└─────────┴─────────┴─────────┘
```

Use the `fill` parameter to replace nulls with specific values:

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
sales.complete('product', 'quarter', fill={'revenue': 0}).print()
```

``` python
shape: (4, 3)
┌─────────┬─────────┬─────────┐
│ product ┆ quarter ┆ revenue │
│ ---     ┆ ---     ┆ ---     │
│ str     ┆ i64     ┆ i64     │
╞═════════╪═════════╪═════════╡
│ B       ┆ 2       ┆ 0       │
│ B       ┆ 1       ┆ 200     │
│ A       ┆ 2       ┆ 150     │
│ A       ┆ 1       ┆ 100     │
└─────────┴─────────┴─────────┘
```

## Expand

`expand()` generates all unique combinations of the specified columns in a
tibble. Unlike `complete()`, it does not preserve the other columns.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# All possible combinations of cyl and gear in mtcars
df.expand('cyl', 'gear').print()
```

``` python
shape: (9, 2)
┌─────┬──────┐
│ cyl ┆ gear │
│ --- ┆ ---  │
│ i64 ┆ i64  │
╞═════╪══════╡
│ 8   ┆ 5    │
│ 8   ┆ 3    │
│ 8   ┆ 4    │
│ 6   ┆ 5    │
│ 6   ┆ 3    │
│ 6   ┆ 4    │
│ 4   ┆ 5    │
│ 4   ┆ 3    │
│ 4   ┆ 4    │
└─────┴──────┘
```

## Expand Grid

`expand_grid()` is a standalone function that creates a Cartesian product from
named lists of values.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
tp.expand_grid(color=["red", "blue"], size=[1, 2, 3]).print()
```

``` python
shape: (6, 2)
┌───────┬──────┐
│ color ┆ size │
│ ---   ┆ ---  │
│ str   ┆ i64  │
╞═══════╪══════╡
│ red   ┆ 1    │
│ red   ┆ 2    │
│ red   ┆ 3    │
│ blue  ┆ 1    │
│ blue  ┆ 2    │
│ blue  ┆ 3    │
└───────┴──────┘
```

## Nesting

`nesting()` creates a tibble of only the *observed* combinations, useful as an
input to `complete()` when you want to limit the expansion.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
tp.nesting(x=[1, 1, 2], y=["a", "b", "a"]).print()
```

``` python
shape: (3, 2)
┌─────┬─────┐
│ x   ┆ y   │
│ --- ┆ --- │
│ i64 ┆ str │
╞═════╪═════╡
│ 1   ┆ b   │
│ 2   ┆ a   │
│ 1   ┆ a   │
└─────┴─────┘
```

## Separate Rows

`separate_rows()` splits a delimiter-separated string column into multiple
rows, one per element.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
data = tp.tibble(
    name=["Alice", "Bob"],
    hobbies=["reading,cooking", "sports,music,art"]
)
data.print()
```

``` python
shape: (2, 2)
┌───────┬──────────────────┐
│ name  ┆ hobbies          │
│ ---   ┆ ---              │
│ str   ┆ str              │
╞═══════╪══════════════════╡
│ Alice ┆ reading,cooking  │
│ Bob   ┆ sports,music,art │
└───────┴──────────────────┘
```

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
data.separate_rows('hobbies', sep=',').print()
```

``` python
shape: (5, 2)
┌───────┬─────────┐
│ name  ┆ hobbies │
│ ---   ┆ ---     │
│ str   ┆ str     │
╞═══════╪═════════╡
│ Alice ┆ reading │
│ Alice ┆ cooking │
│ Bob   ┆ sports  │
│ Bob   ┆ music   │
│ Bob   ┆ art     │
└───────┴─────────┘
```

## Uncount

`uncount()` is the inverse of counting — it expands rows based on a weight
column. A row with weight 3 becomes 3 identical rows.

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
freq = tp.tibble(
    color=["red", "blue", "green"],
    n=[2, 3, 1]
)
freq.print()
```

``` python
shape: (3, 2)
┌───────┬─────┐
│ color ┆ n   │
│ ---   ┆ --- │
│ str   ┆ i64 │
╞═══════╪═════╡
│ red   ┆ 2   │
│ blue  ┆ 3   │
│ green ┆ 1   │
└───────┴─────┘
```

``` {.python exports="both" results="output code" tangle="src-reshaping.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
freq.uncount('n').print()
```

``` python
shape: (6, 1)
┌───────┐
│ color │
│ ---   │
│ str   │
╞═══════╡
│ red   │
│ red   │
│ blue  │
│ blue  │
│ blue  │
│ green │
└───────┘
```
