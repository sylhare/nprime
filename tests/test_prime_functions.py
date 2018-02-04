
import unittest
from tests.prime_testcase import make_test_case
from nprime import pyprime


class TestIsPrime(make_test_case(pyprime.is_prime)):
    """ Tests for miller rabin function """
    pass


class TestFermat(make_test_case(pyprime.fermat)):
    """ Tests for fermat function """
    pass


class TestMillerRabin(make_test_case(pyprime.miller_rabin)):
    """ Tests for miller rabin function """
    pass


if __name__ == '__main__':
    unittest.main()
