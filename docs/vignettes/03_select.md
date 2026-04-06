# Select

The `.select()` method lets you choose specific columns of your data to keep.
Each selection may include:

* Specifying column(s) to include
* Excluding (dropping) some columns
* Renaming columns via a dictionary
* Searching columns using helper functions like `contains` or `starts_with`

```python
import tidypolars_extra as tp

mtcars = tp.tibble(tp.read_data(fn="tidypolars_extra/data/mtcars.csv", sep=",", silently=True))

mtcars
```

## Selecting columns by name

The simplest way to select columns is by passing their names as strings.

```python
mtcars.select("mpg", "cyl")
```

```
shape: (32, 2)
┌──────┬─────┐
│ mpg  ┆ cyl │
╞══════╪═════╡
│ 21.0 ┆ 6   │
│ 21.0 ┆ 6   │
│ 22.8 ┆ 4   │
│ …    ┆ …   │
└──────┴─────┘
```

You can also pass column names using `tp.col()`:

```python
mtcars.select(tp.col("mpg"), tp.col("cyl"))
```

## Excluding columns

To remove columns, use the `.drop()` method:

```python
mtcars.drop("mpg", "cyl")
```

```
shape: (32, 10)
┌───────────────────┬───────┬─────┬───┬─────┬─────┬──────┬──────┐
│ name              ┆ disp  ┆ hp  ┆ … ┆ vs  ┆ am  ┆ gear ┆ carb │
╞═══════════════════╪═══════╪═════╪═══╪═════╪═════╪══════╪══════╡
│ Mazda RX4         ┆ 160.0 ┆ 110 ┆ … ┆ 0   ┆ 1   ┆ 4    ┆ 4    │
│ Mazda RX4 Wag     ┆ 160.0 ┆ 110 ┆ … ┆ 0   ┆ 1   ┆ 4    ┆ 4    │
│ …                 ┆ …     ┆ …   ┆ … ┆ …   ┆ …   ┆ …    ┆ …    │
└───────────────────┴───────┴─────┴───┴─────┴─────┴──────┴──────┘
```

## Renaming columns during selection

You can rename columns in a `select` by passing a dictionary mapping old names
to new names:

```python
mtcars.select({"mpg": "miles_per_gallon"}, "cyl")
```

```
shape: (32, 2)
┌─────────────────┬─────┐
│ miles_per_gallon ┆ cyl │
╞═════════════════╪═════╡
│ 21.0            ┆ 6   │
│ 21.0            ┆ 6   │
│ 22.8            ┆ 4   │
│ …               ┆ …   │
└─────────────────┴─────┘
```

## Searching with helper functions

tidypolars-extra provides several helper functions to select columns by
pattern matching.

### `contains` — match columns containing a substring

```python
mtcars.select(tp.contains("c"))
```

```
shape: (32, 3)
┌─────┬───────┬──────┐
│ cyl ┆ qsec  ┆ carb │
╞═════╪═══════╪══════╡
│ 6   ┆ 16.46 ┆ 4    │
│ 6   ┆ 17.02 ┆ 4    │
│ 4   ┆ 18.61 ┆ 1    │
│ …   ┆ …     ┆ …    │
└─────┴───────┴──────┘
```

### `starts_with` — match columns starting with a prefix

```python
mtcars.select(tp.starts_with("c"))
```

```
shape: (32, 2)
┌─────┬──────┐
│ cyl ┆ carb │
╞═════╪══════╡
│ 6   ┆ 4    │
│ 6   ┆ 4    │
│ 4   ┆ 1    │
│ …   ┆ …    │
└─────┴──────┘
```

### `ends_with` — match columns ending with a suffix

```python
mtcars.select(tp.ends_with("p"))
```

### `matches` — match columns using a regex pattern

```python
mtcars.select(tp.matches("^d"))
```

### `everything` — select all columns

```python
mtcars.select(tp.everything())
```

### `where` — select columns by type

```python
# Select only numeric (float) columns
mtcars.select(tp.where("float"))
```

## Combining selection strategies

You can combine different selection strategies in a single call:

```python
mtcars.select("name", tp.starts_with("c"))
```
