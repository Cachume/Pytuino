from tkinter import *
from tkinter import messagebox , ttk
from PIL import Image, ImageTk, ImageSequence
import datetime
import serial
import time
from config.Ic import *
from libs.pydb import Pydb

class VentanaLeds(Tk):
    estadoarduino= False
    estado = False
    should_continue = True
    def __init__(self):
        super().__init__()
        self.title("Pytuino")
        self.geometry("500x450")
        self.resizable(0,0)
        self.config(bg=IColor_bg)
        self.mostrarLeds()
        self.puertoarduino = "COM3"
        self.imagenp=PhotoImage(file="img/et/0000.png")
        Label(self, text="Pytuino | Manejo de Leds",font=("Open Sans",11,"bold"),bg=IColor_bg).pack(pady=20)
        self.ledimage = Label(self, image=self.imagenp,bg=IColor_bg)
        self.ledimage.pack(pady=14)
        Label(self, text="Selecciona la funcion del led:",font=("Open Sans",11,"bold"),bg=IColor_bg,fg=IColor_bt).place(y=180, x=31)
        valor = StringVar()
        self.Funciones = ttk.Combobox(self, width=30, state="readonly" ,textvariable=valor)
        self.Funciones['values']= self.funcionesc
        self.Funciones.place(y=210, x=40)

        self.arduino = Frame(self,bg=IColor_bt,width=200,height=200)
        self.arduino.place(y=180,x=280)
        Label(self.arduino, text="Conexión Arduino:", bg=IColor_bt, fg=IColor_bg,font=("Open Sans",11,"bold")).place(y=5, x=30)
        Label(self.arduino, text="Estado: ",bg=IColor_bt, fg=IColor_bg, font=("Open Sans",11,"bold")).place(y=60,x=10)
        Label(self.arduino, text="Puerto: "+self.puertoarduino,bg=IColor_bt, fg=IColor_bg, font=("Open Sans",11,"bold")).place(y=90,x=10)
        self.ea=Label(self.arduino, text="Desconectado", fg="red",bg=IColor_bt ,font=("Open Sans", 11,"bold"))
        self.ea.place(y=60,x=70)
        self.botona=Button(self.arduino, text="Conectar", bg="green",fg="#ffffff",border=0,font=("Open Sans",10,"bold"),command=self.arduinoconex)
        self.botona.place(y=140, x=40)
         

        self.accionb = Button(self, text="Comenzar", fg="green", command=self.startleds)
        self.accionb.place(x=110, y=260)
    
    def arduinoconex(self):
        if self.estadoarduino:
            self.botona.config(text="Conectar", bg="green")
            self.ea.config(text="Desconectado", fg="red")
            self.estadoarduino = False
        else:
            self.botona.config(text="Desconectar", bg="red")
            self.ea.config(text="Conectado", fg="green")
            self.estadoarduino = True

    def startleds(self):
        if not self.estado:
            funcion = self.Funciones.get().split("/")
            if funcion[0] == "Encender Todos":
                self.imagen=PhotoImage(file="img/et/"+funcion[1]+".png")
                self.ledimage.config(image=self.imagen)
            elif funcion[0] == "Parpadeo":
                gif = Image.open("img/p/"+funcion[1]+".gif")
                frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
                current_frame = 0
                self.should_continue = True
                self.update_animation(self.ledimage, frames, current_frame)
            self.estado = True
            self.botona['state']='disable'
            self.Funciones['state']='disable'
            self.accionb.config(text="Detener",fg='red')
        else:
            self.imagen=PhotoImage(file="img/et/0000.png")
            self.ledimage.config(image=self.imagen)
            self.should_continue = False
            self.estado = False
            self.botona['state']='normal'
            self.Funciones['state']='normal'
            self.accionb.config(text="Comenzar",fg='green')

    def mostrarLeds(self):
        db = Pydb()
        db.obtenerLeds()
        acciones = {
        "pd": "Parpadeo",
        "et": "Encender Todos"
        }
        self.funcionesc = []
        for datos in db.obtenerLeds():
            datos = datos.split("/")
            self.funcionesc.append(acciones[datos[0]]+"/"+datos[1])

    def update_animation(self, label, frames, current_frame):
        if self.should_continue:  # Solo actualiza si should_continue es True
            image = ImageTk.PhotoImage(frames[current_frame])
            label.config(image=image)
            label.image = image
            current_frame = (current_frame + 1) % len(frames)
            label.after(1000, self.update_animation, label, frames, current_frame)
    
    def obtenerfecha(self):
        fecha = datetime.datetime.now()
        actual = str(fecha.year)+"/"+str(fecha.month)+'/'+str(fecha.day)+' '+str(fecha.hour)+':'+str(fecha.second)
        return actual
        