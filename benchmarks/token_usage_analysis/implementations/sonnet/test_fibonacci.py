import unittest
from fibonacci import fibonacci


class TestFibonacci(unittest.TestCase):
    
    def test_base_cases(self):
        """基本ケースのテスト"""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
    
    def test_small_numbers(self):
        """小さな数値のテスト"""
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)
        self.assertEqual(fibonacci(7), 13)
    
    def test_larger_numbers(self):
        """大きな数値のテスト"""
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(15), 610)
        self.assertEqual(fibonacci(20), 6765)
    
    def test_negative_input(self):
        """負の数の入力テスト"""
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            fibonacci(-10)
    
    def test_error_message(self):
        """エラーメッセージのテスト"""
        with self.assertRaisesRegex(ValueError, "負の数は受け付けません"):
            fibonacci(-1)


if __name__ == '__main__':
    unittest.main()