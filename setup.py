from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from app.toolbox import read_advance
import sys

import app

LONG_DESCRIPTION = read_advance('README.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(name='nprime',
      version='0.0.1',
      description='Python library for primes',
      long_description=LONG_DESCRIPTION,
      author='sylhare',
      author_email='sylhare@outlook.com',
      url='https://github.com/Sylhare/PyPrime',
      tests_require=['pytest'],
      install_requires=['matplotlib>=2.'],
      keywords=['prime', 'fermat', 'miller rabin', 'math'],
      license='GNU',
      packages=find_packages(),
      platforms='any',
      zip_safe=False,
      test_suite='tests.test_pyprime',
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
     )