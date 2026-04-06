
arrange — Sort Rows
===================

``arrange()`` sorts rows by one or more columns. By default, sorting is ascending.
Use ``desc()`` for descending order.

.. contents:: On this page
   :local:
   :depth: 2


Basic Usage
-----------

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    df = tp.tibble(
        name=["Carol", "Alice", "Bob", "Dave"],
        score=[88, 95, 72, 95],
        age=[35, 30, 25, 28],
    )

    # Ascending (default)
    df.arrange("score")

    # Descending
    df.arrange(tp.desc("score"))


Multiple Columns
----------------

Sort by multiple columns. Earlier columns take priority:

.. code-block:: python

    # Sort by score descending, then by name ascending (alphabetical tiebreaker)
    df.arrange(tp.desc("score"), "name")


Comparison
----------

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            df.arrange(tp.desc("score"), "name")

    .. tab-item:: pandas

        .. code-block:: python

            df.sort_values(["score", "name"], ascending=[False, True])

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import _, arrange
            df >> arrange(-_.score, _.name)
