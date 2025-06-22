def fibonacci(n):
    """
    n番目のフィボナッチ数を返す関数（メモ化を使用）
    
    Args:
        n: フィボナッチ数列のインデックス（0以上の整数）
        
    Returns:
        n番目のフィボナッチ数
        
    Raises:
        ValueError: nが負の数の場合
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # メモ化用の辞書
    memo = {}
    
    def fib_helper(num):
        # ベースケース
        if num == 0:
            return 0
        if num == 1:
            return 1
        
        # メモ化された値があれば返す
        if num in memo:
            return memo[num]
        
        # 計算してメモ化
        result = fib_helper(num - 1) + fib_helper(num - 2)
        memo[num] = result
        return result
    
    return fib_helper(n)