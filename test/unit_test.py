# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:34:49 2017

@author: Sylhare

"""

import pyprime as p

#Carmichael number often trigger false positive for the fermat algorithm
CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341]

#The key is the base, the list is the pseudoprimes of that base
PSEUDO_PRIMES = {2: [2047, 3277, 4033, 4681, 8321],
                 3: [121, 703, 1891, 3281, 8401, 8911],
                 4: [341, 1387, 2047, 3277, 4033, 4371],
                 5: [781, 1541, 5461, 5611, 7813],
                 6: [217, 481, 1111, 1261, 2701],
                 7: [25, 325, 703, 2101, 2353, 4525],
                 8: [9, 65, 481, 511, 1417, 2047],
                 9: [91, 121, 671, 703, 1541, 1729]}

#### Testing functions ####
def unit_test(function):
    """
    Perform all of the tests

    Return a string with all of the results

    """
    status = "\n----- Unit Tests -----\n"

    status += ppTest(function)
    status += carmiTest(function)

    status += "\n\n----------------------\n"

    return status


def ppTest(function):
    """
    Test the function on a couple of pseudo primes numbers

    Returns a string with all the results
        True - passes the test
        False - fails the test

    """
    results = {}
    status = "\nPseudo Primes Test:\n"

    for key in PSEUDO_PRIMES:
        results[key] = functionTest(function, PSEUDO_PRIMES[key])
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
    results = functionTest(function, CARMICHAEL)
    status = "\nCarmichael Test:\n"
    status += "[" + passTest(results) + "]: Carmichael"

    return status


def isUniform(lower=2, upper=1000):
    """
    For all the fonction of pyprime, check if they generate the same
    prime numbers as the isPrime function

    Returns True or the results if False

    """
    results = {'ref2':[], 'fermat':[], 'millerRabin':[]}
    ref1 = p.findPrimes(lower, upper)
    ref2 = p.genPrimes(upper)
    fermat = p.findPrimes(lower, upper, p.fermat)
    millerRabin = p.findPrimes(lower, upper, p.millerRabin)

    #Testing if we have the same primes from ref1 in all other functions
    for n in ref1:
        if n not in ref2:
            results['ref2'].append(n)
        if n not in fermat:
            results['fermat'].append(n)
        if n not in millerRabin:
            results['millerRabin'].append(n)

    #Making sure there's more detected primes than in ref1
    for key in results:
        results[key].append(len(results[key]))

        if results[key] != [0]:
            return results

    return True



#### Sub fonctions to create the tests ####
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
