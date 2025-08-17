"""
Coprime for the nprime package.

This module contains functions for working with coprime numbers,
greatest common divisors, and Euler's totient function.
"""


def gcd(a, b):
    """
    Calculate the Greatest Common Divisor of two numbers using Euclidean algorithm.
    
    Args:
        a (int): First integer
        b (int): Second integer
        
    Returns:
        int: Greatest common divisor of a and b
        
    Example:
        >>> gcd(12, 8)
        4
        >>> gcd(17, 13)
        1
        >>> gcd(25, 15)
        5
    """
    while b:
        a, b = b, a % b
    return abs(a)


def are_coprime(a, b):
    """
    Check if two numbers are coprime (their GCD is 1).
    
    Args:
        a (int): First integer
        b (int): Second integer
        
    Returns:
        bool: True if a and b are coprime, False otherwise
        
    Example:
        >>> are_coprime(9, 16)
        True
        >>> are_coprime(12, 8)
        False
        >>> are_coprime(17, 13)
        True
    """
    return gcd(a, b) == 1


def coprimes(n, upper=None):
    """
    Find all numbers that are coprime to n up to a given limit.
    If no upper limit is provided, returns coprimes up to n.
    
    Args:
        n (int): The number to find coprimes for
        upper (int, optional): Upper limit for search. Defaults to n.
        
    Returns:
        list: List of integers that are coprime to n
        
    Example:
        >>> coprimes(12, 20)
        [1, 5, 7, 11, 13, 17, 19]
        >>> coprimes(10)
        [1, 3, 7, 9]
        >>> coprimes(15, 20)
        [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    
    if upper is None:
        upper = n
    
    if not isinstance(upper, int) or upper < 1:
        raise ValueError("upper must be a positive integer")
    
    result = []
    for i in range(1, upper + 1):
        if are_coprime(n, i):
            result.append(i)
    
    return result


def coprime_pairs(upper):
    """
    Find all pairs of coprime numbers up to a given limit.
    
    Args:
        upper (int): Upper limit for the search
        
    Returns:
        list: List of tuples (a, b) where a and b are coprime and a <= b
        
    Example:
        >>> pairs = coprime_pairs(5)
        >>> len(pairs)
        10
        >>> (3, 4) in pairs
        True
        >>> (2, 4) in pairs
        False
    """
    if not isinstance(upper, int) or upper < 1:
        raise ValueError("upper must be a positive integer")
    
    pairs = []
    for a in range(1, upper + 1):
        for b in range(a, upper + 1):
            if are_coprime(a, b):
                pairs.append((a, b))
    
    return pairs


def euler_totient(n):
    """
    Calculate Euler's totient function φ(n), which counts the number of 
    integers from 1 to n that are coprime to n.
    
    Args:
        n (int): Positive integer
        
    Returns:
        int: Number of integers from 1 to n that are coprime to n
        
    Example:
        >>> euler_totient(9)
        6
        >>> euler_totient(12)
        4
        >>> euler_totient(17)
        16
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    
    if n == 1:
        return 1
    
    # Count numbers coprime to n
    count = 0
    for i in range(1, n + 1):
        if are_coprime(n, i):
            count += 1
    
    return count 