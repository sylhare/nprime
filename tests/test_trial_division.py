"""Tests for the trial division algorithm."""
import pytest

from nprime.pyprime import trial_division
from tests.prime_testcase import FIRST_PRIMES


@pytest.mark.parametrize("n", [3.8, -1])
def test_invalid_input_raises(n):
    """Float and negative inputs raise ValueError."""
    with pytest.raises(ValueError):
        trial_division(n)


def test_trial_division_up_to_ten():
    """Trial division of 10 returns known primes and their composites."""
    assert trial_division(10) == {2: [4, 6, 8], 3: [6, 9], 5: [], 7: []}


def test_all_keys_are_primes():
    """All dictionary keys up to 70 match the known first primes."""
    assert sorted(trial_division(70)) == FIRST_PRIMES
