# tidypolars-extra vs siuba

Both tidypolars-extra and siuba bring Tidyverse-style analysis to Python. This page
compares their syntax and highlights the key differences.

## Overview

| Aspect | tidypolars-extra | siuba |
|--------|-----------------|-------|
| **Backend** | Polars (Rust) | pandas |
| **Syntax style** | Method chaining | Pipe operator (`>>`) |
| **Column references** | `col("name")` | `_.name` |
| **Grouped ops** | `by=` parameter | Separate `group_by()` verb |
| **Performance** | Very fast (Polars) | pandas speed |
| **Data type** | `tibble` (Polars DataFrame) | pandas DataFrame |

## Setup

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, n, desc, if_else

df = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave", "Eve"],
    age=[32, 45, 28, 52, 38],
    dept=["Eng", "Sales", "Eng", "HR", "Sales"],
    salary=[95000, 72000, 88000, 65000, 78000]
)
\`\`\`
```

```{tab} siuba
\`\`\`python
import pandas as pd
from siuba import _, filter, select, mutate, arrange
from siuba import group_by, summarize, ungroup
from siuba.dply.verbs import desc

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age": [32, 45, 28, 52, 38],
    "dept": ["Eng", "Sales", "Eng", "HR", "Sales"],
    "salary": [95000, 72000, 88000, 65000, 78000]
})
\`\`\`
```
````

---

## Filtering Rows

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.filter(col("age") > 30, col("salary") > 70000)
\`\`\`
```

```{tab} siuba
\`\`\`python
df >> filter(_.age > 30, _.salary > 70000)
\`\`\`
```
````

**Similarity:** Both support multiple conditions as separate arguments (implicit AND).

**Difference:** tidypolars-extra uses `col("name")` while siuba uses `_.name` (siu expressions).
tidypolars-extra uses method chaining while siuba uses `>>` pipe operator.

---

## Selecting Columns

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# By name
df.select("name", "age", "salary")

# With helpers
from tidypolars_extra import starts_with
df.select(starts_with("s"))
\`\`\`
```

```{tab} siuba
\`\`\`python
# By name
df >> select(_.name, _.age, _.salary)

# With helpers (limited support)
# siuba doesn't have starts_with helpers
df >> select(_.name, _.age, _.salary)
\`\`\`
```
````

**Difference:** tidypolars-extra provides rich tidy-select helpers (`starts_with`,
`ends_with`, `contains`, `matches`, `where`, `everything`) that match R's dplyr.
siuba has more limited selection capabilities.

---

## Creating Columns (Mutate)

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.mutate(
    salary_k=col("salary") / 1000,
    label=if_else(col("age") > 40, "senior", "junior")
)
\`\`\`
```

```{tab} siuba
\`\`\`python
df >> mutate(
    salary_k=_.salary / 1000,
    label=if_else(_.age > 40, "senior", "junior")
)
\`\`\`
```
````

**Similarity:** Both use named keyword arguments with the same verb name. Very similar syntax.

**Difference:** Column references — `col("salary")` vs `_.salary`.

---

## Sorting Rows

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.arrange(desc("salary"))
df.arrange("dept", desc("salary"))
\`\`\`
```

```{tab} siuba
\`\`\`python
df >> arrange(desc(_.salary))
df >> arrange(_.dept, desc(_.salary))
\`\`\`
```
````

**Similarity:** Both use `desc()` wrapper for descending sort. Nearly identical API.

---

## Grouping and Summarizing

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Inline grouping with by=
df.summarize(
    avg_salary=mean("salary"),
    count=n(),
    by="dept"
)

# Or with explicit group_by
(df
 .group_by("dept")
 .summarize(
     avg_salary=mean("salary"),
     count=n()
 )
)
\`\`\`
```

```{tab} siuba
\`\`\`python
# Requires separate group_by step
(df
 >> group_by(_.dept)
 >> summarize(
     avg_salary=_.salary.mean(),
     count=_.salary.size()
 )
)

# Note: siuba needs ungroup() for further ops
(df
 >> group_by(_.dept)
 >> summarize(avg_salary=_.salary.mean())
 >> ungroup()
 >> arrange(desc(_.avg_salary))
)
\`\`\`
```
````

**Key difference:** tidypolars-extra has the convenient `by=` parameter built into
`summarize` and `mutate`, avoiding the need for a separate `group_by()` and `ungroup()`.
siuba requires explicit `group_by()` and `ungroup()` steps.

---

## Joining Tables

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
dept = tp.tibble(
    dept=["Eng", "Sales", "HR"],
    location=["SF", "NY", "Chicago"]
)

df.left_join(dept, on="dept")
df.inner_join(dept, on="dept")
\`\`\`
```

```{tab} siuba
\`\`\`python
from siuba import left_join, inner_join

dept = pd.DataFrame({
    "dept": ["Eng", "Sales", "HR"],
    "location": ["SF", "NY", "Chicago"]
})

df >> left_join(_, dept, on="dept")
df >> inner_join(_, dept, on="dept")
\`\`\`
```
````

**Similarity:** Both use separate named join functions matching R's dplyr. The API
style is very similar.

---

## Reshaping

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Wide to long
df.pivot_longer(
    cols=["age", "salary"],
    names_to="variable",
    values_to="value"
)

# Long to wide
long_df.pivot_wider(
    names_from="variable",
    values_from="value"
)
\`\`\`
```

```{tab} siuba
\`\`\`python
from siuba import gather, spread

# Wide to long (gather)
df >> gather("variable", "value",
             _.age, _.salary)

# Long to wide (spread)
long_df >> spread("variable", "value")
\`\`\`
```
````

**Difference:** tidypolars-extra uses the modern `pivot_longer` / `pivot_wider` naming
(matching tidyr ≥ 1.0), while siuba uses the older `gather` / `spread` names.

---

## Nesting Data

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Nest data by department
nested = df.nest(by="dept")

# Unnest
nested.unnest("data")
\`\`\`
```

```{tab} siuba
\`\`\`python
from siuba import nest, unnest

# Nest data by department
nested = df >> group_by(_.dept) >> nest()

# Unnest
nested >> unnest("data")
\`\`\`
```
````

---

## Full Pipeline Comparison

A complete analysis pipeline side by side:

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, n, desc, if_else

employees = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave", "Eve",
          "Frank", "Grace", "Hank"],
    dept=["Eng", "Eng", "Sales", "Sales",
          "Eng", "HR", "HR", "Sales"],
    salary=[95, 88, 72, 65, 102, 58, 62, 78],
    rating=[4.5, 3.8, 4.2, 3.1, 4.8, 3.5, 4.0, 3.9]
)

result = (
    employees
    .filter(col("salary") > 60)
    .mutate(
        perf=if_else(col("rating") >= 4.0,
                     "high", "standard")
    )
    .summarize(
        avg_salary=mean("salary"),
        n_employees=n(),
        by=["dept", "perf"]
    )
    .arrange("dept", desc("avg_salary"))
)
\`\`\`
```

```{tab} siuba
\`\`\`python
import pandas as pd
from siuba import (_, filter, mutate, group_by,
                   summarize, arrange, ungroup)
from siuba.dply.verbs import desc, if_else

employees = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave", "Eve",
             "Frank", "Grace", "Hank"],
    "dept": ["Eng", "Eng", "Sales", "Sales",
             "Eng", "HR", "HR", "Sales"],
    "salary": [95, 88, 72, 65, 102, 58, 62, 78],
    "rating": [4.5, 3.8, 4.2, 3.1, 4.8, 3.5, 4.0, 3.9]
})

result = (
    employees
    >> filter(_.salary > 60)
    >> mutate(
        perf=if_else(_.rating >= 4.0,
                     "high", "standard")
    )
    >> group_by(_.dept, _.perf)
    >> summarize(
        avg_salary=_.salary.mean(),
        n_employees=_.name.size()
    )
    >> ungroup()
    >> arrange(_.dept, desc(_.avg_salary))
)
\`\`\`
```
````

---

## Summary

| Feature | tidypolars-extra | siuba |
|---------|-----------------|-------|
| Column refs | `col("name")` | `_.name` |
| Chaining | `.method()` | `>> verb()` |
| Grouping | `by=` param or `.group_by()` | `>> group_by()` + `>> ungroup()` |
| Performance | Polars (very fast) | pandas |
| Select helpers | `starts_with`, `ends_with`, etc. | Limited |
| Reshape verbs | `pivot_longer` / `pivot_wider` | `gather` / `spread` |
| Nesting | `.nest(by=...)` | `>> group_by() >> nest()` |
| Output type | `tibble` (Polars-based) | pandas DataFrame |

**When to use tidypolars-extra:** When you need Polars performance with a tidy API,
or when working with large datasets and scientific/academic workflows.

**When to use siuba:** When you're already invested in the pandas ecosystem and
prefer the pipe (`>>`) syntax.
