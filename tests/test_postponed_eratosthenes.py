import unittest

from nprime.pyprime import postponed_sieve_eratosthenes
from tests.prime_testcase import FIRST_PRIMES
from itertools import islice


class TestPostponedSieve(unittest.TestCase):
    """ Tests for postponed sieve of eratosthenes """

    def test_first_few_primes(self):
        """ Making sure that all keys from the trial_division are prime  """
        generator = postponed_sieve_eratosthenes()
        first_primes = list(islice(generator, 0, len(FIRST_PRIMES)))
        self.assertEqual(FIRST_PRIMES, first_primes)


if __name__ == '__main__':
    unittest.main()
