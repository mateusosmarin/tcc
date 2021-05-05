import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def laplace_transform(x, t, s):
    dt = (t.max() - t.min()) / t.size

    x = x[:, np.newaxis, np.newaxis]
    t = t[:, np.newaxis, np.newaxis]

    return np.sum(x * np.exp(-s * t) * dt, axis=0)


@np.vectorize
def rect(t, T):
    if np.abs(t) < T / 2:
        return 1
    elif np.abs(t) == T / 2:
        return 1 / 2
    else:
        return 0


N = 1000
t = np.linspace(-1, 1, N)
x = rect(t, 1)

sigma = np.linspace(-5, 5, 20)
omega = 2 * np.pi * np.linspace(-5, 5, 1000)

sigma, omega = np.meshgrid(sigma, omega)
s = sigma + 1j * omega

X = laplace_transform(x, t, s)

fig = plt.figure()
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_title(r'$\Re\{X(s)\}$')
ax.plot_surface(s.real, s.imag / (2 * np.pi), np.real(laplace_transform(x, t, s)), cmap=cm.jet)
ax.view_init(elev=30, azim=30)
ax.set_xlabel(r'$\sigma$ $[s^{-1}]$')
ax.set_ylabel(r'$i 2 \pi f\ [rad/s]$')
ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.set_title(r'$\Im\{X(s)\}$')
ax.plot_surface(s.real, s.imag / (2 * np.pi), np.imag(laplace_transform(x, t, s)), cmap=cm.jet)
ax.view_init(elev=30, azim=30)
ax.set_xlabel(r'$\sigma$ $[s^{-1}]$')
ax.set_ylabel(r'$i 2 \pi f\ [rad/s]$')
plt.show()
