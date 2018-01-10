import unittest
from app.pyprime import Pyprime as p


class TestPyPrime(unittest.TestCase):

    def test_is_prime(self):
        result = p.is_prime(3)
        self.assertEqual(True, result)