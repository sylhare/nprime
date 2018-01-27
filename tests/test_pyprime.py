import unittest

from app import pyprime

# First primes that the function should succeed at finding
FIRST_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]

# First non prime that the function should confirm as not prime
FIRST_NOT_PRIMES = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28]

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


class CustomAssertions():
    """assertTrue and assertFalse method for lists,
    keeping the unittest.TestCase CamelCase format"""

    def assertTrueList(self, list_to_test):
        for n in list_to_test:
            self.assertTrue(n)

    def assertFalseList(self, list_to_test):
        for n in list_to_test:
            self.assertFalse(n)


class TestPyPrime(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_zero_not_prime(self):
        """Is zero correctly determined not to be prime?"""
        self.assertFalse(pyprime.pyprime(0))

    def test_is_two_prime(self):
        """Is two correctly determined to be prime?"""
        self.assertTrue(pyprime.pyprime(2), msg='Two is prime!')

    def test_is_four_not_prime(self):
        """Is four correctly determined not to be prime?"""
        self.assertFalse(pyprime.pyprime(4), msg='Four is not prime!')

    def test_negative_number(self):
        """Is a negative number correctly determined not to be prime?"""
        for index in range(-1, -10, -1):
            self.assertFalse(pyprime.pyprime(index), msg='{} should not be determined to be prime'.format(index))

    def test_first_primes_prime(self):
        for n in FIRST_PRIMES:
            self.assertTrue(pyprime.pyprime(n))

    def test_first_non_primes_not_prime(self):
        for n in FIRST_NOT_PRIMES:
            self.assertFalse(pyprime.pyprime(n))

    def test_pseudoprimes_not_prime(self):
        for _, value in PSEUDO_PRIMES.items():
            for n in value:
                self.assertFalse(pyprime.pyprime(n))

    def test_carmichael_numbers_not_prime(self):
        for n in CARMICHAEL:
            self.assertFalse(pyprime.pyprime(n))

    def test_float_return_error_message(self):
        self.assertRaises(TypeError, pyprime.pyprime, 3.8)

    def test_bool_return_error_message(self):
        self.assertRaises(TypeError, pyprime.pyprime, True)

    def test_string_return_error_message(self):
        self.assertRaises(TypeError, pyprime.pyprime, "three")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
