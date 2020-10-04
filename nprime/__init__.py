"""
nprime main application package

Auto generate command:
    mkinit nprime/__init__.py --nomods -w
"""
from nprime.pyprime import (fermat, find_primes, generate_primes, is_prime,
                            miller_rabin, pyprime, sacks, sieve_eratosthenes,
                            trial_division, ulam, )

__submodules__ = [
    'pyprime',
]

__version__ = '1.2.1'

__all__ = ['fermat', 'find_primes', 'generate_primes', 'is_prime',
           'miller_rabin', 'pyprime', 'sacks', 'sieve_eratosthenes',
           'trial_division', 'ulam']
