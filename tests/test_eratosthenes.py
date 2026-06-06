"""Tests for the sieve of Eratosthenes implementation."""
import pytest

from nprime.pyprime import sieve_eratosthenes as sieve
from tests.prime_testcase import FIRST_PRIMES


def test_float_raises():
    """Non-integer input raises TypeError."""
    with pytest.raises(TypeError):
        sieve(3.8)


def test_negative_returns_empty():
    """Negative upper bound returns an empty dictionary."""
    assert sieve(-1) == {}


def test_sieve_up_to_ten():
    """Sieve of 10 returns known primes and their composites."""
    assert sieve(10) == {2: [4, 6, 8, 10], 3: [9], 5: [], 7: []}


def test_all_keys_are_primes():
    """All dictionary keys up to 70 match the known first primes."""
    assert sorted(sieve(70)) == FIRST_PRIMES
