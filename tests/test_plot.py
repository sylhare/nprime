import matplotlib.pyplot as plt
import pytest

from nprime.plot import sacks_plot, ulam_plot
from nprime.pyprime import sacks, ulam


@pytest.fixture(autouse=True)
def _no_show(monkeypatch):
    """Stop ``plt.show`` from doing anything and close figures afterwards."""
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    yield
    plt.close("all")


def test_sacks_plot_builds_a_figure():
    """sacks_plot draws every point without raising on the zip iterator."""
    coord, prime_coord = sacks(200)
    sacks_plot(upper=200)

    ax = plt.gcf().axes[0]
    assert ax.lines, "expected at least one plotted series"
    assert sum(len(line.get_xdata()) for line in ax.lines) == len(coord) + len(prime_coord)


def test_ulam_plot_builds_a_figure():
    """ulam_plot draws every point without raising on the zip iterator."""
    coord, prime_coord = ulam(200)
    ulam_plot(upper=200)

    ax = plt.gcf().axes[0]
    assert ax.lines, "expected at least one plotted series"
    assert sum(len(line.get_xdata()) for line in ax.lines) == len(coord) + len(prime_coord)
