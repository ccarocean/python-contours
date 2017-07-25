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

* **TODO** Filled and non-filled contours.
* **TODO** Contours on regular grids.
* **TODO** Contours on unstructured data.

.. end-features


Examples
--------

**TODO**


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
