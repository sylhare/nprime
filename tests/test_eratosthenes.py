
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

    def test_004_are_all_keys_primes(self):
        """ """
        output = list(sieve(70))
        for n in range(0, len(output)):
            self.assertTrue(output[n] == FIRST_PRIMES[n],
                            msg='Missing - {} - in generated prime list '.format(FIRST_PRIMES[n]))


if __name__ == '__main__':
    unittest.main()