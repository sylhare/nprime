"""Tests for primality functions: is_prime, fermat, miller_rabin.

Each function is tested against the same data sets to ensure consistent behavior
across deterministic and probabilistic algorithms.
"""
import pytest

from nprime.pyprime import fermat, is_prime, miller_rabin
from tests.prime_testcase import CARMICHAEL, FIRST_NOT_PRIMES, FIRST_PRIMES, PSEUDO_PRIMES

ALL_PSEUDO_PRIMES = [n for values in PSEUDO_PRIMES.values() for n in values]
PRIME_FUNCTIONS = [is_prime, fermat, miller_rabin]


@pytest.mark.parametrize("func", PRIME_FUNCTIONS)
def test_two_is_prime(func):
    """Two is correctly identified as prime."""
    assert func(2) is True


@pytest.mark.parametrize("func", PRIME_FUNCTIONS)
@pytest.mark.parametrize("n", FIRST_PRIMES)
def test_first_primes(func, n):
    """Known small primes are identified as prime."""
    assert func(n) is True


@pytest.mark.parametrize("func", PRIME_FUNCTIONS)
@pytest.mark.parametrize("n", FIRST_NOT_PRIMES)
def test_first_non_primes(func, n):
    """Known small composites are identified as not prime."""
    assert func(n) is False


@pytest.mark.parametrize("func", PRIME_FUNCTIONS)
@pytest.mark.parametrize("n", ALL_PSEUDO_PRIMES)
def test_pseudo_primes(func, n):
    """Pseudoprimes (false positives for naive tests) are correctly rejected."""
    assert func(n) is False


@pytest.mark.parametrize("func", PRIME_FUNCTIONS)
@pytest.mark.parametrize("n", CARMICHAEL)
def test_carmichael_numbers(func, n):
    """Carmichael numbers (Fermat liars) are correctly rejected."""
    assert func(n) is False
