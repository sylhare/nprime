import matplotlib

# Use a non-interactive backend so plotting tests run on headless CI
# (no display / no Tk) without trying to open a GUI window.
matplotlib.use("Agg")
