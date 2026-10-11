import Nprime.Spec
import Nprime.IsPrime

/-
Deterministic Miller-Rabin (`nprime/pyprime.py::miller_rabin`, fixed witness bases).

`millerRabinDet_complete` proves the real, unbounded direction: for *every* prime
`n` and any bases, the test returns `true` -- it never rejects a prime. It rests on
Fermat's little theorem and the field structure of `ℤ/nℤ` (Mathlib), not on checking
cases.

The converse (a `true` verdict from fixed bases forces primality) is *false* in
general -- strong pseudoprimes exist -- and holds only below a bound established by
computation. `millerRabinDet_sound_below_2000` is that inherently-finite fact,
verified exhaustively for bases `[2, 3]`; it is a machine check, not a theorem for
all `n`.
-/

namespace Nprime

open scoped Classical

/-- Fast modular exponentiation `a ^ e mod m`. -/
def powMod (a e m : Nat) : Nat :=
  if e = 0 then 1 % m
  else
    let half := powMod a (e / 2) m
    let sq := half * half % m
    if e % 2 = 0 then sq else sq * a % m
termination_by e
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero ‹e ≠ 0›) (by decide)

/-- Decompose `m` as `2 ^ s * d` with `d` odd, as `(s, d)`. Mirrors the Python loop
`while d % 2 == 0: d //= 2; s += 1` applied to `n - 1`. -/
def factorTwos (m : Nat) : Nat × Nat :=
  if h : m ≠ 0 ∧ m % 2 = 0 then
    let r := factorTwos (m / 2)
    (r.1 + 1, r.2)
  else (0, m)
termination_by m
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero h.1) (by decide)

/-- The squaring loop: from `x`, square mod `n` up to `fuel` times, `true` on `n - 1`. -/
def mrSquares (n : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | fuel + 1, x =>
    let x' := x * x % n
    if x' == n - 1 then true else mrSquares n fuel x'

/-- One round for witness `a`: `true` means "no evidence `n` is composite". -/
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

/-- **The `2 ^ s · d` decomposition is correct for every `m ≥ 1`.** -/
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
      rw [Nat.pow_succ, Nat.mul_right_comm, ih1]
      omega
    · next h =>
      have hm2 : m % 2 ≠ 0 := by intro hc; exact h ⟨hm, hc⟩
      exact ⟨by simp, by omega⟩

/-! ### Completeness: Miller-Rabin never rejects a prime (all `n`) -/

private theorem powMod_modEq (a m : Nat) : ∀ e, powMod a e m ≡ a ^ e [MOD m] := by
  intro e
  induction e using Nat.strongRecOn with
  | _ e ih =>
    rw [powMod]
    split
    · next he => subst he; simpa using (Nat.mod_modEq 1 m)
    · next he =>
      have hhalf : e / 2 < e := Nat.div_lt_self (Nat.pos_of_ne_zero he) (by decide)
      have IH : powMod a (e / 2) m ≡ a ^ (e / 2) [MOD m] := ih (e / 2) hhalf
      have hsq : powMod a (e / 2) m * powMod a (e / 2) m ≡ a ^ (e / 2) * a ^ (e / 2) [MOD m] :=
        IH.mul IH
      rw [← pow_add] at hsq
      dsimp only
      split
      · next hev =>
        have hee : e / 2 + e / 2 = e := by omega
        rw [hee] at hsq
        exact (Nat.mod_modEq _ _).trans hsq
      · next hod =>
        have hee : e / 2 + e / 2 + 1 = e := by omega
        have step : powMod a (e / 2) m * powMod a (e / 2) m % m * a
            ≡ a ^ (e / 2 + e / 2) * a [MOD m] :=
          ((Nat.mod_modEq _ _).trans hsq).mul_right a
        rw [← pow_succ, hee] at step
        exact (Nat.mod_modEq _ _).trans step

private theorem powMod_lt (a e m : Nat) (hm : 0 < m) : powMod a e m < m := by
  rw [powMod]; split
  · exact Nat.mod_lt _ hm
  · dsimp only; split <;> exact Nat.mod_lt _ hm

private theorem natCast_ne_zero_of_lt (n a : Nat) (ha1 : 0 < a) (ha2 : a < n) :
    (a : ZMod n) ≠ 0 := by
  rw [Ne, ← Nat.cast_zero, ZMod.natCast_eq_natCast_iff]
  simp only [Nat.ModEq, Nat.zero_mod, Nat.mod_eq_of_lt ha2]
  omega

private theorem eq_of_castEq (n y z : Nat) (hy : y < n) (hz : z < n)
    (h : (y : ZMod n) = (z : ZMod n)) : y = z := by
  have hmod := (ZMod.natCast_eq_natCast_iff _ _ _).mp h
  rw [Nat.ModEq, Nat.mod_eq_of_lt hy, Nat.mod_eq_of_lt hz] at hmod
  exact hmod

/-- `x` squared `j` times mod `n`, the value inspected by `mrSquares` at step `j`. -/
private def sqStep (n x : Nat) : Nat := x * x % n
private def sqval (n : Nat) : Nat → Nat → Nat
  | 0, x => x
  | j + 1, x => sqval n j (sqStep n x)

private theorem mrSquares_true (n : Nat) :
    ∀ fuel x j, 1 ≤ j → j ≤ fuel → sqval n j x = n - 1 → mrSquares n fuel x = true := by
  intro fuel
  induction fuel with
  | zero => intro x j h1 h2 _; omega
  | succ fuel ih =>
    intro x j h1 h2 hj
    rw [mrSquares]
    by_cases hx : x * x % n = n - 1
    · simp [hx]
    · have hne : (x * x % n == n - 1) = false := by simpa [Nat.beq_eq] using hx
      simp only [hne, Bool.false_eq_true, if_false]
      have hge : j ≥ 2 := by
        rcases Nat.lt_or_ge j 2 with hlt | hge
        · exfalso; have : j = 1 := by omega
          rw [this] at hj; exact hx hj
        · exact hge
      have hval : sqval n (j - 1) (sqStep n x) = n - 1 := by
        have hs : j = (j - 1) + 1 := by omega
        rw [hs] at hj; exact hj
      exact ih (sqStep n x) (j - 1) (by omega) (by omega) hval

private theorem sqval_cast (n : Nat) :
    ∀ j x, ((sqval n j x : Nat) : ZMod n) = ((x : Nat) : ZMod n) ^ (2 ^ j) := by
  intro j
  induction j with
  | zero => intro x; simp [sqval]
  | succ j ih =>
    intro x
    rw [sqval, ih (sqStep n x)]
    have hstep : ((sqStep n x : Nat) : ZMod n) = ((x : Nat) : ZMod n) ^ 2 := by
      simp only [sqStep]
      rw [(ZMod.natCast_eq_natCast_iff _ _ _).mpr (Nat.mod_modEq (x * x) n)]
      push_cast; ring
    rw [hstep, ← pow_mul]
    congr 1
    rw [pow_succ]; ring

private theorem sqval_lt (n : Nat) (hn : 0 < n) : ∀ j x, 1 ≤ j → sqval n j x < n := by
  intro j
  induction j with
  | zero => intro x h; omega
  | succ j ih =>
    intro x _
    rw [sqval]
    rcases Nat.eq_zero_or_pos j with hj0 | hjpos
    · subst hj0; simp only [sqval, sqStep]; exact Nat.mod_lt _ hn
    · exact ih (sqStep n x) hjpos

/-- In `ℤ/nℤ` with `n` prime: from `α ^ (n-1) = 1` (Fermat) with `n - 1 = 2^s·d`,
either `α ^ d = 1` or some `α ^ (d·2^r) = -1` (`r < s`). The strong-probable-prime
property, via square roots of `1` in a field. -/
private theorem sq_chain (n : Nat) [Fact (Nat.Prime n)] (α : ZMod n) (hα : α ≠ 0)
    (s d : Nat) (h2sd : 2 ^ s * d = n - 1) :
    α ^ d = 1 ∨ ∃ r, r < s ∧ α ^ (d * 2 ^ r) = -1 := by
  have hsat : α ^ (d * 2 ^ s) = 1 := by
    rw [show d * 2 ^ s = 2 ^ s * d from by ring, h2sd]
    exact ZMod.pow_card_sub_one_eq_one hα
  have hex : ∃ r, α ^ (d * 2 ^ r) = 1 := ⟨s, hsat⟩
  have hr0 : α ^ (d * 2 ^ Nat.find hex) = 1 := Nat.find_spec hex
  rcases Nat.eq_zero_or_pos (Nat.find hex) with h0 | hpos
  · left
    have hd : α ^ (d * 2 ^ Nat.find hex) = α ^ d := by rw [h0]; simp
    rw [hd] at hr0; exact hr0
  · right
    refine ⟨Nat.find hex - 1, by have := Nat.find_min' hex hsat; omega, ?_⟩
    have he : d * 2 ^ (Nat.find hex - 1) * 2 = d * 2 ^ Nat.find hex := by
      have h2 : 2 ^ (Nat.find hex - 1) * 2 = 2 ^ Nat.find hex := by
        rw [← pow_succ]; congr 1; omega
      calc d * 2 ^ (Nat.find hex - 1) * 2 = d * (2 ^ (Nat.find hex - 1) * 2) := by ring
        _ = d * 2 ^ Nat.find hex := by rw [h2]
    have hbsq : (α ^ (d * 2 ^ (Nat.find hex - 1))) ^ 2 = 1 := by
      rw [← pow_mul, he]; exact hr0
    have hbne : α ^ (d * 2 ^ (Nat.find hex - 1)) ≠ 1 :=
      Nat.find_min hex (show Nat.find hex - 1 < Nat.find hex from by omega)
    have hmul : α ^ (d * 2 ^ (Nat.find hex - 1)) * α ^ (d * 2 ^ (Nat.find hex - 1)) = 1 := by
      rw [← pow_two]; exact hbsq
    rcases mul_self_eq_one_iff.mp hmul with h1 | hm1
    · exact absurd h1 hbne
    · exact hm1

private theorem mrRound_complete (n : Nat) (hn : Nat.Prime n) (hn4 : 4 ≤ n)
    (a s d : Nat) (h2sd : 2 ^ s * d = n - 1) (hs : 1 ≤ s) :
    mrRound n s d a = true := by
  haveI : Fact (Nat.Prime n) := ⟨hn⟩
  rw [mrRound]
  split
  · rfl
  · next hcond =>
    simp only [Bool.not_eq_true, Bool.or_eq_false_iff, decide_eq_false_iff_not,
      not_lt, not_le] at hcond
    obtain ⟨ha2, han1⟩ := hcond
    dsimp only
    split
    · rfl
    · next hcheck =>
      simp only [Bool.not_eq_true, Bool.or_eq_false_iff, beq_eq_false_iff_ne] at hcheck
      obtain ⟨hx1, hxn1⟩ := hcheck
      set x := powMod a d n with hxdef
      have hα : (a : ZMod n) ≠ 0 := natCast_ne_zero_of_lt n a (by omega) (by omega)
      have hxcast : (x : ZMod n) = (a : ZMod n) ^ d := by
        rw [hxdef, (ZMod.natCast_eq_natCast_iff _ _ _).mpr (powMod_modEq a n d)]
        push_cast; ring
      have hxlt : x < n := by rw [hxdef]; exact powMod_lt a d n (by omega)
      have hαd_ne1 : (a : ZMod n) ^ d ≠ 1 := by
        intro hc
        apply hx1
        have hc2 : (x : ZMod n) = ((1 : Nat) : ZMod n) := by rw [hxcast, hc]; simp
        exact eq_of_castEq n x 1 hxlt (by omega) hc2
      rcases sq_chain n (a : ZMod n) hα s d h2sd with hd1 | ⟨r, hrs, hrneg⟩
      · exact absurd hd1 hαd_ne1
      · have hsvcast : ((sqval n r x : Nat) : ZMod n) = ((n - 1 : Nat) : ZMod n) := by
          rw [sqval_cast n r x, hxcast, ← pow_mul, hrneg, Nat.cast_sub (by omega : 1 ≤ n),
            ZMod.natCast_self]
          ring
        rcases Nat.eq_zero_or_pos r with hr0 | hrpos
        · exfalso; apply hxn1
          rw [hr0] at hsvcast
          simp only [sqval] at hsvcast
          exact eq_of_castEq n x (n - 1) hxlt (by omega) hsvcast
        · have hsveq : sqval n r x = n - 1 :=
            eq_of_castEq n (sqval n r x) (n - 1) (sqval_lt n (by omega) r x hrpos) (by omega)
              hsvcast
          exact mrSquares_true n (s - 1) x r hrpos (by omega) hsveq

/-- **Completeness (all `n`): Miller-Rabin never rejects a prime.** For every prime
`n` and any witness bases, the deterministic test returns `true`. Proved from Fermat's
little theorem, with no bound on `n`. -/
theorem millerRabinDet_complete (n : Nat) (hn : Nat.Prime n) (as : List Nat) :
    millerRabinDet n as = true := by
  have hn2 : 2 ≤ n := hn.two_le
  rw [millerRabinDet]
  split
  · next h4 => interval_cases n <;> decide
  · next h4 =>
    split
    · next hev =>
      exfalso
      have h2dvd : (2 : Nat) ∣ n := Nat.dvd_of_mod_eq_zero (by simpa [Nat.beq_eq] using hev)
      rcases hn.eq_one_or_self_of_dvd 2 h2dvd with h | h <;> omega
    · next hodd =>
      have hmod : n % 2 = 1 := by
        have : n % 2 ≠ 0 := by simpa [Nat.beq_eq] using hodd
        omega
      rw [List.all_eq_true]
      intro a _
      obtain ⟨h2sd, hdodd⟩ := factorTwos_spec (n - 1) (by omega)
      have hs1 : 1 ≤ (factorTwos (n - 1)).1 := by
        rcases Nat.eq_zero_or_pos (factorTwos (n - 1)).1 with hs0 | hs1
        · rw [hs0, pow_zero, one_mul] at h2sd; omega
        · exact hs1
      exact mrRound_complete n hn (by omega) a _ _ h2sd hs1

/-! ### Soundness below a bound (inherently finite) -/

/-- **Bounded soundness.** For `n < 2000`, passing bases `[2, 3]` forces primality.
This is the exhaustive/computational direction (`native_decide`): it is *false* for
general `n` (strong pseudoprimes), so it is a machine check over the range, not a
theorem for all `n`. Bases `[2, 3]` are known exact up to 1 373 653. -/
theorem millerRabinDet_sound_below_2000 :
    ∀ n, n < 2000 → 2 ≤ n → millerRabinDet n [2, 3] = true → IsPrime n := by
  native_decide

/-- Unlike trial division, Miller-Rabin also answers the `0`/`1` edge cases. -/
example : millerRabinDet 0 [2, 3] = false := by native_decide
example : millerRabinDet 1 [2, 3] = false := by native_decide
example : millerRabinDet 102 [2, 3] = false := by native_decide

end Nprime
