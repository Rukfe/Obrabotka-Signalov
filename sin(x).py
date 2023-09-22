import numpy as np
import matplotlib.pyplot as plt

# Создаем массив значений x от 0 до 360 градусов с шагом 1 градус
x = np.arange(0, 360)

# Вычисляем значения y = sin(x) для каждого значения x
y = np.sin(np.radians(x))

# Создаем график
plt.plot(x, y, 'o-')
plt.grid(True)

# Добавляем заголовок и метки осей и отображаем график
plt.title('График функции y = sin(x)')
plt.xlabel('Градусы')
plt.ylabel('y')
plt.show()
