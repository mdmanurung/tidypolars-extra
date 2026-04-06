
.. raw:: html

   <div class="hero-section">
     <h1>tidypolars-extra</h1>
     <p class="tagline">Tidyverse-style data analysis in Python, powered by Polars</p>
     <div class="badges">
       <a href="https://pypi.org/project/tidypolars-extra/">
         <img src="https://img.shields.io/pypi/v/tidypolars-extra.svg" alt="PyPI"/>
       </a>
       <a href="https://github.com/mdmanurung/tidypolars-extra/blob/main/LICENSE">
         <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"/>
       </a>
       <a href="https://www.python.org/downloads/">
         <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python"/>
       </a>
     </div>
     <div class="install-cmd">pip install tidypolars-extra</div>
     <div class="quick-links">
       <a href="guide/overview.html">Get Started</a>
       <a href="comparison.html" class="secondary">See Comparisons</a>
       <a href="api/index.html" class="secondary">API Reference</a>
     </div>
   </div>


**tidypolars-extra** brings the elegance of R's `Tidyverse <https://www.tidyverse.org/>`_
to Python, backed by the speed of `Polars <https://pola.rs/>`_. Write expressive,
readable data analysis code using familiar verbs like ``filter``, ``select``,
``mutate``, ``arrange``, and ``summarize``.

.. raw:: html

   <div class="section-header">
     <h2>Key Features</h2>
     <p>Why choose tidypolars-extra?</p>
   </div>

   <div class="feature-grid">
     <div class="feature-card">
       <h3>⚡ Blazing Fast</h3>
       <p>Built on Polars — one of the fastest DataFrame engines. Enjoy parallel execution, lazy evaluation, and GPU support under the hood.</p>
     </div>
     <div class="feature-card">
       <h3>🧹 Tidy by Design</h3>
       <p>Keep data in a clean rectangular format. No multi-indexes, no confusion — just tidy data frames you can chain and transform.</p>
     </div>
     <div class="feature-card">
       <h3>📖 Familiar Syntax</h3>
       <p>If you know dplyr, tidyr, stringr, or lubridate in R, you already know tidypolars-extra. Same verb names, same logic.</p>
     </div>
     <div class="feature-card">
       <h3>🔬 Built for Research</h3>
       <p>Designed for academic data analysis and publication. Generate LaTeX tables, handle survey data, read SPSS/Stata/R files natively.</p>
     </div>
     <div class="feature-card">
       <h3>🔗 Seamless Interop</h3>
       <p>Convert freely between tidypolars-extra, Polars, and pandas DataFrames. Use the right tool for each step of your pipeline.</p>
     </div>
     <div class="feature-card">
       <h3>🧰 Batteries Included</h3>
       <p>String manipulation (stringr), date handling (lubridate), statistics, type conversion, and column selection helpers — all built in.</p>
     </div>
   </div>


Five Core Table Verbs
=====================

At the heart of tidypolars-extra are five verbs for data transformation — the
same verbs that power dplyr in R:

.. raw:: html

   <div class="verb-grid">
     <div class="verb-card">
       <span class="verb-name">filter()</span>
       <span class="verb-desc">Keep rows that match conditions</span>
     </div>
     <div class="verb-card">
       <span class="verb-name">select()</span>
       <span class="verb-desc">Pick or rename columns</span>
     </div>
     <div class="verb-card">
       <span class="verb-name">mutate()</span>
       <span class="verb-desc">Create or modify columns</span>
     </div>
     <div class="verb-card">
       <span class="verb-name">arrange()</span>
       <span class="verb-desc">Sort rows by values</span>
     </div>
     <div class="verb-card">
       <span class="verb-name">summarize()</span>
       <span class="verb-desc">Aggregate grouped data</span>
     </div>
   </div>


Here's how they work together:

.. code-block:: python

    import tidypolars_extra as tp
    from tidypolars_extra import col

    # Create a tibble
    df = tp.tibble(
        name=["Alice", "Bob", "Carol", "Dave", "Eve"],
        department=["Engineering", "Marketing", "Engineering", "Marketing", "Engineering"],
        salary=[95000, 72000, 88000, 68000, 102000],
        years=[5, 3, 7, 2, 10],
    )

    # Chain the five core verbs
    result = (
        df
        .filter(col("salary") > 70000)              # keep high earners
        .mutate(bonus=col("salary") * 0.1)           # add bonus column
        .select("name", "department", "salary", "bonus")  # pick columns
        .arrange(tp.desc("salary"))                  # sort descending
    )

    # Grouped summarize
    summary = (
        df
        .summarize(
            avg_salary=tp.mean("salary"),
            total_years=tp.sum("years"),
            n=tp.n(),
            by="department",
        )
    )


Quick Comparison
================

.. tab-set::

    .. tab-item:: tidypolars-extra

        .. code-block:: python

            import tidypolars_extra as tp
            from tidypolars_extra import col

            result = (
                df
                .filter(col("age") > 25)
                .mutate(senior=col("years") > 5)
                .select("name", "department", "senior")
                .arrange(tp.desc("name"))
                .summarize(count=tp.n(), by="department")
            )

    .. tab-item:: pandas

        .. code-block:: python

            import pandas as pd

            result = (
                df
                .query("age > 25")
                .assign(senior=lambda d: d["years"] > 5)
                .filter(["name", "department", "senior"])
                .sort_values("name", ascending=False)
                .groupby("department")
                .agg(count=("name", "count"))
                .reset_index()
            )

    .. tab-item:: siuba

        .. code-block:: python

            from siuba import _, filter, mutate, select, arrange, summarize, group_by
            from siuba.dply.verbs import n

            result = (
                df
                >> filter(_.age > 25)
                >> mutate(senior=_.years > 5)
                >> select(_.name, _.department, _.senior)
                >> arrange(-_.name)
                >> group_by(_.department)
                >> summarize(count=n(_))
            )


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents

   guide/overview
   guide/filter
   guide/select
   guide/mutate
   guide/arrange
   guide/summarize
   guide/joins
   guide/reshape
   comparison
   api/index
