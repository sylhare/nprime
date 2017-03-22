# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:34:49 2017

@author: Sylhare

"""


#Carmichael number often trigger false positive for the fermat algorithm
__carmichael = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]

#The key is the base, the list is the pseudoprimes of that base
__pseudoPrimes = {2: [2047, 3277, 4033, 4681, 8321], 
                  3: [121, 703, 1891, 3281, 8401, 8911],
                  4: [341, 1387, 2047, 3277, 4033, 4371],
                  5: [781, 1541, 5461, 5611, 7813],
                  6: [217, 481, 1111, 1261, 2701],
                  7: [25, 325, 703, 2101, 2353, 4525],
                  8: [9, 65, 481, 511, 1417, 2047],
                  9: [91, 121, 671, 703, 1541, 1729]}

def ppTest(function):
    """
    Test the function on a couple of pseudo primes numbers
    
    Returns a string with all the results
        True - passes the test
        False - fails the test
        
    """
    results = {}
    status = "\nPseudo Primes Test:\n"

    for key in __pseudoPrimes:
        results[key] = functionTest(function, __pseudoPrimes[key])
        status += "[" + passTest(results[key]) + "]: PseudoPrime #" \
                  + str(key) + "\n"
        
    return status
    
def carmiTest(function):
    """
    Test the function on the carmichael numbers
    Fermat and millerRabin usually fail this test
    
    Returns a string with the result
        True - passes the test
        False - fails the test
        
    """
    results = functionTest(function, __carmichael)
    status = "\nCarmichael Test:\n"
    status += "[" + passTest(results) + "]: Carmichael" 
    
    return status  
    
def functionTest(function, src):
    """
    Take a function and a source list of numbers to test on the function    
    
    Returns a list of tuples (the number tested, it's own result)
    """
    results = []
    for n in src:
        results.append((n, function(n)))
    
    return results

def passTest(results):
    """
    For Prime testing functions, in order to pass the test,
    the results should be a list of False    
    
    Return OK when pass the test, FAIL otherwise    
    """
    for n in results:
        if n[1]:
            return "FAIL"
    
    return " OK "
