# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:16:46 2017

@author: sylhare
"""

def isPrime(n):
    """
    Check if the number "n" is prime, with n >= 2.
    
    Returns a boolean.
        
    """    
    for i in range(2, int(n**0.5) + 1):
        if(n%i == 0):
            return False     
            
    return True 


def genPrimes(upper=0):
    """
    Generate a list of primes from 2 to a set limit
    
    Returns a list of integer.
        
    """
    primes=[2] 
        
    for n in range(3, upper + 1):    
        k = 0 
        
    #We only check if n is divided by the previous primes
        while (primes[k] <= n**0.5 and n%primes[k] != 0):
            k += 1
            
    #if a number has no dividers, last prime[k] of loop is over n's squareroot   
        if (n**0.5 < primes[k]): 
            primes.append(n)  
           
    return primes  


def findPrimes(lower, upper, primeTest=isPrime):
    """
    Find the number of primes between lower and upper range.
    It should be lower < upper with lower >= 2.
    
    primeTest determines the function used to test the primality of the number
    primeTest is by default isPrime() and should return a boolean    
    
    Returns a list of integer.
    
    """
    #assert will trigger an error if the input is not correct
    assert lower <= upper and lower >= 2, "Should be 2 <= lower < upper"     
    
    primes = []
    
    for n in range(lower, upper + 1):
        if primeTest(n):
            primes.append(n)
            
    return primes  
