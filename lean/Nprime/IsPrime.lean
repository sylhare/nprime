import Nprime.Spec

/-
Verification of the trial-division primality test (`nprime/pyprime.py::is_prime`).

The Python implementation loops candidate divisors `i` from 2 up to and including
`isqrt(n)`, returning `False` on the first divisor found:

    def is_prime(n):
        for i in range(2, math.isqrt(n) + 1):
            if n % i == 0:
                return False
        return True

`isPrime` below is a faithful port. `isPrime_iff` proves it computes exactly the
mathematical `IsPrime` specification for every `n ≥ 2`, and `isPrime_one` records
the (real) edge case: like the Python code, it answers `true` for `1`, which is
*not* prime -- the sort of gap formal verification makes explicit.
-/

namespace Nprime

/-- Faithful port of `is_prime`: no divisor `i` in `2 ≤ i ≤ Nat.sqrt n` divides `n`.
The `i < 2` guard skips the `0` and `1` that `List.range` includes but Python's
`range(2, …)` does not. -/
def isPrime (n : Nat) : Bool :=
  (List.range (Nat.sqrt n + 1)).all (fun i => i < 2 || n % i != 0)

/-- Pointwise reading of `isPrime`: it is `true` exactly when no divisor in the
`[2, Nat.sqrt n]` window divides `n`. -/
theorem isPrime_eq_true_iff (n : Nat) :
    isPrime n = true ↔ ∀ i, i ≤ Nat.sqrt n → 2 ≤ i → n % i ≠ 0 := by
  unfold isPrime
  rw [List.all_eq_true]
  constructor
  · intro h i hle h2
    have hmem : i ∈ List.range (Nat.sqrt n + 1) := List.mem_range.mpr (by omega)
    have := h i hmem
    simp only [Bool.or_eq_true, decide_eq_true_eq, bne_iff_ne] at this
    rcases this with hlt | hne
    · omega
    · exact hne
  · intro h i hmem
    have : i < Nat.sqrt n + 1 := List.mem_range.mp hmem
    simp only [Bool.or_eq_true, decide_eq_true_eq, bne_iff_ne]
    by_cases h2 : 2 ≤ i
    · exact Or.inr (h i (by omega) h2)
    · exact Or.inl (by omega)

/-- For `n ≥ 2`, `Nat.sqrt n < n`. Needed to feed a `≤ Nat.sqrt n` divisor into
the `< n` bound of `IsPrime`. -/
theorem sqrt_lt_self {n : Nat} (hn : 2 ≤ n) : Nat.sqrt n < n := by
  rcases Nat.lt_or_ge (Nat.sqrt n) n with h | h
  · exact h
  · exfalso
    have hsq : Nat.sqrt n * Nat.sqrt n ≤ n := Nat.sqrt_le n
    have hmono : n * n ≤ Nat.sqrt n * Nat.sqrt n := Nat.mul_le_mul h h
    have hnn : n * 2 ≤ n * n := Nat.mul_le_mul (Nat.le_refl n) hn
    have : n * 2 ≤ n := Nat.le_trans hnn (Nat.le_trans hmono hsq)
    omega

/-- The key number-theoretic fact: any proper divisor of `n` forces a divisor no
larger than `Nat.sqrt n`, so trial division only needs to reach the square root. -/
theorem exists_small_divisor {n m : Nat}
    (hm2 : 2 ≤ m) (hmn : m < n) (hdvd : n % m = 0) :
    ∃ d, 2 ≤ d ∧ d ≤ Nat.sqrt n ∧ n % d = 0 := by
  have hmdvd : m ∣ n := Nat.dvd_of_mod_eq_zero hdvd
  have hnmk : n = m * (n / m) := (Nat.mul_div_cancel' hmdvd).symm
  generalize hk : n / m = k at hnmk
  have hkpos : 0 < k := by
    rcases Nat.eq_zero_or_pos k with h0 | hp
    · rw [h0, Nat.mul_zero] at hnmk; omega
    · exact hp
  have hkne1 : k ≠ 1 := by
    intro h1; rw [h1, Nat.mul_one] at hnmk; omega
  have hk2 : 2 ≤ k := by omega
  have hkdvd : k ∣ n := ⟨m, by rw [hnmk]; exact Nat.mul_comm m k⟩
  by_cases hms : m ≤ Nat.sqrt n
  · exact ⟨m, hm2, hms, hdvd⟩
  · refine ⟨k, hk2, ?_, Nat.mod_eq_zero_of_dvd hkdvd⟩
    rcases Nat.lt_or_ge (Nat.sqrt n) k with hk_gt | hk_le
    · exfalso
      have hm1 : Nat.sqrt n + 1 ≤ m := Nat.lt_of_not_le hms
      have hk1 : Nat.sqrt n + 1 ≤ k := hk_gt
      have hbig : (Nat.sqrt n + 1) * (Nat.sqrt n + 1) ≤ m * k :=
        Nat.mul_le_mul hm1 hk1
      have hlt : n < (Nat.sqrt n + 1) * (Nat.sqrt n + 1) := Nat.lt_succ_sqrt n
      rw [← hnmk] at hbig
      omega
    · exact hk_le

/-- **Correctness of `is_prime`.** For every `n ≥ 2`, the trial-division port
returns `true` iff `n` is prime by the reference specification. -/
theorem isPrime_iff (n : Nat) (hn : 2 ≤ n) : isPrime n = true ↔ IsPrime n := by
  rw [isPrime_eq_true_iff]
  constructor
  · intro h
    refine ⟨hn, ?_⟩
    intro m hmn hm2 hdvd
    obtain ⟨d, hd2, hds, hddvd⟩ := exists_small_divisor hm2 hmn hdvd
    exact h d hds hd2 hddvd
  · intro h i hle h2
    obtain ⟨_, hforall⟩ := h
    have hilt : i < n := Nat.lt_of_le_of_lt hle (sqrt_lt_self hn)
    exact hforall i hilt h2

/-- The documented edge case, now a theorem: `isPrime` agrees with Python in
answering `true` for `1`, even though `1` is not prime. Verification pins the
exact boundary where the algorithm and the specification part ways. -/
theorem isPrime_one : isPrime 1 = true := by native_decide

theorem not_isPrime_one : ¬ IsPrime 1 := by decide

/-- Executable cross-checks against the Python doctest examples. -/
example : isPrime 101 = true := by native_decide
example : isPrime 102 = false := by native_decide
example : isPrime 103 = true := by native_decide

end Nprime
