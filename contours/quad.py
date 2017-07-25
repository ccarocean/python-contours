# -* coding: utf-8 -*-
"""Contour calculation of data on structured grids.

    See [1]_ for definition of structured grid types.

.. _Shapely speedups: http://toblerity.org/shapely/manual.html#performance

References
----------
.. [1] Structured grids. (n.d.). Retrieved July 21, 2017, from
   https://geo-ide.noaa.gov/wiki/index.php?title=Structured_grids

"""

# Python 2 support
# pylint: disable=redefined-builtin,unused-wildcard-import,wildcard-import
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import numpy as np
import matplotlib._contour as _contour
from .core import ContourMixin, numpy_formatter


class QuadContourGenerator(ContourMixin):
    """Contour line/polygon generator.

    The default constructor supports general structured (curvilinear) grids.
    If the grid is more structured consider using one of the other
    constructors:

    * :meth:`from_curvilinear` - same as default constructor
    * :meth:`from_rectilinear` - rectilinear grids
    * :meth:`from_uniform` - uniform or Cartesian grids

    .. _Matplotlib: https://matplotlib.org/

    Note
    ----
    This is a wrapper around Matplotlib's :class:`QuadContourGenerator
    <matplotlib.QuadContourGenerator>`, a highly efficient contour generator
    written in pure C++.

    Example
    -------
    A contrived example using :class:`QuadContourGenerator` to compute the area
    and circumference of a circle and a ring.

    >>> from contours.core import shapely_formatter as shapely_fmt
    >>> from contours.quad import QuadContourGenerator
    >>> import numpy as np
    >>> x = np.arange(-1, 1+0.01, 0.01)
    >>> y = np.arange(-1, 1+0.01, 0.01)
    >>> z = np.sqrt(x[:, np.newaxis]**2 + y[np.newaxis, :]**2)
    >>> c = QuadContourGenerator.from_rectilinear(x, y, z, shapely_fmt)
    >>> contour = c.filled_contour(max=1.0)
    >>> print('Area: {:0.2f}'.format(contour[0].area))
    Area: 3.14
    >>> print('Length: {:0.2f}'.format(contour[0].length))
    Length: 6.28
    >>> contour = c.filled_contour(min=0.5, max=1.0)
    >>> print('Area: {:0.2f}'.format(contour[0].area))
    Area: 2.36
    >>> print('Length: {:0.2f}'.format(contour[0].exterior.length))
    Length: 6.28
    >>> print('Length: {:0.2f}'.format(contour[0].interiors[0].length))
    Length: 3.14

    Parameters
    ----------
    x : array_like
        x coordinates of each point in `z`.  Must be the same size as `z`.
    y : array_like
        y coordinates of each point in `z`.  Must be the same size as `z`.
    z : array_like
        The 2-dimensional (possibly curvilinear) grid of data to compute
        contours for.  Masked arrays are supported.
    formatter : callable
        A conversion function to convert from the internal `Matplotlib`_
        contour format to an external format.  See :ref:`formatters` for more
        information.

    Attributes
    ----------
    formatter : :func:`callable`
        A conversion function to convert from the internal `Matplotlib`_
        contour format to an external format.  See :ref:`formatters` for more
        information.

    """

    slots = ('_contour_generator',)

    def __init__(self, x, y, z, formatter=numpy_formatter):
        """Initialize a :class:`QuadContourGenerator`, see class docstring."""
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        z = np.ma.asarray(z, dtype=np.float64)
        if x.shape != z.shape:
            raise TypeError(
                ("'x' and 'z' must be the same shape but 'x' has shape {:s} "
                 "and 'z' has shape {:s}").format(str(x.shape), str(z.shape)))
        if y.shape != z.shape:
            raise TypeError(
                ("'y' and 'z' must be the same shape but 'y' has shape {:s} "
                 "and 'z' has shape {:s}").format(str(y.shape), str(z.shape)))
        mask = z.mask if z.mask is not np.ma.nomask and z.mask.any() else None
        self._contour_generator = _contour.QuadContourGenerator(
            x, y, z.filled(), mask, True, 0)
        super().__init__(formatter)

    @classmethod
    def from_curvilinear(cls, x, y, z, formatter=numpy_formatter):
        """Construct a contour generator from a curvilinear grid.

        Note
        ----
        This is an alias for the default constructor.

        Parameters
        ----------
        x : array_like
            x coordinates of each point in `z`.  Must be the same size as `z`.
        y : array_like
            y coordinates of each point in `z`.  Must be the same size as `z`.
        z : array_like
            The 2-dimensional curvilinear grid of data to compute
            contours for.  Masked arrays are supported.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        return cls(x, y, z, formatter)

    @classmethod
    def from_rectilinear(cls, x, y, z, formatter=numpy_formatter):
        """Construct a contour generator from a rectilinear grid.

        Parameters
        ----------
        x : array_like
            x coordinates of each column of `z`.  Must be the same length as
            the number of columns in `z`.  (len(x) == z.shape[1])
        y : array_like
            y coordinates of each row of `z`.  Must be the same length as the
            number of columns in `z`.  (len(y) == z.shape[0])
        z : array_like
            The 2-dimensional rectilinear grid of data to compute contours for.
            Masked arrays are supported.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        z = np.ma.asarray(z, dtype=np.float64)
        # Check arguments.
        if x.ndim != 1:
            raise TypeError(
                "'x' must be a 1D array but is a {:d}D array".format(x.ndim))
        if y.ndim != 1:
            raise TypeError(
                "'y' must be a 1D array but is a {:d}D array".format(y.ndim))
        if z.ndim != 2:
            raise TypeError(
                "'z' must be a 2D array but it a {:d}D array".format(z.ndim))
        if x.size != z.shape[1]:
            raise TypeError(
                ("the length of 'x' must be equal to the number of columns in "
                 "'z' but the length of 'x' is {:d} and 'z' has {:d} "
                 "columns").format(x.size, z.shape[1]))
        if y.size != z.shape[0]:
            raise TypeError(
                ("the length of 'y' must be equal to the number of rows in "
                 "'z' but the length of 'y' is {:d} and 'z' has {:d} "
                 "rows").format(y.size, z.shape[0]))
        # Convert to curvilinear format and call constructor.
        y, x = np.meshgrid(y, x, indexing='ij')
        return cls(x, y, z, formatter)

    @classmethod
    def from_uniform(
            cls, z, origin=(0, 0), step=(1, 1), formatter=numpy_formatter):
        """Construct a contour generator from a uniform grid.

        NOTE
        ----
        The default `origin` and `step` values is equivalent to calling
        :meth:`matplotlib.axes.Axes.contour` with only the `z` argument.

        Parameters
        ----------
        z : array_like
            The 2-dimensional uniform grid of data to compute contours for.
            Masked arrays are supported.
        origin : (number.Number, number.Number)
            The (x, y) coordinate of data point `z[0,0]`.
        step :  (number.Number, number.Number)
            The (x, y) distance between data points in `z`.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        z = np.ma.asarray(z, dtype=np.float64)
        # Check arguments.
        if z.ndim != 2:
            raise TypeError(
                "'z' must be a 2D array but it a {:d}D array".format(z.ndim))
        if len(origin) != 2:
            raise TypeError(
                "'origin' must be of length 2 but has length {:d}".format(
                    len(origin)))
        if len(step) != 2:
            raise TypeError(
                "'step' must be of length 2 but has length {:d}".format(
                    len(step)))
        if any(s == 0 for s in step):
            raise ValueError(
                "'step' must have non-zero values but is {:s}".format(
                    str(step)))
        # Convert to curvilinear format and call constructor.
        y, x = np.mgrid[
            origin[0]:(origin[0]+step[0]*z.shape[0]):step[0],
            origin[1]:(origin[1]+step[1]*z.shape[1]):step[1]]
        return cls(x, y, z, formatter)
