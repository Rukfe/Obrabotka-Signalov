import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Создаем графический интерфейс пользователя
root = tk.Tk()
root.withdraw()

# Открываем окно выбора файла
filename = filedialog.askopenfilename()

if not filename:
    print("Не был выбран файл")
else:
    # Открывает файл в двоичном режиме ("rb")
    with open(filename, "rb") as file:

        # Читаем данные из файла в массив "data"
        data = np.fromfile(file, dtype=np.float32)

        # Создаем таблицу из массива "data"
        df = pd.DataFrame({"Номер точки": range(len(data)), "Значение": data})

        # Выводим таблицу в терминале
        print("Данные из файла:")
        print(df)

        # Сохраняем таблицу в файл .TXT
        save_filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if not save_filename:
            print("Не удалось сохранить таблицу")
        else:
            df.to_string(save_filename, index=False, header=True, index_names=False,
                         columns=["Номер точки", "Значение"])
            print(f"Таблица сохранена в файл: {save_filename}")
    # Создаем график
    plt.plot(data)
    plt.xlabel("Время")
    plt.ylabel("Значение")
    plt.title("График данных")
    plt.grid(True)
    plt.show()
