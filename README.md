# nprime 

 [![Generic badge](https://img.shields.io/badge/github-nprime-blue.svg)](https://github.com/Sylhare/nprime) [![PyPI version](https://badge.fury.io/py/nprime.svg)](https://badge.fury.io/py/nprime) [![Build Status](https://travis-ci.org/Sylhare/nprime.svg?branch=master)](https://travis-ci.org/Sylhare/nprime) [![codecov](https://codecov.io/gh/Sylhare/nprime/branch/master/graph/badge.svg)](https://codecov.io/gh/Sylhare/nprime) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3f1889b9069645faa6ec38cb4b117b1d)](https://www.codacy.com/app/Sylhare/nprime?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Sylhare/nprime&amp;utm_campaign=Badge_Grade)

## Installation

To install the package use pip:

    pip install nprime


## Introduction

Some algorithm on prime numbers. 

Algorithm developed : 

- Eratosthenes sieve based
- Fermat's test (based on Fermat's theorem)
- Prime generating functions
- Miller Rabin predictive algorithm

## Specifications

- Language: Python **3.5.2** 
- Package:
	- Basic python packages were preferred
	- Matplotlib v2.0 - graph and math

### Integration and pipeline

Code quality is monitored through [codacity](https://www.codacy.com/app/Sylhare/nprime/dashboard).
For the tests coverage, there's [codecov](https://codecov.io/gh/Sylhare/nprime) which is run during the [Travis CI](https://travis-ci.org/Sylhare/nprime) pipeline.

## Math

Here are a bit of information to help understand some of the algorithms

### Congruence

 "`≡`" means congruent, `a ≡ b (mod m)` implies that 
`m / (a-b), ∃ k ∈ Z` that verifies `a = kn + b`
   
 which implies:

    a ≡ 0 (mod n) <-> a = kn <-> "a" is divisible by "n" 
    
### Erathostene's Sieve

For `n ∈ N` and for `∀ a ∈[1, ..., √n]` then `n/a ∉ N` is true.

[![Erathostene example](https://upload.wikimedia.org/wikipedia/commons/b/b9/Sieve_of_Eratosthenes_animation.gif)](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)


### Fermat's Theorem

If `n` is prime then `∀ a ∈[1, ..., n-1]`

```
    a^(n-1) ≡ 1 (mod n) ⇔ a^(n-1) = kn + 1
```
   
### Miller rabin

For `n ∈ N` and `n > 2`, </br>
Take a random `a ∈ {1,...,n−1}` </br>
Find `d` and `s` such as with `n - 1 = 2^s * d` (with d odd) </br>
if `(a^d)^2^r ≡ 1 mod n` for all `r` in `0` to `s-1` </br>
Then `n` is prime.

The test output is false of 1/4 of the "a values" possible in `n`, 
so the test is repeated t times.


### Strong Pseudoprime

A strong [pseudoprime](http://mathworld.wolfram.com/StrongPseudoprime.html) to a base `a` is an odd composite number `n` 
with `n-1 = d·2^s` (for d odd) for which either `a^d = 1(mod n)` or `a^(d·2^r) = -1(mod n)` for some `r = 0, 1, ..., s-1` </br>
