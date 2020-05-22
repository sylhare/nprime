import unittest

from nprime.pyprime import find_primes
from tests.prime_testcase import FIRST_PRIMES


class TestFindPrimes(unittest.TestCase):
    """ Tests for findprimes function """

    def test_001_lower_bigger_than_upper_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, find_primes, 100, 50)

    def test_002_lower_is_equal_to_one_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, find_primes, 1, 50)

    def test_003_lower_is_inferior_to_one_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, find_primes, 0, 50)

    def test_004_lower_equal_upper_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(ValueError, find_primes, 50, 50)

    def test_005_are_first_prime_all_discovered(self):
        """ Test that first primes are found """
        output = find_primes(2, 70)
        for n in range(0, len(output)):
            self.assertEqual(FIRST_PRIMES[n], output[n],
                             msg='Missing - {} - in generated prime list '.format(FIRST_PRIMES[n]))

    def test_006_are_primes_found_in_interval(self):
        """ Test that primes are found in a different interval """
        prime_list_1000_to_1100 = [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
                                   1087, 1091, 1093, 1097]
        self.assertTrue(find_primes(1000, 1100) == prime_list_1000_to_1100)

    def test_007_find_no_primes_when_no_primes(self):
        """ Test that it founds no primes in an interval with no primes """
        self.assertTrue(find_primes(370270, 370370) == [])


if __name__ == '__main__':
    unittest.main()
