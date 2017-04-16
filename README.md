# PyPrime  [![Build Status](https://travis-ci.org/Sylhare/PyPrime.svg?branch=master)](https://travis-ci.org/Sylhare/PyPrime)
---
[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com) [![forthebadge](http://forthebadge.com/images/badges/built-with-science.svg)](http://forthebadge.com)


Some algorythm on prime numbers.

Language: Python 3.5.2 

Algorithm developped : 

- Native one (prime through divisions)
- Eratosthenes sieve based
- Fermat's test (based on Fermat's theorem)
- Prime generating functions

# Math

Here are a bit of information to help understand some of the algorithms

Congruence :
------------
 "`≡`" means congruent, `a ≡ b (mod m)` implies that 
`m / (a-b), ∃ k ∈ Z` that verifies `a = kn + b`
   
 which implies:

    a ≡ 0 (mod n) <-> a = kn <-> "a" is divisible by "n" 

Fermart's Theorem
-----------------
 if `n` is prime then `∀ a ∈[1, ..., n-1]`

	a^(n-1) ≡ 1 (mod n) ⇔ a^(n-1) = kn + 1
   
Miller rabin
------------ 
  Take a random `a ∈ {1,...,n−1}` and `n > 2`, </br>
  Find `d` and `s` such as with `n - 1 = 2^s * d` (with d odd) </br>
  if `(a^d)^2^r ≡ 1 mod n` for all `r` in `0` to `s-1` </br>
  Then `n` is prime.
    
  The test output is false of 1/4 of the "a values" possible in `n`, 
  so the test is repeated t times.


Strong Pseudoprime
-------------------
A strong [pseudoprime](http://mathworld.wolfram.com/StrongPseudoprime.html) to a base `a` is an odd composite number `n` with `n-1 = d·2^s` (for d odd) for which either `a^d = 1(mod n)` or `a^(d·2^r) = -1(mod n)` for some `r = 0, 1, ..., s-1` </br>
