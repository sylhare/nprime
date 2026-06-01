"""Tests for the prime_factors function that returns prime factorization of an integer."""
import math

import pytest

from nprime.pyprime import is_prime, prime_factors

FACTORIZATIONS = [
    (1, []),
    (2, [2]),
    (3, [3]),
    (6, [2, 3]),
    (12, [2, 2, 3]),
    (49, [7, 7]),
    (64, [2, 2, 2, 2, 2, 2]),
    (97, [97]),
    (100, [2, 2, 5, 5]),
    (121, [11, 11]),
    (360, [2, 2, 2, 3, 3, 5]),
    (7919, [7919]),
    (2 * 3 * 5 * 7 * 11 * 13, [2, 3, 5, 7, 11, 13]),
]

INVALID_INPUTS = [0, -1, -5, 3.5, True]


@pytest.mark.parametrize("n, expected", FACTORIZATIONS)
def test_prime_factors(n, expected):
    """Factorization matches known prime decomposition."""
    assert prime_factors(n) == expected


@pytest.mark.parametrize("n, expected", FACTORIZATIONS)
def test_product_of_factors_equals_original(n, expected):
    """Product of returned factors reconstructs the original number."""
    assert (math.prod(expected) if expected else 1) == n


@pytest.mark.parametrize("n", [12, 60, 360, 30030])
def test_all_factors_are_prime(n):
    """Every factor in the result is itself a prime number."""
    for f in prime_factors(n):
        assert is_prime(f)


@pytest.mark.parametrize("n", [360, 2 * 7 * 3 * 11 * 5, 30030])
def test_factors_are_sorted(n):
    """Factors are returned in non-decreasing order."""
    factors = prime_factors(n)
    assert factors == sorted(factors)


@pytest.mark.parametrize("n", INVALID_INPUTS)
def test_invalid_input_raises(n):
    """Zero, negative, float, and bool inputs raise ValueError."""
    with pytest.raises(ValueError):
        prime_factors(n)
