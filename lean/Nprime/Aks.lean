import Nprime.Spec

/-
Verification of the arithmetic core of the AKS primality test
(`nprime/aks_primality.py`).

The full AKS test also needs polynomial arithmetic in `(ℤ/nℤ)[X] / (Xʳ - 1)`,
`euler_totient`, and `find_r`; those are left for a later step. Here we verify the
two integer-arithmetic helpers that AKS is built on and that are the most
bug-prone:

  * `intRoot n b` -- the exact floor of the b-th root of `n`. The Python version
    uses binary search precisely to avoid the rounding errors of `n ** (1/b)`;
    `intRoot_correct` machine-checks that it satisfies the defining bracket
    `intRoot n b ^ b ≤ n < (intRoot n b + 1) ^ b`.

  * `perfectPower n` -- AKS step 1 (a perfect power is composite). `perfectPower_matches_spec`
    checks it against a brute-force existential specification.

Both correctness theorems are exhaustive over a bounded range (`native_decide`),
which also exercises the binary search across that whole range.
-/

namespace Nprime

/-- Binary-search core for `intRoot`, searching for the floor b-th root of `n`
within `[low, high]`. Faithful port of the Python `while low <= high` loop; the
`fuel` counter (structural recursion) bounds the iteration count and is supplied
generously by the caller, so it never runs out before the search converges. -/
def intRootAux (n b : Nat) : Nat → Nat → Nat → Nat
  | 0, _, high => high
  | fuel + 1, low, high =>
    if low > high then high
    else
      let mid := (low + high) / 2
      let mp := mid ^ b
      if mp == n then mid
      else if mp < n then intRootAux n b fuel (mid + 1) high
      else intRootAux n b fuel low (mid - 1)

/-- Exact integer floor of the b-th root of `n` (`int_root` in Python). -/
def intRoot (n b : Nat) : Nat :=
  if n < 2 then n else intRootAux n b (n + 1) 1 n

/-- Whether `n` is a perfect power `a ^ b` with `b ≥ 2` (`perfect_power`, AKS step 1). -/
def perfectPower (n : Nat) : Bool :=
  (List.range (Nat.log2 n + 1)).any fun b =>
    2 ≤ b && (let a := intRoot n b; a ^ b == n || (a + 1) ^ b == n)

/-- Brute-force reference for `perfectPower`: some `a ≥ 2`, `b ≥ 2` with `a ^ b = n`.
`a` is bounded by `√n` and `b` by `log₂ n` (both necessary when `a ^ b = n`,
`b ≥ 2`), so this is a complete search with no numeric blow-up. -/
def perfectPowerSpec (n : Nat) : Bool :=
  (List.range (Nat.sqrt n + 1)).any fun a =>
    (List.range (Nat.log2 n + 1)).any fun b =>
      2 ≤ a && 2 ≤ b && a ^ b == n

/-- **`intRoot` computes the exact floor b-th root**, checked for every `n < 500`
and `1 ≤ b < 10`. -/
theorem intRoot_correct :
    ∀ n, n < 500 → ∀ b, b < 10 → 1 ≤ b →
      intRoot n b ^ b ≤ n ∧ n < (intRoot n b + 1) ^ b := by
  native_decide

/-- **`perfectPower` agrees with its brute-force specification**, for every `n < 2000`. -/
theorem perfectPower_matches_spec :
    ∀ n, n < 2000 → perfectPower n = perfectPowerSpec n := by
  native_decide

/-- Cross-checks against the Python doctests. -/
example : intRoot 27 3 = 3 := by native_decide
example : intRoot 28 3 = 3 := by native_decide
example : intRoot 1024 10 = 2 := by native_decide
example : perfectPower 8 = true := by native_decide
example : perfectPower 9 = true := by native_decide
example : perfectPower 7 = false := by native_decide

end Nprime
