.. toctree::
   :maxdepth: 2
   :hidden:

   getting_started
   comparisons/index
   guide/index
   api/index


.. raw:: html

   <div class="hero-section">
     <h1>tidypolars-extra</h1>
     <p class="tagline">Tidyverse-style data analysis in Python, powered by Polars</p>
     <p>
       <a href="https://pypi.org/project/tidypolars-extra/">
         <img src="https://img.shields.io/pypi/v/tidypolars-extra.svg" alt="PyPI version">
       </a>
       <a href="https://github.com/mdmanurung/tidypolars-extra/blob/main/LICENSE">
         <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
       </a>
       <a href="https://www.python.org/downloads/">
         <img src="https://img.shields.io/pypi/pyversions/tidypolars-extra.svg" alt="Python versions">
       </a>
     </p>
   </div>


**tidypolars-extra** brings the expressiveness of R's Tidyverse to Python, built on top of the
lightning-fast `Polars <https://pola.rs>`_ engine. Write familiar, readable data analysis code
without sacrificing performance.

.. raw:: html

   <div class="install-cmd">
     $ pip install tidypolars-extra
   </div>

----

Five Core Table Verbs
=====================

tidypolars-extra provides an intuitive, chainable API centered on five core verbs for data
manipulation — inspired by dplyr. Each verb does one thing well, and they compose together
to handle any data wrangling task.

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: **filter** — Pick rows
      :class-card: feature-card

      Keep only the rows that match your conditions.

      .. code-block:: python

         df.filter(col("species") == "Human",
                   col("height") > 170)

   .. grid-item-card:: **select** — Pick columns
      :class-card: feature-card

      Choose, rename, or reorder columns.

      .. code-block:: python

         df.select("name", "height", "mass")

         # With helpers
         df.select(starts_with("h"),
                   ends_with("color"))

   .. grid-item-card:: **mutate** — Create columns
      :class-card: feature-card

      Add new columns or transform existing ones.

      .. code-block:: python

         df.mutate(
             bmi=col("mass") / (col("height")/100)**2,
             is_tall=if_else(col("height") > 180,
                             "tall", "short")
         )

   .. grid-item-card:: **arrange** — Sort rows
      :class-card: feature-card

      Order rows by one or more columns.

      .. code-block:: python

         df.arrange("height")

         # Descending order
         df.arrange(desc("mass"))

   .. grid-item-card:: **summarize** — Aggregate
      :class-card: feature-card

      Collapse rows into summary statistics.

      .. code-block:: python

         df.summarize(
             avg_height=mean("height"),
             max_mass=max("mass"),
             n=n(),
             by="species"
         )

----

Quick Example
=============

.. code-block:: python

   import tidypolars_extra as tp
   from tidypolars_extra import col, desc, mean, n, if_else

   # Create a tibble
   df = tp.tibble(
       name=["Alice", "Bob", "Carol", "Dave", "Eve"],
       department=["Engineering", "Marketing", "Engineering", "Marketing", "Engineering"],
       salary=[95000, 72000, 88000, 65000, 102000],
       years=[5, 3, 7, 2, 10]
   )

   # Chain operations fluently
   result = (
       df
       .filter(col("salary") > 60000)
       .mutate(
           seniority=if_else(col("years") >= 5, "Senior", "Junior"),
           salary_k=col("salary") / 1000
       )
       .summarize(
           avg_salary=mean("salary"),
           headcount=n(),
           by="department"
       )
       .arrange(desc("avg_salary"))
   )

.. code-block:: text

   shape: (2, 3)
   ┌─────────────┬────────────┬───────────┐
   │ department  ┆ avg_salary ┆ headcount │
   │ ---         ┆ ---        ┆ ---       │
   │ str         ┆ f64        ┆ u32       │
   ╞═════════════╪════════════╪═══════════╡
   │ Engineering ┆ 95000.0    ┆ 3         │
   │ Marketing   ┆ 68500.0    ┆ 2         │
   └─────────────┴────────────┴───────────┘


----

Key Features
============

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: ⚡ Blazing Fast
      :class-card: feature-card

      Built on Polars — one of the fastest DataFrame libraries.
      Enjoy the speed of Rust with the comfort of Python.

   .. grid-item-card:: 🔗 Chainable API
      :class-card: feature-card

      Compose operations fluently with method chaining.
      No need for intermediate variables.

   .. grid-item-card:: 📊 Tidy Data
      :class-card: feature-card

      Rectangular tables, no multi-indexes, no surprises.
      One observation per row, one variable per column.

   .. grid-item-card:: 📝 Publication Ready
      :class-card: feature-card

      Export directly to LaTeX tables, Excel, CSV, and more.
      Built for academic and scientific workflows.

   .. grid-item-card:: 🧪 Scientific Toolkit
      :class-card: feature-card

      Descriptive statistics, frequency tables, crosstabs,
      and regression helpers included out of the box.

   .. grid-item-card:: 🔄 Interoperable
      :class-card: feature-card

      Convert seamlessly between tidypolars-extra, Pandas,
      and Polars DataFrames.

----

Syntax Comparison at a Glance
==============================

See how tidypolars-extra compares to Pandas and siuba for common operations:

.. tabs::

   .. tab:: tidypolars-extra

      .. code-block:: python

         import tidypolars_extra as tp
         from tidypolars_extra import col, mean, desc

         result = (
             df
             .filter(col("age") > 25)
             .mutate(score_pct=col("score") / 100)
             .summarize(avg=mean("score_pct"), by="group")
             .arrange(desc("avg"))
         )

   .. tab:: pandas

      .. code-block:: python

         import pandas as pd

         result = (
             df[df["age"] > 25]
             .assign(score_pct=lambda x: x["score"] / 100)
             .groupby("group")["score_pct"]
             .mean()
             .reset_index(name="avg")
             .sort_values("avg", ascending=False)
         )

   .. tab:: siuba

      .. code-block:: python

         from siuba import _, filter, mutate, group_by
         from siuba import summarize, arrange
         from siuba.dply.verbs import desc

         result = (
             df
             >> filter(_.age > 25)
             >> mutate(score_pct=_.score / 100)
             >> group_by("group")
             >> summarize(avg=_.score_pct.mean())
             >> arrange(desc(_.avg))
         )

👉 See :doc:`full syntax comparisons <comparisons/index>` for more examples.

----

.. grid:: 1 1 3 3
   :gutter: 3

   .. grid-item-card:: Getting Started
      :link: getting_started
      :link-type: doc
      :class-card: feature-card

      Install tidypolars-extra and write your first analysis in minutes.

   .. grid-item-card:: User Guide
      :link: guide/index
      :link-type: doc
      :class-card: feature-card

      In-depth guides on filtering, selecting, mutating, joining, reshaping, and more.

   .. grid-item-card:: API Reference
      :link: api/index
      :link-type: doc
      :class-card: feature-card

      Complete reference for every class, method, and function.
