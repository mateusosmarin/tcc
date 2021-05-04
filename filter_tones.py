import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input('Filename: ')

with open(filename, 'rb') as f:
    tf = pickle.load(f)

Ts = tf.dt

t = np.arange(0, 200 * Ts, Ts)
x1 = np.sin(2 * np.pi * 2e3 * t)
x2 = np.sin(2 * np.pi * 6e3 * t)
x3 = np.sin(2 * np.pi * 10e3 * t)

plt.figure()
plt.plot(t, x1, label=r'$\sin(2 \pi \; 2 \times 10^3 t)$')
plt.plot(t, x2, label=r'$\sin(2 \pi \; 6 \times 10^3 t)$')
plt.plot(t, x3, label=r'$\sin(2 \pi \; 10 \times 10^3 t)$')
plt.grid(True)
plt.xlabel(r'$t \; [s]$')
plt.ylabel(r'$x(t) \; [V]$')
plt.legend()
plt.show()

t, y1 = tf.output(x1, t)
t, y2 = tf.output(x2, t)
t, y3 = tf.output(x3, t)

plt.figure()
plt.plot(t, y1, label=r'$\mathcal{H}\{\sin(2 \pi \; 2 \times 10^3 t)\}$')
plt.plot(t, y2, label=r'$\mathcal{H}\{\sin(2 \pi \; 6 \times 10^3 t)\}$')
plt.plot(t, y3, label=r'$\mathcal{H}\{\sin(2 \pi \; 10 \times 10^3 t)\}$')
plt.grid(True)
plt.xlabel(r'$t \; [s]$')
plt.ylabel(r'$y(t) \; [V]$')
plt.legend()
plt.show()
