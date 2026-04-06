# Mutate

The `.mutate()` method adds new columns or modifies existing columns in your
data. New columns are defined using keyword arguments, where the key becomes
the column name and the value is a Polars expression.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))

small_cars = mtcars.select("name", "cyl", "mpg", "hp")
```

## Assign new columns

Create a new column `cyl2` that doubles the `cyl` value:

```python
small_cars.mutate(cyl2=tp.col("cyl") * 2)
```

```
shape: (32, 5)
┌───────────────────┬─────┬──────┬─────┬──────┐
│ name              ┆ cyl ┆ mpg  ┆ hp  ┆ cyl2 │
╞═══════════════════╪═════╪══════╪═════╪══════╡
│ Mazda RX4         ┆ 6   ┆ 21.0 ┆ 110 ┆ 12   │
│ Mazda RX4 Wag     ┆ 6   ┆ 21.0 ┆ 110 ┆ 12   │
│ Datsun 710        ┆ 4   ┆ 22.8 ┆ 93  ┆ 8    │
│ …                 ┆ …   ┆ …    ┆ …   ┆ …    │
└───────────────────┴─────┴──────┴─────┴──────┘
```

You can also add a column with a scalar value:

```python
small_cars.mutate(label=tp.lit("car"))
```

## Combining expressions

You can define multiple columns in a single `mutate` call:

```python
small_cars.mutate(
    hp_per_cyl=tp.col("hp") / tp.col("cyl"),
    double_mpg=tp.col("mpg") * 2,
)
```

## Used with grouped operations

The `by` parameter lets you compute group-level statistics and attach them
back to each row. For example, computing the mean `hp` per `cyl` group and
then demeaning the values:

```python
(
    small_cars
    .mutate(
        hp_mean=tp.col("hp").mean(),
        demeaned_hp=tp.col("hp") - tp.col("hp").mean(),
        by="cyl",
    )
)
```

```
shape: (32, 6)
┌────────────────┬─────┬──────┬─────┬────────────┬─────────────┐
│ name           ┆ cyl ┆ mpg  ┆ hp  ┆ hp_mean    ┆ demeaned_hp │
╞════════════════╪═════╪══════╪═════╪════════════╪═════════════╡
│ Mazda RX4      ┆ 6   ┆ 21.0 ┆ 110 ┆ 122.285714 ┆ -12.285714  │
│ Mazda RX4 Wag  ┆ 6   ┆ 21.0 ┆ 110 ┆ 122.285714 ┆ -12.285714  │
│ …              ┆ …   ┆ …    ┆ …   ┆ …          ┆ …           │
└────────────────┴─────┴──────┴─────┴────────────┴─────────────┘
```

## With if_else and case_when

### Using `if_else`

`tp.if_else()` works like a ternary operator — it evaluates a condition and
returns one value when true and another when false:

```python
small_cars.mutate(
    hp_category=tp.if_else(tp.col("hp") > 150, tp.lit("high"), tp.lit("low"))
)
```

```
shape: (32, 5)
┌───────────────────┬─────┬──────┬─────┬─────────────┐
│ name              ┆ cyl ┆ mpg  ┆ hp  ┆ hp_category │
╞═══════════════════╪═════╪══════╪═════╪═════════════╡
│ Mazda RX4         ┆ 6   ┆ 21.0 ┆ 110 ┆ low         │
│ Hornet Sportabout ┆ 8   ┆ 18.7 ┆ 175 ┆ high        │
│ …                 ┆ …   ┆ …    ┆ …   ┆ …           │
└───────────────────┴─────┴──────┴─────┴─────────────┘
```

### Using `case_when`

`tp.case_when()` handles multiple conditions. Conditions are specified as
pairs of `(condition, value)`, with an optional `_default` for unmatched rows:

```python
small_cars.mutate(
    size=tp.case_when(
        tp.col("cyl") == 4, "small",
        tp.col("cyl") == 6, "medium",
        _default="large",
    )
)
```

```
shape: (32, 5)
┌───────────────────┬─────┬──────┬─────┬────────┐
│ name              ┆ cyl ┆ mpg  ┆ hp  ┆ size   │
╞═══════════════════╪═════╪══════╪═════╪════════╡
│ Mazda RX4         ┆ 6   ┆ 21.0 ┆ 110 ┆ medium │
│ Datsun 710        ┆ 4   ┆ 22.8 ┆ 93  ┆ small  │
│ Hornet Sportabout ┆ 8   ┆ 18.7 ┆ 175 ┆ large  │
│ …                 ┆ …   ┆ …    ┆ …   ┆ …      │
└───────────────────┴─────┴──────┴─────┴────────┘
```
