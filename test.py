import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import colorama
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Инициализация модуля colorama
colorama.init()

# Глобальная переменная для хранения данных после чтения файла
data = None

# Переменная для хранения текущего графика
current_plot = None


# Функция для чтения файла
def read_file():
    global data
    # Открываем окно выбора файла
    filename = filedialog.askopenfilename()

    if not filename:
        print("Файл не выбран")
    else:
        # Открываем файл в двоичном режиме ("rb")
        with open(filename, "rb") as file:
            # Читаем данные из файла в массив "data"
            data = np.fromfile(file, dtype=np.float32)

            # Создаем таблицу из массива "data"
            df = pd.DataFrame({"Номер точки": range(len(data)), "Значение": data})
            print("Файл прочитан успешно")

            # Выводим таблицу в терминале
            print("Данные из файла:")
            print(df)

            # Очищаем предыдущее содержимое в списке (для результатов в окне приложения)
            data_listbox.delete(0, tk.END)

            # Заполняем список данными из файла (для результатов в окне приложения)
            for index, value in enumerate(data):
                data_listbox.insert(tk.END, f"{index}: {value}")


# Функция для построения графика исходного сигнала
def plot_std_signal():
    global current_plot
    if data is None:
        print("Файл не был выбран")
    else:
        # Удаляем предыдущий график, если он существует (для результатов в окне приложения)
        if current_plot is not None:
            current_plot.get_tk_widget().pack_forget()
            current_plot = None

        # Создаем график
        fig = Figure(figsize=(60, 2))
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set(title="Исходный сигнал")
        ax.grid(True)

        # Создаем встроенный график Tkinter (для результатов в окне приложения)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.X, expand=True)
        current_plot = canvas


# Функция для построения графика спектра
def plot_spectr_signal():
    print(colorama.Fore.RED + "Внимание!\nПостроение графика спектра пока не доступно!")
    window.destroy()


# Функция для построения графика ЦФ
def plot_cf_signal():
    print(colorama.Fore.RED + "Внимание!\nПостроение графика сигнала после ЦФ пока не доступно!")
    window.destroy()


# Создаем графический интерфейс пользователя
window = tk.Tk()
window.geometry("1100x700")
window.title("Задание 1 v_0.0.1")

# Фрейм для графика
graph_frame = tk.Frame(window)
graph_frame.pack()

# Кнопка "Чтение файла"
read_button = tk.Button(window, text="Чтение файла", command=read_file)
read_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения исходного сигнала"
plot_std_button = tk.Button(window, text="Исходный сигнал", command=plot_std_signal)
plot_std_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения спектра"
plot_spectr_button = tk.Button(window, text="Спектр", command=plot_spectr_signal)
plot_spectr_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения сигнала после ЦФ"
plot_spectr_button = tk.Button(window, text="ЦФ", command=plot_cf_signal)
plot_spectr_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для закрытия окна
close_button = tk.Button(window, text="Выход", command=window.destroy)
close_button.pack(side="right", anchor="se", ipadx=10, ipady=10)

# Список с прокруткой для отображения "Номер точки" и "Значение"
data_frame = tk.Frame(window)
data_frame.pack(side="bottom", anchor="s", ipadx=1, ipady=1)

data_scrollbar = tk.Scrollbar(data_frame)
data_scrollbar.pack(side="right", anchor="s", ipadx=3, ipady=1)

data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
data_listbox.pack(side="right", anchor="s", ipadx=1, ipady=2)

data_scrollbar.config(command=data_listbox.yview)

# Запускаем цикл обработки событий
window.mainloop()
