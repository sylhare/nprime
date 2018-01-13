import unittest


def function_a(any_input):
    if any_input == "input 1":
        result = False
    else:
        result = True

    return result


class AbstractTestCase():

    def test_g001_generic_input_one(self):
        result = self.function("input 1")
        self.assertFalse(result)

    def test_g002_generic_input_two(self):
        result = self.function("input 2")
        self.assertTrue(result)


class TestsFunctionA(unittest.TestCase):

    def setUp(self):
        self.function = function_a

    def test_a001_specific_input(self):
        result = self.assertTrue(self.function("specific input"))
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()