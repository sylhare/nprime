# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:16:46 2017

@author: sylhare

"""

import math
import random


# -- Prime testing functions -- #
def is_prime(n):
    """
    Check if the number "n" is prime, with n > 1.

    Returns a boolean, True if n is prime.

    Example:
        >>> is_prime(101)
        True
        >>> is_prime(102)
        False
        >>> is_prime(103)
        True
    """
    for i in range(2, int(pow(n, 0.5)) + 1):
        if n % i == 0:
            return False
    return True


def fermat(n, t=100):
    """
    Probabilistic algorithm
    Taking "t" randoms "a" and testing the Fermat's theorem on number "n" > 1

    Prime probability is right is 1 - 1/(2^t)
    Returns a boolean: True if n passes the tests.

    Example:
        >>> fermat(101)
        True
        >>> fermat(102)
        False
        >>> fermat(103)
        True
    """
    for _ in range(0, t):
        a = random.randrange(1, n)
        x = pow(a, n - 1, n)  # (a^(n-1)) modulo n

        if x == 1:
            prime = True  # /!\ Probable prime
        else:
            prime = False
            break

    return prime


def miller_rabin(n, t=100):
    """
    A probabilistic algorithm which determines
    whether a given number (n > 1) is prime or not.
    The miller_rabin tests is repeated t times to get more accurate results.

    Returns a boolean: True if n passes the tests

    Example:
        >>> miller_rabin(101)
        True
        >>> miller_rabin(102)
        False
        >>> miller_rabin(103)
        True
    """
    if n == 2:
        prime = True  # To normalize and make the algorythm works with 2
    else:
        prime = False  # All other even number will output false

    # Step 1: Have n-1 = 2^s * m (with m odd, and s number of twos factored)
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2  # d equals to quotient of d divided 2
        s += 1  # s > 1 when n is odd

    for _ in range(0, t):
        #  Step 2: test (a^d)^2^r ≡ 1 mod n for all r
        a = random.randrange(1, n)
        for _ in range(0, s):
            x = pow(a, d * pow(2, s), n)
            if x == 1 or x == -1:
                prime = True  # Should be true for all a
            else:
                return False  # When not true, it's not prime for sure

    return prime  # /!\ Probable prime


# Prime generating functions #
def generate_primes(upper=0):
    """
    Generate a list of primes from 2 to a set limit
    It re-uses the sieve of Eratosthenes, but does not tag composites

    Returns a list of integer.

    Example:
        >>> upper = 50
        >>> primes = list(generate_primes(upper))
        >>> print(primes)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """

    if upper >= 2:
        primes = [2]

        for n in range(3, upper + 1):
            # We only check if n is divided by the previous primes
            sqrt_n = pow(n, 0.5)
            divisor = None
            for p in primes:
                if sqrt_n < p:
                    break
                if n % p == 0:
                    divisor = p
                    break  # not prime
            if divisor is None:
                primes.append(n)  # must be prime
    else:
        primes = []

    return primes


def sieve_eratosthenes(upper):
    """
    Implementation of the sieve of erathostenes that discover the primes and their composite up to a limit.

    :return: a dictionary,
                the key are the primes up to n
                the value is the list of composites of these primes up to n

    Example:
        >>> upper = 10
        >>> sieve_eratosthenes(upper)
        {2: [4, 6, 8, 10], 3: [9], 5: [], 7: []}
    """
    primes = {}
    composites = set()
    for p in range(2, upper + 1):
        if p not in composites:
            primes[p] = list(range(p * p, upper + 1, p))
            composites.update(primes[p])

    return primes


def trial_division(upper):
    """
    Implementation of the trial division that discover the primes and all their divider up to a limit.

    :return: a dictionary,
                the key are the primes up to n
                the value is the list of composites of these primes up to n

    Example:
        >>> upper = 10
        >>> trial_division(upper)
        {2: [4, 6, 8], 3: [6, 9], 5: [], 7: []}
    """

    if isinstance(upper, int) and upper >= 2:
        primes = {2: []}

        for n in range(3, upper):
            prime = True

            for key in primes:
                if n % key == 0:
                    primes[key].append(n)
                    prime = False

            if prime:
                primes[n] = []

    else:
        raise ValueError(" Input must be an integer > 2")

    return primes


def find_primes(lower, upper, prime_test_function=is_prime):
    """
    Find the number of primes between lower and upper range.
    We should have 1 < lower < upper.

    primeTest determines the function used to tests the prime of the number
    primeTest is by default is_prime() and should return a boolean

    Returns a list of prime integer.

    Example:
        >>> upper = 100
        >>> lower = 2
        >>> find_primes(lower, upper)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    """
    if upper <= lower or lower <= 1:
        raise ValueError("We should have 1 < lower < upper")

    primes = []

    for n in range(lower, upper + 1):
        if prime_test_function(n):
            primes.append(n)

    return primes


# Other functions #
def pyprime(n, func=is_prime):
    """
    Function that will encapsulate and tests n before doing function(n)
    It is mostly to encapsulate the primality testing functions
    Basically making sure that:
        n is a number
        n > 1

    Example:
        >>> pyprime(0, is_prime)
        False
        >>> pyprime(29, is_prime)
        True
    """
    # assert will trigger an error if the input is not correct
    if type(n) is int:
        if n > 1:
            return func(n)
        else:
            return False
    else:
        raise TypeError("n should be an integer")


# Graphical Prime functions #
def sacks(upper=1000, prime_test_function=pyprime):  # pragma: no cover
    """
    Generate the sack diagram values up to a set limit (upper)

    primeTest determines the function used to tests the primality of the number
    primeTest is by default is_prime() and should return a boolean

    Returns tho lists:
        1- The none prime polar coordinates: coord
        2- The prime polar coordinates: prime_coord

    Example:
        >>> coord, prime_coord = sacks(100)
        >>> assert len(prime_coord) == 25
        >>> assert len(coord) == 75
    """
    coord = []  # Normal numbers' polar value
    prime_coord = []  # Prime numbers' polar value

    for i in range(0, upper):  # A rotation is made for each perfect square,
        theta = math.sqrt(i) * 2 * math.pi  # i=1 theta= 2pi for a given i, angle=(i*theta)/1
        r = math.sqrt(i)

        if prime_test_function(i):
            prime_coord.append((theta, r))
        else:
            coord.append((theta, r))
    return coord, prime_coord


def ulam(upper=1000, edge=4, prime_test_function=pyprime):  # pragma: no cover
    """
    Ulam's spiral aim to represent the primes and none primes in a spiral way

    edge (edge>3) determines the polygone size by the number of edges, 3 triangle, 4 rectangle, 5 Pentagone ...
    For odd number of edge, the spiral gets misaligned

    primeTest determines the function used to tests the primality of the number
    primeTest is by default is_prime() and should return a boolean

    Returns tho lists:
        1- The none prime polar coordinates: coord
        2- The prime polar coordinates: prime_coord

    Example:
        >>> coord, prime_coord = sacks(100)
        >>> assert len(prime_coord) == 25
        >>> assert len(coord) == 75
    """
    theta = 0  # Keep track of the spiral rotation
    psi = math.radians(360 / edge)  # Angle of the polygone's corner

    turn = 3  # Threshold that indicates to turn at the end of each edge's length
    length = 0  # length of the edge, gets bigger as it spirals
    spiral = 2  # Threshold that indicates when to increase the length of an edge
    spiral_increment = int(edge / 2)  # when the edge length has to go up to spiral

    coord = [(0, 0)]  # Other numbers' coordinates
    prime_coord = []  # Primes' coordinates
    x = 0
    y = 0

    for i in range(2, upper):
        if i == spiral:
            length += 1
            spiral = length * spiral_increment + i

        if i == turn:
            theta += psi
            turn = i + length

        x += math.cos(theta)
        y += math.sin(theta)

        if prime_test_function(i):
            prime_coord.append((x, y))
        else:
            coord.append((x, y))

    return coord, prime_coord
