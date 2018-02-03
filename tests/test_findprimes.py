
import unittest
from nprime import pyprime


class TestFindPrimes(unittest.TestCase):
    """ Tests for findprimes function """

    def test_lower_bigger_than_upper_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, pyprime.find_primes, 100, 50)

    def test_lower_equal_upper_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, pyprime.find_primes, 50, 50)

    def test_lower_is_equal_to_one_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, pyprime.find_primes, 1, 50)

    def test_lower_is_inferior_to_one_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, pyprime.find_primes, 0, 50)

    def test_lower_equal_upper_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, pyprime.find_primes, 50, 50)


if __name__ == '__main__':
    unittest.main()
