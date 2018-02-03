import unittest
from tests import prime_testcase
from nprime import pyprime


class TestPyPrime(prime_testcase.positive_test_case(pyprime.pyprime),
                  prime_testcase.negative_test_case(pyprime.pyprime)):
    """ test for pyprime """

    def setUp(self):
        """ Set up of the tests """
        pass

    def test_float_return_error_message(self):
        """ An error message is raised for a float """
        self.assertRaises(TypeError, pyprime.pyprime, 3.8)

    def test_bool_return_error_message(self):
        """ An error message is raised for a bool """
        self.assertRaises(TypeError, pyprime.pyprime, True)

    def test_string_return_error_message(self):
        """ An error message is raised for a String"""
        self.assertRaises(TypeError, pyprime.pyprime, "three")

    def tearDown(self):
        """ tear down of the tests """
        pass


if __name__ == '__main__':
    unittest.main()
