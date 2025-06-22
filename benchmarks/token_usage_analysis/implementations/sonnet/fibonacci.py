def fibonacci(n):
    """
    n番目のフィボナッチ数を返す（メモ化使用）
    
    Args:
        n (int): フィボナッチ数列のインデックス（0番目は0、1番目は1）
    
    Returns:
        int: n番目のフィボナッチ数
    
    Raises:
        ValueError: nが負の数の場合
    """
    if n < 0:
        raise ValueError("負の数は受け付けません")
    
    memo = {}
    
    def _fibonacci_helper(n):
        if n in memo:
            return memo[n]
        
        if n == 0:
            memo[n] = 0
        elif n == 1:
            memo[n] = 1
        else:
            memo[n] = _fibonacci_helper(n - 1) + _fibonacci_helper(n - 2)
        
        return memo[n]
    
    return _fibonacci_helper(n)