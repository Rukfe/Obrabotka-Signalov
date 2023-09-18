import colorama
import numpy as np
from numpy.fft import fft
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal
import matplotlib.pyplot as plt

canvases = None


def read_file():
    global data
    plt.close('all')

    # Открываем окно выбора файла
    filename = filedialog.askopenfilename()

    if not filename:
        print("Файл не выбран")
    else:
        # Открываем файл в двоичном режиме ("rb")
        with open(filename, "rb") as file:
            # Читаем данные из файла в массив "data"
            data = np.fromfile(file, dtype=np.float32)
            print(colorama.Fore.GREEN, "Файл прочитан успешно")

            # Очищаем предыдущее содержимое в списке (для результатов в окне приложения)
            data_listbox.delete(0, tk.END)

            # Заполняем список данными из файла (для результатов в окне приложения)
            for index, value in enumerate(data):
                data_listbox.insert(tk.END, f"{index}: {value}")


# Строим график исходного сигнала
def std_graph():
    global canvases
    if canvases is not None:
        canvases.get_tk_widget().pack_forget()
        canvases = None

    fig1 = plt.figure(figsize=(60, 2))
    plt.plot(data)
    fig_canvas1 = FigureCanvasTkAgg(fig1, master=app)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack()
    canvases = fig_canvas1


# Строим график спектра сигнала
def spectr_graph():
    global canvases
    if canvases is not None:
        canvases.get_tk_widget().pack_forget()
        canvases = None

    fft_result = np.fft.fft(data)
    spectrum = np.abs(fft_result)
    freqs = np.fft.fftfreq(len(data))

    fig2 = plt.figure(figsize=(60, 2))
    plt.plot(freqs, spectrum)
    canvas2 = FigureCanvasTkAgg(fig2, master=app)  # Создаем холст для отображения графика
    canvas2.draw()
    canvas2.get_tk_widget().pack()
    canvases = canvas2


def plot_cf_signal():
    global canvases
    if canvases is not None:
        canvases.get_tk_widget().pack_forget()
        canvases = None

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
    global channel_dpf
    channel_dpf = signal.filtfilt(filters[1], 1, data)

    # Построение графика сигнала второго канала после фильтрации
    fig4 = plt.figure(figsize=(60, 2))
    plt.plot(channel_dpf)
    plt.grid()
    canvas4 = FigureCanvasTkAgg(fig4, master=app)  # Создаем холст для отображения графика
    canvas4.draw()

    canvas4.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases = canvas4

    threshold = 0.5  # Пороговое значение амплитуды

    # Список для хранения значений битов
    bit_values = []

    # Разбиваем временной ряд на 5 равных частей
    signal_parts = np.array_split(channel_dpf, 5)

    # Определяем значение бита для каждой части сигнала
    for part in signal_parts:
        # Проверяем, превышает ли амплитуда выделенного сигнала пороговое значение
        if np.max(part-0.05) > threshold:
            bit_values.append(1)  # Логическая "1"
        else:
            bit_values.append(0)  # Логическая "0"

    # Преобразуем список значений битов в 5-битовый код
    bit_code = ''.join(str(bit) for bit in bit_values)
    print(f"5-битовый код: {bit_code}")


# Создаем окно приложения
app = tk.Tk()
app.geometry("1100x700")
app.title("Сигнал и спектр")

# Создаем контейнер для графиков
graph_container = tk.Frame(app)
graph_container.pack()

# Кнопка "Чтение файла"
read_button = tk.Button(app, text="Чтение файла", command=read_file)
read_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения исходного сигнала"
plot_std_button = tk.Button(app, text="Исходный сигнал", command=std_graph)
plot_std_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения спектра"
plot_spectr_button = tk.Button(app, text="Спектр", command=spectr_graph)
plot_spectr_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения сигнала после ЦФ"
plot_cf_button = tk.Button(app, text="ЦФ", command=plot_cf_signal)
plot_cf_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Создаем список для отображения данных из файла
data_listbox = tk.Listbox(app)
data_listbox.pack(side="right", anchor="s", ipadx=1, ipady=2)

# Запускаем главный цикл приложения
app.mainloop()
