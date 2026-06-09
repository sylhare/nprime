"""Tests for the AKS deterministic primality test and its helper functions.

The aks function is checked against the same data sets as the other primality
algorithms, plus an exhaustive agreement check against is_prime.
"""
import pytest

from nprime.aks_primality import aks, find_r, int_root, perfect_power, poly_mod_exp, poly_mult_mod_ring
from nprime.pyprime import is_prime
from tests.prime_testcase import CARMICHAEL, FIRST_NOT_PRIMES, FIRST_PRIMES, PSEUDO_PRIMES

ALL_PSEUDO_PRIMES = [n for values in PSEUDO_PRIMES.values() for n in values]


def test_two_is_prime():
    """Two is correctly identified as prime."""
    assert aks(2) is True


@pytest.mark.parametrize("n", FIRST_PRIMES)
def test_first_primes(n):
    """Known small primes are identified as prime."""
    assert aks(n) is True


@pytest.mark.parametrize("n", FIRST_NOT_PRIMES)
def test_first_non_primes(n):
    """Known small composites are identified as not prime."""
    assert aks(n) is False


@pytest.mark.parametrize("n", ALL_PSEUDO_PRIMES)
def test_pseudo_primes(n):
    """Pseudoprimes (false positives for naive tests) are correctly rejected."""
    assert aks(n) is False


@pytest.mark.parametrize("n", CARMICHAEL)
def test_carmichael_numbers(n):
    """Carmichael numbers (Fermat liars) are correctly rejected."""
    assert aks(n) is False


@pytest.mark.parametrize("n", range(2, 200))
def test_matches_is_prime(n):
    """AKS is deterministic, so it must agree with is_prime."""
    assert aks(n) == is_prime(n)


@pytest.mark.parametrize("n, b, expected", [(27, 3, 3), (28, 3, 3), (1024, 10, 2)])
def test_int_root(n, b, expected):
    """int_root returns the integer floor of the b-th root."""
    assert int_root(n, b) == expected


@pytest.mark.parametrize("n, expected", [(8, True), (81, True), (7, False)])
def test_perfect_power(n, expected):
    """perfect_power detects perfect powers a^b with b >= 2."""
    assert perfect_power(n) is expected


def test_find_r():
    """find_r returns the smallest valid r for the AKS test."""
    assert find_r(31) == 29


@pytest.mark.parametrize("p, q, n, r, expected", [
    ([1, 0, 0, 1], [1], 7, 3, [2, 0, 0]),
    ([0, 0, 1], [0, 0, 1], 11, 4, [1, 0, 0, 0]),
])
def test_poly_mult_mod_ring(p, q, n, r, expected):
    """Polynomial multiplication wraps degrees modulo X^r - 1."""
    assert poly_mult_mod_ring(p, q, n, r) == expected


def test_poly_mod_exp():
    """poly_mod_exp expands the binomial (X + a)^n in the ring."""
    assert poly_mod_exp(1, 3, 2, 5) == [4, 4]
