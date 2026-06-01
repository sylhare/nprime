"""Tests for the pyprime wrapper function that validates input before primality testing."""
import pytest

from nprime.pyprime import pyprime

NOT_PRIME = [0, 1] + list(range(-1, -10, -1))
PRIME = [2, 3, 5, 29]
INVALID_TYPES = [3.8, True, "three"]


@pytest.mark.parametrize("n", NOT_PRIME)
def test_not_prime(n):
    """Zero, one and negative integers are not prime."""
    assert pyprime(n) is False


@pytest.mark.parametrize("n", PRIME)
def test_is_prime(n):
    """Known small primes are correctly identified."""
    assert pyprime(n) is True


@pytest.mark.parametrize("n", INVALID_TYPES)
def test_invalid_type_raises(n):
    """Non-integer types (float, bool, str) raise TypeError."""
    with pytest.raises(TypeError):
        pyprime(n)
