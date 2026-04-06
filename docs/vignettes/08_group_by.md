# Group By

Grouping is a fundamental concept when you need to perform operations
**separately** for different subsets of your data. In tidypolars-extra,
grouping is done via the `by` parameter available on `filter`, `mutate`,
and `summarize`.

For example, in the `mtcars` dataset there are 3 possible values for
cylinders (`cyl`). You can group by `cyl` to perform operations separately
for each of these 3 groups of rows.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))

small_cars = mtcars.select("name", "cyl", "gear", "hp")

small_cars
```

## Grouping with `by`

The `by` parameter is supported directly on `filter`, `mutate`, and
`summarize`. This is often more concise than a separate `group_by` step.

### Grouped filter

Keep rows where `hp` is greater than the mean `hp` **within each `cyl` group**:

```python
small_cars.filter(tp.col("hp") > tp.col("hp").mean(), by="cyl")
```

```
shape: (15, 4)
┌───────────────────┬─────┬──────┬─────┐
│ name              ┆ cyl ┆ gear ┆ hp  │
╞═══════════════════╪═════╪══════╪═════╡
│ Datsun 710        ┆ 4   ┆ 4    ┆ 93  │
│ Merc 230          ┆ 4   ┆ 4    ┆ 95  │
│ …                 ┆ …   ┆ …   ┆ …   │
└───────────────────┴─────┴──────┴─────┘
```

### Grouped mutate

Compute the average `hp` within each `cyl` group and attach it to every row:

```python
small_cars.mutate(avg_hp=tp.col("hp").mean(), by="cyl")
```

```
shape: (32, 5)
┌────────────────┬─────┬──────┬─────┬────────────┐
│ name           ┆ cyl ┆ gear ┆ hp  ┆ avg_hp     │
╞════════════════╪═════╪══════╪═════╪════════════╡
│ Mazda RX4      ┆ 6   ┆ 4    ┆ 110 ┆ 122.285714 │
│ Mazda RX4 Wag  ┆ 6   ┆ 4    ┆ 110 ┆ 122.285714 │
│ …              ┆ …   ┆ …   ┆ …   ┆ …          │
└────────────────┴─────┴──────┴─────┴────────────┘
```

### Grouped summarize

Compute summary statistics per group:

```python
small_cars.summarize(avg_hp=tp.col("hp").mean(), by="cyl")
```

```
shape: (3, 2)
┌─────┬────────────┐
│ cyl ┆ avg_hp     │
╞═════╪════════════╡
│ 8   ┆ 209.214286 │
│ 6   ┆ 122.285714 │
│ 4   ┆ 82.636364  │
└─────┴────────────┘
```

## Grouping by multiple columns

Pass a list of column names to `by` to group by multiple columns:

```python
small_cars.summarize(avg_hp=tp.col("hp").mean(), by=["cyl", "gear"])
```

```
shape: (8, 3)
┌─────┬──────┬────────────┐
│ cyl ┆ gear ┆ avg_hp     │
╞═════╪══════╪════════════╡
│ 4   ┆ 4    ┆ 76.0       │
│ 6   ┆ 4    ┆ 116.5      │
│ 8   ┆ 3    ┆ 194.166667 │
│ …   ┆ …   ┆ …          │
└─────┴──────┴────────────┘
```

## Using `group_by` explicitly

You can also use the `.group_by()` method, which returns a `TibbleGroupBy`
object. This object supports `filter`, `mutate`, and `summarize`:

```python
g_cyl = mtcars.group_by("cyl")

# Summarize per group
g_cyl.summarize(avg_hp=tp.col("hp").mean())
```

```{note}
The `by` parameter on `filter`, `mutate`, and `summarize` is typically
preferred for its conciseness and clarity. Both approaches produce the
same result.
```

## Practical example: top N per group

A common pattern is to find the "top N" rows within each group. For example,
the 2 cars with the lowest `hp` in each `cyl` group:

```python
(
    small_cars
    .arrange("hp")
    .mutate(row_num=tp.row_number(), by="cyl")
    .filter(tp.col("row_num") <= 2)
    .drop("row_num")
)
```

```
shape: (6, 4)
┌────────────────┬─────┬──────┬─────┐
│ name           ┆ cyl ┆ gear ┆ hp  │
╞════════════════╪═════╪══════╪═════╡
│ Honda Civic    ┆ 4   ┆ 4    ┆ 52  │
│ Merc 240D      ┆ 4   ┆ 4    ┆ 62  │
│ Valiant        ┆ 6   ┆ 3    ┆ 105 │
│ Mazda RX4      ┆ 6   ┆ 4    ┆ 110 │
│ Dodge Challenger┆ 8   ┆ 3    ┆ 150 │
│ AMC Javelin    ┆ 8   ┆ 3    ┆ 150 │
└────────────────┴─────┴──────┴─────┘
```
