
mutate — Create / Modify Columns
=================================

``mutate()`` creates new columns or modifies existing ones. It accepts keyword
arguments where the name is the output column and the value is an expression.

.. contents:: On this page
   :local:
   :depth: 2


Basic Usage
-----------

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    df = tp.tibble(
        name=["Alice", "Bob", "Carol"],
        salary=[95000, 72000, 88000],
        hours=[40, 35, 45],
    )

    # Add a new column
    df.mutate(hourly_rate=col("salary") / (col("hours") * 52))

    # Modify an existing column
    df.mutate(salary=col("salary") * 1.05)

    # Multiple columns at once
    df.mutate(
        bonus=col("salary") * 0.10,
        total_comp=col("salary") + col("salary") * 0.10,
    )


Conditional Logic
-----------------

Use ``case_when()`` and ``if_else()`` for conditional column creation:

.. code-block:: python

    # case_when: multiple conditions
    df.mutate(
        tier=tp.case_when(
            col("salary") >= 90000, "Senior",
            col("salary") >= 75000, "Mid",
            True, "Junior",
        )
    )

    # if_else: two outcomes
    df.mutate(
        overtime=tp.if_else(col("hours") > 40, "Yes", "No")
    )


Type Conversion
---------------

Convert column types inside ``mutate()``:

.. code-block:: python

    df.mutate(
        salary_str=tp.as_character("salary"),
        hours_float=tp.as_float("hours"),
    )


Grouped Mutate
--------------

Use ``by`` to compute group-level values while keeping all rows:

.. code-block:: python

    df = tp.tibble(
        dept=["Eng", "Eng", "Mktg", "Mktg"],
        name=["Alice", "Bob", "Carol", "Dave"],
        salary=[95000, 88000, 72000, 68000],
    )

    # Add group average as a new column
    df.mutate(dept_avg=tp.mean("salary"), by="dept")

    # Compute percentage of group total
    df.mutate(
        pct_of_dept=col("salary") / col("salary").sum() * 100,
        by="dept",
    )


Using across()
--------------

Apply a function to multiple columns at once:

.. code-block:: python

    df = tp.tibble(x=[1, 2, 3], y=[4, 5, 6], z=[7, 8, 9])

    # Scale all columns
    df.mutate(tp.across(["x", "y", "z"], lambda c: c / c.max(), suffix="_scaled"))


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.mutate(
                bonus=col("salary") * 0.10,
                level=tp.case_when(
                    col("salary") > 90000, "High",
                    True, "Normal",
                ),
            )

    .. tab-item:: pandas

        .. code-block:: python

            import numpy as np

            df.assign(
                bonus=lambda d: d["salary"] * 0.10,
                level=lambda d: np.where(d["salary"] > 90000, "High", "Normal"),
            )

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import _, mutate
            from siuba.dply.vector import if_else

            df >> mutate(
                bonus=_.salary * 0.10,
                level=if_else(_.salary > 90000, "High", "Normal"),
            )
