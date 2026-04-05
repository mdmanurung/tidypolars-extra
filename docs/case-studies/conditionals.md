# Conditional & Grouping Functions

tidypolars4sci provides several conditional and grouping helper functions
inspired by dplyr: `case_match`, `na_if`, `consecutive_id`, `if_all`, and `if_any`.

## Setup

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci as tp
from tidypolars4sci.data import mtcars as df
import polars as pl
```

## Case Match

`case_match()` maps values to new labels, similar to a switch statement.
Arguments are provided as value-result pairs.

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
df.select('name', 'cyl', 'mpg').slice_head(n=8).mutate(
    engine_size=tp.case_match('cyl', 4, 'Small', 6, 'Medium', 8, 'Large')
).print()
```

``` python
shape: (8, 4)
┌───────────────────┬─────┬───────┬─────────────┐
│ name              ┆ cyl ┆ mpg   ┆ engine_size │
│ ---               ┆ --- ┆ ---   ┆ ---         │
│ str               ┆ i64 ┆ f64   ┆ str         │
╞═══════════════════╪═════╪═══════╪═════════════╡
│ Mazda RX4         ┆ 6   ┆ 21.00 ┆ Medium      │
│ Mazda RX4 Wag     ┆ 6   ┆ 21.00 ┆ Medium      │
│ Datsun 710        ┆ 4   ┆ 22.80 ┆ Small       │
│ Hornet 4 Drive    ┆ 6   ┆ 21.40 ┆ Medium      │
│ Hornet Sportabout ┆ 8   ┆ 18.70 ┆ Large       │
│ Valiant           ┆ 6   ┆ 18.10 ┆ Medium      │
│ Duster 360        ┆ 8   ┆ 14.30 ┆ Large       │
│ Merc 240D         ┆ 4   ┆ 24.40 ┆ Small       │
└───────────────────┴─────┴───────┴─────────────┘
```

## Na If

`na_if()` replaces a specific value with `null`. Useful for treating sentinel
values (like 0 or -999) as missing data.

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
data = tp.tibble(x=[1, 0, 3, 0, 5], y=["a", "b", "", "d", ""])
data.print()
```

``` python
shape: (5, 2)
┌─────┬─────┐
│ x   ┆ y   │
│ --- ┆ --- │
│ i64 ┆ str │
╞═════╪═════╡
│ 1   ┆ a   │
│ 0   ┆ b   │
│ 3   ┆     │
│ 0   ┆ d   │
│ 5   ┆     │
└─────┴─────┘
```

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Replace 0 values in column x with null
data.mutate(x=tp.na_if('x', 0)).print()
```

``` python
shape: (5, 2)
┌──────┬─────┐
│ x    ┆ y   │
│ ---  ┆ --- │
│ i64  ┆ str │
╞══════╪═════╡
│ 1    ┆ a   │
│ null ┆ b   │
│ 3    ┆     │
│ null ┆ d   │
│ 5    ┆     │
└──────┴─────┘
```

## Consecutive ID

`consecutive_id()` generates a group identifier that increments each time a
value changes. This is useful for detecting runs or streaks in data.

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
events = tp.tibble(
    time=[1, 2, 3, 4, 5, 6, 7, 8],
    status=["on", "on", "off", "off", "off", "on", "on", "off"]
)

events.mutate(run_id=tp.consecutive_id('status')).print()
```

``` python
shape: (8, 3)
┌──────┬────────┬────────┐
│ time ┆ status ┆ run_id │
│ ---  ┆ ---    ┆ ---    │
│ i64  ┆ str    ┆ i64    │
╞══════╪════════╪════════╡
│ 1    ┆ on     ┆ 1      │
│ 2    ┆ on     ┆ 1      │
│ 3    ┆ off    ┆ 2      │
│ 4    ┆ off    ┆ 2      │
│ 5    ┆ off    ┆ 2      │
│ 6    ┆ on     ┆ 3      │
│ 7    ┆ on     ┆ 3      │
│ 8    ┆ off    ┆ 4      │
└──────┴────────┴────────┘
```

## If All

`if_all()` checks whether a condition holds for all specified columns. Returns
a combined boolean expression suitable for `filter()`.

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Keep rows where both mpg and disp are greater than 20
df.select('name', 'mpg', 'disp').slice_head(n=8).filter(
    tp.if_all(['mpg', 'disp'], lambda x: x > 20)
).print()
```

``` python
shape: (5, 3)
┌────────────────┬───────┬────────┐
│ name           ┆ mpg   ┆ disp   │
│ ---            ┆ ---   ┆ ---    │
│ str            ┆ f64   ┆ f64    │
╞════════════════╪═══════╪════════╡
│ Mazda RX4      ┆ 21.00 ┆ 160.00 │
│ Mazda RX4 Wag  ┆ 21.00 ┆ 160.00 │
│ Datsun 710     ┆ 22.80 ┆ 108.00 │
│ Hornet 4 Drive ┆ 21.40 ┆ 258.00 │
│ Merc 240D      ┆ 24.40 ┆ 146.70 │
└────────────────┴───────┴────────┘
```

## If Any

`if_any()` checks whether a condition holds for at least one of the specified
columns.

``` {.python exports="both" results="output code" tangle="src-conditionals.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
small = tp.tibble(a=[1, 5, 3], b=[10, 2, 8], c=["x", "y", "z"])

# Keep rows where at least one of a or b is greater than 7
small.filter(tp.if_any(['a', 'b'], lambda x: x > 7)).print()
```

``` python
shape: (2, 3)
┌─────┬─────┬─────┐
│ a   ┆ b   ┆ c   │
│ --- ┆ --- ┆ --- │
│ i64 ┆ i64 ┆ str │
╞═════╪═════╪═════╡
│ 1   ┆ 10  ┆ x   │
│ 3   ┆ 8   ┆ z   │
└─────┴─────┴─────┘
```
