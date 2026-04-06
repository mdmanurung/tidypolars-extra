
filter — Keep Rows
==================

``filter()`` keeps rows that match one or more conditions. Multiple conditions
are combined with AND logic.

.. contents:: On this page
   :local:
   :depth: 2


Basic Usage
-----------

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    df = tp.tibble(
        name=["Alice", "Bob", "Carol", "Dave", "Eve"],
        age=[30, 25, 35, 28, 42],
        department=["Eng", "Mktg", "Eng", "Mktg", "Eng"],
        salary=[95000, 72000, 88000, 68000, 102000],
    )

    # Single condition
    df.filter(col("age") > 30)

    # Multiple conditions (AND)
    df.filter(col("age") > 25, col("department") == "Eng")


String Conditions
-----------------

Use Polars string expressions inside ``filter()``:

.. code-block:: python

    # Names containing "a" (case-sensitive)
    df.filter(col("name").str.contains("a"))

    # Department starts with "Eng"
    df.filter(col("name").str.starts_with("A"))


Using Helper Functions
----------------------

.. code-block:: python

    # Check membership
    df.filter(tp.is_in("department", ["Eng", "Sales"]))

    # Check for nulls
    df.filter(tp.is_not_null("salary"))

    # Between
    df.filter(tp.between("age", 25, 35))


Grouped Filter
--------------

Use the ``by`` parameter to filter within groups:

.. code-block:: python

    # Keep the highest earner in each department
    df.filter(col("salary") == col("salary").max(), by="department")


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.filter(col("age") > 30, col("salary") > 80000)

    .. tab-item:: pandas

        .. code-block:: python

            df.query("age > 30 and salary > 80000")

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import _, filter
            df >> filter(_.age > 30, _.salary > 80000)
