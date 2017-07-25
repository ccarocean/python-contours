contours - contour calculation with matplotlib
---------------------------------------------------------

.. begin-description

The `contours` package exposes Matplotlib's contour generators to the user
providing an equivalent of MATLAB's ``contourc`` function.  This is done for
grids (including curvilinear) as well as unstructured data via Delaunay
triangulation (**FUTURE**).

Regular contours can be returned as `NumPy`_ arrays or as `Shapely`_
LineStrings and LinearRings.  Filled contours can be returned as `NumPy`_
arrays or as `Shapely`_ Polygons.

Contour calculation without plotting is currently an open issue `#367`_ for
Matplotlib.  In that discussion, the type of hackery done in this library is
discouraged by the Matplotlib developers.  As of this writing there has been no
decision as to whether exposing contour calculations is a feature that should
be included in Matplotlib or not.  If such a refactoring in Matplotlib ever
takes place, this library will be refactored to avoid using Matplotlib's
internal components.

.. _Shapely: http://toblerity.org/shapely/manual.html

.. _NumPy: http://www.numpy.org

.. _#367: https://github.com/matplotlib/matplotlib/issues/367

.. end-description


.. begin-body

.. begin-links

Links
-----

* `Download <https://github.com/ccarocean/python-contours/archive/master.zip>`_
* `GitHub <https://github.com/ccarocean/python-contours>`_

.. end-links

.. begin-features

Features
--------

* Filled and non-filled contours.
* Contours on regular grids.
* **TODO** Contours on unstructured data.

.. end-features


Examples
--------

A contrived example using `QuadContourGenerator` to compute the area and
circumference of a circle and a ring.

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


.. begin-author

Author
------

The `contours` module was written by Michael R. Shannon (`@mrshannon
<https://github.com/mrshannon>`_) <mrshannon.aerospace@gmail.com> in 2017.

It is maintained by:

* Michael R. Shannon (`@mrshannon <https://github.com/mrshannon>`_)
  <mrshannon.aerospace@gmail.com> 2017-

.. end-author

Testing
-------

**TODO**

.. end-body
