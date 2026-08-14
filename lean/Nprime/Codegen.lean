import Nprime.Ir
import Nprime.IsPrime

/-
The trial-division primality test expressed once, as an IR program, and shown to
coincide with the verified `isPrime`. Emitting `isPrimeProg` therefore produces
Python that provably meets the `IsPrime` specification (`isPrimeProg_correct`).
-/

namespace Nprime

/-- `is_prime` as an IR program: `for i in range(2, isqrt(n) + 1): if n % i == 0 …` -/
def isPrimeProg : TrialLoop where
  lo := .lit 2
  hiExcl := .add (.isqrt .input) (.lit 1)
  cond := .modEqZero .input .loop

/-- The IR semantics of `isPrimeProg` is exactly the verified `isPrime` function.
Holds definitionally: the IR was built to unfold to `isPrime`'s body. -/
theorem denote_isPrimeProg (n : Nat) : isPrimeProg.denote n = isPrime n := rfl

/-- **The generated program meets the specification.** For every `n ≥ 2`, the IR
program (hence the emitted Python) returns `true` iff `n` is prime. -/
theorem isPrimeProg_correct (n : Nat) (hn : 2 ≤ n) :
    isPrimeProg.denote n = true ↔ IsPrime n := by
  rw [denote_isPrimeProg]; exact isPrime_iff n hn

/-- The Python source generated from the verified program. -/
def isPrimePython : String := isPrimeProg.toPython "is_prime"

end Nprime
