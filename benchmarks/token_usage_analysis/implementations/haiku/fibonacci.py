def fibonacci(n):
    """
    Calculate the nth Fibonacci number using memoization.
    
    Args:
        n (int): The index of the Fibonacci number to calculate (0-based).
    
    Returns:
        int: The nth Fibonacci number.
    
    Raises:
        ValueError: If n is negative.
    """
    # Check for negative input
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    
    # Memoization cache to store already calculated Fibonacci numbers
    memo = {}
    
    def fib(k):
        # Base cases
        if k == 0:
            return 0
        if k == 1:
            return 1
        
        # Check if result is already memoized
        if k in memo:
            return memo[k]
        
        # Calculate and memoize the result
        memo[k] = fib(k-1) + fib(k-2)
        return memo[k]
    
    return fib(n)