import numpy as np
import matplotlib.pyplot as plt


def fourier_transform(x, t, f):
    dt = (t.max() - t.min()) / t.size

    t = t[:, np.newaxis]
    x = x[:, np.newaxis]

    return np.sum(x * np.exp(-1j * 2 * np.pi * f * t) * dt, axis=0)


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

f = np.linspace(-20, 20, N)

plt.plot(f, fourier_transform(x, t, f).real,
         label='$\operatorname{Re}\{X(f)\}$')
plt.plot(f, fourier_transform(x, t, f).imag,
         label='$\operatorname{Im}\{X(f)\}$')
plt.xlabel(r'$f\ [Hz]$')
plt.ylabel(r'$\mathcal{F}\{x(t)\}(f)$')
plt.grid(True)
plt.legend()
plt.show()
