
select — Pick Columns
=====================

``select()`` picks, renames, or reorders columns. It supports column names,
lists, dictionaries (for renaming), regex patterns, and tidyselect helpers.

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
        age=[30, 25, 35],
        salary=[95000, 72000, 88000],
        department=["Eng", "Mktg", "Eng"],
    )

    # Select by name
    df.select("name", "salary")

    # Select and rename
    df.select({"name": "employee_name", "salary": "pay"})


Tidyselect Helpers
------------------

tidypolars-extra provides the same column selection helpers as R's tidyselect:

.. code-block:: python

    # Columns starting with "s"
    df.select(tp.starts_with("s"))

    # Columns ending with "ary"
    df.select(tp.ends_with("ary"))

    # Columns containing "al"
    df.select(tp.contains("al"))

    # Columns matching a regex
    df.select(tp.matches(r"^(name|age)$"))

    # All columns
    df.select(tp.everything())

    # Columns by type
    df.select(tp.where("numeric"))
    df.select(tp.where("string"))


Dropping Columns
----------------

Use ``drop()`` to remove columns instead of selecting them:

.. code-block:: python

    df.drop("age", "department")


Reordering with relocate
-------------------------

Move columns to a new position:

.. code-block:: python

    # Move department to the front
    df.relocate("department")

    # Move salary after name
    df.relocate("salary", after="name")

    # Move age before department
    df.relocate("age", before="department")


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.select("name", tp.starts_with("s"))

    .. tab-item:: pandas

        .. code-block:: python

            df[["name"] + [c for c in df.columns if c.startswith("s")]]

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import _, select
            df >> select(_.name, _.startswith("s"))
