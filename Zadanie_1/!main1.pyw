import colorama
import numpy as np
from matplotlib.figure import Figure
from numpy.fft import fft
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal

# Определяем переменные
canvases1, canvases2, canvases4 = None, None, None
global data, filename


def read_file():
    global data

    # Открываем окно выбора файла
    global filename
    filename = filedialog.askopenfilename(filetypes=[("Выберите файл", "*.dat")])

    if not filename:
        print(colorama.Fore.RED, "Файл не выбран")
        log_listbox.insert(tk.END, f"Файл не выбран")
    else:
        # Открываем файл в двоичном режиме ("rb")
        with open(filename, "rb") as file:
            # Читаем данные из файла в массив "data"
            data = np.fromfile(file, dtype=np.float32)
            print(colorama.Fore.GREEN, "Файл прочитан успешно")
            log_listbox.delete(0, tk.END)
            log_listbox.insert(tk.END, f"Файл прочитан успешно")
            log_listbox.insert(tk.END, f"ОБРАТИТЕ ВНИМАНИЕ!")
            log_listbox.insert(tk.END, f"Графики строятся после нажатия кнопки")

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
    global canvases4
    fig4 = Figure(figsize=(60, 2))
    ax = fig4.add_subplot(111)
    ax.set_title("После ЦФ")
    ax.grid(True)
    ax.plot()
    canvas4 = FigureCanvasTkAgg(fig4, master=graph_container3)  # Создаем холст для отображения графика
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases4 = canvas4


# Строим график исходного сигнала
def std_graph():
    global canvases1
    if canvases1 is not None:
        canvases1.get_tk_widget().pack_forget()

    fig1 = Figure(figsize=(60, 2))
    ax = fig1.add_subplot(111)
    ax.set_title("Исходный сигнал")
    ax.grid(True)
    ax.plot(data, color="black")
    fig_canvas1 = FigureCanvasTkAgg(fig1, master=graph_container)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases1 = fig_canvas1


# Строим график спектра сигнала
def spectr_graph():
    global canvases2
    if canvases2 is not None:
        canvases2.get_tk_widget().pack_forget()

    fft_result = np.fft.fft(data)  # Применение преобразования Фурье к массиву данных
    spectrum = np.abs(fft_result)  # Вычисление спектра сигнала
    freqs = np.fft.fftfreq(len(data))  # Вычисление дискретных частот для спектра на основе длины массива данных.

    fig2 = Figure(figsize=(60, 2))
    ax = fig2.add_subplot(111)
    ax.set_title("Спектр")
    ax.grid(True)
    ax.plot(freqs, spectrum, color="black")
    canvas2 = FigureCanvasTkAgg(fig2, master=graph_container2)  # Создаем холст для отображения графика
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases2 = canvas2


def plot_cf_signal():
    global canvases4
    if canvases4 is not None:
        canvases4.get_tk_widget().pack_forget()

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
    canvas4 = FigureCanvasTkAgg(fig4, master=graph_container3)  # Создаем холст для отображения графика
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases4 = canvas4

    threshold = 0.5  # Пороговое значение амплитуды

    # Список для хранения значений битов
    bit_values = []

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
    print(f"5-битовый код: {bit_code}")
    log_listbox.insert(tk.END, f"5 битовый код = {bit_code}")


# Создаем окно приложения
app = tk.Tk()
app.geometry("1200x700")
app.title("ЦОС")
app.iconbitmap("isxodnik\icon.ico")

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
log_listbox.pack(side="left", anchor="sw", ipadx=60, ipady=2)

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
