import tkinter as tk
from tkinter import filedialog
import colorama
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy import signal

# файл:5  канал:2

colorama.init()

# Глобальная переменная для хранения данных после чтения файла
# Переменная для хранения текущего графика
current_plot = None
canvases = None


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
            print(colorama.Fore.GREEN, "Файл прочитан успешно")

            # Очищаем предыдущее содержимое в списке (для результатов в окне приложения)
            data_listbox.delete(0, tk.END)

            # Заполняем список данными из файла (для результатов в окне приложения)
            for index, value in enumerate(data):
                data_listbox.insert(tk.END, f"{index}: {value}")


# Функция для построения графика исходного сигнала
def plot_std_signal():
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
        b = signal.firwin(101, [freq - delta_f / 2, freq + delta_f / 2], fs=fs)
        filters.append(b)

    # Разделение многоканального сигнала на отдельные каналы
    num_channels = len(f0)
    channel_data = np.reshape(data, (num_channels, -1))

    # Выделение сигнала второго канала с помощью фильтрации ДПФ
    channel_fft = signal.lfilter(filters[1], 1, channel_data[1])

    # Преобразуем обратно в одномерный массив
    output_data = np.zeros_like(data)
    output_data[:len(channel_fft)] = channel_fft

    # Построение графика сигнала второго канала после фильтрации
    # Создаем график
    fig = Figure(figsize=(60, 2))
    ax = fig.add_subplot(111)
    ax.plot(output_data)
    ax.set(title="Исходный сигнал")
    ax.grid(True)

    # Создаем встроенный график Tkinter (для результатов в окне приложения)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.X, expand=True)
    canvases = canvas


# Функция для построения графика спектра
def plot_spectrum_signal():
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

# Кнопка для построения исходного сигнала
plot_std_button = tk.Button(window, text="Исходный сигнал", command=plot_std_signal)
plot_std_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения спектра
plot_spectr_button = tk.Button(window, text="Спектр", command=plot_spectrum_signal)
plot_spectr_button.pack(side="left", anchor="sw", ipadx=10, ipady=10)

# Кнопка для построения сигнала после ЦФ
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
