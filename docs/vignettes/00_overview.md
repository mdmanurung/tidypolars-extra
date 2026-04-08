# Overview

**tidypolars-extra** brings R's [Tidyverse](https://www.tidyverse.org/)-style
data manipulation to Python on top of the fast [Polars](https://pola.rs/)
engine. If you already know `dplyr`, `tidyr`, `stringr`, or `lubridate` from
R, you should feel right at home.

This vignette is a quick end-to-end tour of the core verbs — `filter`,
`arrange`, `select`, `mutate`, `group_by`/`summarize`, and joins — using
the [Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) dataset.
Each per-verb vignette that follows covers one verb in depth; this page
shows how they all fit together.

## Setup

Every tidypolars-extra function lives under a single top-level namespace, so
the convention is to import the package as `tp`:

```python
import tidypolars_extra as tp

penguins = tp.tibble(
    tp.read_data(fn="tidypolars_extra/data/penguins.csv", sep=",", silently=True)
)
```

The result is a `tibble` — a thin wrapper around `polars.DataFrame`
that exposes tidyverse-style verbs like `filter`, `mutate`, and `summarize`
while keeping all of Polars' speed underneath.

## A first look at the data

A `tibble` has R-style `nrow` / `ncol` / `names` properties and the usual
`head()` for a quick peek:

```python
penguins.nrow, penguins.ncol
```

```
(344, 8)
```

```python
penguins.names
```

```
['species', 'island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex', 'year']
```

```python
penguins.head()
```

```
shape: (5, 8)
┌─────────┬───────────┬───────────────┬───────────────┬──────────────┬─────────────┬────────┬──────┐
│ species ┆ island    ┆ bill_length_m ┆ bill_depth_mm ┆ flipper_leng ┆ body_mass_g ┆ sex    ┆ year │
│ ---     ┆ ---       ┆ m             ┆ ---           ┆ th_mm        ┆ ---         ┆ ---    ┆ ---  │
│ str     ┆ str       ┆ ---           ┆ f64           ┆ ---          ┆ f64         ┆ str    ┆ i64  │
│         ┆           ┆ f64           ┆               ┆ f64          ┆             ┆        ┆      │
╞═════════╪═══════════╪═══════════════╪═══════════════╪══════════════╪═════════════╪════════╪══════╡
│ Adelie  ┆ Torgersen ┆ 39.1          ┆ 18.7          ┆ 181.0        ┆ 3750.0      ┆ male   ┆ 2007 │
│ Adelie  ┆ Torgersen ┆ 39.5          ┆ 17.4          ┆ 186.0        ┆ 3800.0      ┆ female ┆ 2007 │
│ Adelie  ┆ Torgersen ┆ 40.3          ┆ 18.0          ┆ 195.0        ┆ 3250.0      ┆ female ┆ 2007 │
│ Adelie  ┆ Torgersen ┆ null          ┆ null          ┆ null         ┆ null        ┆ null   ┆ 2007 │
│ Adelie  ┆ Torgersen ┆ 36.7          ┆ 19.3          ┆ 193.0        ┆ 3450.0      ┆ female ┆ 2007 │
└─────────┴───────────┴───────────────┴───────────────┴──────────────┴─────────────┴────────┴──────┘
```

Palmer Penguins contains body measurements for three species
(`Adelie`, `Chinstrap`, `Gentoo`) across three islands. A handful of rows
have missing measurements, which is realistic — most of the verbs below
handle nulls gracefully, and we'll drop them explicitly when we need
complete cases.

## `filter` — keep rows of interest

`filter` keeps rows where **every** condition is `True`. Rows where a
condition evaluates to null are dropped automatically. Reference columns
with `tp.col("name")`:

```python
penguins.filter(tp.col("species") == "Gentoo", tp.col("sex") == "female")
```

```
shape: (58, 8)
┌─────────┬────────┬────────────────┬───────────────┬────────────────┬─────────────┬────────┬──────┐
│ species ┆ island ┆ bill_length_mm ┆ bill_depth_mm ┆ flipper_length ┆ body_mass_g ┆ sex    ┆ year │
│ ---     ┆ ---    ┆ ---            ┆ ---           ┆ _mm            ┆ ---         ┆ ---    ┆ ---  │
│ str     ┆ str    ┆ f64            ┆ f64           ┆ ---            ┆ f64         ┆ str    ┆ i64  │
│         ┆        ┆                ┆               ┆ f64            ┆             ┆        ┆      │
╞═════════╪════════╪════════════════╪═══════════════╪════════════════╪═════════════╪════════╪══════╡
│ Gentoo  ┆ Biscoe ┆ 46.1           ┆ 13.2          ┆ 211.0          ┆ 4500.0      ┆ female ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 48.7           ┆ 14.1          ┆ 210.0          ┆ 4450.0      ┆ female ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 46.5           ┆ 13.5          ┆ 210.0          ┆ 4550.0      ┆ female ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 45.4           ┆ 14.6          ┆ 211.0          ┆ 4800.0      ┆ female ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 43.3           ┆ 13.4          ┆ 209.0          ┆ 4400.0      ┆ female ┆ 2007 │
│ …       ┆ …      ┆ …              ┆ …             ┆ …              ┆ …           ┆ …      ┆ …    │
│ Gentoo  ┆ Biscoe ┆ 43.5           ┆ 15.2          ┆ 213.0          ┆ 4650.0      ┆ female ┆ 2009 │
│ Gentoo  ┆ Biscoe ┆ 46.2           ┆ 14.1          ┆ 217.0          ┆ 4375.0      ┆ female ┆ 2009 │
│ Gentoo  ┆ Biscoe ┆ 47.2           ┆ 13.7          ┆ 214.0          ┆ 4925.0      ┆ female ┆ 2009 │
│ Gentoo  ┆ Biscoe ┆ 46.8           ┆ 14.3          ┆ 215.0          ┆ 4850.0      ┆ female ┆ 2009 │
│ Gentoo  ┆ Biscoe ┆ 45.2           ┆ 14.8          ┆ 212.0          ┆ 5200.0      ┆ female ┆ 2009 │
└─────────┴────────┴────────────────┴───────────────┴────────────────┴─────────────┴────────┴──────┘
```

Use the `|` operator (wrapped in parentheses) for **OR** conditions,
and `&` for explicit **AND**. To drop rows with nulls in specific columns,
use `drop_na`:

```python
complete = penguins.drop_na()
complete.nrow
```

```
333
```

## `arrange` — sort rows

`arrange` sorts ascending by default. Wrap a column in `tp.desc(...)` to
sort it in descending order; later columns break ties:

```python
complete.arrange(tp.desc("body_mass_g"), "bill_length_mm").head()
```

```
shape: (5, 8)
┌─────────┬────────┬────────────────┬───────────────┬──────────────────┬─────────────┬──────┬──────┐
│ species ┆ island ┆ bill_length_mm ┆ bill_depth_mm ┆ flipper_length_m ┆ body_mass_g ┆ sex  ┆ year │
│ ---     ┆ ---    ┆ ---            ┆ ---           ┆ m                ┆ ---         ┆ ---  ┆ ---  │
│ str     ┆ str    ┆ f64            ┆ f64           ┆ ---              ┆ f64         ┆ str  ┆ i64  │
│         ┆        ┆                ┆               ┆ f64              ┆             ┆      ┆      │
╞═════════╪════════╪════════════════╪═══════════════╪══════════════════╪═════════════╪══════╪══════╡
│ Gentoo  ┆ Biscoe ┆ 49.2           ┆ 15.2          ┆ 221.0            ┆ 6300.0      ┆ male ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 59.6           ┆ 17.0          ┆ 230.0            ┆ 6050.0      ┆ male ┆ 2007 │
│ Gentoo  ┆ Biscoe ┆ 48.8           ┆ 16.2          ┆ 222.0            ┆ 6000.0      ┆ male ┆ 2009 │
│ Gentoo  ┆ Biscoe ┆ 51.1           ┆ 16.3          ┆ 220.0            ┆ 6000.0      ┆ male ┆ 2008 │
│ Gentoo  ┆ Biscoe ┆ 45.2           ┆ 16.4          ┆ 223.0            ┆ 5950.0      ┆ male ┆ 2008 │
└─────────┴────────┴────────────────┴───────────────┴──────────────────┴─────────────┴──────┴──────┘
```

## `select` — pick columns

`select` accepts bare column names, negative selections (`"-year"`), and
the tidyselect helpers from `tp.starts_with`, `tp.ends_with`, `tp.contains`,
`tp.matches`, and `tp.everything`:

```python
complete.select("species", "island", "sex", "body_mass_g").head()
```

```
shape: (5, 4)
┌─────────┬───────────┬────────┬─────────────┐
│ species ┆ island    ┆ sex    ┆ body_mass_g │
│ ---     ┆ ---       ┆ ---    ┆ ---         │
│ str     ┆ str       ┆ str    ┆ f64         │
╞═════════╪═══════════╪════════╪═════════════╡
│ Adelie  ┆ Torgersen ┆ male   ┆ 3750.0      │
│ Adelie  ┆ Torgersen ┆ female ┆ 3800.0      │
│ Adelie  ┆ Torgersen ┆ female ┆ 3250.0      │
│ Adelie  ┆ Torgersen ┆ female ┆ 3450.0      │
│ Adelie  ┆ Torgersen ┆ male   ┆ 3650.0      │
└─────────┴───────────┴────────┴─────────────┘
```

```python
complete.select("species", tp.starts_with("bill_")).head()
```

```
shape: (5, 3)
┌─────────┬────────────────┬───────────────┐
│ species ┆ bill_length_mm ┆ bill_depth_mm │
│ ---     ┆ ---            ┆ ---           │
│ str     ┆ f64            ┆ f64           │
╞═════════╪════════════════╪═══════════════╡
│ Adelie  ┆ 39.1           ┆ 18.7          │
│ Adelie  ┆ 39.5           ┆ 17.4          │
│ Adelie  ┆ 40.3           ┆ 18.0          │
│ Adelie  ┆ 36.7           ┆ 19.3          │
│ Adelie  ┆ 39.3           ┆ 20.6          │
└─────────┴────────────────┴───────────────┘
```

```python
complete.select("species", tp.contains("_mm")).head()
```

```
shape: (5, 4)
┌─────────┬────────────────┬───────────────┬───────────────────┐
│ species ┆ bill_length_mm ┆ bill_depth_mm ┆ flipper_length_mm │
│ ---     ┆ ---            ┆ ---           ┆ ---               │
│ str     ┆ f64            ┆ f64           ┆ f64               │
╞═════════╪════════════════╪═══════════════╪═══════════════════╡
│ Adelie  ┆ 39.1           ┆ 18.7          ┆ 181.0             │
│ Adelie  ┆ 39.5           ┆ 17.4          ┆ 186.0             │
│ Adelie  ┆ 40.3           ┆ 18.0          ┆ 195.0             │
│ Adelie  ┆ 36.7           ┆ 19.3          ┆ 193.0             │
│ Adelie  ┆ 39.3           ┆ 20.6          ┆ 190.0             │
└─────────┴────────────────┴───────────────┴───────────────────┘
```

## `mutate` — add or modify columns

`mutate` creates new columns as keyword arguments. Expressions are built
from `tp.col(...)` and regular Python operators. Use `tp.case_when` for
multi-branch logic — conditions are checked top-to-bottom and `_default`
catches everything that falls through:

```python
(
    complete
    .mutate(
        bill_ratio=tp.col("bill_length_mm") / tp.col("bill_depth_mm"),
        size_class=tp.case_when(
            tp.col("body_mass_g") < 3500, "small",
            tp.col("body_mass_g") < 4500, "medium",
            _default="large",
        ),
    )
    .select("species", "sex", "body_mass_g", "bill_ratio", "size_class")
    .head()
)
```

```
shape: (5, 5)
┌─────────┬────────┬─────────────┬────────────┬────────────┐
│ species ┆ sex    ┆ body_mass_g ┆ bill_ratio ┆ size_class │
│ ---     ┆ ---    ┆ ---         ┆ ---        ┆ ---        │
│ str     ┆ str    ┆ f64         ┆ f64        ┆ str        │
╞═════════╪════════╪═════════════╪════════════╪════════════╡
│ Adelie  ┆ male   ┆ 3750.0      ┆ 2.090909   ┆ medium     │
│ Adelie  ┆ female ┆ 3800.0      ┆ 2.270115   ┆ medium     │
│ Adelie  ┆ female ┆ 3250.0      ┆ 2.238889   ┆ small      │
│ Adelie  ┆ female ┆ 3450.0      ┆ 1.901554   ┆ small      │
│ Adelie  ┆ male   ┆ 3650.0      ┆ 1.907767   ┆ medium     │
└─────────┴────────┴─────────────┴────────────┴────────────┘
```

## `group_by` + `summarize` — aggregate by group

`summarize` collapses rows into one row per group. Pass the grouping
columns via `by=`; inside, use aggregators like `tp.mean`, `tp.sd`,
`tp.median`, or `tp.n()` (which counts rows in each group):

```python
complete.summarize(
    n=tp.n(),
    mean_mass=tp.mean("body_mass_g"),
    sd_mass=tp.sd("body_mass_g"),
    mean_bill=tp.mean("bill_length_mm"),
    by="species",
)
```

```
shape: (3, 5)
┌───────────┬─────┬─────────────┬────────────┬───────────┐
│ species   ┆ n   ┆ mean_mass   ┆ sd_mass    ┆ mean_bill │
│ ---       ┆ --- ┆ ---         ┆ ---        ┆ ---       │
│ str       ┆ u32 ┆ f64         ┆ f64        ┆ f64       │
╞═══════════╪═════╪═════════════╪════════════╪═══════════╡
│ Adelie    ┆ 146 ┆ 3706.164384 ┆ 458.620135 ┆ 38.823973 │
│ Chinstrap ┆ 68  ┆ 3733.088235 ┆ 384.335081 ┆ 48.833824 │
│ Gentoo    ┆ 119 ┆ 5092.436975 ┆ 501.476154 ┆ 47.568067 │
└───────────┴─────┴─────────────┴────────────┴───────────┘
```

Pass a list to `by=` to group by multiple columns:

```python
complete.summarize(
    n=tp.n(),
    mean_mass=tp.mean("body_mass_g"),
    by=["species", "sex"],
)
```

```
shape: (6, 4)
┌───────────┬────────┬─────┬─────────────┐
│ species   ┆ sex    ┆ n   ┆ mean_mass   │
│ ---       ┆ ---    ┆ --- ┆ ---         │
│ str       ┆ str    ┆ u32 ┆ f64         │
╞═══════════╪════════╪═════╪═════════════╡
│ Chinstrap ┆ male   ┆ 34  ┆ 3938.970588 │
│ Gentoo    ┆ male   ┆ 61  ┆ 5484.836066 │
│ Adelie    ┆ female ┆ 73  ┆ 3368.835616 │
│ Chinstrap ┆ female ┆ 34  ┆ 3527.205882 │
│ Gentoo    ┆ female ┆ 58  ┆ 4679.741379 │
│ Adelie    ┆ male   ┆ 73  ┆ 4043.493151 │
└───────────┴────────┴─────┴─────────────┘
```

The `by=` argument is also available on `filter` and `mutate` for
grouped row-filtering and grouped window functions — see the
{doc}`Group By <08_group_by>` vignette for the full story.

## Joining tables

Joins combine two tibbles on shared key columns. `left_join` keeps every
row from the left table and attaches matching rows from the right. Let's
build a small lookup table of scientific names and attach it to a per-species
summary:

```python
scientific = tp.tibble(
    species=["Adelie", "Chinstrap", "Gentoo"],
    scientific_name=[
        "Pygoscelis adeliae",
        "Pygoscelis antarcticus",
        "Pygoscelis papua",
    ],
)

summary = complete.summarize(
    n=tp.n(),
    mean_mass=tp.mean("body_mass_g"),
    by="species",
)

summary.left_join(scientific, on="species")
```

```
shape: (3, 4)
┌───────────┬─────┬─────────────┬────────────────────────┐
│ species   ┆ n   ┆ mean_mass   ┆ scientific_name        │
│ ---       ┆ --- ┆ ---         ┆ ---                    │
│ str       ┆ u32 ┆ f64         ┆ str                    │
╞═══════════╪═════╪═════════════╪════════════════════════╡
│ Adelie    ┆ 146 ┆ 3706.164384 ┆ Pygoscelis adeliae     │
│ Chinstrap ┆ 68  ┆ 3733.088235 ┆ Pygoscelis antarcticus │
│ Gentoo    ┆ 119 ┆ 5092.436975 ┆ Pygoscelis papua       │
└───────────┴─────┴─────────────┴────────────────────────┘
```

`inner_join`, `right_join`, and `full_join` work the same way.
When the key columns have different names in each table, use
`left_on=` and `right_on=` instead of `on=`.

## Putting it all together

Because every verb returns a new `tibble`, you can chain them into a
single pipeline that reads top-to-bottom like a recipe — filter,
transform, group, summarize, sort:

```python
(
    penguins
    .drop_na()
    .filter(tp.col("body_mass_g") > 3000)
    .mutate(bill_ratio=tp.col("bill_length_mm") / tp.col("bill_depth_mm"))
    .summarize(
        n=tp.n(),
        mean_ratio=tp.mean("bill_ratio"),
        mean_mass=tp.mean("body_mass_g"),
        by=["species", "sex"],
    )
    .arrange("species", tp.desc("mean_mass"))
)
```

```
shape: (6, 5)
┌───────────┬────────┬─────┬────────────┬─────────────┐
│ species   ┆ sex    ┆ n   ┆ mean_ratio ┆ mean_mass   │
│ ---       ┆ ---    ┆ --- ┆ ---        ┆ ---         │
│ str       ┆ str    ┆ u32 ┆ f64        ┆ f64         │
╞═══════════╪════════╪═════╪════════════╪═════════════╡
│ Adelie    ┆ male   ┆ 73  ┆ 2.123835   ┆ 4043.493151 │
│ Adelie    ┆ female ┆ 65  ┆ 2.118286   ┆ 3424.615385 │
│ Chinstrap ┆ male   ┆ 34  ┆ 2.656501   ┆ 3938.970588 │
│ Chinstrap ┆ female ┆ 32  ┆ 2.647082   ┆ 3572.65625  │
│ Gentoo    ┆ male   ┆ 61  ┆ 3.152081   ┆ 5484.836066 │
│ Gentoo    ┆ female ┆ 58  ┆ 3.202391   ┆ 4679.741379 │
└───────────┴────────┴─────┴────────────┴─────────────┘
```

## Where to go next

Each core verb has its own vignette with more worked examples and edge
cases:

- {doc}`Filter <01_filter>` — row selection, grouped filters, helper functions
- {doc}`Arrange <02_arrange>` — sorting, ties, nulls
- {doc}`Select <03_select>` — tidyselect helpers, negation, reordering
- {doc}`Rename <04_rename>` — renaming columns
- {doc}`Mutate <05_mutate>` — new columns, `case_when`, `if_else`, grouped mutates
- {doc}`Transmute <06_transmute>` — mutate + select in one step
- {doc}`Summarize <07_summarize>` — aggregations and helper stats
- {doc}`Group By <08_group_by>` — the `by=` argument and explicit groups

For the full list of string, date, factor, and statistical helpers, see the
{doc}`API reference </autoapi/index>`.
