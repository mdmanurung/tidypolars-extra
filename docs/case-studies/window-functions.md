# Ranking & Window Functions

tidypolars4sci provides a comprehensive set of ranking and window functions
analogous to dplyr: `dense_rank`, `min_rank`, `percent_rank`, `cume_dist`,
`ntile`, `nth`, and `cummean`.

## Setup

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
import tidypolars4sci_ext as tp
from tidypolars4sci.data import mtcars as df
import polars as pl

# Use a small subset for clarity
cars = df.select('name', 'mpg', 'cyl').slice_head(n=8)
```

## Dense Rank

`dense_rank()` assigns ranks without gaps. Tied values get the same rank,
and the next rank is always one higher.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
cars.mutate(mpg_rank=tp.dense_rank('mpg')).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬──────────┐
│ name              ┆ mpg   ┆ cyl ┆ mpg_rank │
│ ---               ┆ ---   ┆ --- ┆ ---      │
│ str               ┆ f64   ┆ i64 ┆ u32      │
╞═══════════════════╪═══════╪═════╪══════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 4        │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 4        │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 6        │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 5        │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 3        │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 2        │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 1        │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 7        │
└───────────────────┴───────┴─────┴──────────┘
```

## Min Rank

`min_rank()` assigns ranks with gaps at ties. Note how after the tied rank 4,
the next rank jumps to 6 (not 5).

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
cars.mutate(mpg_rank=tp.min_rank('mpg')).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬──────────┐
│ name              ┆ mpg   ┆ cyl ┆ mpg_rank │
│ ---               ┆ ---   ┆ --- ┆ ---      │
│ str               ┆ f64   ┆ i64 ┆ u32      │
╞═══════════════════╪═══════╪═════╪══════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 4        │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 4        │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 7        │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 6        │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 3        │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 2        │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 1        │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 8        │
└───────────────────┴───────┴─────┴──────────┘
```

## Percent Rank

`percent_rank()` scales ranks to a 0–1 range.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
cars.mutate(mpg_pct=tp.percent_rank('mpg')).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬─────────┐
│ name              ┆ mpg   ┆ cyl ┆ mpg_pct │
│ ---               ┆ ---   ┆ --- ┆ ---     │
│ str               ┆ f64   ┆ i64 ┆ f64     │
╞═══════════════════╪═══════╪═════╪═════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 0.43    │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 0.43    │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 0.86    │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 0.71    │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 0.29    │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 0.14    │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 0.00    │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 1.00    │
└───────────────────┴───────┴─────┴─────────┘
```

## Cumulative Distribution

`cume_dist()` computes the proportion of values less than or equal to each value.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
cars.mutate(mpg_cdf=tp.cume_dist('mpg')).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬─────────┐
│ name              ┆ mpg   ┆ cyl ┆ mpg_cdf │
│ ---               ┆ ---   ┆ --- ┆ ---     │
│ str               ┆ f64   ┆ i64 ┆ f64     │
╞═══════════════════╪═══════╪═════╪═════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 0.62    │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 0.62    │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 0.88    │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 0.75    │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 0.38    │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 0.25    │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 0.12    │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 1.00    │
└───────────────────┴───────┴─────┴─────────┘
```

## Ntile

`ntile()` divides rows into approximately equal-sized buckets.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Divide into 4 quartile buckets by mpg
cars.mutate(quartile=tp.ntile('mpg', 4)).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬──────────┐
│ name              ┆ mpg   ┆ cyl ┆ quartile │
│ ---               ┆ ---   ┆ --- ┆ ---      │
│ str               ┆ f64   ┆ i64 ┆ i64      │
╞═══════════════════╪═══════╪═════╪══════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 2        │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 3        │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 4        │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 3        │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 2        │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 1        │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 1        │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 4        │
└───────────────────┴───────┴─────┴──────────┘
```

## Nth

`nth()` extracts the nth value from a column, useful in `summarize` contexts.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
# Get the 2nd mpg value within each cylinder group
df.summarize(second_mpg=tp.nth('mpg', 1), by='cyl').print()
```

``` python
shape: (3, 2)
┌─────┬────────────┐
│ cyl ┆ second_mpg │
│ --- ┆ ---        │
│ i64 ┆ list[f64]  │
╞═════╪════════════╡
│ 4   ┆ [24.40]    │
│ 8   ┆ [14.30]    │
│ 6   ┆ [21.00]    │
└─────┴────────────┘
```

## Cumulative Mean

`cummean()` computes a running average.

``` {.python exports="both" results="output code" tangle="src-window.py" cache="yes" hlines="yes" colnames="yes" noweb="no" session="*Python-Org*"}
cars.mutate(running_avg_mpg=tp.cummean('mpg')).print()
```

``` python
shape: (8, 4)
┌───────────────────┬───────┬─────┬─────────────────┐
│ name              ┆ mpg   ┆ cyl ┆ running_avg_mpg │
│ ---               ┆ ---   ┆ --- ┆ ---             │
│ str               ┆ f64   ┆ i64 ┆ f64             │
╞═══════════════════╪═══════╪═════╪═════════════════╡
│ Mazda RX4         ┆ 21.00 ┆ 6   ┆ 21.00           │
│ Mazda RX4 Wag     ┆ 21.00 ┆ 6   ┆ 21.00           │
│ Datsun 710        ┆ 22.80 ┆ 4   ┆ 21.60           │
│ Hornet 4 Drive    ┆ 21.40 ┆ 6   ┆ 21.55           │
│ Hornet Sportabout ┆ 18.70 ┆ 8   ┆ 20.98           │
│ Valiant           ┆ 18.10 ┆ 6   ┆ 20.50           │
│ Duster 360        ┆ 14.30 ┆ 8   ┆ 19.61           │
│ Merc 240D         ┆ 24.40 ┆ 4   ┆ 20.21           │
└───────────────────┴───────┴─────┴─────────────────┘
```
