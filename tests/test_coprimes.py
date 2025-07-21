import unittest
from nprime.coprime import gcd, are_coprime, coprimes, coprime_pairs, euler_totient


class TestCoprimes(unittest.TestCase):
    """Test cases for coprime functions"""

    def test_gcd_basic(self):
        """Test basic GCD calculations"""
        self.assertEqual(gcd(12, 8), 4)
        self.assertEqual(gcd(17, 13), 1)
        self.assertEqual(gcd(25, 15), 5)
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(5, 0), 5)

    def test_gcd_edge_cases(self):
        """Test GCD edge cases"""
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(7, 7), 7)
        self.assertEqual(gcd(-12, 8), 4)
        self.assertEqual(gcd(12, -8), 4)
        self.assertEqual(gcd(-12, -8), 4)

    def test_are_coprime_basic(self):
        """Test basic coprime checks"""
        self.assertTrue(are_coprime(9, 16))
        self.assertFalse(are_coprime(12, 8))
        self.assertTrue(are_coprime(17, 13))
        self.assertTrue(are_coprime(15, 8))
        self.assertFalse(are_coprime(15, 9))

    def test_are_coprime_edge_cases(self):
        """Test coprime edge cases"""
        self.assertTrue(are_coprime(1, 5))
        self.assertTrue(are_coprime(5, 1))
        self.assertTrue(are_coprime(1, 1))
        self.assertFalse(are_coprime(6, 9))

    def test_coprimes_basic(self):
        """Test finding coprimes of a number"""
        # Test coprimes of 12 up to 20
        result = coprimes(12, 20)
        expected = [1, 5, 7, 11, 13, 17, 19]
        self.assertEqual(result, expected)
        
        # Test coprimes of 10 up to 10
        result = coprimes(10)
        expected = [1, 3, 7, 9]
        self.assertEqual(result, expected)
        
        # Test coprimes of 15 up to 20
        result = coprimes(15, 20)
        expected = [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]
        self.assertEqual(result, expected)

    def test_coprimes_small_numbers(self):
        """Test coprimes for small numbers"""
        # Coprimes of 1
        self.assertEqual(coprimes(1, 5), [1, 2, 3, 4, 5])
        
        # Coprimes of prime numbers should be all numbers less than them
        prime_7_coprimes = coprimes(7)
        self.assertEqual(prime_7_coprimes, [1, 2, 3, 4, 5, 6])

    def test_coprimes_error_handling(self):
        """Test error handling in coprimes function"""
        with self.assertRaises(ValueError):
            coprimes(0)
        with self.assertRaises(ValueError):
            coprimes(-5)
        with self.assertRaises(ValueError):
            coprimes(5, 0)
        with self.assertRaises(ValueError):
            coprimes(5, -3)

    def test_coprime_pairs_basic(self):
        """Test finding coprime pairs"""
        pairs = coprime_pairs(5)
        self.assertEqual(len(pairs), 10)
        self.assertIn((1, 1), pairs)
        self.assertIn((1, 2), pairs)
        self.assertIn((1, 3), pairs)
        self.assertIn((1, 4), pairs)
        self.assertIn((1, 5), pairs)
        self.assertIn((2, 3), pairs)
        self.assertIn((2, 5), pairs)
        self.assertIn((3, 4), pairs)
        self.assertIn((3, 5), pairs)
        self.assertIn((4, 5), pairs)
        
        # These should NOT be in pairs
        self.assertNotIn((2, 4), pairs)
        self.assertNotIn((3, 6), pairs)

    def test_coprime_pairs_small(self):
        """Test coprime pairs for small numbers"""
        pairs = coprime_pairs(3)
        expected = [(1, 1), (1, 2), (1, 3), (2, 3)]
        self.assertEqual(pairs, expected)

    def test_coprime_pairs_error_handling(self):
        """Test error handling in coprime_pairs function"""
        with self.assertRaises(ValueError):
            coprime_pairs(0)
        with self.assertRaises(ValueError):
            coprime_pairs(-5)

    def test_euler_totient_basic(self):
        """Test Euler's totient function"""
        self.assertEqual(euler_totient(1), 1)
        self.assertEqual(euler_totient(9), 6)  # coprimes: 1,2,4,5,7,8
        self.assertEqual(euler_totient(12), 4)  # coprimes: 1,5,7,11
        self.assertEqual(euler_totient(17), 16)  # prime, so all numbers 1-16

    def test_euler_totient_primes(self):
        """Test Euler's totient for prime numbers"""
        # For prime p, φ(p) = p - 1
        self.assertEqual(euler_totient(2), 1)
        self.assertEqual(euler_totient(3), 2)
        self.assertEqual(euler_totient(5), 4)
        self.assertEqual(euler_totient(7), 6)
        self.assertEqual(euler_totient(11), 10)

    def test_euler_totient_powers_of_primes(self):
        """Test Euler's totient for powers of primes"""
        # φ(4) = φ(2²) should be 2
        self.assertEqual(euler_totient(4), 2)  # coprimes: 1,3
        # φ(8) = φ(2³) should be 4
        self.assertEqual(euler_totient(8), 4)  # coprimes: 1,3,5,7
        # φ(9) = φ(3²) should be 6
        self.assertEqual(euler_totient(9), 6)  # coprimes: 1,2,4,5,7,8

    def test_euler_totient_error_handling(self):
        """Test error handling in euler_totient function"""
        with self.assertRaises(ValueError):
            euler_totient(0)
        with self.assertRaises(ValueError):
            euler_totient(-5)


if __name__ == '__main__':
    unittest.main() 