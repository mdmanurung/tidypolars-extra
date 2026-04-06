# Arrange

The `.arrange()` method lets you sort the rows of your data through two steps:

* Choosing columns to sort by
* Specifying an order (ascending or descending)

Below, we illustrate this with a single variable, multiple variables, and
more general expressions.

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))

small_mtcars = mtcars.select("name", "cyl", "mpg", "hp")

small_mtcars
```

## Arranging rows by a single variable

The simplest way to use `arrange` is to specify a column name. Rows are sorted
in **ascending** order by default.

For example, the code below arranges rows from least to greatest horsepower (`hp`).

```python
small_mtcars.arrange("hp")
```

```
shape: (32, 4)
┌────────────────┬─────┬──────┬─────┐
│ name           ┆ cyl ┆ mpg  ┆ hp  │
╞════════════════╪═════╪══════╪═════╡
│ Honda Civic    ┆ 4   ┆ 30.4 ┆ 52  │
│ Merc 240D      ┆ 4   ┆ 24.4 ┆ 62  │
│ Toyota Corolla ┆ 4   ┆ 33.9 ┆ 65  │
│ …              ┆ …   ┆ …    ┆ …   │
└────────────────┴─────┴──────┴─────┘
```

To sort in **descending** order, wrap the column name with `tp.desc()`.

```python
small_mtcars.arrange(tp.desc("hp"))
```

```
shape: (32, 4)
┌───────────────────┬─────┬──────┬─────┐
│ name              ┆ cyl ┆ mpg  ┆ hp  │
╞═══════════════════╪══════╪═════╪═════╡
│ Maserati Bora     ┆ 8   ┆ 15.0 ┆ 335 │
│ Ford Pantera L    ┆ 8   ┆ 15.8 ┆ 264 │
│ Duster 360        ┆ 8   ┆ 14.3 ┆ 245 │
│ …                 ┆ …   ┆ …    ┆ …   │
└───────────────────┴─────┴──────┴─────┘
```

## Arranging rows by multiple variables

When `arrange` receives multiple arguments, it sorts so that the first column
specified changes the slowest, followed by the second, and so on.

```python
small_mtcars.arrange("cyl", "mpg")
```

```
shape: (32, 4)
┌───────────────┬─────┬──────┬─────┐
│ name          ┆ cyl ┆ mpg  ┆ hp  │
╞═══════════════╪═════╪══════╪═════╡
│ Volvo 142E    ┆ 4   ┆ 21.4 ┆ 109 │
│ Toyota Corona ┆ 4   ┆ 21.5 ┆ 97  │
│ Datsun 710    ┆ 4   ┆ 22.8 ┆ 93  │
│ …             ┆ …   ┆ …    ┆ …   │
└───────────────┴─────┴──────┴─────┘
```

You can mix ascending and descending in the same call:

```python
small_mtcars.arrange(tp.desc("cyl"), "mpg")
```

```
shape: (32, 4)
┌─────────────────────┬─────┬──────┬─────┐
│ name                ┆ cyl ┆ mpg  ┆ hp  │
╞═════════════════════╪═════╪══════╪═════╡
│ Cadillac Fleetwood  ┆ 8   ┆ 10.4 ┆ 205 │
│ Lincoln Continental ┆ 8   ┆ 10.4 ┆ 215 │
│ Camaro Z28          ┆ 8   ┆ 13.3 ┆ 245 │
│ …                   ┆ …   ┆ …    ┆ …   │
└─────────────────────┴─────┴──────┴─────┘
```
