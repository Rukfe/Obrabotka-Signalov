import numpy as np
import matplotlib.pyplot as plt

omega = np.pi / 100
omega_zero = np.pi / 5
N = 500
M = 0.028

t = np.linspace(0, N, num=N+1)
S = (1 + M * np.sin(omega * t)) * np.sin(omega_zero * t)

plt.plot(t, S)
plt.xlabel('t')
plt.ylabel('S(t)')
plt.title('Graph of S(t)=[1 + M * sin (Ω*t)] * sin(ω0 * t)')
plt.grid(True)
plt.show()