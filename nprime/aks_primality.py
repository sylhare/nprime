"""
Implements the Agrawal–Kayal–Saxena primality test.

This is based on the implemention in [SsophoclisAKS]_, but contains fixes to
avoid floating point calculations.

References:
    .. [Wiki_AKS_primality_test] https://en.wikipedia.org/wiki/AKS_primality_test
    .. [SsophoclisAKS] https://github.com/Ssophoclis/AKS-algorithm/tree/master
    .. [RosetaAKS] https://rosettacode.org/wiki/AKS_test_for_primes
"""

import math


def int_root(n, b):
    """
    Returns the integer floor of the b-th root of n
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
    Checks if number is a power of another integer,
    if it returns true, then it is composite.
    """
    for b in range(2, int(math.log2(n)) + 1):
        a = int_root(n, b)
        if pow(a, b) == n:
            return True
        if pow(a + 1, b) == n:  # account for rounding down
            return True
    return False


def find_r_v1(n):
    """Find smallest r such that the order of n mod r > log2(n)^2."""
    maxK = math.log2(n) ** 2
    nexR = True
    r = 1
    while nexR:
        r += 1
        nexR = False
        k = 0
        while k <= maxK and not nexR:
            k = k + 1
            val = fast_mod(n, k, r)
            if val == 0 or val == 1:
                nexR = True
    return r


def find_r_broken(n):
    """
    Find the smallest integer r >= 2 such that the multiplicative order of n modulo r
    is greater than (log2(n))^2.

    Multiplicative order ord_r(n) is the smallest positive integer k where n^k ≡ 1 (mod r).

    Args:
        n (int): The integer whose order modulo r we want to find.

    Returns:
        int: The smallest r satisfying ord_r(n) > (log2(n))^2

    Example:
        >>> find_r(7)
        11

        for i in range(3, 100):
            a = find_r(i)
            b = find_r_v1(i)
            c = findR(i)
            assert a == b == c

        import timerit
        ti = timerit.Timerit(1, bestof=1, verbose=2)
        for timer in ti.reset('time'):
            with timer:
                results1 = [find_r_v1(i) for i in range(3, 100)]

        for timer in ti.reset('time'):
            with timer:
                results2 = [find_r(i) for i in range(3, 100)]
    """
    max_k = int(math.ceil(math.log2(n) ** 2))
    r = 2

    while True:
        # Only consider r coprime with n
        if math.gcd(n, r) != 1:
            r += 1
            continue

        # Check multiplicative order of n modulo r
        order_found = False
        for k in range(1, max_k + 1):
            if fast_mod(n, k, r) == 1:
                # order divides k, so order ≤ max_k -> no good, try next r
                order_found = True
                break

        if not order_found:
            # order > max_k found, return this r
            return r

        r += 1


def fast_mod(base, power, n):
    """
    Compute ``(base ** power) % n`` efficiently using binary exponentiation.

    Example:
        >>> print(fast_mod(2, 10, 1000))
        >>> print(fast_mod(3, 0, 7))
        >>> print(fast_mod(10, 1, 6))
        >>> print(fast_mod(7, 256, 13))
        24
        1
        4
        9
    """
    result = 1 % n
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % n
        base = (base * base) % n
        power >>= 1  # Shift exponent right by 1 bit to divide by 2
    return result


def poly_mod_exp_v1(base, power, r):
    """Use fast modular exponentiation for polynomials to raise them to a big power."""
    x = []
    a = base[0]

    for i in range(len(base)):
        x.append(0)
    x[0] = 1
    n = power

    while power > 0:
        if power % 2 == 1:
            x = poly_mult_v1(x, base, n, r)
        base = poly_mult_v1(base, base, n, r)
        power = power // 2

    x[(0)] = x[(0)] - a
    x[(n % r)] = x[(n % r)] - 1
    return x


def poly_mult_v1(a, b, n, r):
    """Function used by poly_mod_exp_v1 to multiply two polynomials together."""
    x = []
    for i in range(len(a) + len(b) - 1):
        x.append(0)
    for i in range(len(a)):
        for j in range(len(b)):
            x[(i + j) % r] += a[(i)] * b[(j)]
            x[(i + j) % r] = x[(i + j) % r] % n
    for i in range(r, len(x)):
        x = x[:-1]
    return x


def poly_mult_mod_ring(p, q, n, r):
    """
    Function used by poly_mod_exp_v1 to multiply two polynomials together.

    Operates in the polynomial ring (ℤ/nℤ)[X] / (X^r - 1), meaning:

    - Coefficients are reduced modulo n (i.e., integers in ℤ/nℤ, from 0 to n-1)
    - Polynomial arithmetic is performed modulo the relation X^r ≡ 1

    This means that any term with degree ≥ r is wrapped around by reducing X^r to 1,
    so powers are taken modulo r. For example:

        X^r ≡ 1         → X^(r+1) ≡ X, X^(r+2) ≡ X^2, etc.
        X^k ≡ X^(k % r)

    As a result, all polynomials are represented with degree less than r, and
    arithmetic "wraps around" like a ring buffer of coefficients.

    Example polynomial form:

        a[0] + a[1] * X^1 + a[2] * X^2 + ... + a[r-1] * X^(r-1)

    where:
        - a[i] ∈ ℤ/nℤ
        - degree is < r due to reduction modulo X^r - 1

    Args:
        p, q : Lists of integer coefficients (least-significant first)
        n    : Modulus for coefficients (ℤ/nℤ)
        r    : Modulus for degree (polynomials reduced modulo X^r - 1)

    Returns:
        List of coefficients representing (p * q) mod (X^r - 1), with
        coefficients mod n

    Doctest:
        >>> # Case 1: No wraparound - degree of result < r
        >>> # (1 + 2x) * (1 + 2x) = 1 + 4x + 4x²
        >>> poly_mul_mod_xr_minus_1([1, 2], [1, 2], n=5, r=4)
        [1, 4, 4, 0]

        >>> # Case 2: Wraparound happens - degree of result ≥ r
        >>> # (1 + x³) * 1 = 1 + x³ → x³ ≡ 1 (mod X³ - 1), so result is 2
        >>> poly_mult_mod_ring([1, 0, 0, 1], [1], n=7, r=3)
        [2, 0, 0]

        >>> # Case 3: Both polynomials cause wrap - higher degree reduction
        >>> # x² * x² = x⁴ ≡ 1, so result is x⁴ ≡ 1 at index 0
        >>> poly_mult_mod_ring([0, 0, 1], [0, 0, 1], n=11, r=4)
        [1, 0, 0, 0]

        >>> # Case 4: All zeros
        >>> poly_mult_mod_ring([0], [0], n=3, r=2)
        [0, 0]

    Ignore:
        # Check for consistency with original code.
        for i in range(100):
            import random
            def random_poly():
                degree = random.randint(1, 10)
                return [random.randint(1, 10) for _ in range(degree)]
            p = random_poly()
            q = random_poly()
            n = random.randint(1, 10)
            r = random.randint(1, 10)
            r1 = poly_mult_mod_ring(p, q, n, r)
            r2 = poly_mult_v1(p, q, n, r)
            assert r1 == r2
    """
    res = [0] * min(r, len(p) + len(q) - 1)
    for i, coeff_p in enumerate(p):
        for j, coeff_q in enumerate(q):
            deg = (i + j) % r
            res[deg] = (res[deg] + coeff_p * coeff_q) % n
    return res


def poly_mod_exp_v2(a, n, r, mod):
    """Computes (x + a)^n mod (x^r - 1, mod), returned as a list of coefficients."""
    result = [1] + [0] * (r - 1)
    base = [a, 1] + [0] * (r - 2)

    while n > 0:
        if n % 2 == 1:
            result = poly_mult_mod_ring(result, base, mod, r)
        base = poly_mult_mod_ring(base, base, mod, r)
        n //= 2

    return result


def euler_totient_v1(r):
    """Counts the number of positive integers up to r that are relatively prime to r"""
    x = 0
    for i in range(1, r + 1):
        if math.gcd(r, i) == 1:
            x += 1
    return x


def euler_totient(r):
    """
    Returns Euler's totient function φ(r): the number of integers in [1, r]
    that are coprime to r.

    Efficient version using the Euler product formula:
        φ(r) = r * Π (1 - 1/p) for all distinct primes p dividing r

    Example:
        >>> [euler_totient(i) for i in range(13)]
        [0, 1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4]
    """
    if r == 0:
        # no positive integers coprime with 0
        return 0

    result = r  # Initialize result as r; will multiply by (1 - 1/p) for each prime factor p
    p = 2  # Start checking for prime factors from 2 upwards

    # Check all possible prime factors up to sqrt(r)
    while p * p <= r:
        # If p divides r, it is a prime factor
        if r % p == 0:
            # Remove all powers of p from r
            while r % p == 0:
                r //= p
            # Update result according to Euler product formula: multiply by (1 - 1/p)
            result -= result // p
        # Move to the next candidate factor
        p += 1

    # If remaining r is greater than 1, it is a prime factor larger than sqrt(original r)
    if r > 1:
        result -= result // r
    return result


def aks(n):
    """
    The AKS (Agrawal–Kayal–Saxena) primality test.

    This algorithm runs in polynomial time, although the exponent is large.
    This is O(log(n)^12), and could be improved to O(log(n)^6).

    References:

        .. [PRIMES_in_p] Agrawal, Manindra, Neeraj Kayal, and Nitin Saxena. "PRIMES is in P." Annals of mathematics (2004): 781-793.
                         https://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf

    Example:
        >>> aks(101)
        True
        >>> aks(102)
        False
        >>> aks(103)
        True

        >>> n = 2**4423 - 1
        >>> aks(n)
        >>> aks(4423)

        for

        from nprime import is_prime

        import ubelt as ub

        for n in range(2, 111):
            assert is_prime(n) == aks(n)

        for case in cases:
            if not is_prime(case):
                print(case)

        miller_rabin(n, 1)
        miller_rabin(n, 1)
    """
    # step 1
    if perfect_power(n):
        return False

    # step 2
    r = find_r_v1(n)

    # step 3
    for a in range(2, min(r, n)):
        if math.gcd(a, n) > 1:
            return False

    # step 4
    if n <= r:
        return True

    # step 5
    if 0:
        limit = math.floor((euler_totient(r)) ** (1 / 2) * math.log2(n))
        for a in range(1, limit):
            x = poly_mod_exp_v1([a, 1], n, r)
            if any(x):
                return False

    # Alternative
    if 1:
        limit = int(math.isqrt(euler_totient(r)) * math.log2(n))
        for a in range(1, limit + 1):
            poly = poly_mod_exp_v2(a, n, r, n)
            expected = [0] * r
            expected[0] = a % n
            expected[n % r] = 1 % n
            if poly != expected:
                return False

    return True  # step 6
