API Reference
=============

Complete reference for all classes, methods, and functions in tidypolars-extra.

.. toctree::
   :maxdepth: 2

   tibble
   functions
   helpers
   statistics
   strings
   dates
   type_conversion
   io


Core Class
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Description
   * - :doc:`tibble <tibble>`
     - Enhanced DataFrame with Tidyverse-style methods

Core One-table Verbs
--------------------

Available as methods on the :class:`~tidypolars_extra.tibble_df.tibble` class:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``filter(*args, by=None)``
     - Keep rows that match conditions
   * - ``select(*args)``
     - Keep or rename specific columns
   * - ``mutate(*args, by=None, **kwargs)``
     - Add or modify columns
   * - ``arrange(*args)``
     - Sort rows by columns
   * - ``summarize(*args, by=None, **kwargs)``
     - Aggregate rows into summaries

Other One-table Verbs
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``distinct(*args, keep_all=False)``
     - Select distinct/unique rows
   * - ``count(*args, sort=False, name='n')``
     - Count rows by group
   * - ``slice(*args, by=None)``
     - Select rows by position
   * - ``slice_head(n=5, *, by=None)``
     - Grab first n rows
   * - ``slice_tail(n=5, *, by=None)``
     - Grab last n rows
   * - ``rename(*args, **kwargs)``
     - Rename columns
   * - ``relocate(*args, before=None, after=None)``
     - Move columns to new position
   * - ``drop(*args)``
     - Drop columns
   * - ``pull(var=None)``
     - Extract a column as Series

Two-table Verbs
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``left_join(df, on=..., ...)``
     - Keep all left rows, add matching right columns
   * - ``inner_join(df, on=..., ...)``
     - Keep only rows that match in both tables
   * - ``full_join(df, on=..., ...)``
     - Keep all rows from both tables
   * - ``bind_rows(*args)``
     - Stack DataFrames vertically
   * - ``bind_cols(*args)``
     - Stack DataFrames horizontally

Tidy Verbs
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``pivot_longer(cols=..., names_to=..., values_to=...)``
     - Reshape from wide to long format
   * - ``pivot_wider(names_from=..., values_from=...)``
     - Reshape from long to wide format
   * - ``separate(sep_col, into, sep=...)``
     - Split one column into multiple
   * - ``unite(col=..., unite_cols=..., sep=...)``
     - Combine multiple columns into one
   * - ``nest(by)``
     - Create nested DataFrames
   * - ``unnest(col)``
     - Expand nested DataFrames
   * - ``crossing(*args, **kwargs)``
     - Generate all combinations

Functional API
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Description
   * - :doc:`functions <functions>`
     - Conditional logic, predicates, and utilities
   * - :doc:`helpers <helpers>`
     - Column selection helpers and ``across()``
   * - :doc:`statistics <statistics>`
     - Statistical and mathematical functions
   * - :doc:`strings <strings>`
     - String manipulation (stringr-style)
   * - :doc:`dates <dates>`
     - Date/time operations (lubridate-style)
   * - :doc:`type_conversion <type_conversion>`
     - Type casting functions
   * - :doc:`io <io>`
     - Data I/O and file reading
