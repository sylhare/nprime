from setuptools import setup, find_packages
from nprime.toolbox import read_advance
from nprime.toolbox import convert


LONG_DESCRIPTION = convert("README.md")

setup(name='nprime',
      version='0.0.2',
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