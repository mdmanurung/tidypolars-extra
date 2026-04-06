# Rename

The `.rename()` method gives one or more columns new names while keeping all
columns in the data.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))

small_cars = mtcars.select("mpg", "cyl", "hp")
```

## Renaming with keyword arguments

The simplest way to rename columns is to pass `new_name="old_name"` as keyword
arguments:

```python
small_cars.rename(miles_per_gallon="mpg")
```

```
shape: (32, 3)
┌──────────────────┬─────┬─────┐
│ miles_per_gallon  ┆ cyl ┆ hp  │
╞══════════════════╪═════╪═════╡
│ 21.0             ┆ 6   ┆ 110 │
│ 21.0             ┆ 6   ┆ 110 │
│ 22.8             ┆ 4   ┆ 93  │
│ …                ┆ …   ┆ …   │
└──────────────────┴─────┴─────┘
```

## Renaming with a dictionary

You can also pass a dictionary mapping old names to new names:

```python
small_cars.rename({"mpg": "miles_per_gallon", "hp": "horsepower"})
```

```
shape: (32, 3)
┌──────────────────┬─────┬────────────┐
│ miles_per_gallon  ┆ cyl ┆ horsepower │
╞══════════════════╪═════╪════════════╡
│ 21.0             ┆ 6   ┆ 110        │
│ 21.0             ┆ 6   ┆ 110        │
│ 22.8             ┆ 4   ┆ 93         │
│ …                ┆ …   ┆ …          │
└──────────────────┴─────┴────────────┘
```

## Rename vs. select

`rename` keeps **all** columns while changing specific names. This is equivalent
to renaming inside a `select` while also selecting everything else:

```python
# Using rename (simpler)
small_cars.rename(miles_per_gallon="mpg")

# Equivalent using select + dictionary rename
small_cars.select({"mpg": "miles_per_gallon"}, "cyl", "hp")
```

## Batch renaming with `tolower`

You can convert all column names to lowercase in one call:

```python
df = tp.tibble(X=[1, 2], Y=[3, 4], Z=[5, 6])
df.rename(tolower=True)
```

```
shape: (2, 3)
┌─────┬─────┬─────┐
│ x   ┆ y   ┆ z   │
╞═════╪═════╪═════╡
│ 1   ┆ 3   ┆ 5   │
│ 2   ┆ 4   ┆ 6   │
└─────┴─────┴─────┘
```
