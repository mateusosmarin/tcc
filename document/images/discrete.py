import numpy as np
import matplotlib.pyplot as plt

Ts = 0.5 ** 4
t = np.arange(0, 4, Ts)

n = t / Ts
x = np.exp(-n * Ts) * np.sin(2 * np.pi * n * Ts)

plt.stem(n, x)
plt.xlabel('n [samples]')
plt.ylabel('x[n]')
plt.grid(True)
plt.show()
