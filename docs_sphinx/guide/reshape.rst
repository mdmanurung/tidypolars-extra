
Reshaping — Pivot Longer & Wider
================================

tidypolars-extra provides ``pivot_longer()`` and ``pivot_wider()`` for
converting between wide and long data formats, just like tidyr in R.

.. contents:: On this page
   :local:
   :depth: 2


pivot_longer — Wide to Long
----------------------------

Convert columns into rows. Use this when column names contain data values.

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    wide = tp.tibble(
        student=["Alice", "Bob"],
        math=[90, 85],
        science=[88, 92],
        english=[95, 78],
    )

    long = wide.pivot_longer(
        cols=["math", "science", "english"],
        names_to="subject",
        values_to="score",
    )

Result:

.. code-block:: text

    shape: (6, 3)
    ┌─────────┬─────────┬───────┐
    │ student ┆ subject ┆ score │
    │ ---     ┆ ---     ┆ ---   │
    │ str     ┆ str     ┆ i64   │
    ╞═════════╪═════════╪═══════╡
    │ Alice   ┆ math    ┆ 90    │
    │ Alice   ┆ science ┆ 88    │
    │ Alice   ┆ english ┆ 95    │
    │ Bob     ┆ math    ┆ 85    │
    │ Bob     ┆ science ┆ 92    │
    │ Bob     ┆ english ┆ 78    │
    └─────────┴─────────┴───────┘


pivot_wider — Long to Wide
---------------------------

Spread a key-value pair across columns. The inverse of ``pivot_longer()``.

.. code-block:: python

    wide_again = long.pivot_wider(
        names_from="subject",
        values_from="score",
    )


A More Realistic Example
-------------------------

Survey data often arrives in long format:

.. code-block:: python

    survey = tp.tibble(
        respondent=["R1", "R1", "R1", "R2", "R2", "R2"],
        question=["q1", "q2", "q3", "q1", "q2", "q3"],
        answer=[5, 3, 4, 4, 5, 2],
    )

    # Spread to one column per question
    survey.pivot_wider(names_from="question", values_from="answer")


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            wide.pivot_longer(
                cols=["math", "science", "english"],
                names_to="subject",
                values_to="score",
            )

    .. tab-item:: pandas

        .. code-block:: python

            wide.melt(
                id_vars="student",
                value_vars=["math", "science", "english"],
                var_name="subject",
                value_name="score",
            )

    .. tab-item:: siuba

        .. code-block:: python

            # siuba relies on pandas melt/pivot
            wide.melt(
                id_vars="student",
                value_vars=["math", "science", "english"],
                var_name="subject",
                value_name="score",
            )
