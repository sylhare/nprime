import unittest
from tests import prime_testcase
from nprime import pyprime


class TestMillerRabin(prime_testcase.positive_test_case(pyprime.miller_rabin),
                      prime_testcase.negative_test_case(pyprime.miller_rabin)):
    """ Tests for miller rabin function """
    pass


if __name__ == '__main__':
    unittest.main()
