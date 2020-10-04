""" nprime package """
from setuptools import setup, find_packages

import nprime


def convert(markdown_path):
    """Convert a Markdown file to a reStructuredText file with the pypandoc"""
    try:
        import pypandoc
        output = pypandoc.convert(markdown_path, 'rst')
        # pypandoc.convert(markdown_path, 'rst', outputfile="README.rst") # Create the rst file
    except(IOError, ImportError):
        output = open(markdown_path).read()

    return output


LONG_DESCRIPTION = convert("README.md")

setup(name='nprime',
      version=nprime.__version__,
      description='Python library for primes algorithms',
      long_description=LONG_DESCRIPTION,
      author='sylhare',
      author_email='sylhare@outlook.com',
      url='https://github.com/Sylhare/nprime',
      license='GNU General Public License v3.0',
      tests_require=['pytest'],
      install_requires=['matplotlib>=2.1'],
      keywords=['prime',
                'fermat',
                'miller rabin',
                'math'],
      packages=find_packages(),
      package_data={
          'License': ['LICENSE'],
          'Readme': ['README.md'],
      },
      platforms='any',
      zip_safe=True,
      test_suite='tests',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Education",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Libraries",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Utilities"]
      )
