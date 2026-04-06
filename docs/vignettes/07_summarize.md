# Summarize

The `.summarize()` method (also available as `.summarise()`) lets you compute
summary statistics — a single value per group (or for the entire dataset if no
groups are specified). The result has as many rows as there are unique groups.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))
```

## Summarize over everything

When used without grouping, `summarize` returns a single row.

```python
mtcars.summarize(avg_mpg=tp.col("mpg").mean())
```

```
shape: (1, 1)
┌───────────┐
│ avg_mpg   │
╞═══════════╡
│ 20.090625 │
└───────────┘
```

## Summarizing per group

Use the `by` parameter to compute summaries within groups. For example, there
are 3 values of cylinders (`cyl`) — 4, 6, and 8 — so the result will have 3
rows:

```python
mtcars.summarize(avg_mpg=tp.col("mpg").mean(), by="cyl")
```

```
shape: (3, 2)
┌─────┬───────────┐
│ cyl ┆ avg_mpg   │
╞═════╪═══════════╡
│ 8   ┆ 15.1      │
│ 6   ┆ 19.742857 │
│ 4   ┆ 26.663636 │
└─────┴───────────┘
```

## Multiple summary statistics

You can compute multiple summary statistics in a single call:

```python
mtcars.summarize(
    avg_mpg=tp.col("mpg").mean(),
    max_hp=tp.col("hp").max(),
    min_wt=tp.col("wt").min(),
    by="cyl",
)
```

```
shape: (3, 4)
┌─────┬───────────┬────────┬────────┐
│ cyl ┆ avg_mpg   ┆ max_hp ┆ min_wt │
╞═════╪═══════════╪════════╪════════╡
│ 8   ┆ 15.1      ┆ 335    ┆ 3.17   │
│ 6   ┆ 19.742857 ┆ 175    ┆ 2.62   │
│ 4   ┆ 26.663636 ┆ 113    ┆ 1.513  │
└─────┴───────────┴────────┴────────┘
```

## Summarize with a literal value

You can also include a literal (scalar) value in the summary:

```python
mtcars.summarize(
    measure=tp.lit("mean miles per gallon"),
    value=tp.col("mpg").mean(),
    by="cyl",
)
```

```
shape: (3, 3)
┌─────┬──────────────────────┬───────────┐
│ cyl ┆ measure              ┆ value     │
╞═════╪══════════════════════╪═══════════╡
│ 8   ┆ mean miles per gallon┆ 15.1      │
│ 6   ┆ mean miles per gallon┆ 19.742857 │
│ 4   ┆ mean miles per gallon┆ 26.663636 │
└─────┴──────────────────────┴───────────┘
```

## Using `count` for quick frequency tables

The `.count()` method is a convenient shortcut for counting rows per group:

```python
mtcars.count("cyl")
```

```
shape: (3, 2)
┌─────┬─────┐
│ cyl ┆ n   │
╞═════╪═════╡
│ 4   ┆ 11  │
│ 8   ┆ 14  │
│ 6   ┆ 7   │
└─────┴─────┘
```
