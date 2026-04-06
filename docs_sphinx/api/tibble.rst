tibble
======

The ``tibble`` class is the core data structure in tidypolars-extra — an enhanced
Polars DataFrame with Tidyverse-style methods.

.. autoclass:: tidypolars_extra.tibble_df.tibble
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :exclude-members: __init__, __repr__, __str__, __eq__, __ne__

Constructor
-----------

.. automethod:: tidypolars_extra.tibble_df.tibble.__init__

Conversion Functions
--------------------

.. autofunction:: tidypolars_extra.tibble_df.from_polars

.. autofunction:: tidypolars_extra.tibble_df.from_pandas

TibbleGroupBy
-------------

.. autoclass:: tidypolars_extra.tibble_df.TibbleGroupBy
   :members:
   :undoc-members:
   :show-inheritance:
