import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import time

class SimpleGraphApp:

    grafica = False

    def __init__(self, root):
        self.root = root
        self.root.title("Motor temperatura")

        # Configurar la figura de Matplotlib
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Temperatura del Motor")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.line, = self.ax.plot([], [], 'r-', label="Temperatura")
        self.ax.legend()

        self.x_data = [0]
        self.y_data = [0]

        # Crear el canvas de Matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Crear el Entry para ingresar valores
        self.entry = ttk.Entry(self.root)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Crear el botón para agregar valores a la gráfica
        self.add_button = ttk.Button(self.root, text="Iniciar/Detener", command=self.iniciarf)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.ser = serial.Serial("COM3", 9600, timeout=1)
        time.sleep(2)

    def iniciarf(self):
        self.grafica = not self.grafica
        if self.grafica:
            self.update_graph()

    def add_value(self):
        try:
            value = float(self.entry.get())
            self.x_data.append(len(self.x_data) + 1)
            self.y_data.append(value)
            self.line.set_data(self.x_data, self.y_data)
            self.ax.set_xlim(0, len(self.x_data) + 1)
            self.ax.set_ylim(min(self.y_data) - 1, max(self.y_data) + 1)
            self.canvas.draw()
            self.entry.delete(0, tk.END)
        except ValueError:
            print("Please enter a valid number")

    def update_graph(self):
        if self.grafica:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("Temperature:"):
                    value = float(line.split(":")[1].strip().split()[0])
                    print(value)
                    self.x_data.append(len(self.x_data) + 1)
                    self.y_data.append(value)
                    self.line.set_data(self.x_data, self.y_data)
                    self.ax.set_xlim(0, len(self.x_data) + 1)
                    self.ax.set_ylim(min(self.y_data) - 1, max(self.y_data) + 1)
                    self.canvas.draw()
            except Exception as e:
                print(f"Error reading line: {e}")
            # Programar la siguiente actualización
            self.root.after(1000, self.update_graph)  # Llamar de nuevo a update_graph después de 2000 ms


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGraphApp(root)
    root.mainloop()
