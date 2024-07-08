from tkinter import *
from tkinter import messagebox , ttk
import serial

class VentanaArduino(Toplevel):

    puertoarduino = ""
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Arduino Conexión | Pyduino")
        self.geometry("500x200")
        etiqueta_secundaria = Label(self, text="Antes de comenzar.")
        etiqueta_secundaria.pack(pady=20)
        valor=StringVar()
        puertoa= Label(self,text="Para poder utilizar el programa por favor selecciona el puerto de tu arduino").pack(pady=10)
        seleccionar_puerto = ttk.Combobox(self, width=20, textvariable=valor)
        seleccionar_puerto['values'] = ('COM1','COM2','COM3','COM4','COM5')
        seleccionar_puerto.pack(pady=10)
        botonp= Button(self, text="Seleccionar Puerto", command=lambda : self.vef(valor.get())).pack()
        if self.puertoarduino == "error":
            # error = Label(self,text="Ha ocurrido un error al conectar al arduino, prueba con otro puerto",fg='red',font='bold')
            # error.pack(pady=30)
            messagebox.showerror(title='Error al conectar con arduino',message="El puerto es incorrecto o esta ocupado.")

    def vef(self, valor):
        print(valor)
        try:
            arduino = serial.Serial(valor, 9600)
            self.parent.puertoarduino = self.puertoarduino='COM3'
            messagebox.showinfo(title="Pyduino | Conexion exitosa ", message="Arduino esta conectado.")
            print("Arduino está conectado.")
            self.destroy()
        except serial.SerialException:
            self.parent.puertoarduino = self.puertoarduino='error'
            print("Arduino no está conectado.")
            messagebox.showinfo(title="Pyduino | Conexion erronea", message="No se puede conectar con el arduino.")