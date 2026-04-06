# Set Operations

tidypolars4sci provides set operations analogous to dplyr: `union`, `union_all`,
`intersect`, and `setdiff`. These work on tibbles with the same column structure.

## Setup

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci_ext as tp
from tidypolars4sci.data import mtcars as df
import polars as pl

# Create two overlapping subsets of mtcars
first_four = df.select('name', 'mpg', 'cyl').slice_head(n=4)
rows_3_to_6 = df.select('name', 'mpg', 'cyl').slice(list(range(2, 6)))

first_four.print()
```

``` python
shape: (4, 3)
┌────────────────┬───────┬─────┐
│ name           ┆ mpg   ┆ cyl │
│ ---            ┆ ---   ┆ --- │
│ str            ┆ f64   ┆ i64 │
╞════════════════╪═══════╪═════╡
│ Mazda RX4      ┆ 21.00 ┆ 6   │
│ Mazda RX4 Wag  ┆ 21.00 ┆ 6   │
│ Datsun 710     ┆ 22.80 ┆ 4   │
│ Hornet 4 Drive ┆ 21.40 ┆ 6   │
└────────────────┴───────┴─────┘
```

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
rows_3_to_6.print()
```

``` python
shape: (4, 3)
┌───────────────────┬───────┬─────┐
│ name              ┆ mpg   ┆ cyl │
│ ---               ┆ ---   ┆ --- │
│ str               ┆ f64   ┆ i64 │
╞═══════════════════╪═══════╪═════╡
│ Datsun 710        ┆ 22.80 ┆ 4   │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   │
│ Hornet Sportabout ┆ 18.70 ┆ 8   │
│ Valiant           ┆ 18.10 ┆ 6   │
└───────────────────┴───────┴─────┘
```

## Union All

`union_all()` stacks both tables, keeping all rows including duplicates.

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
first_four.union_all(rows_3_to_6).print()
```

``` python
shape: (8, 3)
┌───────────────────┬───────┬─────┐
│ name              ┆ mpg   ┆ cyl │
│ ---               ┆ ---   ┆ --- │
│ str               ┆ f64   ┆ i64 │
╞═══════════════════╪═══════╪═════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   │
│ Datsun 710        ┆ 22.80 ┆ 4   │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   │
│ Datsun 710        ┆ 22.80 ┆ 4   │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   │
│ Hornet Sportabout ┆ 18.70 ┆ 8   │
│ Valiant           ┆ 18.10 ┆ 6   │
└───────────────────┴───────┴─────┘
```

## Union

`union()` combines and deduplicates, like SQL's `UNION`.

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Combine 4-cyl and 6-cyl subsets (no overlap, so same as union_all)
cyl4 = df.filter(pl.col('cyl') == 4).select('name', 'mpg', 'cyl').slice_head(n=4)
cyl6 = df.filter(pl.col('cyl') == 6).select('name', 'mpg', 'cyl').slice_head(n=4)

cyl4.union(cyl6).print()
```

``` python
shape: (8, 3)
┌────────────────┬───────┬─────┐
│ name           ┆ mpg   ┆ cyl │
│ ---            ┆ ---   ┆ --- │
│ str            ┆ f64   ┆ i64 │
╞════════════════╪═══════╪═════╡
│ Datsun 710     ┆ 22.80 ┆ 4   │
│ Mazda RX4 Wag  ┆ 21.00 ┆ 6   │
│ Hornet 4 Drive ┆ 21.40 ┆ 6   │
│ Fiat 128       ┆ 32.40 ┆ 4   │
│ Valiant        ┆ 18.10 ┆ 6   │
│ Merc 240D      ┆ 24.40 ┆ 4   │
│ Merc 230       ┆ 22.80 ┆ 4   │
│ Mazda RX4      ┆ 21.00 ┆ 6   │
└────────────────┴───────┴─────┘
```

## Intersect

`intersect()` returns rows that appear in both tables.

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
first_four.intersect(rows_3_to_6).print()
```

``` python
shape: (2, 3)
┌────────────────┬───────┬─────┐
│ name           ┆ mpg   ┆ cyl │
│ ---            ┆ ---   ┆ --- │
│ str            ┆ f64   ┆ i64 │
╞════════════════╪═══════╪═════╡
│ Datsun 710     ┆ 22.80 ┆ 4   │
│ Hornet 4 Drive ┆ 21.40 ┆ 6   │
└────────────────┴───────┴─────┘
```

## Setdiff

`setdiff()` returns rows in the first table that are not in the second.

``` {.python exports="both" results="output code" tangle="src-set-ops.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
first_four.setdiff(rows_3_to_6).print()
```

``` python
shape: (2, 3)
┌───────────────┬───────┬─────┐
│ name          ┆ mpg   ┆ cyl │
│ ---           ┆ ---   ┆ --- │
│ str           ┆ f64   ┆ i64 │
╞═══════════════╪═══════╪═════╡
│ Mazda RX4     ┆ 21.00 ┆ 6   │
│ Mazda RX4 Wag ┆ 21.00 ┆ 6   │
└───────────────┴───────┴─────┘
```
