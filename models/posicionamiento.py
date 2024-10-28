from tkinter import *
from tkinter import messagebox

class Posicionamiento(Tk):

    def __init__(self,parent):
        super().__init__()
        self.principal = parent
        self.title("Posicionamiento | Pyduino")
        self.geometry("300x180")
        self.resizable(0,0)
        label = Label(self, text="Selecciona el Modo de Posicionamiento")
        label.pack(padx=20, pady=20)
        boton_manual = Button(self, text="Manual", command=lambda: self.seleccionar_modo("Manual"))
        boton_manual.pack(side=LEFT, padx=45, pady=3)
        boton_automatico = Button(self, text="Automático", command=lambda: self.seleccionar_modo("Automático"))
        boton_automatico.pack(side=RIGHT, padx=45, pady=3)
        
    
    def seleccionar_modo(self,modo):
        messagebox.showinfo("Modo Seleccionado", f"Modo {modo} seleccionado")
        self.principal.modoposicionamiento = modo
        self.destroy()
        