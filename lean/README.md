# Lean verification

Machine-checked correctness proofs for the algorithms in `nprime/`, stated against
Mathlib's canonical `Nat.Prime`. Each claim below is proved for **all** integers by
Lean's kernel, so `lake build` *is* the proof. The primality results are real
theorems, not bounded/exhaustive checks over a range.

## What is proved (unbounded, kernel-checked)

| Theorem | Statement |
| --- | --- |
| `isPrime_iff_nat_prime` | trial-division `is_prime n` decides `Nat.Prime n`, for `n ≥ 2` |
| `millerRabinDet_complete` | a prime always passes Miller-Rabin, for any bases (Fermat's little theorem + `ℤ/nℤ` a field) |
| `factorTwos_spec` | the `n - 1 = 2^s · d` decomposition is correct |
| `intRoot_exact` | `int_root n b` is the exact floor `b`-th root |
| `perfectPower_sound` | a reported perfect power is composite (AKS step 1) |

`IsPrime`, the elementary specification, is itself proved equal to `Nat.Prime`
(`isPrime_iff_prime`), so no algorithm is validated against a definition tailored to
match its own code.

## What is not proved

Deterministic Miller-Rabin *soundness* -- that passing fixed bases `[2, 3]` forces
primality -- is **false** for general `n` (strong pseudoprimes exist) and holds only
below a bound established by computation. `millerRabinDet_sound_below_2000` records it
as a `native_decide` check over `n < 2000`: a machine check, not a theorem for all `n`.
Full AKS correctness (the ring `(ℤ/nℤ)[X]/(Xʳ - 1)`, `find_r`) and Rabin's ¾-witness
soundness are out of scope.

## Layout

| File | Contents |
| --- | --- |
| `Nprime/Spec.lean` | `IsPrime` and its equivalence with `Nat.Prime`. |
| `Nprime/IsPrime.lean` | Trial division (`is_prime`) and its full correctness. |
| `Nprime/MillerRabin.lean` | Deterministic Miller-Rabin: unbounded completeness + bounded soundness check. |
| `Nprime/Aks.lean` | AKS arithmetic core: `intRoot_exact`, `perfectPower_sound`. |
| `Nprime/Ir.lean` | Deeply-embedded IR for trial-search algorithms (`denote` + `toPython`). |
| `Nprime/Codegen.lean` | `is_prime` as IR + `isPrimeProg_correct`. |
| `Generate.lean` | `lake exe codegen`, emits `generated/is_prime.py`. |

## Build

```bash
cd lean
lake exe cache get   # first time only: downloads prebuilt Mathlib
lake build           # verifies every proof
```

Requires [`elan`](https://github.com/leanprover/elan); the Lean version is pinned in
`lean-toolchain` and matched by the Mathlib revision in `lakefile.toml`.

## Verify-then-generate

Rather than checking hand-written Python against Lean, the verified Lean is the
*source*: `is_prime` is written once as an IR program (`isPrimeProg`) whose Lean
semantics is proved to meet the spec (`isPrimeProg_correct`), and the same IR is
rendered to Python by `toPython`:

```bash
lake exe codegen     # writes generated/is_prime.py
```

The generated file matches the hand-written `nprime/is_prime` and agrees with it on
every `n` in `0..20000`. The only unverified link is the `toPython` printer, the usual
trusted boundary of code extraction. Only proven-correct deciders are emitted, so
Miller-Rabin and AKS are not generated: their primality correctness is not proved for
all `n` (see above).

## Adding an algorithm

Port the Python to an executable Lean `def`, state a theorem relating it to `Nat.Prime`
(or `IsPrime`), prove it, and add `import Nprime.<Name>` to `Nprime.lean`.
