===============
Paver-Templates
===============


Create the the layout of a paver-enable package, including:

- pavement.py;
- README.rst, with basic installation instructions;
- LICENSE (support BSD and (A/L)GPL licenses by default). For a GPL licenses,
  it will copy the required GPL license copies;
- MANIFEST.in;
- docs/conf.py and docs/index.rst. docs/index.rst simple include the content
  of README.rst;
- and your empty package. 


Installation
============

The easiest way to get Paver-Templates is if you have setuptools_ installed::

    easy_install paver-templates

Without setuptools, it's still pretty easy. Download the Paver-Template .tgz
file from `Paver-Templates' Cheeseshop page`_, untar it and run::

    python setup.py install

.. _Paver-Templates' Cheeseshop page: http://pypi.python.org/pypi/paver-templates/
.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall


Usage
=====

As simple as::

    paster create -t paver_package <package name>

