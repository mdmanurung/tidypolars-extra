# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root to path so autodoc can find the package
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
project = "tidypolars-extra"
copyright = "2024, Michael David Manurung"
author = "Michael David Manurung"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "myst_parser",
]

# MyST-Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Source file suffixes
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for autodoc -----------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "groupwise",
}
autodoc_typehints = "description"
autosummary_generate = True

# Napoleon settings for NumPy-style docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/mdmanurung/tidypolars-extra",
    "logo": {
        "text": "tidypolars-extra",
    },
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navigation_with_keys": True,
    "show_prev_next": True,
    "header_links_before_dropdown": 6,
    "primary_sidebar_end": [],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    "pygments_light_style": "friendly",
    "pygments_dark_style": "monokai",
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_sidebars = {
    "index": [],
    "**": ["sidebar-nav-bs"],
}

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "polars": ("https://docs.pola.rs/api/python/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# -- Copy button configuration -----------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: "
copybutton_prompt_is_regexp = True
