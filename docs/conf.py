#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,redefined-builtin
"""
contours documentation build configuration file
"""

import re
import os
import sys

# Add documented modules to path.
sys.path.insert(0, os.path.abspath('..'))


# General Options
# ###################################################################
needs_sphinx = '1.4'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'contours'
copyright = '2017, Michael R. Shannon'
author = 'Michael R. Shannon'
version = re.search(
    r"^__version__\s*=\s*'(.*)'",
    open('../contours/__init__.py').read(),
    re.M).group(1)
release = version
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'


# Extension Options
# ###################################################################
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.graphviz',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinxcontrib.fulltoc']

autodoc_member_order = 'alphabetical'
graphviz_output_format = 'svg'
inheritance_graph_attrs = {
    'bgcolor': 'transparent',
    'rankdir': 'TB',
    'ratio': 'compress',
    'size': '"6.5, 7.0"'}
intersphinx_mapping = {
    'py': ('https://docs.python.org/3', None),
    'np': ('http://docs.scipy.org/doc/numpy/', None),
    'mpl': ('http://matplotlib.org', None),
    'shapely': ('http://toblerity.org/shapely', None)}
todo_include_todos = True


# HTML Output Options
# ###################################################################
html_theme = 'nature'
html_static_path = ['_static']


# HTML Help Output Options
# ###################################################################
htmlhelp_basename = 'contoursdoc'


# LaTeX (PDF) Output Options
# ###################################################################
latex_show_pagerefs = True
latex_show_urls = 'footnote'
latex_documents = [
    (master_doc, 'contours.tex', 'contours Documentation',
     'Michael R. Shannon', 'manual', True),
]


# Manual Page Output Options
# ###################################################################
man_pages = [
    (master_doc, 'contours', 'contours Documentation',
     [author], 1)
]


# Texinfo Page Output Options
# ###################################################################
texinfo_documents = [
    (master_doc, 'contours', 'contours Documentation',
     author, 'contours', 'One line description of project.',
     'Miscellaneous'),
]
