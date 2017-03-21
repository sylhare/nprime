# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:16:46 2017
@author: sylhare

"""

import random


### Primarity testing functions ###

def isPrime(n):
    """
    Check if the number "n" is prime, with n > 1.
    
    Returns a boolean, True if n is prime.
        
    """    
    for i in range(2, int(pow(n, 0.5)) + 1):
        if(n%i == 0):
            return False     
            
    return True 


def fermat(n, t=10):
    """ 
    Probabilistic algorithm
    Taking "t" randoms "a" and testing the Fermat's theorem on number "n" > 1
    
    Prime probability is right is 1 - 1/(2^t)    
    Returns a boolean: True if n passes the test.
        
    """
      
    for k in range(0, t):
        a = random.randrange(1, n)
        x = pow(a, n-1, n) #(a^(n-1)) modulo n
        
        if x == 1:
            prime = True    #/!\ Probable prime
        else:
            prime = False
            break
        
    return prime

   
def millerRabin(n, t=10):
    """
    A probabilistic algorithm which determines 
    whether a given number (n > 1) is prime or not. 
    The millerRabin test is repeated t times to get more accurate results.
    
    Returns a boolean: True if n passes the test   
    
    """
    if n == 2:
        prime = True #To normalize and make the algorythm works with 2
    else:
        prime = False #All other even number will output false
    
    #Step 1: Have n-1 = 2^s * m (with m odd, and s number of twos factored)
    d = n - 1
    s = 0
    while (d % 2 == 0): 
        d //= 2 # d equals to quotient of d divided 2            
        s += 1  # s > 1 when n is odd
    
    for k in range(0, t):
        #Step 2: test (a^d)^2^r ≡ 1 mod n for all r
        a = random.randrange(1, n)
        for r in range(0, s):
            x = pow(a, d * pow(2, s), n)
            if x == 1 or x == -1:
                prime = True        #Should be true for all a
            else:
                return False        #When not true, it's not prime for sure
            
    return prime     #/!\ Probable prime
   
   
### Prime generating functions ###

def genPrimes(upper=0):
    """
    Generate a list of primes from 2 to a set limit
    It reuses the sieve of Eratosthenes
    
    Returns a list of integer.
        
    """
    primes=[2] 
        
    for n in range(3, upper + 1):    
        k = 0 
        
    #We only check if n is divided by the previous primes
        while (primes[k] <= pow(n, 0.5) and n%primes[k] != 0):
            k += 1
            
    #if a number has no dividers, last prime[k] of loop is over n's squareroot   
        if (pow(n, 0.5) < primes[k]): 
            primes.append(n)  
            
    return primes       


def findPrimes(lower, upper, primeTest=isPrime):
    """
    Find the number of primes between lower and upper range.
    We should have 2 <= lower < upper.
    
    primeTest determines the function used to test the primality of the number
    primeTest is by default isPrime() and should return a boolean    
    
    Returns a list of integer.
    
    """
    #assert will trigger an error if the input is not correct
    assert 2 <= lower and lower <= upper
    
    primes = []
    
    for n in range(lower, upper + 1):
        if primeTest(n):
            primes.append(n)
            
    return primes  
