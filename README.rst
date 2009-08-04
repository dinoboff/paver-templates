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
    


Usage
=====

As simple as::

    paster create -t paver_package <package name>
    
 
   
Development
===========

If you would like to help the development of this package, `fork this project`_
or `report bugs`_.

The Paver-template project contains a virtualenv bootstrap script 
that will install all required packages for development::

	python bootstrap --no-site-packages
	source virtual-env/bin/activate
	paver develop

If you would rather use virtualenvwrapper, the project contains a list of 
requirement suitable for pip::

	mkvirtualenv --no-site-packages paver-templates
	easy_install pip
	pip install -r dev-requirements.txt
	paver develop



.. _Paver-Templates' Cheeseshop page: http://pypi.python.org/pypi/paver-templates/
.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _fork this project: http://github.com/dinoboff/paver-templates/
.. _report bugs: http://github.com/dinoboff/paver-templates/issues