"""Tests for the postponed sieve of Eratosthenes infinite generator."""
from itertools import islice

from nprime.pyprime import postponed_sieve_eratosthenes
from tests.prime_testcase import FIRST_PRIMES


def test_first_few_primes():
    """First primes from the generator match the known sequence."""
    generator = postponed_sieve_eratosthenes()
    first_primes = list(islice(generator, 0, len(FIRST_PRIMES)))
    assert FIRST_PRIMES == first_primes
