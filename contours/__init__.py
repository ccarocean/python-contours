# -* coding: utf-8 -*-
"""Contour calculations."""

# Python 2 support
from __future__ import absolute_import

from .core import numpy_formatter, matlab_formatter, shapely_formatter
from .quad import QuadContourGenerator

__version__ = '0.0.2'
