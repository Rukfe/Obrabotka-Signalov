import numpy as np
import plotly.graph_objects as go

# Создаем массив значений x от 0 до 360 градусов с шагом 1 градус
x = np.arange(0, 360)

# Вычисляем значения y = sin(x) для каждого значения x
y = np.sin(np.radians(x))

# Создаем график
fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))

# Добавляем заголовок и метки осей
fig.update_layout(title='График функции y = sin(x)', xaxis_title='Градусы', yaxis_title='y')

# Отображаем график
fig.show()
