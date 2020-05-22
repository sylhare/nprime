import unittest

from nprime.pyprime import generate_primes
from tests.prime_testcase import FIRST_PRIMES


class TestGeneratesPrimes(unittest.TestCase):
    """ Tests for generate prime function """

    def test_001_is_there_2_in_list_of_first_prime(self):
        """ there should only be 2 in the list, if limit is set to 2 """
        self.assertEqual([2], generate_primes(2))

    def test_002_inferior_to_two_return_nothing(self):
        """ No prime should be generated if upper is inferior to 2"""
        self.assertEqual([], generate_primes(1))

    def test_003_are_first_prime_all_generated(self):
        output = generate_primes(70)
        for n in range(0, len(output)):
            self.assertEqual(FIRST_PRIMES[n], output[n],
                              msg='Missing - {} - in generated prime list '.format(FIRST_PRIMES[n]))


if __name__ == '__main__':
    unittest.main()
