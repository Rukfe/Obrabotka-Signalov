import numpy as np
import plotly.graph_objects as go


omega = np.pi / 100
omega_zero = np.pi / 5
N = 500
M = 0.028

t = np.linspace(0, N, num=N + 1)
S = (1 + M * np.sin(omega * t)) * np.sin(omega_zero * t)

fig = go.Figure(data=go.Scatter(x=t, y=S, mode='lines'))

# Добавляем заголовок и метки осей
fig.update_layout(title='График функции S(t)=[1 + M * sin (Ω*t)] * sin(ω0 * t)', xaxis_title='t', yaxis_title='S')

# Отображаем график
fig.show()
