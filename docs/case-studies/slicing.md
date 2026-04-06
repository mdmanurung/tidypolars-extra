# Advanced Row Selection

Beyond `slice_head` and `slice_tail`, tidypolars4sci provides `slice_min`,
`slice_max`, and `slice_sample` for selecting rows based on values or at random.

## Setup

``` {.python exports="both" results="output code" tangle="src-slicing.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci_ext as tp
from tidypolars4sci.data import mtcars as df
import polars as pl
```

## Slice Min

`slice_min()` selects the rows with the smallest values of a column. By default,
ties are included (`with_ties=True`).

``` {.python exports="both" results="output code" tangle="src-slicing.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# 3 lightest cars by weight
df.slice_min('wt', n=3).select('name', 'wt', 'mpg', 'cyl').print()
```

``` python
shape: (3, 4)
┌────────────────┬──────┬───────┬─────┐
│ name           ┆ wt   ┆ mpg   ┆ cyl │
│ ---            ┆ ---  ┆ ---   ┆ --- │
│ str            ┆ f64  ┆ f64   ┆ i64 │
╞════════════════╪══════╪═══════╪═════╡
│ Honda Civic    ┆ 1.61 ┆ 30.40 ┆ 4   │
│ Toyota Corolla ┆ 1.83 ┆ 33.90 ┆ 4   │
│ Lotus Europa   ┆ 1.51 ┆ 30.40 ┆ 4   │
└────────────────┴──────┴───────┴─────┘
```

## Slice Max

`slice_max()` selects rows with the largest values. Notice that with `n=3` and
`with_ties=True`, we get 4 rows because Duster 360 and Camaro Z28 are tied at
245 hp.

``` {.python exports="both" results="output code" tangle="src-slicing.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# 3 most powerful cars (ties included by default)
df.slice_max('hp', n=3).select('name', 'hp', 'mpg', 'cyl').print()
```

``` python
shape: (4, 4)
┌────────────────┬─────┬───────┬─────┐
│ name           ┆ hp  ┆ mpg   ┆ cyl │
│ ---            ┆ --- ┆ ---   ┆ --- │
│ str            ┆ i64 ┆ f64   ┆ i64 │
╞════════════════╪═════╪═══════╪═════╡
│ Duster 360     ┆ 245 ┆ 14.30 ┆ 8   │
│ Camaro Z28     ┆ 245 ┆ 13.30 ┆ 8   │
│ Ford Pantera L ┆ 264 ┆ 15.80 ┆ 8   │
│ Maserati Bora  ┆ 335 ┆ 15.00 ┆ 8   │
└────────────────┴─────┴───────┴─────┘
```

## Slice Min by Group

Use the `by` parameter to select top/bottom rows within each group.

``` {.python exports="both" results="output code" tangle="src-slicing.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Lightest car in each cylinder group
df.slice_min('wt', n=1, by='cyl').select('name', 'cyl', 'wt', 'mpg').print()
```

``` python
shape: (3, 4)
┌────────────────┬─────┬──────┬───────┐
│ name           ┆ cyl ┆ wt   ┆ mpg   │
│ ---            ┆ --- ┆ ---  ┆ ---   │
│ str            ┆ i64 ┆ f64  ┆ f64   │
╞════════════════╪═════╪══════╪═══════╡
│ Lotus Europa   ┆ 4   ┆ 1.51 ┆ 30.40 │
│ Mazda RX4      ┆ 6   ┆ 2.62 ┆ 21.00 │
│ Ford Pantera L ┆ 8   ┆ 3.17 ┆ 15.80 │
└────────────────┴─────┴──────┴───────┘
```

## Slice Sample

`slice_sample()` randomly selects rows. Use `n` for a fixed number of rows
or `prop` for a fraction.

``` {.python exports="both" results="output code" tangle="src-slicing.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Random sample of 5 rows (output will vary)
df.slice_sample(n=5).select('name', 'mpg', 'cyl').print()
```

``` python
shape: (5, 3)
┌───────────────────┬───────┬─────┐
│ name              ┆ mpg   ┆ cyl │
│ ---               ┆ ---   ┆ --- │
│ str               ┆ f64   ┆ i64 │
╞═══════════════════╪═══════╪═════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   │
│ Datsun 710        ┆ 22.80 ┆ 4   │
│ Hornet Sportabout ┆ 18.70 ┆ 8   │
│ Merc 280          ┆ 19.20 ┆ 6   │
│ Lotus Europa      ┆ 30.40 ┆ 4   │
└───────────────────┴───────┴─────┘
```

Note: Since `slice_sample` is random, your output will differ from above.
