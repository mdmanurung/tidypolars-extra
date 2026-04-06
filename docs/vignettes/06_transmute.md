# Transmute

A "transmute" operation is the combination of a `.mutate()` followed by a
`.select()` — it creates new columns and keeps **only** those columns (along
with any explicitly selected ones).

tidypolars-extra does not have a dedicated `transmute` method. Instead, you
chain `.mutate()` and `.select()` to achieve the same result.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))
```

## Basic transmute

Keep `cyl` and `mpg`, and create a new `hp_per_cyl` column:

```python
(
    mtcars
    .mutate(hp_per_cyl=tp.col("hp") / tp.col("cyl"))
    .select("cyl", "mpg", "hp_per_cyl")
)
```

```
shape: (32, 3)
┌─────┬──────┬────────────┐
│ cyl ┆ mpg  ┆ hp_per_cyl │
╞═════╪══════╪════════════╡
│ 6   ┆ 21.0 ┆ 18.333333  │
│ 6   ┆ 21.0 ┆ 18.333333  │
│ 4   ┆ 22.8 ┆ 23.25      │
│ …   ┆ …    ┆ …          │
└─────┴──────┴────────────┘
```

## Multiple new columns

```python
(
    mtcars
    .mutate(
        hp_per_cyl=tp.col("hp") / tp.col("cyl"),
        weight_tons=tp.col("wt") / 2.205,
    )
    .select("name", "hp_per_cyl", "weight_tons")
)
```

```
shape: (32, 3)
┌───────────────────┬────────────┬──────────────┐
│ name              ┆ hp_per_cyl ┆ weight_tons  │
╞═══════════════════╪════════════╪══════════════╡
│ Mazda RX4         ┆ 18.333333  ┆ 1.188209     │
│ Mazda RX4 Wag     ┆ 18.333333  ┆ 1.303855     │
│ Datsun 710        ┆ 23.25      ┆ 1.053288     │
│ …                 ┆ …          ┆ …            │
└───────────────────┴────────────┴──────────────┘
```
