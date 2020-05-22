import unittest

from nprime.pyprime import sieve_eratosthenes as sieve
from tests.prime_testcase import FIRST_PRIMES


class TestEratosthenes(unittest.TestCase):
    """ Tests for generate prime function """

    def test_001_is_not_integer_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertRaises(TypeError, sieve, 3.8)

    def test_002_is_inferior_to_two_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertEqual({}, sieve(-1))

    def test_003_is_sieve_showing_primes_and_composite(self):
        """ The sieve should work for the first 10 numbers"""
        self.assertEqual({2: [4, 6, 8, 10], 3: [9], 5: [], 7: []}, sieve(10))

    def test_004_are_all_keys_primes(self):
        """ Making sure that all keys from the sieve are prime  """
        primes = list(sieve(70))
        primes.sort()
        self.assertEqual(FIRST_PRIMES, primes)


if __name__ == '__main__':
    unittest.main()
