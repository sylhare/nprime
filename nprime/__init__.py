"""
nprime main application package

Auto generate command:
    mkinit nprime/__init__.py --nomods -w
"""
from nprime.aks_primality import aks
from nprime.coprime import (are_coprime, coprime_pairs, coprimes, euler_totient,
                            gcd, )
from nprime.pyprime import (fermat, find_primes, generate_primes, is_perfect,
                            is_prime, miller_rabin, prime_factors, pyprime,
                            sacks, sieve_eratosthenes, trial_division, ulam, )

__submodules__ = [
    'aks_primality',
    'coprime',
    'pyprime',
]

__version__ = '1.3.1'

__all__ = ['aks', 'are_coprime', 'coprime_pairs', 'coprimes', 'euler_totient',
           'fermat', 'find_primes', 'gcd', 'generate_primes', 'is_perfect',
           'is_prime', 'miller_rabin', 'prime_factors', 'pyprime', 'sacks',
           'sieve_eratosthenes', 'trial_division', 'ulam']
