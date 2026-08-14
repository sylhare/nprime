import Mathlib

/-
Reference definition of primality. `IsPrime` is the explicit textbook predicate
(at least 2, no divisor strictly between 1 and `n`). `isPrime_iff_prime` proves it
equal to Mathlib's canonical `Nat.Prime`, so every algorithm is checked against the
standard definition rather than an ad hoc mirror written to match the code.
-/

namespace Nprime

/-- `n` is prime: at least 2, with no proper divisor `m` in `2 ≤ m < n`. The bound
`m < n` is written first so `Nat.decidableBallLT` makes `IsPrime` decidable. -/
def IsPrime (n : Nat) : Prop :=
  2 ≤ n ∧ ∀ m, m < n → 2 ≤ m → n % m ≠ 0

instance : DecidablePred IsPrime := fun _ => inferInstanceAs (Decidable (_ ∧ _))

/-- The elementary `IsPrime` predicate coincides with Mathlib's `Nat.Prime`. -/
theorem isPrime_iff_prime (n : Nat) : IsPrime n ↔ Nat.Prime n := by
  unfold IsPrime
  rw [Nat.prime_def_lt']
  refine and_congr_right (fun _ => ?_)
  constructor
  · exact fun h m hm2 hmn hdvd => h m hmn hm2 (Nat.dvd_iff_mod_eq_zero.mp hdvd)
  · exact fun h m hmn hm2 hmod => h m hm2 hmn (Nat.dvd_iff_mod_eq_zero.mpr hmod)

end Nprime
