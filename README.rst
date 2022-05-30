===============================
ponder
===============================

.. image:: https://img.shields.io/travis/claresloggett/ponder.svg
        :target: https://travis-ci.org/claresloggett/ponder

.. image:: https://img.shields.io/pypi/v/ponder.svg
        :target: https://pypi.python.org/pypi/ponder


A library to allow scikit-learn to automatically handle Pandas DataFrames

* Free software: MIT license
* Documentation: https://claresloggett.github.io/ponder.

Overview
--------

Ponder adds methods to scikit-learn models to allow them to work more easily
with Pandas.

Scikit-learn classes are built to expect numpy arrays as input. In many cases,
if we have a Pandas' DataFrame, we'd like to encode it numerically and convert
it to a numpy array for use with sklearn. Pandas automates this process as far
as possible to streamline your sklearn code.
 
Ponder adds methods to scikit-learn model instances to allow easy handling of
Pandas DataFrames. These methods take advantage of Pandas' dtypes to decide how
columns should be handled. We provide sensible defaults so that passing
DataFrames and Series into the scikit-learn object should "just work".
