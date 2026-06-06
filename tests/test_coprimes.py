"""Tests for coprime functions: gcd, are_coprime, coprimes, coprime_pairs, euler_totient."""
import pytest

from nprime.coprime import are_coprime, coprime_pairs, coprimes, euler_totient, gcd

GCD_CASES = [
    (12, 8, 4),
    (17, 13, 1),
    (25, 15, 5),
    (48, 18, 6),
    (0, 5, 5),
    (5, 0, 5),
    (1, 1, 1),
    (7, 7, 7),
    (-12, 8, 4),
    (12, -8, 4),
    (-12, -8, 4),
]

COPRIME_PAIRS = [(9, 16), (17, 13), (15, 8), (1, 5), (5, 1), (1, 1)]
NOT_COPRIME_PAIRS = [(12, 8), (15, 9), (6, 9)]

COPRIMES_CASES = [
    (12, 20, [1, 5, 7, 11, 13, 17, 19]),
    (10, 10, [1, 3, 7, 9]),
    (15, 20, [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19]),
    (1, 5, [1, 2, 3, 4, 5]),
    (7, 7, [1, 2, 3, 4, 5, 6]),
]

EULER_TOTIENT_CASES = [
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 2),
    (5, 4),
    (7, 6),
    (8, 4),
    (9, 6),
    (11, 10),
    (12, 4),
    (17, 16),
]


@pytest.mark.parametrize("a, b, expected", GCD_CASES)
def test_gcd(a, b, expected):
    """Greatest common divisor for positive, zero, and negative inputs."""
    assert gcd(a, b) == expected


@pytest.mark.parametrize("a, b", COPRIME_PAIRS)
def test_are_coprime(a, b):
    """Pairs with gcd 1 are coprime."""
    assert are_coprime(a, b) is True


@pytest.mark.parametrize("a, b", NOT_COPRIME_PAIRS)
def test_are_not_coprime(a, b):
    """Pairs sharing a common factor are not coprime."""
    assert are_coprime(a, b) is False


@pytest.mark.parametrize("n, upper, expected", COPRIMES_CASES)
def test_coprimes(n, upper, expected):
    """List of integers coprime to n up to upper."""
    assert coprimes(n, upper) == expected


@pytest.mark.parametrize("n, upper", [(0, None), (-5, None), (5, 0), (5, -3)])
def test_coprimes_invalid(n, upper):
    """Zero, negative n or upper raises ValueError."""
    with pytest.raises(ValueError):
        if upper is None:
            coprimes(n)
        else:
            coprimes(n, upper)


def test_coprime_pairs_basic():
    """All coprime pairs up to 5, verifying inclusions and exclusions."""
    pairs = coprime_pairs(5)
    assert len(pairs) == 10
    for p in [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]:
        assert p in pairs
    assert (2, 4) not in pairs
    assert (3, 6) not in pairs


def test_coprime_pairs_small():
    """Coprime pairs up to 3 returns exact expected list."""
    assert coprime_pairs(3) == [(1, 1), (1, 2), (1, 3), (2, 3)]


@pytest.mark.parametrize("n", [0, -5])
def test_coprime_pairs_invalid(n):
    """Zero or negative input raises ValueError."""
    with pytest.raises(ValueError):
        coprime_pairs(n)


@pytest.mark.parametrize("n, expected", EULER_TOTIENT_CASES)
def test_euler_totient(n, expected):
    """Euler's totient for small values, primes, and prime powers."""
    assert euler_totient(n) == expected


@pytest.mark.parametrize("n", [0, -5])
def test_euler_totient_invalid(n):
    """Zero or negative input raises ValueError."""
    with pytest.raises(ValueError):
        euler_totient(n)
