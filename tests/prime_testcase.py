"""
__author__=Sylhare

Make prime test case that can be reusable for any prime finding function
"""

import unittest

# First primes that the function should succeed at finding
FIRST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]

# First non prime that the function should confirm as not prime
FIRST_NOT_PRIMES = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28]

# Carmichael number often trigger false positive for the fermat algorithm
CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]

# The key is the base, the list is the pseudoprimes of that base
PSEUDO_PRIMES = {2: [2047, 3277, 4033, 4681, 8321],
                 3: [121, 703, 1891, 3281, 8401, 8911],
                 4: [341, 1387, 2047, 3277, 4033, 4371],
                 5: [781, 1541, 5461, 5611, 7813],
                 6: [217, 481, 1111, 1261, 2701],
                 7: [25, 325, 703, 2101, 2353, 4525],
                 8: [9, 65, 481, 511, 1417, 2047],
                 9: [91, 121, 671, 703, 1541, 1729]}


def make_test_case(prime_function):
    """Make prime test case"""

    class PrimeTestCase(unittest.TestCase):
        def test_001_is_two_prime(self):
            """Is two correctly determined to be prime?"""
            self.assertTrue(prime_function(2), msg='Two is prime!')

        def test_002_first_primes_prime(self):
            """ test if true for the first known primes """
            for n in FIRST_PRIMES:
                self.assertTrue(prime_function(n))

        def test_003_is_four_not_prime(self):
            """Is four correctly determined not to be prime?"""
            self.assertFalse(prime_function(4), msg='Four is not prime!')

        def test_004_first_non_primes_not_prime(self):
            """ test false for the first non primes """
            for n in FIRST_NOT_PRIMES:
                self.assertFalse(prime_function(n), msg='{} should not be determined to be prime'.format(n))

        def test_005_pseudoprimes_numbers_not_prime(self):
            """ test False for pseudo primes """
            for _, value in PSEUDO_PRIMES.items():
                for n in value:
                    self.assertFalse(prime_function(n), msg='{} should not be determined to be prime'.format(n))

        def test_006_carmichael_numbers_not_prime(self):
            """ Test false for carmichael numbers """
            for n in CARMICHAEL:
                self.assertFalse(prime_function(n), msg='{} should not be determined to be prime'.format(n))

    return PrimeTestCase


if __name__ == '__main__':
    unittest.main()
