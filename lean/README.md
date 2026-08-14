# Lean verification (prototype)

Formal, machine-checked correctness proofs for the algorithms in `nprime/`.

Each Python algorithm is mirrored as an executable Lean 4 function, then proven
to compute exactly the textbook mathematical specification. A successful build
(`lake build`) *is* the proof: Lean's kernel checks every step, so nothing can be
"green" unless the algorithm is provably correct.

## Why

Tests check finitely many inputs. A Lean proof of `isPrime n = true ↔ IsPrime n`
covers **all** `n` at once. It also pins down edge cases precisely -- this
prototype proves, for example, that the trial-division `is_prime` returns `true`
for `1` even though `1` is not prime (`isPrime_one` / `not_isPrime_one`), the
exact boundary where the Python code and the specification diverge.

## Two proof strategies

Different algorithms admit different depths of guarantee:

- **Unbounded proofs** cover *all* inputs. `isPrime_iff` (trial division) and
  `factorTwos_spec` (the Miller-Rabin `n-1 = 2^s·d` decomposition) are of this
  kind -- kernel-checked, no bound.

- **Bounded exhaustive proofs** cover every input below a limit via `native_decide`,
  which compiles the check to native code and certifies the result. Used where a
  full proof needs heavy number theory: the deterministic Miller-Rabin/spec
  equivalence (`< 2000`) and the AKS helpers. These are genuine theorems, but only
  about the checked range, and they trust the Lean compiler (the `native_decide`
  boundary) rather than only the kernel.

Where an unbounded proof is out of reach without Mathlib, that limit is stated
explicitly rather than papered over -- e.g. Miller-Rabin's unbounded soundness
rests on Fermat's little theorem and the structure of `(ℤ/nℤ)ˣ`, so it is called
out in `MillerRabin.lean` and left for a Mathlib-backed follow-up.

## Layout

| File | Contents |
| --- | --- |
| `Nprime/Spec.lean` | `IsPrime` -- the reference definition of primality (dependency-free). |
| `Nprime/IsPrime.lean` | Port of `pyprime.py::is_prime` (trial division) + `isPrime_iff`, its full correctness proof. |
| `Nprime/MillerRabin.lean` | Deterministic Miller-Rabin: unbounded proof of the `2^s·d` decomposition + exhaustive `[2,3]`-base equivalence with the spec below 2000. |
| `Nprime/Aks.lean` | AKS arithmetic core: `intRoot` (exact floor b-th root) and `perfectPower`, each verified against a spec over a bounded range. |
| `Nprime/Ir.lean` | Tiny deeply-embedded IR for trial-search algorithms, with a Lean semantics (`denote`) and a Python emitter (`toPython`). |
| `Nprime/Codegen.lean` | `isPrimeProg` (the algorithm as IR) + `isPrimeProg_correct`: the emitted code meets the spec. |
| `Generate.lean` | `lake exe codegen` entry point that writes `generated/is_prime.py`. |
| `Nprime.lean` | Library root importing every module. |

No Mathlib dependency: the whole project builds in a few seconds on the stock
Lean toolchain pinned in `lean-toolchain`.

## Build

```bash
cd lean
lake build          # verifies every proof
```

Requires [`elan`](https://github.com/leanprover/elan) (Lean toolchain manager);
the exact Lean version is pinned in `lean-toolchain`.

## The correctness statement

```lean
-- Nprime/IsPrime.lean
theorem isPrime_iff (n : Nat) (hn : 2 ≤ n) : isPrime n = true ↔ IsPrime n
```

The proof relies on the classic square-root bound (`exists_small_divisor`): any
composite `n` has a divisor `≤ √n`, which is why trial division only needs to
reach `math.isqrt(n)`.

## Verify-then-generate: Lean as the source of truth

Rather than checking hand-written Python against Lean, we can make the verified
Lean the *source* and generate the Python from it, so the shipped code is correct
by construction. This is how verified software ships (CompCert, seL4, Fiat-Crypto).

The pipeline:

1. The algorithm is written once as an IR program `isPrimeProg` (`Codegen.lean`).
2. `denote_isPrimeProg` proves its Lean semantics *is* the verified `isPrime`
   (definitionally -- `rfl`), so `isPrimeProg_correct` gives, for all `n ≥ 2`:
   ```lean
   isPrimeProg.denote n = true ↔ IsPrime n
   ```
3. The *same* IR is rendered to Python by `toPython` and written out:
   ```bash
   lake exe codegen        # writes generated/is_prime.py
   ```

The generated `generated/is_prime.py` is checked to match the hand-written
`nprime/is_prime`: it passes the library's own primality test data and agrees
with it on every `n` in `0..20000`. The only unverified link is the `toPython`
pretty-printer -- the standard trusted boundary of any extraction pipeline.

Note the generator faithfully carries the proof's precondition: like the original,
`generated is_prime(1)` returns `True`, and the correctness theorem only claims
`n ≥ 2` -- the gap is explicit, not hidden.

## Extending to the other algorithms

The pattern for each new algorithm:

1. Port the Python function to an executable Lean `def` in a new `Nprime/<Name>.lean`.
2. State a theorem relating it to `IsPrime` (or another spec in `Spec.lean`).
3. Prove it, and add `import Nprime.<Name>` to `Nprime.lean`.

Covered so far: `is_prime`, `miller_rabin` (deterministic variant), and the AKS
helpers `int_root` / `perfect_power`.

Good next candidates: `generate_primes` / `sieve_eratosthenes` (every element is
prime and none are missed), `prime_factors` (product equals `n`, each factor
prime), and `is_perfect` (sum of proper divisors equals `n`). Remaining AKS work:
the polynomial ring `(ℤ/nℤ)[X]/(Xʳ-1)`, `find_r`, and a bounded full-`aks`/spec
equivalence. A Mathlib-backed track could then prove the unbounded Miller-Rabin
and AKS soundness that the dependency-free prototype checks only over a range.
