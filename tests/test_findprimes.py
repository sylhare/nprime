"""Tests for the find_primes function that discovers primes in a given range."""
import pytest

from nprime.pyprime import find_primes
from tests.prime_testcase import FIRST_PRIMES

INVALID_RANGES = [
    (100, 50),
    (1, 50),
    (0, 50),
    (50, 50),
]

FIND_PRIMES_CASES = [
    (2, 70, FIRST_PRIMES),
    (1000, 1100, [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097]),
    (370270, 370370, []),
]


@pytest.mark.parametrize("lower, upper", INVALID_RANGES)
def test_invalid_range_raises(lower, upper):
    """Reversed, equal, or sub-1 bounds raise ValueError."""
    with pytest.raises(ValueError):
        find_primes(lower, upper)


@pytest.mark.parametrize("lower, upper, expected", FIND_PRIMES_CASES)
def test_find_primes(lower, upper, expected):
    """Primes found in a range match known values, including empty intervals."""
    assert find_primes(lower, upper) == expected
