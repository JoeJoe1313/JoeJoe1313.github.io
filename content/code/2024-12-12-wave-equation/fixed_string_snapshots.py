import matplotlib.pyplot as plt
import numpy as np

# Define constants
L = np.pi * np.sqrt(5)
a = 2 / 3
x = np.linspace(0, L, 101)


# Define the initial condition phi(x)
def phi(x):
    y = np.zeros_like(x)
    y[(1 < x) & (x < 3)] = np.sin(np.pi * x[(1 < x) & (x < 3)]) ** 3
    return y


# Define the initial velocity psi(x)
def psi(x):
    return np.zeros_like(x)


# Correct the method name to np.trapz
def fourier_u(x, t):
    y = np.zeros_like(x)
    for k in range(1, 101):
        Xk = np.sin(k * np.pi * x / L)
        Ak = (2 / L) * np.trapz(phi(x) * Xk, x)
        Bk = (2 / (a * k * np.pi)) * np.trapz(psi(x) * Xk, x)
        Tk = Ak * np.cos(a * k * np.pi * t / L) + Bk * np.sin(a * k * np.pi * t / L)
        y += Tk * Xk
    return y


# Time points for snapshots
time_snapshots = [0, 20, 30]
snapshot_filenames = []

# Create and save snapshots again
snapshot_filenames = []
for t in time_snapshots:
    y = fourier_u(x, t)
    plt.figure(figsize=(16, 2))
    plt.plot(x, y, label=f"t = {t}", color="r")
    plt.xlabel("x")
    plt.ylabel("u(x, t)")
    plt.title(f"String Vibration at t = {t}")
    # plt.grid(True)
    plt.legend()
    snapshot_filename = f"string_snapshot_t{t}.png"
    plt.savefig(snapshot_filename)
    snapshot_filenames.append(snapshot_filename)
    plt.close()
