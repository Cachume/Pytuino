import tkinter as tk
from tkinter import Scale, Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaMotor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Menu Motor | Pyduino")
        self.geometry("350x400")
        self.resizable(0, 0)
        self.valor = tk.StringVar()
        self.lede = 0
        self.ledse = tk.Label(self, text="Velocidad del motor: " + str(self.lede))
        self.ledse.pack(pady=15)

        # Barra de velocidad
        self.barra_velocidad = Scale(self, from_=0, to=10, orient="horizontal")
        self.barra_velocidad.pack(pady=30)

        # Botón de enviar comando (aún no implementado)
        enviar_button = Button(self, text="Enviar Comando", bg="black", fg="white",command=self.actualizar_grafica)
        enviar_button.pack()

        # Configuración de la gráfica
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        # self.puerto = puertoarduino

    def actualizar_grafica(self, valor):
        self.lede = int(valor)
        self.ledse.config(text="Velocidad del motor: " + valor)
        self.ax.clear()
        self.ax.plot([0, 1], [0, self.lede], 'r-')
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Velocidad')
        self.ax.set_title('Gráfica de Velocidad del Motor')
        self.ax.grid(True)
        self.canvas.draw()
