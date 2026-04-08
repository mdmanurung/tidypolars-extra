# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
project = "tidypolars-extra"
copyright = "2024, tidypolars-extra contributors"
author = "Mikhael Dito Manurung"

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
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "source_repository": "https://github.com/mdmanurung/tidypolars-extra",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_with_keys": True,
}

html_title = "tidypolars-extra"
