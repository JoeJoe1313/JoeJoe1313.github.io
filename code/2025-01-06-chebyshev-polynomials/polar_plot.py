import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.chebyshev import Chebyshev

theta = np.linspace(0, 2 * np.pi, 2000)
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})

# Generate and fill between consecutive curves
for n in range(0, 19 * 2, 2):
    r1 = n + Chebyshev([0] * n + [1])(theta / np.pi - 1)
    r2 = (n + 2) + Chebyshev([0] * (n + 2) + [1])(theta / np.pi - 1)

    # Create black and white alternating pattern
    if n % 4 == 0:
        ax.fill_between(theta, r1, r2, color="black")
    else:
        ax.fill_between(theta, r1, r2, color="white")
ax.set_title("x = t/π - 1", y=1)
plt.axis("off")
plt.show()
