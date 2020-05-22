import unittest

from nprime.pyprime import trial_division as trial_division
from tests.prime_testcase import FIRST_PRIMES


class TestTrialDivision(unittest.TestCase):
    """ Tests for generate prime function """

    def test_001_is_not_integer_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertRaises(ValueError, trial_division, 3.8)

    def test_002_is_inferior_to_two_return_error(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertRaises(ValueError, trial_division, -1)

    def test_003_is_trial_division_showing_primes_and_composite(self):
        """ The trial_division should work for the first 10 numbers"""
        self.assertEqual({2: [4, 6, 8], 3: [6, 9], 5: [], 7: []}, trial_division(10))

    def test_004_are_all_keys_primes(self):
        """ Making sure that all keys from the trial_division are prime  """
        primes = list(trial_division(70).keys())
        primes.sort()
        self.assertEqual(FIRST_PRIMES, primes)


if __name__ == '__main__':
    unittest.main()
