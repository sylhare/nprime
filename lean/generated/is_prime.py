# Generated from the verified Lean model in lean/Nprime/Codegen.lean.
# Do not edit by hand -- regenerate with `lake exe codegen`.
import math


def is_prime(n):
    for i in range(2, (math.isqrt(n) + 1)):
        if n % i == 0:
            return False
    return True
