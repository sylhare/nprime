
import unittest
from tests import prime_testcase
from nprime import pyprime


class TestFermat(prime_testcase.positive_test_case(pyprime.fermat),
                 prime_testcase.negative_test_case(pyprime.fermat)):
    """ Tests for fermat function """
    pass


if __name__ == '__main__':
    unittest.main()
