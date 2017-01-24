# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:16:46 2017
@author: sylhare

Here are a bit of information to understand some of the algorithms

Congruence :
------------
 "≡" means congruent
   a ≡ b (mod m) implies that m/(a-b), ∃ k ∈ Z that verifies a = kn + b
   
 which implies:
   a ≡ 0 (mod n) <-> a = kn <-> "a" is divisible by "n" 

Fermart's Theorem
-----------------
 if n is prime then ∀ a ∈[1, ..., n-1]
   a^(n-1) ≡ 1 (mod n) ⇔ a^(n-1) = kn + 1
   
"""

import random


### Primarity testing functions ###

def isPrime(n):
    """
    Check if the number "n" is prime, with n >= 2.
    
    Returns a boolean, True if n is prime.
        
    """    
    for i in range(2, int(n**0.5) + 1):
        if(n%i == 0):
            return False     
            
    return True 


def fermatTest(n, t=10):
    """ 
    Probabilistic algorithm
    Taking "t" randoms "a" and testing the Fermat's theorem on number "n" >= 2
    
    Prime probability is right is 1 - 1/(2^t)    
    Returns a boolean: True if n passes the test.
        
    """
      
    for k in range(0, t):
        a = random.randint(1, n-1, 1)
        x = pow(a, n-1, n) #(a^(n-1)) modulo n
        
        if x == 1:
            prime = True    #/!\ Probable prime
        else:
            prime = False
            break
        
    return prime


### Prime generating functions ###

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
