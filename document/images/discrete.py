import numpy as np
import matplotlib.pyplot as plt

Ts = 0.25
n = np.arange(0, int(4 / Ts) + 1, Ts)
x = np.exp(-n*Ts) * np.sin(2 * np.pi * n * Ts)

plt.stem(n, x)
plt.xlabel('n')
plt.ylabel('x[n]')
plt.grid(True)
plt.show()
