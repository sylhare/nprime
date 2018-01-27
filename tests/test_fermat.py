import unittest
from app import pyprime as p


class TestFermat(unittest.TestCase):

    __test_function = p.fermat

    def setUp(self):
        pass

    def test_is_zero_not_prime(self):
        """Is zero correctly determined not to be prime?"""
        self.assertFalse(self.__test_function(8))

    def test_is_two_prime(self):
        """Is two correctly determined to be prime?"""
        self.assertTrue(p.pyprime(2), msg='Two is prime!')

    def test_is_four_not_prime(self):
        """Is four correctly determined not to be prime?"""
        self.assertFalse(p.pyprime(4), msg='Four is not prime!')

    def test_negative_number(self):
        """Is a negative number correctly determined not to be prime?"""
        for index in range(-1, -10, -1):
            self.assertFalse(p.pyprime(index), msg='{} should not be determined to be prime'.format(index))

    def test_first_primes_prime(self):
        for n in t.FIRST_PRIMES:
            self.assertTrue(p.pyprime(n))

    def test_first_non_primes_not_prime(self):
        for n in t.FIRST_NOT_PRIMES:
            self.assertFalse(p.pyprime(n))

    def test_pseudoprimes_not_prime(self):
        for base, value in t.PSEUDO_PRIMES.items():
            for n in value:
                self.assertFalse(p.pyprime(n))

    def test_carmichael_numbers_not_prime(self):
        for n in t.CARMICHAEL:
            self.assertFalse(p.pyprime(n))

    def test_float_return_error_message(self):
        self.assertRaises(TypeError, p.pyprime, 3.8)

    def test_bool_return_error_message(self):
        self.assertRaises(TypeError, p.pyprime, True)

    def test_string_return_error_message(self):
        self.assertRaises(TypeError, p.pyprime, "three")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()