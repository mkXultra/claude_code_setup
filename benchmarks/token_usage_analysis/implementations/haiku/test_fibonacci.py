import unittest
from fibonacci import fibonacci

class TestFibonacci(unittest.TestCase):
    def test_base_cases(self):
        """Test the base cases of the Fibonacci sequence"""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
    
    def test_known_values(self):
        """Test some known Fibonacci numbers"""
        test_cases = [
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (10, 55)
        ]
        for n, expected in test_cases:
            self.assertEqual(fibonacci(n), expected)
    
    def test_negative_input(self):
        """Test that negative inputs raise a ValueError"""
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            fibonacci(-10)

if __name__ == '__main__':
    unittest.main()