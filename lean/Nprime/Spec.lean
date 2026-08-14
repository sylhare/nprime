/-
Mathematical reference definition of primality, used as the specification that
every algorithm implementation is verified against.

Kept dependency-free (no Mathlib) so the whole project builds in seconds on the
stock Lean toolchain. The definition is deliberately the textbook one: `n` is
prime when it is at least 2 and has no divisor strictly between 1 and `n`.
-/

namespace Nprime

/-- `n` is prime: at least 2, with no proper divisor `m` in the range `2 ≤ m < n`.

The bound `m < n` is written first so Lean's built-in bounded-quantifier
decision procedure (`Nat.decidableBallLT`) makes `IsPrime` decidable for free. -/
def IsPrime (n : Nat) : Prop :=
  2 ≤ n ∧ ∀ m, m < n → 2 ≤ m → n % m ≠ 0

instance : DecidablePred IsPrime := fun _ => inferInstanceAs (Decidable (_ ∧ _))

end Nprime
