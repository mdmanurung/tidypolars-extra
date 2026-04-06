# Join Operations

tidypolars4sci provides a full set of join operations matching dplyr's API:
`right_join`, `semi_join`, `anti_join`, and `cross_join`, in addition to the
existing `inner_join`, `left_join`, and `full_join`.

## Setup

``` {.python exports="both" results="output code" tangle="src-joins.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci_ext as tp
from tidypolars4sci.data import mtcars as df
import polars as pl
```

## Right Join

`right_join()` keeps all rows from the right table. Where there is no match
in the left table, columns are filled with `null`.

``` {.python exports="both" results="output code" tangle="src-joins.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Select a few 4-cylinder cars
small = df.filter(pl.col('cyl') == 4).select('name', 'cyl', 'mpg').slice_head(n=3)

# A lookup table including cylinder counts not in our subset
lookup = tp.tibble(cyl=[4, 6, 10], engine_type=["Inline", "V-type", "Experimental"])

small.right_join(lookup, on='cyl').print()
```

``` python
shape: (5, 4)
┌────────────┬───────┬─────┬──────────────┐
│ name       ┆ mpg   ┆ cyl ┆ engine_type  │
│ ---        ┆ ---   ┆ --- ┆ ---          │
│ str        ┆ f64   ┆ i64 ┆ str          │
╞════════════╪═══════╪═════╪══════════════╡
│ Datsun 710 ┆ 22.80 ┆ 4   ┆ Inline       │
│ Merc 240D  ┆ 24.40 ┆ 4   ┆ Inline       │
│ Merc 230   ┆ 22.80 ┆ 4   ┆ Inline       │
│ null       ┆ null  ┆ 6   ┆ V-type       │
│ null       ┆ null  ┆ 10  ┆ Experimental │
└────────────┴───────┴─────┴──────────────┘
```

Note that `cyl=6` and `cyl=10` appear with null values for `name` and `mpg`
because those cylinder counts have no matches in `small`.

## Semi Join

`semi_join()` filters the left table to only rows that have a match in the right
table. It does not add any columns from the right table.

``` {.python exports="both" results="output code" tangle="src-joins.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Find cars with hp > 200
high_hp = df.filter(pl.col('hp') > 200).select('name', 'cyl', 'hp')

# Use semi_join to keep only those cars from the full dataset
df.select('name', 'cyl', 'mpg', 'hp').semi_join(high_hp, on='name').print()
```

``` python
shape: (7, 4)
┌─────────────────────┬─────┬───────┬─────┐
│ name                ┆ cyl ┆ mpg   ┆ hp  │
│ ---                 ┆ --- ┆ ---   ┆ --- │
│ str                 ┆ i64 ┆ f64   ┆ i64 │
╞═════════════════════╪═════╪═══════╪═════╡
│ Duster 360          ┆ 8   ┆ 14.30 ┆ 245 │
│ Cadillac Fleetwood  ┆ 8   ┆ 10.40 ┆ 205 │
│ Lincoln Continental ┆ 8   ┆ 10.40 ┆ 215 │
│ Chrysler Imperial   ┆ 8   ┆ 14.70 ┆ 230 │
│ Camaro Z28          ┆ 8   ┆ 13.30 ┆ 245 │
│ Ford Pantera L      ┆ 8   ┆ 15.80 ┆ 264 │
│ Maserati Bora       ┆ 8   ┆ 15.00 ┆ 335 │
└─────────────────────┴─────┴───────┴─────┘
```

## Anti Join

`anti_join()` is the opposite of `semi_join`: it returns rows from the left
table that do *not* have a match in the right table.

``` {.python exports="both" results="output code" tangle="src-joins.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Cars to exclude
exclude = tp.tibble(name=["Mazda RX4", "Datsun 710", "Hornet 4 Drive"])

# All cars except the excluded ones
df.select('name', 'mpg', 'cyl').anti_join(exclude, on='name').slice_head(n=6).print()
```

``` python
shape: (6, 3)
┌───────────────────┬───────┬─────┐
│ name              ┆ mpg   ┆ cyl │
│ ---               ┆ ---   ┆ --- │
│ str               ┆ f64   ┆ i64 │
╞═══════════════════╪═══════╪═════╡
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   │
│ Hornet Sportabout ┆ 18.70 ┆ 8   │
│ Valiant           ┆ 18.10 ┆ 6   │
│ Duster 360        ┆ 14.30 ┆ 8   │
│ Merc 240D         ┆ 24.40 ┆ 4   │
│ Merc 230          ┆ 22.80 ┆ 4   │
└───────────────────┴───────┴─────┘
```

## Cross Join

`cross_join()` creates a Cartesian product of two tables — every combination
of rows from both tables.

``` {.python exports="both" results="output code" tangle="src-joins.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
colors = tp.tibble(color=["red", "blue"])
sizes = tp.tibble(size=["S", "M", "L"])

colors.cross_join(sizes).print()
```

``` python
shape: (6, 2)
┌───────┬──────┐
│ color ┆ size │
│ ---   ┆ ---  │
│ str   ┆ str  │
╞═══════╪══════╡
│ red   ┆ S    │
│ red   ┆ M    │
│ red   ┆ L    │
│ blue  ┆ S    │
│ blue  ┆ M    │
│ blue  ┆ L    │
└───────┴──────┘
```
