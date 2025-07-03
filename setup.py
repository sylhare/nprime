""" nprime package """
from setuptools import setup, find_packages


def convert(markdown_path):
    """Convert a Markdown file to a reStructuredText file with the pypandoc"""
    try:
        import pypandoc
        output = pypandoc.convert_file(markdown_path, 'rst')
    except(IOError, ImportError, OSError):
        with open(markdown_path, 'r', encoding='utf-8') as f:
            output = f.read()
    return output


LONG_DESCRIPTION = convert("README.md")

setup(name='nprime',
      description='Python library for primes algorithms',
      long_description=LONG_DESCRIPTION,
      author='sylhare',
      author_email='sylhare@outlook.com',
      url='https://github.com/Sylhare/nprime',
      license='GNU General Public License v3.0',
      tests_require=['pytest'],
      install_requires=['matplotlib>=3.5.0'],
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
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "Programming Language :: Python :: 3 :: Only",
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
