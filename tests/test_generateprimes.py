"""Tests for the generate_primes function that lists primes up to a limit."""
import pytest

from nprime.pyprime import generate_primes
from tests.prime_testcase import FIRST_PRIMES

GENERATE_CASES = [
    (2, [2]),
    (1, []),
    (0, []),
    (70, FIRST_PRIMES),
]


@pytest.mark.parametrize("upper, expected", GENERATE_CASES)
def test_generate_primes(upper, expected):
    """Generated primes up to upper match known values, including edge cases below 2."""
    assert generate_primes(upper) == expected
