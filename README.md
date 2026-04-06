# tidypolars-extra

**tidypolars-extra** is an extension of [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci), which provides Tidyverse-like functions for data manipulation and analysis in Python using [Polars](https://github.com/pola-rs/polars) as the backend.

This project builds upon the original [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci) by adding extra functionalities and improvements while maintaining the same familiar API.

## Features

- Tidyverse-style API for [Polars](https://github.com/pola-rs/polars) DataFrames
- Scientific research utilities including LaTeX table generation
- Fast data manipulation powered by Polars
- Familiar R-like syntax for Python users

## Installation

You can install tidypolars-extra with `pip`:

```bash
pip install tidypolars-extra
```

## Basic usage

tidypolars-extra methods are designed to work like tidyverse functions:

```python
import tidypolars_extra as tp

# create tibble data frame
df = tp.tibble(x = range(3),
               y = range(3, 6),
               z = ['a', 'a', 'b'])

(
    df
    .select('x', 'y', 'z')
    .filter(tp.col('x') < 4, tp.col('y') > 1)
    .arrange(tp.desc('z'), 'x')
    .mutate(double_x = tp.col('x') * 2,
            x_plus_y = tp.col('x') + tp.col('y')
            )
)
┌─────┬─────┬─────┬──────────┬──────────┐
│ x   ┆ y   ┆ z   ┆ double_x ┆ x_plus_y │
│ --- ┆ --- ┆ --- ┆ ---      ┆ ---      │
│ i64 ┆ i64 ┆ str ┆ i64      ┆ i64      │
╞═════╪═════╪═════╪══════════╪══════════╡
│ 2   ┆ 5   ┆ b   ┆ 4        ┆ 7        │
├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤
│ 0   ┆ 3   ┆ a   ┆ 0        ┆ 3        │
├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤
│ 1   ┆ 4   ┆ a   ┆ 2        ┆ 5        │
└─────┴─────┴─────┴──────────┴──────────┘

```

## Converting to/from pandas data frames

If you need to use a package that requires pandas or polars data frames, you can convert from a tidypolars_extra `tibble` to either of those `DataFrame` formats.

```python
# convert to pandas...
df = df.to_pandas()
# ... or convert to polars
df = df.to_polars()
```

To convert from a pandas or polars `DataFrame` to a tidypolars `tibble`:

```python
# convert from pandas...
df = tp.from_pandas(df)
# or covert from polars
df = tp.from_polars(df)
```

## Acknowledgments

This project is an extension of:
- [tidypolars4sci](https://github.com/DiogoFerrari/tidypolars4sci) by Diogo Ferrari
- [tidypolars](https://pypi.org/project/tidypolars/) — the original starting point
