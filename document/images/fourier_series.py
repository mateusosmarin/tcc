import numpy as np
import matplotlib.pyplot as plt


def fourier(x, t, T, N):
    dt = (t.max() - t.min()) / t.size

    t = t[:, np.newaxis]
    x = x[:, np.newaxis]

    n = np.arange(-N, N + 1)

    cn = 1 / T * np.sum(x * np.exp(-1j * 2 * np.pi * n * t / T) * dt, axis=0)

    return np.sum(cn * np.exp(1j * 2 * np.pi * n * t / T), axis=1)


@np.vectorize
def rect(t, T):
    if np.abs(t) < T / 2:
        return 1
    elif np.abs(t) == T / 2:
        return 1 / 2
    else:
        return 0


T = 2
t = np.linspace(-T / 2, T / 2, 1000)
x = rect(t, 1)

plt.plot(t, x, label="Original")
plt.plot(t, fourier(x, t, T, 4).real, label="N = 4")
plt.plot(t, fourier(x, t, T, 16).real, label="N = 16")
plt.plot(t, fourier(x, t, T, 64).real, label="N = 64")
plt.xlabel('t [s]')
plt.ylabel('x(t)')
plt.legend()
plt.grid(True)
plt.show()
