import tkinter as tk
import numpy as np
import cmath
from tkinter import Button, Frame, filedialog, messagebox, simpledialog
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



N = 500  # число отсчетов
M = 65  # порядок фильтра
M_2 = M // 2
freqDiskret = 2000 #частота дискретизации
freqNeiqvist = freqDiskret / 2
x = np.zeros(N, dtype=np.float32)  # входной сигнал
y = np.zeros(N, dtype=np.float32)
h = np.zeros(M, dtype=np.float32)  # импульсная характеристика


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Задание 3 (ЦОС)")
        self.iconbitmap("KFU.ico")
        self.geometry("1200x700")
        
        
        self.graphIsx = Frame(self)
        self.graphIsx.pack()
        self.graphIsxEmpty()
        
        self.graphImp = Frame(self)
        self.graphImp.pack()
        self.graphImpEmpty()
        
        self.graphCf = Frame(self)
        self.graphCf.pack()
        self.graphCfEmpty()
        

        self.file_button = tk.Button(self, text="Выбрать файл и построить\nграфик исходного сигнала", command=self.open_file)
        self.file_button.pack(side="left", anchor="sw", ipadx=10, ipady=2)
        
        self.exit_button = tk.Button(self, text="Выход", command=self.quit)
        self.exit_button.pack(side="right", anchor="se", ipadx=10, ipady=10)
        

        self.impBtn = Button(self, text="Характеристика h(i)", command=partial(self.numChannel))
        self.impBtn.pack(side="left", anchor="sw", ipadx=10, ipady=10)
        
        self.cfBtn = Button(self, text="ЦФ", command=self.channelCF)
        self.cfBtn.pack(side="left", anchor="sw", ipadx=10, ipady=10)
        
        self.listBoxIsx = tk.Listbox(self)
        self.listBoxIsx.pack(side="left", anchor="sw", ipadx=5, ipady=2)
        self.listBoxIsx.insert(tk.END, 'Исходный сигнал')
        
        self.listBoxImpulse = tk.Listbox(self)
        self.listBoxImpulse.pack(side="left", anchor="sw", ipadx=5, ipady=2)
        self.listBoxImpulse.insert(tk.END, 'Характеристика h(i)')
        
        self.listBoxCF = tk.Listbox(self)
        self.listBoxCF.pack(side="left", anchor="sw", ipadx=5, ipady=2)
        self.listBoxCF.insert(tk.END, 'После ЦФ')
        
    def graphIsxEmpty(self):
        # создание пустого графика
        global isxCanvas
        figIsx = Figure(figsize=(60, 2))
        self.ax = figIsx.add_subplot(111)
        self.ax.set_title("Исходный сигнал")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(figIsx, master=self.graphIsx)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        isxCanvas = self.canvas
        
    def graphImpEmpty(self):
        # создание пустого графика
        global impulseCanvas
        figImpulse = Figure(figsize=(60, 2))
        self.ax = figImpulse.add_subplot(111)
        self.ax.set_title("Отсчеты импульсной хар-ки h(i). Порядок фильтра M = 65")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(figImpulse, master=self.graphImp)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        impulseCanvas = self.canvas 
        
    def graphCfEmpty(self):
        # создание пустого графика
        global cfCanvas
        figCf = Figure(figsize=(60, 2))
        self.ax = figCf.add_subplot(111)
        self.ax.set_title("После ЦФ")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(figCf, master=self.graphCf)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        cfCanvas = self.canvas       
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('.dat файлы', '*.dat')])
        if not file_path:
            messagebox.showerror("Ошибка!", "Файл не был прочитан!")
            return()
        with open(file_path, 'rb') as file:
            k = 0
            while True:
                global data
                data = file.read(4)  # 4 байта для float32
                if not data:
                    messagebox.showinfo("Успех!", "Файл был прочитан!")
                    break
                x[k] = np.frombuffer(data, dtype=np.float32)[0]
                y[k] = np.frombuffer(data, dtype=np.float32)[0]
                self.listBoxIsx.insert(tk.END, f'{k + 1}.  {x[k]}')
                k += 1
                
        # построение графика
        global isxCanvas
        if isxCanvas is not None:
            isxCanvas.get_tk_widget().pack_forget()
        figIsx = Figure(figsize = (60 , 2))
        self.ax = figIsx.add_subplot(111)
        self.ax.set_title("Исходный сигнал")
        self.ax.grid(True)
        self.ax.plot(np.arange(0, N), x, color="black")
        self.canvas = FigureCanvasTkAgg(figIsx, master=self.graphIsx)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        
    def numChannel(self):
        global channelNum
        try:
            if data is None:
                messagebox.showerror('Ошибка!', 'Не был выбран файл')
                return()
        except NameError:
            messagebox.showerror('Ошибка!', 'Не был выбран файл')
            return()
        
        channelNum = simpledialog.askinteger("Ввод канала", "Введите номер канала (от 1 до 5):")
        if channelNum is not None and channelNum > 0 and channelNum <= 5 or not channelNum:
            self.impulseChar(channelNum)
        
    def impulseChar(self, channelNum):
        if channelNum is None:
            messagebox.showerror('Ошибка!', 'Введите верное значение канала (целое число от 1 до 5)')
            return()
        freqCenter = channelNum * 40 #несущая частота с полученным каналом
        freqLow = (freqCenter - 20)
        freqHigh = (freqCenter + 20)
        count = 2
        
        h[0] = (freqHigh - freqLow) / freqNeiqvist
        self.listBoxImpulse.insert(tk.END, '1. ' + str(h[0]))
        
        for k in range(-M_2, M_2 + 1):
            if k == 0:
                h[k + M_2] = (freqHigh - freqLow) / freqNeiqvist
            else:
                h[k + M_2] = (np.sin(np.pi * k * freqHigh / freqNeiqvist) / (np.pi * k) -
                            np.sin(np.pi * k * freqLow / freqNeiqvist) / (np.pi * k))
                if k >= 0:
                    self.listBoxImpulse.insert(tk.END, f"{count}. {str(h[k + M_2])}")
                    count += 1
                    
        global impulseCanvas
        if impulseCanvas is not None:
            impulseCanvas.get_tk_widget().pack_forget()
        figImpulse = Figure(figsize=(60, 2))
        self.ax = figImpulse.add_subplot(111)
        self.ax.set_title("Отсчеты импульсной хар-ки h(i). Порядок фильтра M = 65")
        self.ax.grid(True)
        self.ax.bar(range(-M_2, M_2 + 1), h, width=0.8, color = "black")
        self.canvas = FigureCanvasTkAgg(figImpulse, master=self.graphImp)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        impulseCanvas = self.canvas
        
    def channelCF(self):
        try:
            if data is None:
                messagebox.showerror('Ошибка!', 'Не был выбран файл')
                return()
        except NameError:
            messagebox.showerror('Ошибка!', 'Не был выбран файл')
            return()
            
        global channelNum
            # Создание цифрового фильтра с прямоугольной идеальной формой АЧХ
        fs = 2000  # Частота дискретизации
        delta_f = 40  # Ширина полосы частот канала
        f0 = [40, 80, 120, 160, 200]  # Центральные частоты каналов (40, 80, 120, 160, 200 Гц)
        count = 1
        
    # Вычисляем границы полосы частот для выбранного канала
        try:
            if channelNum is None:
                messagebox.showerror('Ошибка!', 'Введите верное значение канала (целое число от 1 до 5)')
                return()
            f1 = f0[channelNum - 1] - delta_f / 2
            f2 = f0[channelNum - 1] + delta_f / 2
        except NameError:
            messagebox.showerror('Ошибка!', 'Не был выбран канал (можно выбрать через кнопку "Характеристика h(i)")')
            return()
            
    # Создаем фильтр для выбранного канала
        for n in range(M):
            if n == M_2:
                h[n] = (2 * (f2 - f1)) / fs
            else:
                h[n] = (np.sin(2 * cmath.pi * (n - M_2) * f2 / fs) - np.sin(2 * cmath.pi * (n - M_2) * f1 / fs)) / (
                            cmath.pi * (n - M_2))
    
     # Фильтруем сигнал с помощью импульсной характеристики
        y_filtered = np.convolve(x, h, mode='same')
        for value in y_filtered:
            self.listBoxCF.insert(tk.END, f"{count}. {value}")
            count += 1
        

        global cfCanvas
        if cfCanvas is not None:
            cfCanvas.get_tk_widget().pack_forget()
        figCf = Figure(figsize=(60, 2))
        self.ax = figCf.add_subplot(111)
        self.ax.set_title("После ЦФ")
        self.ax.grid(True)
        self.ax.plot(y_filtered, color = "black")
        self.canvas = FigureCanvasTkAgg(figCf, master=self.graphCf)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True)
        cfCanvas = self.canvas

    
if __name__ == '__main__':
    app = Application()
    app.mainloop()