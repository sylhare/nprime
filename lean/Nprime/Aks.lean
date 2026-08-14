import Nprime.Spec

/-
Arithmetic core of the AKS primality test (`nprime/aks_primality.py`).

Two unbounded, kernel-checked results (no `native_decide`):

  * `intRoot_exact` -- `intRoot n b` is the exact floor of the `b`-th root of `n`,
    for every `n` and `b ≥ 1`. The Python uses binary search to dodge the rounding
    of `n ** (1/b)`; this proves that search returns the true bracketing root.

  * `perfectPower_sound` -- AKS step 1: if `perfectPower n` reports `true` then `n`
    is composite, for every `n ≥ 2`. (A perfect power `a ^ b`, `b ≥ 2`, is composite.)

Full AKS (the ring `(ℤ/nℤ)[X]/(Xʳ-1)`, `find_r`, `euler_totient`) is out of scope.
-/

namespace Nprime

/-- Binary-search core for `intRoot`, faithful port of the Python `while low <= high`
loop; `fuel` bounds the iteration count and is supplied generously by the caller. -/
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

/-- Exact integer floor of the `b`-th root of `n` (`int_root` in Python). -/
def intRoot (n b : Nat) : Nat := if n < 2 then n else intRootAux n b (n + 1) 1 n

/-- Whether `n` is a perfect power `a ^ b` with `b ≥ 2` (`perfect_power`, AKS step 1). -/
def perfectPower (n : Nat) : Bool :=
  (List.range (Nat.log2 n + 1)).any fun b =>
    2 ≤ b && (let a := intRoot n b; a ^ b == n || (a + 1) ^ b == n)

/-- Loop invariant for the binary search: the answer stays bracketed in `[low, high]`,
with `(low-1)^b ≤ n < (high+1)^b`; enough fuel guarantees convergence. -/
private theorem intRootAux_spec (n b : Nat) (hb : 1 ≤ b) :
    ∀ fuel low high, 1 ≤ low → low ≤ high + 1 → (low - 1) ^ b ≤ n →
      n < (high + 1) ^ b → high + 1 - low ≤ fuel →
      (intRootAux n b fuel low high) ^ b ≤ n ∧
        n < (intRootAux n b fuel low high + 1) ^ b := by
  intro fuel
  induction fuel with
  | zero =>
    intro low high h1 h2 h3 h4 _
    simp only [intRootAux]
    have hlow : low = high + 1 := by omega
    refine ⟨?_, h4⟩
    rw [hlow] at h3; simpa using h3
  | succ fuel ih =>
    intro low high h1 h2 h3 h4 h5
    simp only [intRootAux]
    split
    · next hgt =>
      have hlow : low = high + 1 := by omega
      refine ⟨?_, h4⟩
      rw [hlow] at h3; simpa using h3
    · next hle =>
      split
      · next hmp =>
        have hmpe : ((low + high) / 2) ^ b = n := by simpa using hmp
        refine ⟨by omega, ?_⟩
        rw [← hmpe]
        exact Nat.pow_lt_pow_left (by omega) (by omega)
      · next hmp =>
        split
        · next hlt =>
          have hmplt : ((low + high) / 2) ^ b < n := by simpa using hlt
          refine ih ((low + high) / 2 + 1) high (by omega) (by omega) ?_ h4 (by omega)
          simpa using Nat.le_of_lt hmplt
        · next hge =>
          have hmpgt : n < ((low + high) / 2) ^ b := by
            have hne : ((low + high) / 2) ^ b ≠ n := by simpa using hmp
            omega
          refine ih low ((low + high) / 2 - 1) h1 (by omega) h3 ?_ (by omega)
          have hmid1 : (low + high) / 2 - 1 + 1 = (low + high) / 2 := by omega
          rw [hmid1]; exact hmpgt

/-- **`intRoot` is the exact floor `b`-th root**, for every `n` and `b ≥ 1`:
`intRoot n b ^ b ≤ n < (intRoot n b + 1) ^ b`. -/
theorem intRoot_exact (n b : Nat) (hb : 1 ≤ b) :
    intRoot n b ^ b ≤ n ∧ n < (intRoot n b + 1) ^ b := by
  rw [intRoot]
  split
  · next h2 =>
    interval_cases n
    · exact ⟨by simp [Nat.zero_pow (show 0 < b by omega)], by simp⟩
    · refine ⟨by simp, ?_⟩
      show 1 < 2 ^ b
      have : 2 ≤ 2 ^ b := Nat.le_self_pow (show b ≠ 0 by omega) 2
      omega
  · next h2 =>
    refine intRootAux_spec n b hb (n + 1) 1 n (by omega) (by omega) ?_ ?_ (by omega)
    · simp [Nat.zero_pow (show 0 < b by omega)]
    · have := Nat.le_self_pow (show b ≠ 0 by omega) (n + 1); omega

/-- A power `a ^ b` with `b ≥ 2` equal to `n ≥ 2` makes `n` composite. -/
private theorem not_prime_of_pow (a b n : Nat) (hb : 2 ≤ b) (hn : 2 ≤ n)
    (h : a ^ b = n) : ¬ Nat.Prime n := by
  intro hp
  have hdvd : a ∣ n := by rw [← h]; exact dvd_pow_self a (by omega : b ≠ 0)
  rcases hp.eq_one_or_self_of_dvd a hdvd with ha1 | han
  · rw [ha1, one_pow] at h; omega
  · rw [han] at h
    have h2 : n ^ 2 ≤ n ^ b := Nat.pow_le_pow_right (by omega) hb
    rw [h, pow_two] at h2
    have : 2 * n ≤ n := Nat.le_trans (Nat.mul_le_mul_right n (by omega : 2 ≤ n)) h2
    omega

/-- **AKS step 1 soundness (all `n ≥ 2`): a reported perfect power is composite.** -/
theorem perfectPower_sound (n : Nat) (hn : 2 ≤ n) (h : perfectPower n = true) :
    ¬ Nat.Prime n := by
  rw [perfectPower, List.any_eq_true] at h
  obtain ⟨b, _, hb⟩ := h
  simp only [Bool.and_eq_true, decide_eq_true_eq, Bool.or_eq_true] at hb
  obtain ⟨hb2, hdisj⟩ := hb
  rcases hdisj with he | he
  · exact not_prime_of_pow (intRoot n b) b n hb2 hn (by simpa using he)
  · exact not_prime_of_pow (intRoot n b + 1) b n hb2 hn (by simpa using he)

/-- Cross-checks against the Python doctests. -/
example : intRoot 27 3 = 3 := by native_decide
example : intRoot 1024 10 = 2 := by native_decide
example : perfectPower 8 = true := by native_decide
example : perfectPower 7 = false := by native_decide

end Nprime
