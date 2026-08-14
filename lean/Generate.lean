import Nprime.Codegen

open Nprime

/-- Emit the Python generated from the verified IR program. -/
def main : IO Unit := do
  IO.FS.createDirAll "generated"
  IO.FS.writeFile "generated/is_prime.py" isPrimePython
  IO.println "wrote generated/is_prime.py:\n"
  IO.println isPrimePython
