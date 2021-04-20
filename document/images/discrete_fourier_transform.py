import numpy as np
import matplotlib.pyplot as plt

def discrete_fourier_transform(x, n, k):
    x = x[:, np.newaxis]
    n = n[:, np.newaxis]

    N = k.size

    return np.sum(x * np.exp(-1j * 2 * np.pi * (k / N) * n), axis=0)

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

T = (t.max() - t.min()) / t.size
n = t // T

K = 1000
k = np.fft.fftfreq(K) * K

x = rect(t, 1)

plt.figure()
plt.stem(k, discrete_fourier_transform(x, n, k).real, markerfmt='C0o', label=r'$\Re\{X[k]\}$')
plt.stem(k, discrete_fourier_transform(x, n, k).imag, markerfmt='C1o', label=r'$\Im\{X[k]\}$')
plt.xlabel('k')
plt.ylabel('X[k]')
plt.grid(True)
plt.legend()
plt.show()
