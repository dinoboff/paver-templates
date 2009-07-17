import os
import sys

from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages

# import here packages only needed for development
try:
    from github.tools.task import *
    from paver.virtual import bootstrap
except:
    pass
    

version = "0.1.0"

long_description = open('README.rst', 'r').read()

classifiers = [
    # Get more strings from 
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]

install_requires = [
    'Sphinx',
    'pkginfo',
    'Paver',
    'PasteScript',
    'Cheetah',
    ]

entry_points="""
    # -*- Entry points: -*-
    [paste.paster_create_template]
    paver_package = paver.templates:PaverTemplate
    """

setup(
    name='paver-templates',
    version=version,
    description='Paver-enable template',
    long_description=long_description,
    classifiers=classifiers,
    keywords='Paver PasteScript template',
    author='Damien Lebrun',
    author_email='dinoboff@hotmail.com',
    url='',
    license='BSD',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=[],
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=install_requires,
    entry_points=entry_points,
    )

options(
    minilib=Bunch(
        extra_files=[
            'doctools',
            'virtual'
            ]
        ),
    virtualenv=Bunch(
        script_name='bootstrap.py',
        dest_dir='./virtual-env/',
        packages_to_install=[
            'github-tools',
            'virtualenv',
            'pkginfo',
            'Nose',
            ]
        ),
    sphinx=Bunch(
        docroot='docs',
        builddir='build',
        sourcedir='source',
        ),
    )

@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""