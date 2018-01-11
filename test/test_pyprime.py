import unittest
import app.pyprime as p


class TestPyPrime(unittest.TestCase):


    def test_is_prime_with_3(self):
        result = p.is_prime(3)
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()