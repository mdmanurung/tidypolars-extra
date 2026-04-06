
summarize — Aggregate Data
==========================

``summarize()`` (or ``summarise()``) computes summary statistics from a tibble.
It is most powerful when combined with the ``by`` parameter for grouped
aggregation.

.. contents:: On this page
   :local:
   :depth: 2


Basic Usage
-----------

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    df = tp.tibble(
        department=["Eng", "Eng", "Mktg", "Mktg", "Eng"],
        name=["Alice", "Bob", "Carol", "Dave", "Eve"],
        salary=[95000, 88000, 72000, 68000, 102000],
        years=[5, 3, 7, 2, 10],
    )

    # Overall summary
    df.summarize(
        avg_salary=tp.mean("salary"),
        total_years=tp.sum("years"),
        n=tp.n(),
    )


Grouped Summarize
-----------------

Pass the ``by`` parameter to aggregate within groups:

.. code-block:: python

    df.summarize(
        avg_salary=tp.mean("salary"),
        max_years=tp.max("years"),
        headcount=tp.n(),
        by="department",
    )

Multiple grouping columns:

.. code-block:: python

    df2 = tp.tibble(
        region=["East", "East", "West", "West", "East"],
        department=["Eng", "Mktg", "Eng", "Mktg", "Eng"],
        revenue=[100, 80, 90, 70, 110],
    )

    df2.summarize(
        total_rev=tp.sum("revenue"),
        by=["region", "department"],
    )


Available Aggregation Functions
-------------------------------

tidypolars-extra provides many aggregation functions from the ``stats`` module:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Function
     - Description
   * - ``tp.mean(col)``
     - Arithmetic mean
   * - ``tp.median(col)``
     - Median
   * - ``tp.sum(col)``
     - Sum
   * - ``tp.min(col)``
     - Minimum
   * - ``tp.max(col)``
     - Maximum
   * - ``tp.sd(col)``
     - Standard deviation
   * - ``tp.var(col)``
     - Variance
   * - ``tp.n()``
     - Row count
   * - ``tp.n_distinct(col)``
     - Count of distinct values
   * - ``tp.first(col)``
     - First value
   * - ``tp.last(col)``
     - Last value
   * - ``tp.quantile(col, q)``
     - Quantile at fraction q


Counting
--------

Use ``count()`` as a shortcut for frequency tables:

.. code-block:: python

    df.count("department")

    # Equivalent to:
    df.summarize(n=tp.n(), by="department")


Comparison
----------

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

            from siuba import _, group_by, summarize
            from siuba.dply.verbs import n

            (
                df
                >> group_by(_.department)
                >> summarize(
                    avg_salary=_.salary.mean(),
                    headcount=n(_),
                )
            )
