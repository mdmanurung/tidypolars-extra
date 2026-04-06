# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
project = "tidypolars-extra"
copyright = "2024, tidypolars-extra contributors"
author = "Michael David Manurung"

try:
    from importlib.metadata import version as get_version

    release = get_version("tidypolars-extra")
except Exception:
    release = "0.1.0"

version = release

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "autoapi.extension",
    "sphinx_copybutton",
    "sphinx_design",
]

# MyST (Markdown) settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
]

# Napoleon settings (NumPy-style docstrings)
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False

# AutoAPI settings
autoapi_dirs = ["../tidypolars_extra"]
autoapi_type = "python"
autoapi_ignore = ["*/data/*", "*/reexports*"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_keep_files = False
autoapi_add_toctree_entry = True
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"

# Source settings
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Suppress expected warnings
suppress_warnings = [
    "autoapi.python_import_resolution",
    "ref.python",
]

# -- Options for HTML output -------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "github_url": "https://github.com/mdmanurung/tidypolars-extra",
    "show_prev_next": True,
    "navbar_align": "left",
    "navigation_with_keys": False,
    "show_toc_level": 2,
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/tidypolars-extra/",
            "icon": "fa-solid fa-box",
        },
    ],
}

html_context = {
    "github_user": "mdmanurung",
    "github_repo": "tidypolars-extra",
    "github_version": "main",
    "doc_path": "docs",
}

html_title = "tidypolars-extra"
html_short_title = "tidypolars-extra"
