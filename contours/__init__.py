# -* coding: utf-8 -*-
"""Contour calculations."""

# Python 2 support
# pylint: disable=redefined-builtin,unused-wildcard-import,wildcard-import
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from .core import numpy_formatter, matlab_formatter, shapely_formatter
from .quad import QuadContourGenerator

__version__ = '0.0.1'
