# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:16:46 2017

@author: sylhare
"""
def isPrime(n):
    """
    Check if the number "n" is prime.
    Returns a boolean.
        
    """
    if (type(n) is not int or n<2  ):
        return False
        
    else:    
        for i in range (2, int(n**0.5+1)):
            if(n%i==0):
                return False
        return True     
