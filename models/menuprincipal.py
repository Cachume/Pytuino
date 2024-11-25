from customtkinter import *
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
from serial import Serial
import serial.tools.list_ports
import time

class MenuPrincipal(CTk):

    datosposicionamiento = None
    def __init__(self):
        super().__init__()
        self.title("Menu Principal | Pyduino")
        self.geometry("800x500")
        self.resizable(0,0)
        self.GetPuertos()
        self.boton = CTkButton(self, text="Iniciar Trabajo", fg_color="#0ED611", font=("Arial", 12, 'bold'),command=lambda: self.initWork())
        self.boton.place(x=640, y=450)

        self.logoimagen = CTkImage(dark_image=Image.open("img/pytuino_logo.png"),
                                   light_image=Image.open("img/pytuino_logo.png"),size=(240,80))
        CTkLabel(self, image=self.logoimagen,text="").pack(pady=1)

        #Frame de Informacion
        Feedback_frame = CTkFrame(self, fg_color="#DAF7A6", width=220, height=190)
        Feedback_frame.place(x=10, y=10)
        CTkLabel(Feedback_frame, text="Monitoreo", font=("Arial", 13, 'bold'), fg_color="transparent",text_color="black").place(x=20, y=15)
        CTkLabel(Feedback_frame, text="Estado:", font=("Arial", 14), fg_color="transparent",text_color="black").place(x=20, y=60)
        CTkLabel(Feedback_frame, text="Posición:", font=("Arial", 14), fg_color="transparent",text_color="black").place(x=20, y=80)
        CTkLabel(Feedback_frame, text="Tiempo de operacion:", font=("Arial", 14), fg_color="transparent",text_color="black").place(x=20, y=100)
        #Valores Interfaces
        self.val_estado = CTkLabel(Feedback_frame, text="Detenido", font=("Arial", 14,'bold'), fg_color="transparent",text_color="red")
        self.val_estado.place(x=70, y=60)
        self.val_posicion = CTkLabel(Feedback_frame, text="Descanso", font=("Arial", 14,'bold'), fg_color="transparent",text_color="yellow")
        self.val_posicion.place(x=80, y=80)

        #Frame de Conexion arduino
        arduino_frame = CTkFrame(self, fg_color="#008184", width=200, height=190)
        arduino_frame.place(x=590, y=10)
        CTkLabel(arduino_frame, text="Puerto Arduino", text_color="#ffffff", fg_color="#008184", font=("Open Sans", 12, "bold")).place(x=60, y=10)
        if self.arduinoconex[0]:
            imgconex = CTkImage(dark_image=Image.open("img/conex.png"),
                                   light_image=Image.open("img/conex.png"),size=(95,90))
            CTkLabel(arduino_frame, image=imgconex,text="").place(x=55, y=50)
            CTkLabel(arduino_frame, text="Conexion Exitosa", text_color="#ffffff", fg_color="#008184",
                      font=("Open Sans", 14, "bold")).place(x=40, y=150)
            
        #Frame de Material de transporte
        material_frame = CTkFrame(self, fg_color="#DAF7A6", width=220, height=200)
        material_frame.place(x=10, y=210)
        CTkLabel(material_frame, text="Material de transporte.", font=("Arial", 14, 'bold'),
                  fg_color="#DAF7A6",text_color="black").place(x=25, y=20)
        self.imgconex = CTkImage(dark_image=Image.open("img/sinseleccionar.png"),
                                   light_image=Image.open("img/sinseleccionar.png"),size=(95,90))
        self.mateimage = CTkLabel(material_frame, image=self.imgconex,text="")
        self.mateimage.place(x=60, y=60)
        self.matetext = CTkLabel(material_frame, text="Sin seleccionar.", font=("Arial", 14, 'bold'),
                  fg_color="#DAF7A6",text_color="black")
        self.matetext.place(x=50, y=150)
        
        #Modos de trabajo
        posiciona_frame = CTkFrame(self,fg_color="#F7DC6F", width=340, height=200)
        posiciona_frame.place(x=240, y=120)
        CTkLabel(posiciona_frame, text="Posicionamiento", font=("Arial", 16, 'bold'),
                  fg_color="#F7DC6F",text_color="black").place(x=100, y=20)
        CTkLabel(posiciona_frame, text="Tipo de Manejo:", font=("Arial", 15),
                 fg_color="transparent",text_color="black").place(x=30, y=60)
        CTkLabel(posiciona_frame, text="Material Seleccionado:", font=("Arial", 15),
                 fg_color="transparent",text_color="black").place(x=30, y=80)
        
        self.tdm = CTkLabel(posiciona_frame, text="N/A", font=("Arial", 15,'bold'),
                 fg_color="transparent",text_color="black")
        self.tdm.place(x=135, y=60)
        self.mase = CTkLabel(posiciona_frame, text="N/A", font=("Arial", 15,'bold'),
                 fg_color="transparent",text_color="black")
        self.mase.place(x=178, y=80)
        CTkButton(posiciona_frame, text="Gestionar Posicionamiento",
                  font=("Arial", 15,'bold'),fg_color="#008184",command=lambda: self.posicionamiento()).place(x=120, y=155)

    def posicionamiento(self):
        from posicionamiento import Posicionamiento
        rendi = Posicionamiento(self)
        rendi.grab_set()
        rendi.wait_window()
        print(self.datosposicionamiento)
        self.tdm.configure(text=self.datosposicionamiento[0])
        self.mase.configure(text=self.datosposicionamiento[1])
        if self.datosposicionamiento[0]=="Automatico":
            self.matetext.configure(text=self.datosposicionamiento[1])
            self.matetext.place(x=60, y=150)
            imgmat = CTkImage(dark_image=Image.open("img/caja.png"),
                                   light_image=Image.open("img/caja.png"),size=(95,90))
            self.mateimage.configure(image=imgmat)
        elif self.datosposicionamiento[0]=="Manual":
            self.matetext.configure(text="Sin seleccionar")
            self.matetext.place(x=50, y=150)
            self.mateimage.configure(image=self.imgconex)

    def GetPuertos(self):
        puertos = [port.device for port in serial.tools.list_ports.comports()]
        self.puertospermitidos = []
        for puerto in puertos:
            try:
                ser = serial.Serial(puerto, 9600, timeout=2)
                print(puerto)
                instruccion = "ConexionPython/0"
                time.sleep(2)
                ser.write(instruccion.encode())
                response = ser.readline().decode('utf-8').strip()
                print(response)
                if response == "PytuinoArmConexion":
                    messagebox.showinfo("PytuinoArm", "Conexión creada con éxito")
                    self.arduinoconex = [True, ser]  # Almacena el objeto serial
                    print(self.arduinoconex)
                    break  # Sal del bucle una vez que se encuentra la conexión
                else:
                    ser.close()
            except serial.SerialException:
                print("No hay conexión en el puerto:", puerto)

    def initWork(self):
        if self.datosposicionamiento is None:
            messagebox.showerror("PytuinoArm | Error de Conexión","No se puede iniciar el trabajo sin seleccionar un modo de trabajo")
            return
        
        if self.arduinoconex[0] is True:
            print("Estamos conectados")
            if self.datosposicionamiento[0]=="Automatico":
                print("Modo automatico")
            elif self.datosposicionamiento[0]=="Manual":
                from manualMode import manualMode
                self.arduinoconex[1].write("ModoManual/0".encode())
                print(self.arduinoconex[1].readline().decode('utf-8').strip())
                modomanual= manualMode(self.arduinoconex[1])
                modomanual.grab_set()
        else:
            messagebox.showerror("PytuinoArm | Error de Conexión","No se puede iniciar el trabajo sin tener la conexión con el Arduino")        
mp = MenuPrincipal()
mp.mainloop()