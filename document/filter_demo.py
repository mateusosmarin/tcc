import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Nome do arquivo do filtro exportado
filename = "filter.pickle"

# O arquivo deve ser aberto para leitura em formato binario (rb)
with open(filename, "rb") as file:
    # O metodo pickle.load permite carregar o objeto serializado
    tf = pickle.load(file)

# Obtem o periodo e frequencia de amostragem definidos no filtro
Ts = tf.dt
fs = 1 / Ts

# Constroi um vetor de tempo amostrado em Ts
t = np.arange(0, 200 * Ts, Ts)

# Sintetiza dois tons de frequencias 10 kHz e 1 kHz
x1 = np.sin(2 * np.pi * 10e3 * t)
x2 = np.sin(2 * np.pi * 1e3 * t)

# Aplica-se o filtro utilizando o metodo tf.output
t, y1 = tf.output(x1, t)
t, y2 = tf.output(x2, t)

# Obtem a resposta em frequencia do filtro
f, h = signal.freqz(tf.num, tf.den, fs=fs)

# Calcula a amplitude da resposta em dB
mag = 20 * np.log(np.abs(h))
# Calcula a fase da resposta em graus
phase = np.degrees(np.unwrap(np.angle(h)))

fig, axes = plt.subplots(2, 1)
fig.canvas.set_window_title("Resposta em frequencia")

# Cria figura para amplitude da resposta em frequencia
axes[0].plot(f, mag)
axes[0].set_xlabel(r"$f\[Hz]$")
axes[0].set_ylabel(r"$|H(\mathrm{i} 2 \pi f)|^2\ [dB]$")
axes[0].grid(True)

# Cria figura para fase da resposta em frequencia
axes[1].plot(f, phase)
axes[1].set_xlabel(r"$f\[Hz]$")
axes[1].set_ylabel(r"$\angle{H(\mathrm{i} 2 \pi f)\ [deg]}$")
axes[1].grid(True)

fig.tight_layout()

# Exibe sinais sintetizados
plt.figure("Sinais sintetizados")
plt.plot(t, x1, label=r"$\sin(2 \pi\ 10 \ times 10^3 t)$")
plt.plot(t, x2, label=r"$\sin(2 \pi\ 1 \ times 10^3 t)$")
plt.xlabel(r"$t\ [s]$")
plt.ylabel(r"$x(t)$")
plt.grid(True)
plt.legend()

# Exibe sinais filtrados
plt.figure("Sinais filtrados")
plt.plot(t, y1,
         label=r"$\mathcal{H}\{\sin(2 \pi\ 10 \ times 10^3 t)\}$")
plt.plot(t, y2,
         label=r"$\mathcal{H}\{\sin(2 \pi\ 1 \ times 10^3 t)\}$")
plt.xlabel(r"$t\ [s]$")
plt.ylabel(r"$y(t)$")
plt.grid(True)
plt.legend()

plt.show()
