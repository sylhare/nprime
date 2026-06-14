from nprime.pyprime import pyprime, sacks_points, ulam_points

PATH_STYLE = dict(color='0.6', linewidth=1.5, linestyle='solid',
                  solid_capstyle='round', antialiased=True, zorder=1)


def sacks_plot(upper=10000, prime_test_function=pyprime, show_path=False):  # pragma: no cover
    """
    Render the sacks_plot from the sacks function.
    By default the coord is plot in white and the prime_coord in black

    Set show_path=True to draw the underlying spiral as a grey line to follow.

    Return a polar plot of the sacks' diagram

    """
    import matplotlib.pyplot as plt
    coord, prime_coord, path = _split_points(sacks_points(upper, prime_test_function))

    plt.figure()
    ax = plt.subplot(111, projection='polar', facecolor='white')
    plt.title('Sacks\' Diagram', loc='right')
    ax.plot(*zip(*coord, strict=False), "w+", markersize=1, zorder=0)
    if show_path:
        ax.plot(*zip(*path, strict=False), **PATH_STYLE)
    ax.plot(*zip(*prime_coord, strict=False), "ko", markersize=2, zorder=2)
    plt.show()


def ulam_plot(upper=10000, edge=4, prime_test_function=pyprime, show_path=False):  # pragma: no cover
    """
    Render the sacks_plot from the ulam function.
    By default the coord is plot in white and the prime_coord in black

    Set show_path=True to draw the underlying spiral as a grey line to follow.

    Return a polar plot of the ulam's spiral

    """
    import matplotlib.pyplot as plt
    coord, prime_coord, path = _split_points(ulam_points(upper, edge, prime_test_function))

    plt.figure()
    plt.title('Ulam\'s spiral', loc='right')
    plt.plot(*zip(*coord, strict=False), 'w+', markersize=1, zorder=0)
    if show_path:
        plt.plot(*zip(*path, strict=False), **PATH_STYLE)
    plt.plot(*zip(*prime_coord, strict=False), 'ko', markersize=2, zorder=2)
    plt.grid(True)
    plt.show()


def _split_points(points):
    """Consume an ordered ``(point, is_prime)`` stream into (coord, prime_coord, path)."""
    coord, prime_coord, path = [], [], []
    for point, prime in points:
        path.append(point)
        (prime_coord if prime else coord).append(point)
    return coord, prime_coord, path
