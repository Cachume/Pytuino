from tkinter import *
from tkinter import messagebox, Menu, ttk
from os import path
import datetime
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
from funcmanual import KeyApp

class menuPrincipal(Tk):
    puertoarduino = ""
    datosuser = ""
    modoposicionamiento = None
    tipotransporte = None
    arduino = None

    def __init__(self, usuario):
        super().__init__()
        self.datosuser = usuario
        self.GetPuertos(0)
        self.title("Menu Principal | Pyduino")
        self.geometry("800x500")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        icono = PhotoImage(file="img/logos/logoapp.png")
        self.iconphoto(True, icono)

        # Sección de Bienvenida # Label(self, text="Te has conectado como:", font=("Arial", 11, 'bold')).place(x=10, y=10)
        # Label(self, text="Usuario: " + self.datosuser[1], font=("Arial", 10, 'bold')).place(x=10, y=40)
        # Label(self, text="Tipo de acceso: " + str(self.datosuser[3]), font=("Arial", 10, 'bold')).place(x=10, y=70)
        # Label(self, text="Última Conexión: " + self.datosuser[4], font=("Arial", 10, 'bold')).place(x=10, y=100)
       

        # Imagen del logo
        imagen_original = Image.open("img/pytuino_logo.png")
        imagen_redimensionada = imagen_original.resize((160, 50))
        self.logoimagen = ImageTk.PhotoImage(imagen_redimensionada)
        Label(self, image=self.logoimagen, bg="#ffffff").pack(pady=1)

        # Sección de Control de Velocidad
        velocidad_frame = Frame(self, background="#DAF7A6", width=200, height=140)
        velocidad_frame.place(x=10, y=210)
        Label(velocidad_frame, text="Control de Velocidad", font=("Arial", 12, 'bold'), bg="#DAF7A6").place(x=20, y=30)
        self.velocidad = Scale(velocidad_frame, from_=1, to=3, orient=HORIZONTAL, bg="#DAF7A6")
        self.velocidad.set(5)  # Velocidad inicial
        self.velocidad.place(x=40, y=70)

        # Sección de Posicionamiento Automático
        self.posiciona_frame = Frame(self, background="#F7DC6F", width=340, height=160)
        self.posiciona_frame.place(x=235, y=120)
        Label(self.posiciona_frame, text="Posicionamiento", font=("Arial", 11, 'bold'), bg="#F7DC6F").place(x=100, y=20)
        self.posiboton = Button(self.posiciona_frame, text="Gestionar Posicionamiento", command=lambda: self.mover_grua("pos2"),bg="#B9770E",fg="#ffffff",font=("Open Sans", 9, "bold"))
        self.posiboton.place(x=80, y=80)

        # Botón de Emergencia (Modo de Seguridad)
        self.boton_emergencia = Button(self, text="EMERGENCIA", bg="red", fg="white", font=("Arial", 12, 'bold'), command=self.emergencia)
        self.boton_emergencia.place(x=650, y=450)

        self.boton_inicio = Button(self, text="Iniciar Trabajo", bg="#0ED611", fg="white", font=("Arial", 12, 'bold'),command=self.iniciar)
        self.boton_inicio.place(x=500, y=450)

        # Sección de Feedback Visual#
        Feedback_frame = Frame(self, background="#DAF7A6", width=200, height=190)
        Feedback_frame.place(x=10, y=10)
        Label(Feedback_frame, text="Monitoreo", font=("Arial", 11, 'bold'), bg="#DAF7A6").place(x=20, y=15)
        self.estado_grua = Label(Feedback_frame, text="Estado: Inactivo", font=("Arial", 10), bg="#DAF7A6")
        self.estado_grua.place(x=20, y=60)
        self.posicion_actual = Label(Feedback_frame, text="Posición: N/A", font=("Arial", 10), bg="#DAF7A6")
        self.posicion_actual.place(x=20, y=80)
        self.velocidad_actual = Label(Feedback_frame, text="Velocidad: " + str(self.velocidad.get()), font=("Arial", 10), bg="#DAF7A6")
        self.velocidad_actual.place(x=20, y=100)
        self.tiempo_operacion = Label(Feedback_frame, text="Tiempo de operacion: 00:00", font=("Arial", 10), bg="#DAF7A6")
        self.tiempo_operacion.place(x=20, y=120)

        # Actualizar la velocidad actual en tiempo real
        self.velocidad.bind("<Motion>", self.actualizar_velocidad)

        # Sección de Conexión Arduino
        arduino_frame = Frame(self, background="#008184", width=200, height=190)
        arduino_frame.place(x=590, y=10)
        Label(arduino_frame, text="Puerto Arduino", fg="#ffffff", bg="#008184", font=("Open Sans", 11, "bold")).place(x=45, y=10)
        Label(arduino_frame, text="Selecciona tu puerto:", fg="#ffffff", bg="#008184", font=("Open Sans", 10, "bold")).place(x=25, y=60)

        valor = StringVar()
        self.seleccionar_puerto = ttk.Combobox(arduino_frame, width=20, textvariable=valor, state="readonly")
        self.seleccionar_puerto['values'] = self.puertospermitidos
        self.seleccionar_puerto.place(x=25, y=100, width=150)
        self.boton_arduino = Button(arduino_frame, text="Conectar",bg="#0ED611",fg="#ffffff",font=("Open Sans", 10, "bold"),command=lambda: self.connectArduino(self.seleccionar_puerto.get()))
        self.boton_arduino.place(x=65,y=140)

    def actualizar_velocidad(self, event):
        self.velocidad_actual.config(text="Velocidad: " + str(self.velocidad.get()))

    def mover_grua(self, posicion):
        from models.posicionamiento import Posicionamiento
        rendi = Posicionamiento(self)
        rendi.grab_set()
        rendi.wait_window()
        print(self.modoposicionamiento)
        if self.modoposicionamiento == "Manual":
            self.posiboton.place(x=80, y=90)
            Label(self.posiciona_frame, text="Modo Manual Seleccionado",font=("Open Sans", 12, "bold"),bg="#F7DC6F").place(x=60, y=50)
        elif self.modoposicionamiento == "Automatico":
            Label(self.posiciona_frame, text="Modo Automatico Seleccionado",font=("Open Sans", 12, "bold"),bg="#F7DC6F").place(x=40, y=50)
            Label(self.posiciona_frame, text="Objeto de transporte: "+ self.tipotransporte,font=("Open Sans", 12, "bold"),bg="#F7DC6F").place(x=30, y=74)
            self.posiboton.place(x=80, y=110)
        self.estado_grua.config(text="Estado: Moviendo")
        self.posicion_actual.config(text="Posición: " + posicion)
        self.after(1000, lambda: self.estado_grua.config(text="Estado: Inactivo"))

    def emergencia(self):
        self.estado_grua.config(text="Estado: Emergencia activada")

    def iniciar(self):
        if self.arduino == None:
            messagebox.showerror("PytuinoArm","No has conectado el arduino por favor, selecciona su puerto")
        else:
            if self.modoposicionamiento == "Manual":
                manual = KeyApp()
                manual.grab_set()
                manual.wait_window()
            elif self.modoposicionamiento == "Automatico":
                print("asd")

    def connectArduino(self,puerto):
        try:
            self.arduino = serial.Serial(puerto,9600,timeout=2)
            messagebox.showinfo("PytuinoArm","Arduino conectado con exito")
        except:
            messagebox.showerror("PytuinoArm","Error al conectar con arduino, intenta otro puerto")

    def GetPuertos(self, value):
        puertos = [port.device for port in serial.tools.list_ports.comports()]
        self.puertospermitidos = []

        for puerto in puertos:
            try:
                with serial.Serial(puerto, 9600, timeout=2) as ser:
                    self.puertospermitidos.append(puerto)
            except serial.SerialException:
                print("No hay conexión en el puerto:", puerto)

        if value == 1:
            self.seleccionar_puerto['values'] = self.puertospermitidos
            messagebox.showinfo(title="Pytuino", message=f"Se ha actualizado la lista de puertos: {len(self.puertospermitidos)}")

app = menuPrincipal((1, 'Albert', '30506910', 1, 'Administrador'))
app.mainloop()
