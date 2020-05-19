"""
nprime main application package

Auto generate command:
    mkinit nprime/__init__.py -w
"""

from nprime import pyprime

from nprime.pyprime import (fermat, find_primes, generate_primes, is_prime,
                            miller_rabin, pyprime, sacks, sieve_eratosthenes,
                            trial_division, ulam, )

__all__ = ['fermat', 'find_primes', 'generate_primes', 'is_prime',
           'miller_rabin', 'pyprime', 'pyprime', 'sacks',
           'sieve_eratosthenes', 'trial_division', 'ulam', ]

__submodules__ = [
    'pyprime',
]

__version__ = '1.1.1'
