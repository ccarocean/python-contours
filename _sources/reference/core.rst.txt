:mod:`core` Module
==================

.. currentmodule:: contours.core

.. automodule:: contours.core


Summary
-------

.. autosummary::
    :nosignatures:

    MPLPATHCODE
    numpy_formatter
    matlab_formatter
    shapely_formatter
    ContourMixin

Enumerations
------------

.. autoclass:: MPLPATHCODE
    :members:


.. _formatters:

Formatters
----------

Contour formatters are meant to be given as the `formatter` argument when
constructing a contour generator.  The default formatter is
:func:`numpy_formatter`.

.. autofunction:: numpy_formatter()

.. autofunction:: matlab_formatter()

.. autofunction:: shapely_formatter()

Writting your own formatter.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Formatter functions follow the general format below.

.. function:: sample_formatter(level, vertices, codes=None)

    .. note::

        The :func:`sample_formatter` does not have an implementation.

    :param numbers.Number level: The level of the contour or a tuple giving the
        (min, max) for filled contours.
    :param list(numpy.ndarray) vertices: A list of arrays where each array is
        Nx2 and gives the vertices of a contour.  If the vertices are for
        a filled contour the vertices also give any holes and `codes` will be
        given. Exteriors are always CCW and interiors are always CW.
    :param list(numpy.ndarray) codes: A list of arrays contiaining
        :class:`MPLPATHCODE` drawing codes.  Each polyline in each array begins
        with :obj:`MPLPATHCODE.MOVETO` and ends with
        :obj:`MPLPATHCODE.CLOSEPOLY`. Each array can contain multiple
        polylines, the first gives the exterior of the polygon while the rest
        give the holes. *Only given for filled contours.*

    :returns: This is implementation dependent but the general rule is that is
        should represent the contour or filled contour in some way.


Classes
-------

.. inheritance-diagram:: ContourMixin

.. autoclass:: ContourMixin
    :show-inheritance:

    **Methods:**
        .. autosummary::

            contour
            filled_contour

    .. automethod:: contour

    .. automethod:: filled_contour
