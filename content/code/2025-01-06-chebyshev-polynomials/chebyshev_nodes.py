import matplotlib.pyplot as plt
import numpy as np


def chebyshev_polynomial(n, x):
    """Generate values of nth Chebyshev polynomial at points x"""
    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return x
    else:
        T_prev = np.ones_like(x)  # T_0
        T_curr = x  # T_1
        for k in range(2, n + 1):
            T_next = 2 * x * T_curr - T_prev
            T_prev = T_curr
            T_curr = T_next
        return T_curr


def chebyshev_nodes(n):
    """Generate n Chebyshev nodes in [-1,1]"""
    k = np.arange(1, n + 1)
    return np.cos((2 * k - 1) * np.pi / (2 * n))


n = 8
nodes = chebyshev_nodes(n)

# Generate half circle points
theta = np.linspace(0, np.pi, 100)
x_circle = np.cos(theta)
y_circle = np.sin(theta)

# Plot Chebyshev polynomial
x = np.linspace(-1, 1, 200)
y = chebyshev_polynomial(n, x)
plt.plot(x, y, "g-", alpha=0.3, label=f"T_{n}(x)", color="blue")

# axs[i].legend()
# Plot half circle
plt.plot(x_circle, y_circle, "black", alpha=1)

# Plot points on circle and their projections
y_nodes = np.sqrt(1 - nodes**2)  # y coordinates on circle
if n == 8:
    print(y_nodes)
plt.plot(nodes, y_nodes, "ro")  # points on circle
plt.plot(nodes, np.zeros_like(nodes), "bo")  # projected points

# Draw projection lines
for x, y in zip(nodes, y_nodes):
    plt.plot([x, x], [0, y], "r--", alpha=0.3)

# Add x-axis
plt.plot([-1, 1], [0, 0], "k-", alpha=0.3)

# Set limits and labels
plt.xlim([-1.2, 1.2])
plt.ylim([-1.2, 1.2])
plt.xlabel("x")
plt.ylabel("T_8(x)")
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(False)
plt.title("Chebyshev Nodes")
plt.tight_layout()
plt.savefig("content/images/2025-01-06-chebyshev-polynomials/chebyshev_nodes.png")
plt.show()
