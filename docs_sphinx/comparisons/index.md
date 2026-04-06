# Syntax Comparisons

See how tidypolars-extra compares to **pandas** and **siuba** for common data analysis tasks.
All three libraries can accomplish the same goals — the difference is in readability and
expressiveness.

```{toctree}
:maxdepth: 2

vs_pandas
vs_siuba
```

## Philosophy

tidypolars-extra adopts the Tidyverse approach:

- **Verb-based API** — each function does one thing (`filter`, `select`, `mutate`, `arrange`, `summarize`)
- **Method chaining** — compose operations fluently without intermediate variables
- **Consistent interface** — every verb takes a DataFrame and returns a DataFrame
- **Powered by Polars** — get the ergonomics of dplyr with the speed of Rust

## At a Glance

````{tabs}
```{tab} tidypolars-extra
\`\`\`python
import tidypolars_extra as tp
from tidypolars_extra import col, mean, desc

(df
 .filter(col("age") > 30)
 .select("name", "age", "score")
 .mutate(grade=col("score") / 100)
 .arrange(desc("grade")))
\`\`\`
```

```{tab} pandas
\`\`\`python
import pandas as pd

(df
 .query("age > 30")
 [["name", "age", "score"]]
 .assign(grade=lambda x: x["score"] / 100)
 .sort_values("grade", ascending=False))
\`\`\`
```

```{tab} siuba
\`\`\`python
from siuba import _, filter, select, mutate, arrange
from siuba.dply.verbs import desc

(df
 >> filter(_.age > 30)
 >> select(_.name, _.age, _.score)
 >> mutate(grade=_.score / 100)
 >> arrange(desc(_.grade)))
\`\`\`
```
````
