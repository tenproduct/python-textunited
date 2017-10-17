========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-textunited/badge/?style=flat
    :target: https://readthedocs.org/projects/python-textunited
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tenplatform/python-textunited.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tenplatform/python-textunited

.. |codecov| image:: https://codecov.io/gh/tenproduct/python-textunited/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/gh/tenproduct/python-textunited

.. |version| image:: https://img.shields.io/pypi/v/python-textunited.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/python-textunited

.. |commits-since| image:: https://img.shields.io/github/commits-since/tenplatform/python-textunited/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tenproduct/python-textunited/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/python-textunited.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/python-textunited

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/python-textunited.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/python-textunited

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/python-textunited.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/python-textunited


.. end-badges

A wrapper around the Text United API written in Python. Each Text United
object is represented by a corresponding Python object. The attributes
of these objects are cached, but the child objects are not.

* Free software: GNU General Public License v3 or later (GPLv3+)

Installation
============

::

    pip install python-textunited

Documentation
=============

https://python-textunited.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

