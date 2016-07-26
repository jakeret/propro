#!/usr/bin/env python

import os
import sys
from setuptools.command.test import test as TestCommand
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


readme = open('README.rst').read()

history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requires = ["click", "psutil"] #during runtime
tests_require=['pytest>=2.3'] #for testing

PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name='propro',
    version='0.1.0',
    description='Profiles a process',
    long_description=readme + '\n\n' + history,
    author='Joel Akeret',
    author_email='jakeret@phys.ethz.ch',
    url='http://www.astro.ethz.ch/refregier/research/index',
    packages=find_packages(PACKAGE_PATH, "test"),
    package_dir={'propro': 'propro'},
    include_package_data=True,
    install_requires=requires,
    license='Proprietary',
    zip_safe=False,
    keywords='propro',
    entry_points={
    'console_scripts': [
        'propro = propro.cli:run',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Intended Audience :: Science/Research",
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=tests_require,
    cmdclass = {'test': PyTest},
)