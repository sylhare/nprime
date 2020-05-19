from nprime.pyprime import sacks, pyprime, ulam


def sacks_plot(upper=10000, prime_test_function=pyprime):  # pragma: no cover
    """
    Render the sacks_plot from the sacks function.
    By default the coord is plot in white and the prime_coord in black

    Return a polar plot of the sacks' diagram

    """
    import matplotlib.pyplot as plt
    coord, prime_coord = sacks(upper, prime_test_function)

    plt.figure()
    ax = plt.subplot(111, projection='polar', facecolor='white')
    plt.title('Sacks\' Diagram', loc='right')
    ax.plot(zip(*coord), "w+", markersize=1)
    ax.plot(zip(*prime_coord), "ko", markersize=2)
    plt.show()


def ulam_plot(upper=10000, edge=4, prime_test_function=pyprime):  # pragma: no cover
    """
    Render the sacks_plot from the ulam function.
    By default the coord is plot in white and the prime_coord in black

    Return a polar plot of the ulam's spiral

    """
    import matplotlib.pyplot as plt
    coord, prime_coord = ulam(upper, edge, prime_test_function)

    plt.figure()
    plt.title('Ulam\'s sprial', loc='right')
    plt.plot(zip(*coord), 'w+', markersize=1)
    plt.plot(zip(*prime_coord), 'ko', markersize=2)
    plt.grid(True)
    plt.show()
