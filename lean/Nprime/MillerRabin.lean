import Nprime.Spec
import Nprime.IsPrime

/-
Verification of the Miller-Rabin primality test (`nprime/pyprime.py::miller_rabin`).

Miller-Rabin is *probabilistic*: with random witnesses it can only be wrong in one
direction (a composite slipping through), never the other. We verify the standard
**deterministic** variant -- the same algorithm with a fixed list of witness bases,
which is what is used in practice when an exact answer is required.

What is proved here, dependency-free:

  * `factorTwos_spec` -- the `n - 1 = 2^s * d` decomposition (the loop that Python
    writes as `while d % 2 == 0: d //= 2; s += 1`) is correct for *every* input.
    This is the fiddly, bug-prone part of the algorithm.

  * `millerRabinDet_agrees_below_2000` -- the deterministic test with bases `[2, 3]`
    computes exactly the `IsPrime` specification for all `n < 2000`. This is an
    exhaustive, machine-checked equivalence (via `native_decide`), which also
    validates `powMod` and the round logic over that whole range.

The unbounded soundness of Miller-Rabin ("a `false` verdict means genuinely
composite, for all n") rests on Fermat's little theorem and the structure of
`(ℤ/nℤ)ˣ`; that needs Mathlib and is out of scope for this dependency-free
prototype. The bounded theorem sidesteps it by checking every case.
-/

namespace Nprime

/-- Fast modular exponentiation `a ^ e mod m`, keeping intermediate values below
`m^2` so exhaustive checking stays cheap. -/
def powMod (a e m : Nat) : Nat :=
  if e = 0 then 1 % m
  else
    let half := powMod a (e / 2) m
    let sq := half * half % m
    if e % 2 = 0 then sq else sq * a % m
termination_by e
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero ‹e ≠ 0›) (by decide)

/-- Decompose `m` as `2 ^ s * d` with `d` odd, returning `(s, d)`. Mirrors the
Python loop `while d % 2 == 0: d //= 2; s += 1` applied to `n - 1`. -/
def factorTwos (m : Nat) : Nat × Nat :=
  if h : m ≠ 0 ∧ m % 2 = 0 then
    let r := factorTwos (m / 2)
    (r.1 + 1, r.2)
  else (0, m)
termination_by m
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero h.1) (by decide)

/-- The squaring loop: from `x`, square mod `n` up to `fuel` times looking for
`n - 1`. Returns `true` if `n - 1` is reached (witness gives no evidence). -/
def mrSquares (n : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | fuel + 1, x =>
    let x' := x * x % n
    if x' == n - 1 then true else mrSquares n fuel x'

/-- One Miller-Rabin round for witness `a`: `true` means "no evidence that `n` is
composite" (probable prime for this base). Out-of-range witnesses are skipped. -/
def mrRound (n s d a : Nat) : Bool :=
  if a < 2 || n - 1 ≤ a then true
  else
    let x := powMod a d n
    if x == 1 || x == n - 1 then true
    else mrSquares n (s - 1) x

/-- Deterministic Miller-Rabin over a fixed list of witness bases. -/
def millerRabinDet (n : Nat) (as : List Nat) : Bool :=
  if n < 4 then n == 2 || n == 3
  else if n % 2 == 0 then false
  else
    let sd := factorTwos (n - 1)
    as.all (fun a => mrRound n sd.1 sd.2 a)

/-- **The `2^s · d` decomposition is correct for every `m ≥ 1`.** -/
theorem factorTwos_spec :
    ∀ m, m ≠ 0 →
      2 ^ (factorTwos m).1 * (factorTwos m).2 = m ∧ (factorTwos m).2 % 2 = 1 := by
  intro m
  induction m using Nat.strongRecOn with
  | _ m ih =>
    intro hm
    rw [factorTwos]
    split
    · next h =>
      obtain ⟨hne, heven⟩ := h
      have hlt : m / 2 < m := Nat.div_lt_self (Nat.pos_of_ne_zero hne) (by decide)
      have hhalf : m / 2 ≠ 0 := by omega
      obtain ⟨ih1, ih2⟩ := ih (m / 2) hlt hhalf
      refine ⟨?_, ih2⟩
      rw [Nat.pow_succ]
      rw [Nat.mul_right_comm, ih1]
      omega
    · next h =>
      have hm2 : m % 2 ≠ 0 := by
        intro hc; exact h ⟨hm, hc⟩
      refine ⟨?_, by omega⟩
      simp

/-- **The deterministic test matches the specification, exhaustively, below 2000.**
Bases `[2, 3]` are *known in the literature* to be exact up to 1 373 653; this
theorem machine-checks only the range `n < 2000`. Extending the guarantee beyond
the checked range needs the number-theoretic soundness argument, not exhaustion. -/
theorem millerRabinDet_agrees_below_2000 :
    ∀ n, n < 2000 → 2 ≤ n → (millerRabinDet n [2, 3] = true ↔ IsPrime n) := by
  native_decide

/-- Unlike the trial-division `isPrime`, Miller-Rabin also answers the `0`/`1`
edge cases correctly. -/
example : millerRabinDet 0 [2, 3] = false := by native_decide
example : millerRabinDet 1 [2, 3] = false := by native_decide

/-- Cross-checks against the Python doctest examples. -/
example : millerRabinDet 101 [2, 3] = true := by native_decide
example : millerRabinDet 102 [2, 3] = false := by native_decide
example : millerRabinDet 103 [2, 3] = true := by native_decide

end Nprime
