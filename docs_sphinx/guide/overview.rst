
User Guide
==========

Welcome to the tidypolars-extra user guide. This section walks through the core
verbs and concepts, with runnable examples.

.. contents:: On this page
   :local:
   :depth: 2

Installation
------------

Install from PyPI:

.. code-block:: bash

    pip install tidypolars-extra

Import convention:

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col, lit


Creating Data
-------------

Create a ``tibble`` — tidypolars-extra's enhanced DataFrame — using keyword
arguments (like R's ``tibble()``):

.. code-block:: python

    df = tp.tibble(
        name=["Alice", "Bob", "Carol", "Dave"],
        age=[30, 25, 35, 28],
        score=[88.5, 92.0, 79.5, 95.0],
    )
    df

You can also convert from pandas or Polars:

.. code-block:: python

    import pandas as pd
    import polars as pl

    # From pandas
    pdf = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    df = tp.from_pandas(pdf)

    # From polars
    pldf = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    df = tp.from_polars(pldf)


The Verbs
---------

tidypolars-extra provides five core verbs for data transformation, mirroring
R's dplyr:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Verb
     - Purpose
     - Example
   * - ``filter()``
     - Keep rows that match conditions
     - ``df.filter(col("age") > 25)``
   * - ``select()``
     - Pick, rename, or reorder columns
     - ``df.select("name", "age")``
   * - ``mutate()``
     - Create or modify columns
     - ``df.mutate(age2=col("age") ** 2)``
   * - ``arrange()``
     - Sort rows
     - ``df.arrange(tp.desc("score"))``
   * - ``summarize()``
     - Aggregate data (often grouped)
     - ``df.summarize(avg=tp.mean("score"), by="dept")``


Beyond these five, tidypolars-extra also provides:

- **Reshaping**: ``pivot_longer()``, ``pivot_wider()``
- **Joins**: ``left_join()``, ``inner_join()``, ``full_join()``
- **Row operations**: ``slice()``, ``slice_head()``, ``slice_tail()``, ``distinct()``
- **Column operations**: ``rename()``, ``relocate()``, ``drop()``, ``unite()``, ``separate()``
- **Missing values**: ``drop_null()``, ``fill()``, ``replace_null()``
- **String tools**: ``str_detect()``, ``str_replace()``, ``str_to_upper()``, and more
- **Date tools**: ``year()``, ``month()``, ``as_date()``, and more
- **Statistics**: ``mean()``, ``sd()``, ``cor()``, ``rank()``, and more


Working with Expressions
------------------------

tidypolars-extra uses Polars expressions (``col``, ``lit``) for column references
inside verbs:

.. code-block:: python

    from tidypolars_extra import col, lit

    # col() refers to a column
    df.filter(col("age") > 30)

    # lit() creates a literal value
    df.mutate(constant=lit(100))

    # Expressions can be composed
    df.mutate(
        score_pct=col("score") / col("score").max() * 100,
        label=tp.case_when(
            col("score") > 90, "A",
            col("score") > 80, "B",
            True, "C",
        ),
    )


Grouping
--------

Many verbs accept a ``by`` parameter for grouped operations — no need to call
``group_by()`` separately:

.. code-block:: python

    df = tp.tibble(
        dept=["Eng", "Eng", "Mktg", "Mktg"],
        name=["Alice", "Bob", "Carol", "Dave"],
        salary=[95000, 88000, 72000, 68000],
    )

    # Grouped summarize
    df.summarize(avg=tp.mean("salary"), by="dept")

    # Grouped mutate (add group-level stats per row)
    df.mutate(dept_avg=tp.mean("salary"), by="dept")

    # Grouped filter
    df.filter(col("salary") == col("salary").max(), by="dept")


Method Chaining
---------------

All verbs return a ``tibble``, so you can chain them fluently:

.. code-block:: python

    result = (
        df
        .filter(col("salary") > 70000)
        .mutate(bonus=col("salary") * 0.10)
        .select("name", "dept", "bonus")
        .arrange(tp.desc("bonus"))
    )


Column Selection Helpers
------------------------

tidypolars-extra includes tidyselect-style helpers for flexible column selection:

.. code-block:: python

    # Select columns that start with "score"
    df.select(tp.starts_with("score"))

    # Select columns containing "name"
    df.select(tp.contains("name"))

    # Select by regex
    df.select(tp.matches(r"^s\w+"))

    # Select by data type
    df.select(tp.where("numeric"))

    # Combine with everything()
    df.select("id", tp.everything())


Next Steps
----------

Explore each verb in detail:

.. toctree::
   :maxdepth: 1

   filter
   select
   mutate
   arrange
   summarize
   joins
   reshape
