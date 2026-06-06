"""Tests for the is_perfect function that checks if a number is a perfect number."""
import pytest

from nprime.pyprime import is_perfect

PERFECT_NUMBERS = [6, 28, 496, 8128]
NOT_PERFECT_NUMBERS = [1, 2, 3, 4, 5, 7, 12, 27, 29, 97, 100, 495, 497]
INVALID_INPUTS = [0, -1, -6, 2.5, True]


@pytest.mark.parametrize("n", PERFECT_NUMBERS)
def test_is_perfect(n):
    """Known perfect numbers are correctly identified."""
    assert is_perfect(n) is True


@pytest.mark.parametrize("n", NOT_PERFECT_NUMBERS)
def test_is_not_perfect(n):
    """Non-perfect numbers including primes, composites, and boundary values."""
    assert is_perfect(n) is False


@pytest.mark.parametrize("exp", range(1, 10))
def test_powers_of_two_are_not_perfect(exp):
    """No power of two is a perfect number."""
    assert is_perfect(2 ** exp) is False


@pytest.mark.parametrize("n", INVALID_INPUTS)
def test_invalid_input_raises(n):
    """Zero, negative, float, and bool inputs raise ValueError."""
    with pytest.raises(ValueError):
        is_perfect(n)
