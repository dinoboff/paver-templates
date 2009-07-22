import os
import sys

from paver.easy import *
from paver.setuputils import setup
from setuptools import find_packages

# import here packages only needed for development
try:
    from github.tools.task import *
    from git import Git
    from paver.virtual import bootstrap
except:
    pass
    

version = "0.1.0b2"

long_description = open('README.rst', 'r').read() + open('CHANGES.rst', 'r').read() 

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
    "setuptools>=0.6c9",
    "Paver>=1.0.1",
    "pkginfo>=0.4.1",
    "PasteScript>=1.7.3",
    "Sphinx>=0.6.2",
    "Cheetah>=2.2.1",
    "virtualenv>=1.3.3",
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
    url='http://dinoboff.github.com/paver-templates',
    license='BSD',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['paver'],
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
            "virtualenv>=1.3.3",
            "github-tools>=0.1.6",
            "nose>=0.11.1",
            ]
        ),
    sphinx=Bunch(
        docroot='docs',
        builddir='build',
        sourcedir='source',
        ),
    )


@task
@needs('generate_setup', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""


@task
@needs('gh_pages_build', 'github.tools.task.gh_pages_update')
def gh_pages_update():
    """Overrides github.tools.task to rebuild the doc (with sphinx)."""
    
    
tag_name = 'v%s' % version
    
@task
def tag():
    """tag a new version of this distribution"""
    git = Git('.')
    git.pull('origin', 'master')
    git.tag(tag_name)


@task
def adjust_options():
    options.update(
        gh_pages_update=Bunch(commit_message='Update doc to %s' % version))


@task
@needs('sdist', 'tag', 'setuptools.command.upload',
    'adjust_options', 'gh_pages_update')
def upload():
    """Upload the distribution to pypi, the new tag and the doc to Github"""
    Git('.').push('origin', 'master', tag_name)