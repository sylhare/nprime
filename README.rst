nprime |PyPI version| |Build Status| |codecov| |Codacy Badge|
=============================================================

|forthebadge| |forthebadge|

Installation
------------

To install the package use pip:

::

    pip install nprime

Introduction
------------

Some algorithm on prime numbers.

Algorithm developed :

-  Native one (prime through divisions)
-  Eratosthenes sieve based
-  Fermat's test (based on Fermat's theorem)
-  Prime generating functions
-  Miller Rabin predictive algorithm

Specifications
--------------

-  Language: Python **3.5.2**
-  Package:

   -  Basic python packages were preferred
   -  Matplotlib v2.0 - graph and math

Continuous integration
~~~~~~~~~~~~~~~~~~~~~~

Travis will be used to run the tests automatically.

Code Quality
~~~~~~~~~~~~

Ensured with PEP-8 (for the language format) and
`Pylint <https://www.pylint.org/>`__ (for the code quality). PyLint is
now only run by an other review tool integrated to this repo
(`codacity <https://www.codacy.com/app/Sylhare/PyPrime/dashboard>`__,
`erbert <https://ebertapp.io/github/Sylhare/PyPrime>`__, ...)

Math
----

Here are a bit of information to help understand some of the algorithms

Congruence
~~~~~~~~~~

"``≡``" means congruent, ``a ≡ b (mod m)`` implies that
``m / (a-b), ∃ k ∈ Z`` that verifies ``a = kn + b``

which implies:

::

    a ≡ 0 (mod n) <-> a = kn <-> "a" is divisible by "n" 

Fermart's Theorem
~~~~~~~~~~~~~~~~~

if ``n`` is prime then ``∀ a ∈[1, ..., n-1]``

::

    a^(n-1) ≡ 1 (mod n) ⇔ a^(n-1) = kn + 1

Miller rabin
~~~~~~~~~~~~

Take a random ``a ∈ {1,...,n−1}`` and ``n > 2``, Find ``d`` and ``s``
such as with ``n - 1 = 2^s * d`` (with d odd) if ``(a^d)^2^r ≡ 1 mod n``
for all ``r`` in ``0`` to ``s-1`` Then ``n`` is prime.

The test output is false of 1/4 of the "a values" possible in ``n``, so
the test is repeated t times.

Strong Pseudoprime
~~~~~~~~~~~~~~~~~~

A strong
`pseudoprime <http://mathworld.wolfram.com/StrongPseudoprime.html>`__ to
a base ``a`` is an odd composite number ``n`` with ``n-1 = d·2^s`` (for
d odd) for which either ``a^d = 1(mod n)`` or ``a^(d·2^r) = -1(mod n)``
for some ``r = 0, 1, ..., s-1``

.. |PyPI version| image:: https://badge.fury.io/py/nprime.svg
   :target: https://badge.fury.io/py/nprime
.. |Build Status| image:: https://travis-ci.org/Sylhare/PyPrime.svg?branch=master
   :target: https://travis-ci.org/Sylhare/PyPrime
.. |codecov| image:: https://codecov.io/gh/Sylhare/PyPrime/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Sylhare/PyPrime
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/e5a9dd6a55fb4709becbb84b8c538d54
   :target: https://www.codacy.com/app/Sylhare/PyPrime?utm_source=github.com&utm_medium=referral&utm_content=Sylhare/PyPrime&utm_campaign=Badge_Grade
.. |forthebadge| image:: http://forthebadge.com/images/badges/made-with-python.svg
   :target: http://forthebadge.com
.. |forthebadge| image:: http://forthebadge.com/images/badges/built-with-science.svg
   :target: http://forthebadge.com
