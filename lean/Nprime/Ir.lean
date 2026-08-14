/-
Deeply-embedded IR for the "trial-search" primality algorithms: one bounded loop
returning `False` on the first `i` meeting a condition, `True` otherwise. Each node
has two interpretations that must agree -- `denote` (Lean meaning, used in proofs)
and `toPython` (emitted source). Emitting from the *same* IR whose `denote` is
proven correct makes the Python correct by construction; the only unverified link
is the `toPython` printer, the usual trusted boundary of extraction.
-/

namespace Nprime

/-- Arithmetic expressions over the input `n` and the loop variable `i`. -/
inductive Expr where
  | input                      -- the argument `n`
  | loop                       -- the loop variable `i`
  | lit (k : Nat)
  | add (a b : Expr)
  | isqrt (a : Expr)
  deriving Repr

/-- Boolean conditions inside the loop. -/
inductive BExpr where
  | modEqZero (a b : Expr)     -- `a % b == 0`
  deriving Repr

/-- A bounded trial-search loop. Its fixed control flow is "return `False` on the
first `i` in `[lo, hiExcl)` with `cond`, else `True`". -/
structure TrialLoop where
  lo : Expr
  hiExcl : Expr
  cond : BExpr
  deriving Repr

def Expr.eval (n i : Nat) : Expr → Nat
  | .input => n
  | .loop => i
  | .lit k => k
  | .add a b => a.eval n i + b.eval n i
  | .isqrt a => Nat.sqrt (a.eval n i)

def BExpr.eval (n i : Nat) : BExpr → Bool
  | .modEqZero a b => a.eval n i % b.eval n i == 0

/-- Lean semantics: `True` unless some `i ∈ [lo, hiExcl)` meets `cond`. Bounds are
evaluated at `i = 0`, matching Python's `range(...)`; this agrees with the emitted
code only for loop-independent bounds (true of every program here). Keep loop
bounds independent of `i`. -/
def TrialLoop.denote (L : TrialLoop) (n : Nat) : Bool :=
  (List.range (L.hiExcl.eval n 0)).all
    (fun i => i < L.lo.eval n 0 || !(L.cond.eval n i))

def Expr.toPython : Expr → String
  | .input => "n"
  | .loop => "i"
  | .lit k => toString k
  | .add a b => s!"({a.toPython} + {b.toPython})"
  | .isqrt a => s!"math.isqrt({a.toPython})"

def BExpr.toPython : BExpr → String
  | .modEqZero a b => s!"{a.toPython} % {b.toPython} == 0"

/-- Render a loop as a complete Python function definition. -/
def TrialLoop.toPython (name : String) (L : TrialLoop) : String :=
  "# Generated from the verified Lean model in lean/Nprime/Codegen.lean.\n" ++
  "# Do not edit by hand -- regenerate with `lake exe codegen`.\n" ++
  "import math\n\n\n" ++
  s!"def {name}(n):\n" ++
  s!"    for i in range({L.lo.toPython}, {L.hiExcl.toPython}):\n" ++
  s!"        if {L.cond.toPython}:\n" ++
  "            return False\n" ++
  "    return True\n"

end Nprime
