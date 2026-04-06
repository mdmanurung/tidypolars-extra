# User Guide

This guide covers the core data analysis operations available in tidypolars-extra,
organized by task. Each page includes detailed examples and explanations.

```{toctree}
:maxdepth: 2

verb_filter
verb_arrange
verb_select
verb_mutate
verb_summarize
verb_group_by
verb_joins
verb_reshape
verb_strings
verb_dates
```

## Overview

tidypolars-extra organizes data analysis around a small set of composable **verbs**.
Each verb takes a DataFrame (tibble) as input and returns a new DataFrame — making
them easy to chain together.

### Core Verbs

| Verb | Purpose | Example |
|------|---------|---------|
| `filter` | Pick rows by condition | `df.filter(col("x") > 5)` |
| `arrange` | Sort rows | `df.arrange(desc("x"))` |
| `select` | Pick columns | `df.select("a", "b")` |
| `mutate` | Add/transform columns | `df.mutate(y=col("x") * 2)` |
| `summarize` | Aggregate rows | `df.summarize(m=mean("x"), by="g")` |
| `group_by` | Define groups | `df.group_by("g")` |

### Additional Verbs

| Verb | Purpose | Example |
|------|---------|---------|
| `distinct` | Unique rows | `df.distinct("x")` |
| `count` | Count rows by group | `df.count("x")` |
| `slice` | Pick rows by position | `df.slice(0, 5)` |
| `rename` | Rename columns | `df.rename(new="old")` |
| `relocate` | Move columns | `df.relocate("z", before="a")` |
| `drop` | Remove columns | `df.drop("x")` |
| `pull` | Extract a column | `df.pull("x")` |

### Joins

| Verb | Purpose |
|------|---------|
| `left_join` | Keep all rows from left table |
| `inner_join` | Keep only matching rows |
| `full_join` | Keep all rows from both tables |

### Reshaping

| Verb | Purpose |
|------|---------|
| `pivot_longer` | Wide → Long format |
| `pivot_wider` | Long → Wide format |
| `separate` | Split one column into many |
| `unite` | Combine columns into one |
| `nest` / `unnest` | Nest/unnest DataFrames |

### String Operations

Functions from R's `stringr`, prefixed with `str_`:

`str_detect`, `str_replace`, `str_extract`, `str_to_upper`, `str_to_lower`,
`str_trim`, `str_sub`, `paste`, `paste0`

### Date/Time Operations

Functions from R's `lubridate`:

`year`, `month`, `mday`, `hour`, `minute`, `second`, `as_date`, `as_datetime`,
`make_date`, `make_datetime`
