import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 4, 1000)
x = np.exp(-t) * np.sin(2 * np.pi * t)

plt.plot(t, x)
plt.xlabel('t [s]')
plt.ylabel('x(t)')
plt.grid(True)
plt.show()
