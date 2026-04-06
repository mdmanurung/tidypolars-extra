
API Reference
=============

Complete reference for all tidypolars-extra modules.

.. contents:: Modules
   :local:
   :depth: 1


Tibble — Core DataFrame
-----------------------

The ``tibble`` class extends ``polars.DataFrame`` with tidyverse-style methods
for data manipulation.

.. currentmodule:: tidypolars_extra.tibble_df

.. autoclass:: tibble
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: _repr_html_, __init__, __copy__, __getattribute__, __dir__

.. autoclass:: TibbleGroupBy
   :members:
   :show-inheritance:


Special Functions
-----------------

Conditional logic, null handling, membership tests, and window functions.

.. currentmodule:: tidypolars_extra.funs

.. autofunction:: if_else
.. autofunction:: case_when
.. autofunction:: coalesce
.. autofunction:: between
.. autofunction:: is_in
.. autofunction:: is_not_in
.. autofunction:: is_null
.. autofunction:: is_not_null
.. autofunction:: is_not
.. autofunction:: is_finite
.. autofunction:: is_infinite
.. autofunction:: lead
.. autofunction:: replace_null
.. autofunction:: round
.. autofunction:: row_number
.. autofunction:: n_distinct
.. autofunction:: rep
.. autofunction:: map


Statistics
----------

Aggregation and statistical functions for use inside ``summarize()`` and
``mutate()``.

.. currentmodule:: tidypolars_extra.stats

.. autofunction:: mean
.. autofunction:: median
.. autofunction:: sum
.. autofunction:: min
.. autofunction:: max
.. autofunction:: sd
.. autofunction:: var
.. autofunction:: quantile
.. autofunction:: n
.. autofunction:: count
.. autofunction:: first
.. autofunction:: last
.. autofunction:: length
.. autofunction:: abs
.. autofunction:: sqrt
.. autofunction:: log
.. autofunction:: log10
.. autofunction:: floor
.. autofunction:: cor
.. autofunction:: cov
.. autofunction:: rank
.. autofunction:: scale


String Functions (stringr)
--------------------------

R-style string manipulation functions.

.. currentmodule:: tidypolars_extra.stringr

.. autofunction:: paste
.. autofunction:: paste0
.. autofunction:: str_c
.. autofunction:: str_detect
.. autofunction:: str_extract
.. autofunction:: str_starts
.. autofunction:: str_ends
.. autofunction:: str_replace
.. autofunction:: str_replace_all
.. autofunction:: str_remove
.. autofunction:: str_remove_all
.. autofunction:: str_length
.. autofunction:: str_sub
.. autofunction:: str_to_lower
.. autofunction:: str_to_upper
.. autofunction:: str_trim
.. autofunction:: str_wrap


Date/Time Functions (lubridate)
-------------------------------

Date and time extraction and creation functions.

.. currentmodule:: tidypolars_extra.lubridate

.. autofunction:: as_date
.. autofunction:: as_datetime
.. autofunction:: make_date
.. autofunction:: make_datetime
.. autofunction:: year
.. autofunction:: month
.. autofunction:: mday
.. autofunction:: wday
.. autofunction:: yday
.. autofunction:: week
.. autofunction:: quarter
.. autofunction:: hour
.. autofunction:: minute
.. autofunction:: second
.. autofunction:: dt_round


Column Selection Helpers
------------------------

Tidyselect-style helpers for flexible column selection inside ``select()``
and other verbs.

.. currentmodule:: tidypolars_extra.helpers

.. autofunction:: starts_with
.. autofunction:: ends_with
.. autofunction:: contains
.. autofunction:: matches
.. autofunction:: everything
.. autofunction:: where
.. autofunction:: desc
.. autofunction:: across
.. autofunction:: lag


Type Conversion
---------------

Functions for casting column types.

.. currentmodule:: tidypolars_extra.type_conversion

.. autofunction:: as_integer
.. autofunction:: as_float
.. autofunction:: as_character
.. autofunction:: as_string
.. autofunction:: as_boolean
.. autofunction:: as_logical
.. autofunction:: as_factor
.. autofunction:: as_categorical
.. autofunction:: cast


I/O — Reading and Writing Data
-------------------------------

Functions for reading data from various file formats.

.. currentmodule:: tidypolars_extra.io

.. autoclass:: read_data
   :members:
   :show-inheritance:


Re-exports from Polars
----------------------

These are re-exported directly from Polars for convenience:

.. currentmodule:: tidypolars_extra.reexports

- ``col`` — Column reference expression
- ``lit`` — Literal value expression
- ``exclude`` — Exclude columns
- ``Expr`` — Expression type
- ``Series`` — Series type
- ``element`` — Element expression (for lists)
- Data types: ``Int8``, ``Int16``, ``Int32``, ``Int64``, ``UInt8``, ``UInt16``,
  ``UInt32``, ``UInt64``, ``Float32``, ``Float64``, ``Boolean``, ``Utf8``,
  ``List``, ``Date``, ``Datetime``, ``Object``


Built-in Datasets
-----------------

.. currentmodule:: tidypolars_extra.data

Pre-loaded tibbles available for practice and examples:

.. code-block:: python

    from tidypolars_extra.data import mtcars, diamonds, starwars, vote

- **mtcars** — Motor Trend car road tests (32 × 11)
- **diamonds** — Diamond prices and characteristics
- **starwars** — Star Wars characters (87 × 14)
- **vote** — Voting dataset
