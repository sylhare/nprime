# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:16:46 2017

@author: sylhare

"""

import random
import math
import matplotlib.pyplot as plt


# -- Primarity testing functions -- #
def is_prime(n):
    """
    Check if the number "n" is prime, with n > 1.

    Returns a boolean, True if n is prime.

    """
    for i in range(2, int(pow(n, 0.5)) + 1):
        if n % i == 0:
            return False
    return True


def eratosthenes(n):
    """
    :return: a boolean, True if n is prime
    """

    return False


def fermat(n, t=10):
    """
    Probabilistic algorithm
    Taking "t" randoms "a" and testing the Fermat's theorem on number "n" > 1

    Prime probability is right is 1 - 1/(2^t)
    Returns a boolean: True if n passes the tests.

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


def miller_rabin(n, t=10):
    """
    A probabilistic algorithm which determines
    whether a given number (n > 1) is prime or not.
    The miller_rabin tests is repeated t times to get more accurate results.

    Returns a boolean: True if n passes the tests

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
    It reuses the sieve of Eratosthenes

    Returns a list of integer.

    """
    primes = [2]

    for n in range(3, upper + 1):
        k = 0

        # We only check if n is divided by the previous primes
        while primes[k] <= pow(n, 0.5) and n % primes[k] != 0:
            k += 1

        # if a number has no dividers, last prime[k] of loop is over n's square root
        if pow(n, 0.5) < primes[k]:
            primes.append(n)

    return primes


def find_primes(lower, upper, prime_test_function=is_prime):
    """
    Find the number of primes between lower and upper range.
    We should have 1 < lower < upper.

    primeTest determines the function used to tests the primality of the number
    primeTest is by default is_prime() and should return a boolean

    Returns a list of integer.

    """
    if 1 > lower >= upper:
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
def sacks(upper=1000, prime_test_function=pyprime):
    """
    Generate the sack diagram values up to a set limit (upper)

    primeTest determines the function used to tests the primality of the number
    primeTest is by default is_prime() and should return a boolean

    Returns tho lists:
        1- The none prime polar coordinates: coord
        2- The prime polar coordinates: pricoo

    """
    coord = []  # Normal numbers' polar value
    pricoo = []  # Prime numbers' polar value

    for i in range(0, upper):  # A rotation is made for each perfect square,
        theta = math.sqrt(i) * 2 * math.pi  # i=1 theta= 2pi for a given i, angle=(i*theta)/1
        r = math.sqrt(i)

        if prime_test_function(i):
            pricoo.append((theta, r))
        else:
            coord.append((theta, r))
    return coord, pricoo


# noinspection PyCompatibility
def sacks_plot(upper=10000, prime_test_function=pyprime):
    """
    Render the sacks_plot from the sacks function.
    By default the coord is plot in white and the pricoo in black

    Return a polar plot of the sacks' diagram

    """
    coord, pricoo = sacks(upper, prime_test_function)

    plt.figure()
    ax = plt.subplot(111, projection='polar', facecolor='white')
    plt.title('Sacks\' Diagram', loc='right')
    # noinspection PyCompatibility
    ax.plot(*zip(*coord), "w+", markersize=1)
    ax.plot(*zip(*pricoo), "ko", markersize=2)
    plt.show()


def ulam(upper=1000, edge=4, prime_test_function=pyprime):
    """
    Ulam's spiral aim to represent the primes and none primes in a spiral way

    edge (edge>3) determines the polygone size by the number of edges, 3 triangle, 4 rectangle, 5 Pentagone ...
    For odd number of edge, the spiral gets misaligned

    primeTest determines the function used to tests the primality of the number
    primeTest is by default is_prime() and should return a boolean

    Returns tho lists:
        1- The none prime polar coordinates: coord
        2- The prime polar coordinates: pricoo

    """
    theta = 0  # Keep track of the spiral rotation
    psi = math.radians(360 / edge)  # Angle of the polygone's corner

    turn = 3  # Threshold that indicates to turn at the end of each edge's length
    length = 0  # length of the edge, gets bigger as it spirals
    spiral = 2  # Threshold that indicates when to increase the length of an edge
    spiral_increment = int(edge / 2)  # when the edge length has to go up to spiral

    coord = [(0, 0)]  # Other numbers' coordinates
    pricoo = []  # Primes' coordinates
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
            pricoo.append((x, y))
        else:
            coord.append((x, y))

    return coord, pricoo


def ulam_plot(upper=10000, edge=4, prime_test_function=pyprime):
    """
    Render the sacks_plot from the ulam function.
    By default the coord is plot in white and the pricoo in black

    Return a polar plot of the ulam's spiral

    """
    coord, pricoo = ulam(upper, edge, prime_test_function)

    plt.figure()
    plt.title('Ulam\'s sprial', loc='right')
    plt.plot(*zip(*coord), 'w+', markersize=1)
    plt.plot(*zip(*pricoo), 'ko', markersize=2)
    plt.grid(True)
    plt.show()
