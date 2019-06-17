# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:23:52 2017

@author: sylhare

"""

from demo import custom_unit_testing as ut
from nprime import pyprime as p


def main():
    """ example of the prime function and custom tests """
    # Demo of the Primary testing functions
    print(p.is_prime(7))
    print(p.fermat(7))
    print(p.miller_rabin(7))

    # Demo of the Prime generating functions
    print(p.generate_primes(7))
    print(p.find_primes(2, 7, p.fermat))

    # Demo of the custom_test functions
    print(ut.custom_test(p.is_prime))

    # Demo of Graphical Prime functions
    p.sacks_plot()
    p.ulam_plot()


if __name__ == '__main__':
    main()
