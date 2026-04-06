
Syntax Comparison
=================

This page shows side-by-side comparisons of common data manipulation tasks across
**tidypolars-extra**, **pandas**, and **siuba**. All examples assume the following setup:

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            import tidypolars_extra as tp
            from tidypolars_extra import col

            df = tp.tibble(
                name=["Alice", "Bob", "Carol", "Dave", "Eve"],
                department=["Eng", "Mktg", "Eng", "Mktg", "Eng"],
                salary=[95000, 72000, 88000, 68000, 102000],
                years=[5, 3, 7, 2, 10],
                active=[True, True, False, True, True],
            )

    .. tab-item:: pandas

        .. code-block:: python

            import pandas as pd

            df = pd.DataFrame({
                "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
                "department": ["Eng", "Mktg", "Eng", "Mktg", "Eng"],
                "salary": [95000, 72000, 88000, 68000, 102000],
                "years": [5, 3, 7, 2, 10],
                "active": [True, True, False, True, True],
            })

    .. tab-item:: siuba

        .. code-block:: python

            import pandas as pd
            from siuba import _, filter, mutate, select, arrange
            from siuba import summarize, group_by

            df = pd.DataFrame({
                "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
                "department": ["Eng", "Mktg", "Eng", "Mktg", "Eng"],
                "salary": [95000, 72000, 88000, 68000, 102000],
                "years": [5, 3, 7, 2, 10],
                "active": [True, True, False, True, True],
            })


Filtering Rows
--------------

Keep rows where salary exceeds 80,000 and the employee is active.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.filter(col("salary") > 80000, col("active") == True)

    .. tab-item:: pandas

        .. code-block:: python

            df.query("salary > 80000 and active == True")

    .. tab-item:: siuba

        .. code-block:: python

            df >> filter(_.salary > 80000, _.active == True)


Selecting Columns
-----------------

Pick specific columns or use helpers.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            # By name
            df.select("name", "salary")

            # With helpers
            df.select(tp.starts_with("s"), tp.contains("name"))

    .. tab-item:: pandas

        .. code-block:: python

            # By name
            df[["name", "salary"]]

            # With filter
            df.filter(regex="^s|name")

    .. tab-item:: siuba

        .. code-block:: python

            # By name
            df >> select(_.name, _.salary)

            # siuba supports tidyselect-style helpers too
            df >> select(_.startswith("s"))


Adding / Modifying Columns
--------------------------

Create new columns or transform existing ones.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.mutate(
                bonus=col("salary") * 0.10,
                experience=tp.case_when(
                    col("years") >= 5, "Senior",
                    True, "Junior",
                ),
            )

    .. tab-item:: pandas

        .. code-block:: python

            df.assign(
                bonus=lambda d: d["salary"] * 0.10,
                experience=lambda d: d["years"].apply(
                    lambda y: "Senior" if y >= 5 else "Junior"
                ),
            )

    .. tab-item:: siuba

        .. code-block:: python

            from siuba.dply.vector import if_else

            df >> mutate(
                bonus=_.salary * 0.10,
                experience=if_else(_.years >= 5, "Senior", "Junior"),
            )


Sorting Rows
------------

Sort by salary descending, then by name ascending.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.arrange(tp.desc("salary"), "name")

    .. tab-item:: pandas

        .. code-block:: python

            df.sort_values(["salary", "name"], ascending=[False, True])

    .. tab-item:: siuba

        .. code-block:: python

            df >> arrange(-_.salary, _.name)


Grouped Summarize
-----------------

Compute summary statistics by group.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.summarize(
                avg_salary=tp.mean("salary"),
                headcount=tp.n(),
                by="department",
            )

    .. tab-item:: pandas

        .. code-block:: python

            (
                df
                .groupby("department")
                .agg(
                    avg_salary=("salary", "mean"),
                    headcount=("salary", "count"),
                )
                .reset_index()
            )

    .. tab-item:: siuba

        .. code-block:: python

            from siuba.dply.verbs import n

            (
                df
                >> group_by(_.department)
                >> summarize(
                    avg_salary=_.salary.mean(),
                    headcount=n(_),
                )
            )


Joins
-----

Combine two tables using a left join.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            dept_info = tp.tibble(
                department=["Eng", "Mktg"],
                budget=[500000, 300000],
            )

            df.left_join(dept_info, by="department")

    .. tab-item:: pandas

        .. code-block:: python

            dept_info = pd.DataFrame({
                "department": ["Eng", "Mktg"],
                "budget": [500000, 300000],
            })

            df.merge(dept_info, on="department", how="left")

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import left_join

            dept_info = pd.DataFrame({
                "department": ["Eng", "Mktg"],
                "budget": [500000, 300000],
            })

            df >> left_join(_, dept_info, by="department")


Reshaping: Pivot Longer
-----------------------

Convert wide data to long format.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            wide = tp.tibble(id=[1, 2], score_a=[90, 85], score_b=[80, 95])

            wide.pivot_longer(cols=["score_a", "score_b"],
                              names_to="test", values_to="score")

    .. tab-item:: pandas

        .. code-block:: python

            wide = pd.DataFrame({"id": [1, 2], "score_a": [90, 85], "score_b": [80, 95]})

            wide.melt(id_vars="id", value_vars=["score_a", "score_b"],
                      var_name="test", value_name="score")

    .. tab-item:: siuba

        .. code-block:: python

            # siuba relies on pandas melt under the hood
            wide.melt(id_vars="id", value_vars=["score_a", "score_b"],
                      var_name="test", value_name="score")


Reshaping: Pivot Wider
----------------------

Convert long data to wide format.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            long = tp.tibble(
                name=["Alice", "Alice", "Bob", "Bob"],
                metric=["height", "weight", "height", "weight"],
                value=[165, 60, 180, 80],
            )

            long.pivot_wider(names_from="metric", values_from="value")

    .. tab-item:: pandas

        .. code-block:: python

            long = pd.DataFrame({
                "name": ["Alice", "Alice", "Bob", "Bob"],
                "metric": ["height", "weight", "height", "weight"],
                "value": [165, 60, 180, 80],
            })

            long.pivot_table(index="name", columns="metric",
                             values="value", aggfunc="first").reset_index()

    .. tab-item:: siuba

        .. code-block:: python

            # Use pandas pivot_table
            long.pivot_table(index="name", columns="metric",
                             values="value", aggfunc="first").reset_index()


String Operations
-----------------

Pattern matching and string manipulation.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.mutate(
                upper_name=tp.str_to_upper("name"),
                is_eng=tp.str_detect("department", "Eng"),
                short_name=tp.str_sub("name", 0, 3),
            )

    .. tab-item:: pandas

        .. code-block:: python

            df.assign(
                upper_name=lambda d: d["name"].str.upper(),
                is_eng=lambda d: d["department"].str.contains("Eng"),
                short_name=lambda d: d["name"].str[:3],
            )

    .. tab-item:: siuba

        .. code-block:: python

            df >> mutate(
                upper_name=_.name.str.upper(),
                is_eng=_.department.str.contains("Eng"),
                short_name=_.name.str[:3],
            )


Chained Pipeline
----------------

A full pipeline combining multiple operations.

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            result = (
                df
                .filter(col("active") == True)
                .mutate(
                    bonus=col("salary") * 0.10,
                    seniority=tp.case_when(
                        col("years") >= 7, "Senior",
                        col("years") >= 3, "Mid",
                        True, "Junior",
                    ),
                )
                .select("name", "department", "seniority", "bonus")
                .arrange(tp.desc("bonus"))
                .summarize(
                    avg_bonus=tp.mean("bonus"),
                    count=tp.n(),
                    by="seniority",
                )
            )

    .. tab-item:: pandas

        .. code-block:: python

            import numpy as np

            result = (
                df
                .query("active == True")
                .assign(
                    bonus=lambda d: d["salary"] * 0.10,
                    seniority=lambda d: np.select(
                        [d["years"] >= 7, d["years"] >= 3],
                        ["Senior", "Mid"],
                        default="Junior",
                    ),
                )
                .filter(["name", "department", "seniority", "bonus"])
                .sort_values("bonus", ascending=False)
                .groupby("seniority")
                .agg(avg_bonus=("bonus", "mean"), count=("bonus", "count"))
                .reset_index()
            )

    .. tab-item:: siuba

        .. code-block:: python

            from siuba.dply.vector import case_when, n

            result = (
                df
                >> filter(_.active == True)
                >> mutate(
                    bonus=_.salary * 0.10,
                    seniority=case_when({
                        _.years >= 7: "Senior",
                        _.years >= 3: "Mid",
                        True: "Junior",
                    }),
                )
                >> select(_.name, _.department, _.seniority, _.bonus)
                >> arrange(-_.bonus)
                >> group_by(_.seniority)
                >> summarize(avg_bonus=_.bonus.mean(), count=n(_))
            )
