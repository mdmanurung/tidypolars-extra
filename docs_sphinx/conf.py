# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "tidypolars-extra"
copyright = "2024, Michael David Manurung"
author = "Michael David Manurung"
release = "0.0.1.22"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for autodoc -----------------------------------------------------

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

# Napoleon settings for NumPy-style docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

html_theme_options = {
    "logo": {
        "text": "tidypolars-extra",
    },
    "github_url": "https://github.com/mdmanurung/tidypolars-extra",
    "show_toc_level": 2,
    "navbar_align": "left",
    "navigation_with_keys": False,
    "header_links_before_dropdown": 6,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/tidypolars-extra/",
            "icon": "fa-solid fa-box",
        },
    ],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
}

html_sidebars = {
    "index": [],
    "comparison": [],
}

html_context = {
    "github_user": "mdmanurung",
    "github_repo": "tidypolars-extra",
    "github_version": "main",
    "doc_path": "docs_sphinx",
}

# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "polars": ("https://docs.pola.rs/api/python/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]
