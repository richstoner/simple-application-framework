.. manage documentation master file, created by
   sphinx-quickstart on Sat Jun  7 10:53:34 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Simple Application Framework Documentation
==========================================

The simple application framework is a set of tools to make the deployment and hosting of a moderately complex
python-based application simple. It uses nginx, supervisor, and anaconda as core components. It can be extended to
include a database like mongo or elasticsearch, a task queue like celery, and other more specialized components.

This project consists of two parts:

1. The fabric file
------------------

.. toctree::
   :maxdepth: 4

   fabfile


2. The fabriccloud package
--------------------------

a set of tools to provision and manage the hosting framework


.. toctree::
   :maxdepth: 4

   fabriccloud


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

