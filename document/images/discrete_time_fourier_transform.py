import numpy as np
import matplotlib.pyplot as plt


def discrete_time_fourier_transform(x, n, f, T):
    n = n[:, np.newaxis]
    x = x[:, np.newaxis]

    return np.sum(x * np.exp(-1j * 2 * np.pi * f * n * T), axis=0)


@np.vectorize
def rect(t, T):
    if np.abs(t) < T / 2:
        return 1
    elif np.abs(t) == T / 2:
        return 1 / 2
    else:
        return 0


@np.vectorize
def sinc(t):
    return np.sin(np.pi * t) / (np.pi * t) if t != 0 else 1


N = 1000

t = np.linspace(-1, 1, N)
x = rect(t, 1)

T = (t.max() - t.min()) / t.size

f = np.linspace(-20, 20, 1000)
n = t * N / (t.max() - t.min())

plt.figure()
plt.plot(f, discrete_time_fourier_transform(x, n, f, T).real,
         label=r'$\Re\{\widehat{x_T}(f)\}$')
plt.plot(f, discrete_time_fourier_transform(x, n, f, T).imag,
         label=r'$\Im\{\widehat{x_T}(f)\}$')
plt.xlabel('f [Hz]')
plt.ylabel(r'$\widehat{x_T}(f)$')
plt.grid(True)
plt.legend()
plt.show()
