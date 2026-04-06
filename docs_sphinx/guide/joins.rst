
Joins — Combine Tables
======================

tidypolars-extra supports the same join types as dplyr: ``left_join()``,
``inner_join()``, and ``full_join()``.

.. contents:: On this page
   :local:
   :depth: 2


Setup
-----

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    employees = tp.tibble(
        emp_id=[1, 2, 3, 4],
        name=["Alice", "Bob", "Carol", "Dave"],
        dept_id=[10, 20, 10, 30],
    )

    departments = tp.tibble(
        dept_id=[10, 20, 40],
        dept_name=["Engineering", "Marketing", "Sales"],
    )


left_join
---------

Keep all rows from the left table. Unmatched right rows become null:

.. code-block:: python

    employees.left_join(departments, by="dept_id")

Result keeps all 4 employees. Dave (dept_id=30) has null for ``dept_name``.
Sales (dept_id=40) is dropped because no employee belongs to it.


inner_join
----------

Keep only rows that match in both tables:

.. code-block:: python

    employees.inner_join(departments, by="dept_id")

Only Alice, Bob, and Carol are returned (dept_id 10 and 20 match).


full_join
---------

Keep all rows from both tables. Unmatched values become null:

.. code-block:: python

    employees.full_join(departments, by="dept_id")

All employees and all departments appear. Missing values are filled with null.


Joining on Multiple Keys
-------------------------

Pass a list of column names to ``by``:

.. code-block:: python

    left = tp.tibble(a=[1, 2], b=["x", "y"], val=[10, 20])
    right = tp.tibble(a=[1, 2], b=["x", "z"], info=["yes", "no"])

    left.left_join(right, by=["a", "b"])


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            employees.left_join(departments, by="dept_id")

    .. tab-item:: pandas

        .. code-block:: python

            employees.merge(departments, on="dept_id", how="left")

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import left_join
            employees >> left_join(_, departments, by="dept_id")
