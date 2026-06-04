"""
Implements the Agrawal–Kayal–Saxena (AKS) primality test.

The AKS test, introduced in [PRIMES_in_p]_, was the first primality test proven
to be deterministic, general (it works for every integer) and to run in
polynomial time. This implementation favours readability over raw speed and is
based on [SsophoclisAKS]_, with fixes to avoid floating point calculations.

References:
    .. [Wiki_AKS_primality_test] https://en.wikipedia.org/wiki/AKS_primality_test
    .. [SsophoclisAKS] https://github.com/Ssophoclis/AKS-algorithm/tree/master
    .. [RosetaAKS] https://rosettacode.org/wiki/AKS_test_for_primes
    .. [PRIMES_in_p] Agrawal, Manindra, Neeraj Kayal, and Nitin Saxena.
                     "PRIMES is in P." Annals of mathematics (2004): 781-793.
                     https://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf
"""

import math

from nprime.coprime import euler_totient


def int_root(n, b):
    """
    Return the integer floor of the b-th root of n.

    Uses a binary search so the result is exact and avoids the rounding errors
    of ``n ** (1 / b)``.

    Example:
        >>> int_root(27, 3)
        3
        >>> int_root(28, 3)
        3
        >>> int_root(1024, 10)
        2
    """
    if n < 2:
        return n

    low, high = 1, n
    while low <= high:
        mid = (low + high) // 2
        mid_pow = pow(mid, b)
        if mid_pow == n:
            return mid
        elif mid_pow < n:
            low = mid + 1
        else:
            high = mid - 1
    return high


def perfect_power(n):
    """
    Check whether n is a perfect power a^b with b >= 2.

    A perfect power is always composite, so this is the first rejection step of
    the AKS test.

    Example:
        >>> perfect_power(8)
        True
        >>> perfect_power(9)
        True
        >>> perfect_power(7)
        False
    """
    for b in range(2, int(math.log2(n)) + 1):
        a = int_root(n, b)
        # int_root rounds down, so check both a and a + 1 to be safe.
        if pow(a, b) == n or pow(a + 1, b) == n:
            return True
    return False


def find_r(n):
    """
    Find the smallest r such that the multiplicative order of n modulo r is
    greater than log2(n)^2.

    The order ord_r(n) is the smallest positive integer k where n^k ≡ 1 (mod r).
    Any r that shares a factor with n (so that n^k ≡ 0 for some k) is skipped as
    well, which keeps the candidate coprime to n.

    Example:
        >>> find_r(31)
        29
    """
    max_k = math.log2(n) ** 2
    k_upper = int(max_k) + 1
    r = 1
    while True:
        r += 1
        order_exceeds_max_k = all(pow(n, k, r) not in (0, 1) for k in range(1, k_upper + 1))
        if order_exceeds_max_k:
            return r


def poly_mult_mod_ring(p, q, n, r):
    """
    Multiply two polynomials in the ring (ℤ/nℤ)[X] / (X^r - 1).

    In this ring:

    - Coefficients are reduced modulo n (integers in [0, n - 1]).
    - Polynomial arithmetic is performed modulo X^r - 1, so any term of degree
      ``d`` is folded back onto degree ``d % r`` (X^r ≡ 1, X^(r+1) ≡ X, ...).

    Polynomials are represented as lists of coefficients, least-significant
    first: ``a[0] + a[1] * X + ... + a[r-1] * X^(r-1)``.

    Args:
        p, q : Lists of integer coefficients (least-significant first).
        n    : Modulus for the coefficients (ℤ/nℤ).
        r    : Modulus for the degree (polynomials reduced modulo X^r - 1).

    Returns:
        List of coefficients representing ``(p * q) mod (X^r - 1)``, with
        coefficients taken mod n.

    Example:
        >>> # (1 + 2x) * (1 + 2x) = 1 + 4x + 4x^2, no wraparound for r = 4.
        >>> poly_mult_mod_ring([1, 2], [1, 2], n=5, r=4)
        [1, 4, 4]
        >>> # (1 + x^3) * 1 = 1 + x^3, and x^3 ≡ 1 (mod X^3 - 1), so the result is 2.
        >>> poly_mult_mod_ring([1, 0, 0, 1], [1], n=7, r=3)
        [2, 0, 0]
        >>> # x^2 * x^2 = x^4 ≡ 1 (mod X^4 - 1), landing back at degree 0.
        >>> poly_mult_mod_ring([0, 0, 1], [0, 0, 1], n=11, r=4)
        [1, 0, 0, 0]
    """
    res = [0] * min(r, len(p) + len(q) - 1)
    for i, coeff_p in enumerate(p):
        for j, coeff_q in enumerate(q):
            deg = (i + j) % r
            res[deg] = (res[deg] + coeff_p * coeff_q) % n
    return res


def poly_mod_exp(a, n, r, mod):
    """
    Compute ``(X + a)^n mod (X^r - 1, mod)`` as a list of coefficients.

    Uses binary exponentiation, squaring within the polynomial ring at each step
    so the work stays polynomial in the size of n.

    Example:
        >>> # (X + 1)^3 = X^3 + 3X^2 + 3X + 1, reduced mod (X^2 - 1, 5):
        >>> # X^3 ≡ X and X^2 ≡ 1, giving (3 + 1) + (1 + 3)X = 4 + 4X.
        >>> poly_mod_exp(1, 3, 2, 5)
        [4, 4]
    """
    result = [1] + [0] * (r - 1)
    base = [a, 1] + [0] * (r - 2)

    while n > 0:
        if n % 2 == 1:
            result = poly_mult_mod_ring(result, base, mod, r)
        base = poly_mult_mod_ring(base, base, mod, r)
        n //= 2

    return result


def aks(n):
    """
    The AKS (Agrawal–Kayal–Saxena) primality test.

    Returns True if n is prime. The algorithm is deterministic and runs in
    polynomial time, although the exponent is large (about O(log(n)^12) here),
    so it is far slower in practice than the probabilistic tests in this package
    and is included mainly for its theoretical interest.

    Example:
        >>> aks(101)
        True
        >>> aks(102)
        False
        >>> aks(103)
        True
    """
    # Step 1: a perfect power a^b (b >= 2) is always composite.
    if perfect_power(n):
        return False

    # Step 2: find r with ord_r(n) > log2(n)^2.
    r = find_r(n)

    # Step 3: any 1 < gcd(a, n) < n for a <= r exposes a non-trivial factor.
    for a in range(2, min(r, n)):
        if math.gcd(a, n) > 1:
            return False

    # Step 4: for small n (n <= r) the previous step already proved primality.
    if n <= r:
        return True

    # Step 5: verify the polynomial congruence (X + a)^n ≡ X^n + a
    # in (ℤ/nℤ)[X] / (X^r - 1) for every a up to the AKS bound.
    limit = int(math.isqrt(euler_totient(r)) * math.log2(n))
    for a in range(1, limit + 1):
        poly = poly_mod_exp(a, n, r, n)
        expected = [0] * r
        expected[0] = a % n
        expected[n % r] = 1 % n
        if poly != expected:
            return False

    # Step 6: all checks passed, n is prime.
    return True
