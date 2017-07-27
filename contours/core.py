# -* coding: utf-8 -*-
"""Common enums, functions, and classes for the `contours` package."""

# Python 2 support
# pylint: disable=redefined-builtin,unused-wildcard-import,wildcard-import
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import numbers
import itertools
from enum import IntEnum
import numpy as np

# Attempt to import shapely and enable speedups.
try:
    import shapely.speedups
    if shapely.speedups.available:
        shapely.speedups.enable()
finally:
    try:
        from shapely.geometry import LineString, LinearRing, Polygon
    except ImportError:
        pass


class MPLPATHCODE(IntEnum):
    """Matplotlib path codes.

    These are included in this library for the purpose of writting your own
    formatter.  The description of each one is copied verbatim from the
    documentation for :class:`matplotlib.path.Path`.
    """

    STOP = 0
    """1 vertex (ignored)

    A marker fo the end of the entire path (currently not required and
    ignored).
    """

    MOVETO = 1
    """1 vertex

    Pick up the pen and move to the given vertex.
    """

    LINETO = 2
    """1 vertex

    Draw a line from the current position to the given vertex.
    """

    CURVE3 = 3
    """1 control point, 1 endpoint

    Draw a quadratic Bezier curve from he current position, with the given
    control point, to the given end point.
    """

    CURVE4 = 4
    """2 control points, 1 endpoint

    Draw a cubic Bezier curve from the current position, with the given control
    points, to the given and point.
    """

    CLOSEPOLY = 79
    """1 vertex (ignored)

    Draw a line segment to the start point of the current polyline.
    """


def null_formatter(level, vertices, codes=None):
    """Null formatter that passes through the raw vertices and codes."""
    return level, vertices, codes


def numpy_formatter(_, vertices, codes=None):
    """`NumPy`_ style contour formatter.

    Contours are returned as a list of Nx2 arrays containing the x and y
    vertices of the contour line.

    For filled contours the direction of vertices matters:

    * CCW (ACW): The vertices give the exterior of a contour polygon.
    * CW: The vertices give a hole of a contour polygon.  This hole will
        always be inside the exterior of the last contour exterior.

    .. note:: This is the fastest format.

    .. _NumPy: http://www.numpy.org

    """
    if codes is None:
        return vertices
    numpy_vertices = []
    for vertices_, codes_ in zip(vertices, codes):
        starts = np.nonzero(codes_ == MPLPATHCODE.MOVETO)[0]
        stops = np.nonzero(codes_ == MPLPATHCODE.CLOSEPOLY)[0]
        for start, stop in zip(starts, stops):
            numpy_vertices.append(vertices_[start:stop+1, :])
    return numpy_vertices


def matlab_formatter(level, vertices, codes=None):
    """`MATLAB`_ style contour formatter.

    Contours are returned as a single Nx2, `MATLAB`_ style, contour array.
    There are two types of rows in this format:

    * Header: The first element of a header row is the level of the contour
      (the lower level for filled contours) and the second element is the
      number of vertices (to follow) belonging to this contour line.
    * Vertex: x,y coordinate pairs of the vertex.

    A header row is always followed by the coresponding number of vertices.
    Another header row may follow if there are more contour lines.

    For filled contours the direction of vertices matters:

    * CCW (ACW): The vertices give the exterior of a contour polygon.
    * CW: The vertices give a hole of a contour polygon.  This hole will
        always be inside the exterior of the last contour exterior.

    For further explanation of this format see the `Mathworks documentation
    <https://www.mathworks.com/help/matlab/ref/contour-properties.html#prop_ContourMatrix>`_
    noting that the MATLAB format used in the `contours` package is the
    transpose of that used by `MATLAB`_ (since `MATLAB`_ is column-major
    and `NumPy`_ is row-major by default).

    .. _NumPy: http://www.numpy.org

    .. _MATLAB: https://www.mathworks.com/products/matlab.html

    """
    vertices = numpy_formatter(level, vertices, codes)
    if codes is not None:
        level = level[0]
    headers = np.vstack((
        [v.shape[0] for v in vertices],
        [level]*len(vertices))).T
    vertices = np.vstack(
        list(it.__next__() for it in
             itertools.cycle((iter(headers), iter(vertices)))))
    return vertices


def shapely_formatter(_, vertices, codes=None):
    """`Shapely`_ style contour formatter.

    Contours are returned as a list of :class:`shapely.geometry.LineString`,
    :class:`shapely.geometry.LinearRing`, and :class:`shapely.geometry.Point`
    geometry elements.

    Filled contours return a list of :class:`shapely.geometry.Polygon`
    elements instead.

    .. note:: If possible, `Shapely speedups`_ will be enabled.

    .. _Shapely: http://toblerity.org/shapely/manual.html

    .. _Shapely speedups: http://toblerity.org/shapely/manual.html#performance


    See Also
    --------
    `descartes <https://bitbucket.org/sgillies/descartes/>`_ : Use `Shapely`_
    or GeoJSON-like geometric objects as matplotlib paths and patches.

    """
    elements = []
    if codes is None:
        for vertices_ in vertices:
            if np.all(vertices_[0, :] == vertices_[-1, :]):
                # Contour is single point.
                if len(vertices) < 3:
                    elements.append(Point(vertices_[0, :]))
                # Contour is closed.
                else:
                    elements.append(LinearRing(vertices_))
            # Contour is open.
            else:
                elements.append(LineString(vertices_))
    else:
        for vertices_, codes_ in zip(vertices, codes):
            starts = np.nonzero(codes_ == MPLPATHCODE.MOVETO)[0]
            stops = np.nonzero(codes_ == MPLPATHCODE.CLOSEPOLY)[0]
            try:
                rings = [LinearRing(vertices_[start:stop+1, :])
                        for start, stop in zip(starts, stops)]
                elements.append(Polygon(rings[0], rings[1:]))
            except ValueError as err:
                # Verify error is from degenerate (single point) polygon.
                if np.any(stop - start - 1 == 0):
                    # Polygon is single point, remove the polygon.
                    if stops[0] < starts[0]+2:
                        pass
                    # Polygon has single point hole, remove the hole.
                    else:
                        rings = [
                            LinearRing(vertices_[start:stop+1, :])
                            for start, stop in zip(starts, stops)
                            if stop >= start+2]
                        elements.append(Polygon(rings[0], rings[1:]))
                else:
                    raise(err)
    return elements


class ContourMixin(object):
    """Mixin to provide the public contour methods.

    Parameters
    ----------
    formatter : callable
        A conversion function to convert from the internal Matplotlib contour
        format to an external format.  See :ref:`formatters` for more
        information.

    Attributes
    ----------
    formatter : :func:`callable`
        A conversion function to convert from the internal Matplotlib contour
        format to an external format.  See :ref:`formatters` for more
        information.

    """

    __slots__ = ('formatter',)

    def __init__(self, formatter=numpy_formatter, *args, **kwargs):
        """Initialize a :class:`ContourMixin`, see class docstring."""
        # pylint: disable=unused-argument
        self.formatter = formatter

    def contour(self, level):
        """Get contour lines at the given level.

        Parameters
        ----------
        level : numbers.Number
            The data level to calculate the contour lines for.

        Returns
        -------
        :
            The result of the :attr:`formatter` called on the contour at the
            given `level`.

        """
        if not isinstance(level, numbers.Number):
            raise TypeError(
                ("'_level' must be of type 'numbers.Number' but is "
                 "'{:s}'").format(type(level)))
        vertices = self._contour_generator.create_contour(level)
        return self.formatter(level, vertices)

    def filled_contour(self, min=None, max=None):
        """Get contour polygons between the given levels.

        Parameters
        ----------
        min : numbers.Number or None
            The minimum data level of the contour polygon.  If :obj:`None`,
            ``numpy.finfo(numpy.float64).min`` will be used.
        max : numbers.Number or None
            The maximum data level of the contour polygon.  If :obj:`None`,
            ``numpy.finfo(numpy.float64).max`` will be used.

        Returns
        -------
        :
            The result of the :attr:`formatter` called on the filled contour
            between `min` and `max`.

        """
        # pylint: disable=redefined-builtin,redefined-outer-name
        # Get the contour vertices.
        if min is None:
            min = np.finfo(np.float64).min
        if max is None:
            max = np.finfo(np.float64).max
        vertices, codes = (
            self._contour_generator.create_filled_contour(min, max))
        return self.formatter((min, max), vertices, codes)
