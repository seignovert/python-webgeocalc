# -*- coding: utf-8 -*-
'''Configuration file for the Sphinx documentation builder.

This file does only contain a selection of the most common options. For a
full list see the documentation:
http://www.sphinx-doc.org/en/master/config
'''

# -- Project information -----------------------------------------------------

project = 'WebGeoCalc API'
copyright = '2019, Benoit Seignovert'
author = 'Benoit Seignovert'

# -- General configuration ---------------------------------------------------

extensions = [
    'pbr.sphinxext',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
htmlhelp_basename = 'WebGeoCalcAPIdoc'

# -- Extension configuration -------------------------------------------------
autodoc_default_flags = ['members', 'show-inheritance']
autodoc_member_order = 'bysource'
pygments_style = None
