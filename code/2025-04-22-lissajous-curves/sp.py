import matplotlib.pyplot as plt
import numpy as np


def spherical_lissajous(m1, m2, alpha, num_points=1000):
    t = np.linspace(0, 2 * np.pi, num_points)
    x = np.sin(m2 * t) * np.cos(m1 * t - alpha * np.pi)
    y = np.sin(m2 * t) * np.sin(m1 * t - alpha * np.pi)
    z = np.cos(m2 * t)
    return x, y, z


x, y, z = spherical_lissajous(3, 2, 0)
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(x, y, z)
ax.set_title("Spherical Lissajous Curve: m1=3, m2=2, α=0")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 50)
x_sphere = np.outer(np.cos(u), np.sin(v))
y_sphere = np.outer(np.sin(u), np.sin(v))
z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_sphere, y_sphere, z_sphere, color="b", alpha=0.1)
plt.show()
