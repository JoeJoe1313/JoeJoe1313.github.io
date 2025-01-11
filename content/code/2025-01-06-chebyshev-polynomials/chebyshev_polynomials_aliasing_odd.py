from typing import Union

import matplotlib.pyplot as plt
import numpy as np


def chebyshev_polynomial(
    n: int, x: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    """
    Calculate nth Chebyshev polynomial of the first kind T_n(x).

    Args:
        n: Order of polynomial (non-negative integer)
        x: Point(s) at which to evaluate polynomial

    Returns:
        Value of T_n(x)
    """
    if n < 0:
        raise ValueError("Order must be non-negative")

    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return x
    else:
        t_prev = np.ones_like(x)  # T_0
        t_curr = x  # T_1

        for _ in range(2, n + 1):
            t_next = 2 * x * t_curr - t_prev
            t_prev = t_curr
            t_curr = t_next

        return t_curr


def chebyshev_nodes(n):
    """Generate n Chebyshev nodes in [-1,1]"""
    k = np.arange(1, n + 1)
    return np.cos((2 * k - 1) * np.pi / (2 * n))


if __name__ == "__main__":

    x = np.linspace(-1, 1, 1000)
    plt.figure(figsize=(12, 6))
    plt.plot(x, -chebyshev_polynomial(1, x), "--", label=f"-T_{1}(x)", alpha=0.5)
    for n in [1, 2, 3, 5, 7, 9]:
        y = chebyshev_polynomial(n, x)
        plt.plot(x, y, label=f"T_{n}(x)")

    # plot nodes for n = 2
    n = 2
    nodes = chebyshev_nodes(n)
    y_nodes = np.cos(n * np.arccos(nodes))
    plt.plot(nodes, np.zeros_like(nodes), "bo", label="T_2(x) roots")
    for node in nodes:
        plt.plot([node, node], [-1, 1], "--", color="gray", alpha=0.5)

    # plt.grid(True)
    # Set aspect ratio to be equal
    # plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x")
    plt.ylabel("T_n(x)")
    plt.title("Chebyshev Polynomials Aliasing")
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.axhline(y=0, color="k", linestyle="-", alpha=0.7)
    plt.savefig(
        "content/images/2025-01-06-chebyshev-polynomials/chebyshev_polynomials_aliasing_odd.png"
    )
    plt.show()
