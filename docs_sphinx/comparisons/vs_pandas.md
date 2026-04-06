# tidypolars-extra vs pandas

A side-by-side comparison of common data analysis patterns in tidypolars-extra and pandas.

## Setup

Both examples use the same dataset:

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, sd, n, desc, if_else, starts_with

df = tp.tibble(
    name=["Alice", "Bob", "Carol", "Dave", "Eve"],
    age=[32, 45, 28, 52, 38],
    department=["Eng", "Sales", "Eng", "HR", "Sales"],
    salary=[95000, 72000, 88000, 65000, 78000],
    score=[88, 92, 75, 85, 91]
)
\`\`\`
```

```{tab} pandas
\`\`\`python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age": [32, 45, 28, 52, 38],
    "department": ["Eng", "Sales", "Eng", "HR", "Sales"],
    "salary": [95000, 72000, 88000, 65000, 78000],
    "score": [88, 92, 75, 85, 91]
})
\`\`\`
```
````

---

## Filtering Rows

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Single condition
df.filter(col("age") > 30)

# Multiple conditions (AND)
df.filter(col("age") > 30, col("salary") > 70000)

# OR condition
df.filter((col("department") == "Eng") | (col("department") == "Sales"))
\`\`\`
```

```{tab} pandas
\`\`\`python
# Single condition
df[df["age"] > 30]
# or df.query("age > 30")

# Multiple conditions (AND)
df[(df["age"] > 30) & (df["salary"] > 70000)]

# OR condition
df[df["department"].isin(["Eng", "Sales"])]
\`\`\`
```
````

**Key difference:** tidypolars-extra uses `col()` expressions and multiple arguments are
implicitly combined with AND. pandas requires manual `&` / `|` operators with parentheses.

---

## Selecting Columns

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# By name
df.select("name", "age", "salary")

# With helpers
df.select(starts_with("s"))          # salary, score
df.select("name", "age":"salary")    # name, age, department, salary

# Drop columns
df.drop("score")
\`\`\`
```

```{tab} pandas
\`\`\`python
# By name
df[["name", "age", "salary"]]

# With filter
df.filter(regex="^s")               # salary, score
df.loc[:, "name":"salary"]          # name, age, department, salary

# Drop columns
df.drop(columns=["score"])
\`\`\`
```
````

**Key difference:** tidypolars-extra provides tidy-select helpers (`starts_with`, `ends_with`,
`contains`, `matches`) that are more readable than regex patterns.

---

## Creating / Transforming Columns

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.mutate(
    salary_k=col("salary") / 1000,
    score_pct=col("score") / 100,
    label=if_else(col("score") > 85, "high", "low")
)
\`\`\`
```

```{tab} pandas
\`\`\`python
df.assign(
    salary_k=lambda x: x["salary"] / 1000,
    score_pct=lambda x: x["score"] / 100,
    label=lambda x: x["score"].apply(
        lambda v: "high" if v > 85 else "low"
    )
)
\`\`\`
```
````

**Key difference:** tidypolars-extra's `mutate` uses Polars expressions directly.
pandas' `assign` requires `lambda` wrappers and `.apply()` for row-level conditions.

---

## Sorting

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Ascending
df.arrange("salary")

# Descending
df.arrange(desc("salary"))

# Multiple columns
df.arrange("department", desc("salary"))
\`\`\`
```

```{tab} pandas
\`\`\`python
# Ascending
df.sort_values("salary")

# Descending
df.sort_values("salary", ascending=False)

# Multiple columns
df.sort_values(["department", "salary"],
               ascending=[True, False])
\`\`\`
```
````

**Key difference:** tidypolars-extra uses the `desc()` wrapper per-column, which is more
readable than the `ascending=[True, False]` list in pandas.

---

## Grouping and Summarizing

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.summarize(
    avg_salary=mean("salary"),
    max_score=tp.max("score"),
    count=n(),
    by="department"
)
\`\`\`
```

```{tab} pandas
\`\`\`python
(df
 .groupby("department")
 .agg(
     avg_salary=("salary", "mean"),
     max_score=("score", "max"),
     count=("name", "size")
 )
 .reset_index()
)
\`\`\`
```
````

**Key difference:** tidypolars-extra has `by=` built into `summarize`, no need for a
separate `groupby()` call. Named aggregations use intuitive function wrappers like
`mean("salary")` instead of tuples.

---

## Joining Tables

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
dept_info = tp.tibble(
    department=["Eng", "Sales", "HR"],
    location=["SF", "NY", "Chicago"]
)

df.left_join(dept_info, on="department")
df.inner_join(dept_info, on="department")
df.full_join(dept_info, on="department")
\`\`\`
```

```{tab} pandas
\`\`\`python
dept_info = pd.DataFrame({
    "department": ["Eng", "Sales", "HR"],
    "location": ["SF", "NY", "Chicago"]
})

df.merge(dept_info, on="department", how="left")
df.merge(dept_info, on="department", how="inner")
df.merge(dept_info, on="department", how="outer")
\`\`\`
```
````

**Key difference:** tidypolars-extra uses separate methods (`left_join`, `inner_join`,
`full_join`) instead of pandas' single `merge(how=...)` parameter. This makes the
join type immediately visible when reading code.

---

## Reshaping: Pivot Longer & Wider

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Wide to long
df.pivot_longer(
    cols=["salary", "score"],
    names_to="metric",
    values_to="value"
)

# Long to wide
long_df.pivot_wider(
    names_from="metric",
    values_from="value"
)
\`\`\`
```

```{tab} pandas
\`\`\`python
# Wide to long
df.melt(
    id_vars=["name", "age", "department"],
    value_vars=["salary", "score"],
    var_name="metric",
    value_name="value"
)

# Long to wide
long_df.pivot_table(
    index=["name", "age", "department"],
    columns="metric",
    values="value"
).reset_index()
\`\`\`
```
````

**Key difference:** tidypolars-extra's `pivot_longer` automatically determines which
columns to keep as identifiers. pandas' `melt` requires you to explicitly list
`id_vars`.

---

## Handling Missing Values

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
# Drop rows with nulls
df.drop_null()
df.drop_null("salary", "score")

# Fill nulls
df.fill(cols=["salary"], direction="down")
df.replace_null(replace={"salary": 0})
\`\`\`
```

```{tab} pandas
\`\`\`python
# Drop rows with NaN
df.dropna()
df.dropna(subset=["salary", "score"])

# Fill NaN
df["salary"].ffill()
df.fillna({"salary": 0})
\`\`\`
```
````

---

## Distinct Rows

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
df.distinct("department")
df.distinct("department", keep_all=True)
\`\`\`
```

```{tab} pandas
\`\`\`python
df[["department"]].drop_duplicates()
df.drop_duplicates(subset=["department"])
\`\`\`
```
````

---

## Summary

| Operation | tidypolars-extra | pandas |
|-----------|-----------------|--------|
| Filter | `df.filter(col("x") > 5)` | `df[df["x"] > 5]` |
| Select | `df.select("a", "b")` | `df[["a", "b"]]` |
| Mutate | `df.mutate(y=col("x") * 2)` | `df.assign(y=lambda d: d["x"]*2)` |
| Arrange | `df.arrange(desc("x"))` | `df.sort_values("x", ascending=False)` |
| Summarize | `df.summarize(m=mean("x"), by="g")` | `df.groupby("g").agg(...)` |
| Join | `df.left_join(df2, on="k")` | `df.merge(df2, on="k", how="left")` |
| Pivot long | `df.pivot_longer(cols=[...])` | `df.melt(id_vars=[...])` |
| Pivot wide | `df.pivot_wider(names_from=..., ...)` | `df.pivot_table(...)` |
| Distinct | `df.distinct("x")` | `df.drop_duplicates("x")` |
