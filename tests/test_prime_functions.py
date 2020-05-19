import unittest

from nprime.pyprime import is_prime, fermat, miller_rabin
from tests.prime_testcase import make_test_case


class TestIsPrime(make_test_case(is_prime)):
    """ Tests for miller rabin function """
    pass


class TestFermat(make_test_case(fermat)):
    """ Tests for fermat function """
    pass


class TestMillerRabin(make_test_case(miller_rabin)):
    """ Tests for miller rabin function """
    pass


if __name__ == '__main__':
    unittest.main()
