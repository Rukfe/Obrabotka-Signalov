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

            # Выводим таблицу в терминале
            print("Данные из файла:")
            print(df)

            status_label.config(text="Файл прочитан успешно")

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
        fig = Figure(figsize=(18, 3.5))
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set(xlabel="Время", ylabel="Значение",
               title="Исходный сигнал")
        ax.grid(True)

        # Создаем встроенный график Tkinter (для результатов в окне приложения)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
window.geometry("1920x1080")
window.title("Задание 1 v_0.0.1")

# Кнопка "Чтение файла"
read_button = tk.Button(window, text="Чтение файла", command=read_file)
read_button.place(x=10, y=935, width=110, height=70)

# Кнопка для построения исходного сигнала"
plot_std_button = tk.Button(window, text="Исходный сигнал", command=plot_std_signal)
plot_std_button.place(x=130, y=935, width=110, height=70)

# Кнопка для построения спектра"
plot_spectr_button = tk.Button(window, text="Спектр", command=plot_spectr_signal)
plot_spectr_button.place(x=250, y=935, width=110, height=70)

# Кнопка для построения сигнала после ЦФ"
plot_spectr_button = tk.Button(window, text="ЦФ", command=plot_cf_signal)
plot_spectr_button.place(x=370, y=935, width=110, height=70)

# Кнопка для закрытия окна
close_button = tk.Button(window, text="Выход", command=window.destroy)
close_button.place(x=1790, y=935, width=110, height=70)

# Список с прокруткой для отображения "Номер точки" и "Значение"
data_frame = tk.Frame(window)
data_frame.place(x=1490, y=840, width=110)

# Фрейм для графика
graph_frame = tk.Frame(window)
graph_frame.pack()

# Статусное сообщение
status_label = tk.Label(window, text="")
status_label.pack()

data_scrollbar = tk.Scrollbar(data_frame)
data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

data_listbox = tk.Listbox(data_frame, yscrollcommand=data_scrollbar.set)
data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

data_scrollbar.config(command=data_listbox.yview)

# Запускаем цикл обработки событий
window.mainloop()
