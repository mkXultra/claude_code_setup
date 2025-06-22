import unittest
from fibonacci import fibonacci


class TestFibonacci(unittest.TestCase):
    
    def test_base_cases(self):
        """ベースケースのテスト"""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
    
    def test_small_numbers(self):
        """小さい数値のテスト"""
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)
        self.assertEqual(fibonacci(7), 13)
    
    def test_larger_numbers(self):
        """大きい数値のテスト"""
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(15), 610)
        self.assertEqual(fibonacci(20), 6765)
    
    def test_negative_input(self):
        """負の数の入力に対するエラーテスト"""
        with self.assertRaises(ValueError) as context:
            fibonacci(-1)
        self.assertIn("non-negative", str(context.exception))
        
        with self.assertRaises(ValueError):
            fibonacci(-10)
    
    def test_efficiency(self):
        """効率性のテスト（大きな数でも高速に計算できることを確認）"""
        # メモ化されているため、大きな数でも高速に計算可能
        result = fibonacci(100)
        self.assertEqual(result, 354224848179261915075)


if __name__ == '__main__':
    unittest.main()