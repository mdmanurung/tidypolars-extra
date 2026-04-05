# Additional dplyr Verbs

tidypolars4sci provides several additional dplyr-style verbs: `transmute`,
`rename_with`, `add_count`, `tally`, `drop_na`, `replace_na`, and GroupBy
utility methods.

## Setup

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci as tp
from tidypolars4sci.data import mtcars as df
import polars as pl
```

## Transmute

`transmute()` creates new columns and drops all others (unlike `mutate()` which
keeps everything).

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
df.select('name', 'mpg', 'wt').slice_head(n=6).transmute(
    name=pl.col('name'),
    km_per_liter=pl.col('mpg') * 0.425144
).print()
```

``` python
shape: (6, 2)
┌───────────────────┬──────────────┐
│ name              ┆ km_per_liter │
│ ---               ┆ ---          │
│ str               ┆ f64          │
╞═══════════════════╪══════════════╡
│ Mazda RX4         ┆ 8.93         │
│ Mazda RX4 Wag     ┆ 8.93         │
│ Datsun 710        ┆ 9.69         │
│ Hornet 4 Drive    ┆ 9.10         │
│ Hornet Sportabout ┆ 7.95         │
│ Valiant           ┆ 7.70         │
└───────────────────┴──────────────┘
```

## Rename With

`rename_with()` applies a function to rename columns.

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Rename all columns to uppercase
df.select('name', 'mpg', 'cyl', 'hp').slice_head(n=4).rename_with(str.upper).print()
```

``` python
shape: (4, 4)
┌────────────────┬───────┬─────┬─────┐
│ NAME           ┆ MPG   ┆ CYL ┆ HP  │
│ ---            ┆ ---   ┆ --- ┆ --- │
│ str            ┆ f64   ┆ i64 ┆ i64 │
╞════════════════╪═══════╪═════╪═════╡
│ Mazda RX4      ┆ 21.00 ┆ 6   ┆ 110 │
│ Mazda RX4 Wag  ┆ 21.00 ┆ 6   ┆ 110 │
│ Datsun 710     ┆ 22.80 ┆ 4   ┆ 93  │
│ Hornet 4 Drive ┆ 21.40 ┆ 6   ┆ 110 │
└────────────────┴───────┴─────┴─────┘
```

## Add Count

`add_count()` adds a count column for each group without collapsing rows
(unlike `count()` or `tally()`).

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
df.select('name', 'cyl', 'mpg').slice_head(n=8).add_count('cyl').print()
```

``` python
shape: (8, 4)
┌───────────────────┬─────┬───────┬─────┐
│ name              ┆ cyl ┆ mpg   ┆ n   │
│ ---               ┆ --- ┆ ---   ┆ --- │
│ str               ┆ i64 ┆ f64   ┆ u32 │
╞═══════════════════╪═════╪═══════╪═════╡
│ Hornet Sportabout ┆ 8   ┆ 18.70 ┆ 2   │
│ Duster 360        ┆ 8   ┆ 14.30 ┆ 2   │
│ Mazda RX4         ┆ 6   ┆ 21.00 ┆ 4   │
│ Mazda RX4 Wag     ┆ 6   ┆ 21.00 ┆ 4   │
│ Hornet 4 Drive    ┆ 6   ┆ 21.40 ┆ 4   │
│ Valiant           ┆ 6   ┆ 18.10 ┆ 4   │
│ Datsun 710        ┆ 4   ┆ 22.80 ┆ 2   │
│ Merc 240D         ┆ 4   ┆ 24.40 ┆ 2   │
└───────────────────┴─────┴───────┴─────┘
```

## Tally

`tally()` provides a simple count of all rows. Use it on a tibble for total
count or after `group_by` for group counts.

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
df.tally().print()
```

``` python
shape: (1, 1)
┌─────┐
│ n   │
│ --- │
│ u32 │
╞═════╡
│ 32  │
└─────┘
```

## Drop NA / Replace NA

`drop_na()` and `replace_na()` are tidyr-style aliases for `drop_null()` and
`replace_null()`.

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
data = tp.tibble(x=[1, None, 3, None], y=["a", "b", None, None])
data.print()
```

``` python
shape: (4, 2)
┌──────┬──────┐
│ x    ┆ y    │
│ ---  ┆ ---  │
│ i64  ┆ str  │
╞══════╪══════╡
│ 1    ┆ a    │
│ null ┆ b    │
│ 3    ┆ null │
│ null ┆ null │
└──────┴──────┘
```

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Drop rows with any null
data.drop_na().print()
```

``` python
shape: (1, 2)
┌─────┬─────┐
│ x   ┆ y   │
│ --- ┆ --- │
│ i64 ┆ str │
╞═════╪═════╡
│ 1   ┆ a   │
└─────┴─────┘
```

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Replace nulls with specific values per column
data.replace_na({'x': 0, 'y': 'missing'}).print()
```

``` python
shape: (4, 2)
┌─────┬─────────┐
│ x   ┆ y       │
│ --- ┆ ---     │
│ i64 ┆ str     │
╞═════╪═════════╡
│ 1   ┆ a       │
│ 0   ┆ b       │
│ 3   ┆ missing │
│ 0   ┆ missing │
└─────┴─────────┘
```

## GroupBy Utility Methods

The grouped tibble provides `n_groups()`, `group_keys()`, `group_split()`,
and `ungroup()`.

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
g = df.group_by('cyl')

# Number of groups
print("Number of groups:", g.n_groups())
```

``` python
Number of groups: 3
```

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# View unique group keys
g.group_keys().print()
```

``` python
shape: (3, 1)
┌─────┐
│ cyl │
│ --- │
│ i64 │
╞═════╡
│ 4   │
│ 6   │
│ 8   │
└─────┘
```

``` {.python exports="both" results="output code" tangle="src-verbs.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Ungroup to get back a plain tibble
g.ungroup().select('name', 'cyl').slice_head(n=4).print()
```

``` python
shape: (4, 2)
┌────────────────┬─────┐
│ name           ┆ cyl │
│ ---            ┆ --- │
│ str            ┆ i64 │
╞════════════════╪═════╡
│ Mazda RX4      ┆ 6   │
│ Mazda RX4 Wag  ┆ 6   │
│ Datsun 710     ┆ 4   │
│ Hornet 4 Drive ┆ 6   │
└────────────────┴─────┘
```
