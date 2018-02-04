
import unittest
from tests.prime_testcase import FIRST_PRIMES
from nprime.pyprime import sieve_eratosthenes as sieve


class TestEratosthenes(unittest.TestCase):
    """ Tests for generate prime function """

    def test_001_is_not_integer_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertRaises(ValueError, sieve, 3.8)

    def test_002_is_inferior_to_two_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertRaises(ValueError, sieve, -1)

    def test_003_is_sieve_showing_primes_and_composite(self):
        """ The sieve should work for the first 10 numbers"""
        self.assertTrue(sieve(10) == {2: [4, 6, 8], 3: [6, 9], 5: [], 7: []})

    @unittest.skip("Does not work with Travis CI")
    def test_004_are_all_keys_primes(self):
        """ Making sure that all keys from the sieve are prime  """
        self.assertTrue(list(sieve(70)) == FIRST_PRIMES)


if __name__ == '__main__':
    unittest.main()