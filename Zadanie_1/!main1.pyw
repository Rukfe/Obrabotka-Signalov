import os
import numpy as np
from matplotlib.figure import Figure
from numpy.fft import fft
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal

# Определяем переменные
canvases1, canvases2, canvases3 = None, None, None
global data, filename


def read_file():
    global data, filename
    filename = filedialog.askopenfilename(filetypes=[("Выберите файл", "*.dat")])  # Открываем окно выбора файла
    if not filename:
        log_listbox.insert(tk.END, f"Файл не выбран")
    else:
        # Открываем файл в двоичном режиме ("rb")
        with open(filename, "rb") as file:
            # Читаем данные из файла в массив "data"
            data = np.fromfile(file, dtype=np.float32)
            log_listbox.delete(0, tk.END)
            log_listbox.insert(tk.END, f"Файл прочитан успешно")
            log_listbox.insert(tk.END, f"ОБРАТИТЕ ВНИМАНИЕ!!!")
            log_listbox.insert(tk.END, f"1) Здесь ведется работа ТОЛЬКО со 2-ым каналом")
            log_listbox.insert(tk.END, f"2) Графики строятся ТОЛЬКО после нажатия кнопки")

            # Очищаем предыдущее содержимое в списке (для результатов в окне приложения)
            data_listbox_isx.delete(0, tk.END)

            # Заполняем список данными из файла (для результатов в окне приложения)
            for index, value in enumerate(data):
                data_listbox_isx.insert(tk.END, f"{index + 1}: {value}")


# Создаем функции для построения пустых графиков в приложении
def graph_empty_isx():
    global canvases1
    fig1 = Figure(figsize=(60, 2))
    ax = fig1.add_subplot(111)
    ax.set_title("Исходный сигнал")
    ax.grid(True)
    ax.plot()
    fig_canvas1 = FigureCanvasTkAgg(fig1, master=graph_container)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases1 = fig_canvas1


def graph_empty_spectr():
    global canvases2
    fig2 = Figure(figsize=(60, 2))
    ax = fig2.add_subplot(111)
    ax.set_title("Спектр")
    ax.grid(True)
    ax.plot()
    canvas2 = FigureCanvasTkAgg(fig2, master=graph_container2)  # Создаем холст для отображения графика
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases2 = canvas2


def graph_empty_cf():
    global canvases3
    fig4 = Figure(figsize=(60, 2))
    ax = fig4.add_subplot(111)
    ax.set_title("После ЦФ")
    ax.grid(True)
    ax.plot()
    canvas3 = FigureCanvasTkAgg(fig4, master=graph_container3)  # Создаем холст для отображения графика
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases3 = canvas3


# Выполняем функцию для построения графика исходного сигнала
def std_graph():
    global canvases1
    if canvases1 is not None:
        canvases1.get_tk_widget().pack_forget()

    # Строим график исходного сигнала
    fig1 = Figure(figsize=(60, 2))
    ax = fig1.add_subplot(111)
    ax.set_title("Исходный сигнал")
    ax.grid(True)
    ax.plot(data, color="black")
    fig_canvas1 = FigureCanvasTkAgg(fig1, master=graph_container)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases1 = fig_canvas1


# Выполняем функцию для нахождения спектра сигнала и построения его графика
def spectr_graph():
    # Проверка на наличие / отсутствие графика в приложении
    global canvases2
    if canvases2 is not None:
        canvases2.get_tk_widget().pack_forget()

    fft_result = np.fft.fft(data)  # Применение преобразования Фурье к массиву данных
    spectrum = np.abs(fft_result)  # Вычисление спектра сигнала
    freqs = np.fft.fftfreq(len(data))  # Вычисление дискретных частот для спектра на основе длины массива данных.

    half_length = len(data) // 2  # Берем половину длины массива данных
    spectrum = spectrum[:half_length]  # Берем только первую половину спектра
    freqs = freqs[:half_length]  # Берем только первую половину частот
    # Это все мы делали для отображения спектра только в левой части

    # Строим график спектра
    fig2 = Figure(figsize=(60, 2))  # Создание нового объекта графика с заданными размерами
    ax = fig2.add_subplot(111)  # Добавление области для построения графика в новую фигуру
    ax.set_title("Спектр")  # Задаем заголовок графика.
    ax.grid(True)  # Включение отображения сетки на графике
    ax.plot(freqs, spectrum, color="black")  # Построение графика спектра сигнала и задаем цвет графика
    canvas2 = FigureCanvasTkAgg(fig2, master=graph_container2)  # Создаем холст для отображения графика
    canvas2.draw()  # Отрисовка построенного графика на холсте
    canvas2.get_tk_widget().pack(fill=tk.X, expand=True)  # Размещение холста в приложении и настройка его размеров
    canvases2 = canvas2  # Сохранение объекта холста в глобальной переменной, чтобы он мог быть использован позже


def plot_cf_signal():
    global canvases3
    if canvases3 is not None:
        canvases3.get_tk_widget().pack_forget()

    # Создание цифрового фильтра с прямоугольной идеальной формой АЧХ
    fs = 2000  # Частота дискретизации
    delta_f = 40  # Ширина полосы частот канала
    f0 = [40, 80, 120, 160, 200]  # Центральные частоты каналов (40, 80, 120, 160, 200 Гц)

    # Создание фильтров для каждого канала
    filters = []
    for freq in f0:
        b = signal.firwin(165, [freq - delta_f / 2, freq + delta_f / 2], fs=fs, pass_zero="bandpass")
        filters.append(b)

    # Выделение сигнала второго канала с помощью фильтрации ДПФ
    channel_dpf = signal.filtfilt(filters[1], 1, data)

    # Заполняем список данными выделенного канала (для результатов в окне приложения)
    data_listbox_cf.delete(0, tk.END)
    for index, value in enumerate(channel_dpf):
        data_listbox_cf.insert(tk.END, f"{index + 1}: {value}")

    # Построение графика сигнала второго канала после фильтрации
    fig4 = Figure(figsize=(60, 2))
    ax = fig4.add_subplot(111)
    ax.set_title("После ЦФ")
    ax.grid(True)
    ax.plot(channel_dpf, color="black")
    canvas3 = FigureCanvasTkAgg(fig4, master=graph_container3)  # Создаем холст для отображения графика
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases3 = canvas3

    threshold = 0.5  # Пороговое значение амплитуды
    bit_values = []  # Список для хранения значений битов

    # Разбиваем временной ряд на 5 равных частей
    signal_parts = np.array_split(channel_dpf, 5)

    # Определяем значение бита для каждой части сигнала
    for part in signal_parts:
        # Проверяем, превышает ли амплитуда выделенного сигнала пороговое значение
        if np.max(part - 0.05) > threshold:
            bit_values.append(1)  # Логическая "1"
        else:
            bit_values.append(0)  # Логическая "0"

    # Преобразуем список значений битов в 5-битовый код
    bit_code = ''.join(str(bit) for bit in bit_values)
    log_listbox.insert(tk.END, f"5 битовый код = {bit_code}")


# Создаем отдельное окно (приложение)
app = tk.Tk()  # Создаем окно приложения
app.geometry("1200x700")  # Задаем размер окна 
app.title("ЦОС (Задание 1)")  # Задаем название окна 
if os.path.exists("icon.ico"):  # Проверка, существует ли файл иконки
    app.iconbitmap("icon.ico")  # Если файл существует, используем его в качестве иконки
else:
    app.iconbitmap()  # Иначе используем стандартную иконку окна 

# Создаем контейнеры для графиков
graph_container = tk.Frame(app)
graph_container.pack()
graph_empty_isx()

graph_container2 = tk.Frame(app)
graph_container2.pack()
graph_empty_spectr()

graph_container3 = tk.Frame(app)
graph_container3.pack()
graph_empty_cf()

# Кнопка "Чтение файла"
read_button = tk.Button(app, text="Чтение файла", command=read_file)
read_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения исходного сигнала
plot_std_button = tk.Button(app, text="Исходный сигнал", command=std_graph)
plot_std_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения спектра
plot_spectr_button = tk.Button(app, text="Спектр", command=spectr_graph)
plot_spectr_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения сигнала после ЦФ
plot_cf_button = tk.Button(app, text="ЦФ", command=plot_cf_signal)
plot_cf_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Список состояния и вывод 5-битового кода
log_listbox = tk.Listbox(app)
log_listbox.pack(side="left", anchor="sw", ipadx=85, ipady=2)

# Кнопка для закрытия окна
close_button = tk.Button(app, text="Выход", command=app.destroy)
close_button.pack(side="right", anchor="se", ipadx=10, ipady=10)

# Создаем список для отображения данных цф
data_listbox_cf = tk.Listbox(app)
data_listbox_cf.pack(side="right", anchor="s", ipadx=25, ipady=2)
data_listbox_cf.insert(tk.END, f"Данные после ЦФ:")

# Создаем список для отображения данных из файла
data_listbox_isx = tk.Listbox(app)
data_listbox_isx.pack(side="right", anchor="s", ipadx=25, ipady=2)
data_listbox_isx.insert(tk.END, f"Данные исходного сигнала:")

# Запускаем главный цикл приложения
app.mainloop()
