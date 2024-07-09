from tkinter import *
from tkinter import messagebox, Menu, ttk, Canvas
from os import path
import datetime
from models.leds import VentanaLeds
from models.motor import VentanaMotor
import serial
import serial.tools.list_ports
from libs.pydb import PytuinoDB
from models.admin.adminLogin import loginadmin
from models.admin.admin import Admin


class menuPrincipal(Tk):

    puertoarduino = ""
    datosuser = ""
    
    def __init__(self, usuario):
        super().__init__()
        self.datosuser = usuario
        self.GetPuertos(0)
        self.title("Menu Principal | Pyduino")
        self.geometry("700x400")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        icono = PhotoImage(file="img/logos/logoapp.png")
        self.iconphoto(True, icono)

        #Declaracion del menu
        self.barraMenu= Menu(self)
        self.config(menu=self.barraMenu)
        #Agregando opciones al menu
        self.ledimg = PhotoImage(file="img/ledmenu.png")
        self.ledmotor = PhotoImage(file="img/motormenu.png")
        self.opcionesMenu = Menu(self.barraMenu, tearoff=False)
        self.opcionesMenu.add_command(label="Manejo Leds",image=self.ledimg,compound=LEFT, command=self.leds)
        self.opcionesMenu.add_command(label="Manejo Motor",image=self.ledmotor,compound=LEFT, command=self.motor)
        self.barraMenu.add_cascade(label="Opciones", menu=self.opcionesMenu)
        self.barraMenu.add_command(label="Reiniciar", command=self.reiniciara)
        
        #Widgets Principales
        self.logoimagen = PhotoImage(file="img/pytuino_logo.png")
        self.logoapp= Label(self,image=self.logoimagen,bg="#ffffff").pack(pady=1)
        # etiqueta_secundaria = Label(self, text="¡Bienvenido al modulo principal", bg="#ffffff", font=("Open Sans",11,"bold"))
        # etiqueta_secundaria.pack(pady=20)
        self.boton_admin = Button(self, text="Activar modo admin",bg="#008184", fg="#ffffff", font=("Arial",13,'bold'),command=self.modeAdmin)
        self.boton_admin.place(x=40,y=300)

        #Widgets Frame Arduino
        self.arduino_Frame = Frame(self, background="#008184", width=190, height=190)
        self.logoinformacion = PhotoImage(file="img/informacion.png")
        self.logoactualizar = PhotoImage(file="img/actualizar.png")
        self.arduino_Frame.place(y=100, x=500)
        self.arduino_titulo = Label(self.arduino_Frame, text="Puerto Arduino",fg="#ffffff" ,bg="#008184",font=("Open Sans", 11, "bold"))
        self.arduino_titulo.place(x=35,y=5)
        Label(self.arduino_Frame,text="Selecciona tu puerto:",fg="#ffffff" ,bg="#008184",font=("Open Sans", 10, "bold")).place(x=20, y=60)
        valor=StringVar()
        self.seleccionar_puerto = ttk.Combobox(self.arduino_Frame, width=20, textvariable=valor, state="readonly")
        self.seleccionar_puerto['values'] = self.puertospermitidos
        self.seleccionar_puerto.place(x=25, y=100)
        # botonasignar = Button(self.arduino_Frame, text="Asignar Puerto",bg="#ffd948",fg="#008184",border=0,font=("Open Sans", 10,"bold"))
        # botonasignar.place(y=145, x=30)
        informacion = Button(self.arduino_Frame,image=self.logoinformacion,bg="#008184", border=0, command=self.ayudaarduino).place(y=155,x=155)
        Button(self.arduino_Frame,image=self.logoactualizar,bg="#008184", border=0, command=lambda: self.GetPuertos(1)).place(y=155,x=110)
        #Widgets Frame Usuario
        self.userFrame = Frame(self,bg="#ffffff" ,width=220, height=200)
        self.userFrame.place(y=100,x=10)
        Label(self.userFrame, text="Te has conectado como:", font=("Arial",11,'bold')).place(x=10,y=23)
        Label(self.userFrame, text="Usuario: " + self.datosuser[1], font=("Arial",10,'bold')).place(x=10,y=60)
        Label(self.userFrame, text="Tipo de acceso: "+str(self.datosuser[3]), font=("Arial",10,'bold')).place(x=10,y=90)
        Label(self.userFrame, text="Ultima Conexión: "+self.datosuser[4], font=("Arial",10,'bold')).place(x=10,y=125)
        
        ruta_archivo = "cache/logs/" + self.datosuser[1] + ".txt"
        if path.exists(ruta_archivo):
            archivouser = open(ruta_archivo, 'a+')
            print("El archivo existe")
            archivouser.write("\n\n")
            archivouser.write("\n["+self.obtenerfecha()+"] El usuario ha iniciado sesion")
            archivouser.close()
        else:
            archivouser = open(ruta_archivo, 'w')
            print("El archivo no existe, se va a crear")
            archivouser.write("===========================")
            archivouser.write("\n    Archivo log: Albert    ")
            archivouser.write("\n   Fecha: "+self.obtenerfecha()+"")
            archivouser.write("\n===========================")
            archivouser.write("\n")
    
    def ayudaarduino(self):
        messagebox.showinfo(title="Pytuino Ayuda Arduino",message="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        
    def leds(self):
         archivo = open("cache/logs/" + self.datosuser[1] + ".txt", "a+")
         archivo.write('\n['+self.obtenerfecha()+'] El usuario ha ingresado a manejo leds')
         led=VentanaLeds()
         led.grab_set()
         led.wait_window()
         print("ledowo")
         archivo.write('\n['+self.obtenerfecha()+'] El usuario ha salido de manejo leds')
         archivo.close()
 
    def motor(self):
        motor=VentanaMotor()
        motor.grab_set()
        motor.wait_window()
        motor.destroy()
    
    def obtenerfecha(self):
        fecha = datetime.datetime.now()
        actual = str(fecha.year)+"/"+str(fecha.month)+'/'+str(fecha.day)+' '+str(fecha.hour)+':'+str(fecha.second)
        return actual
    
    def reiniciara(self):
        self.destroy()
        self.__init__(self.datosuser)
    
    def GetPuertos(self, value):
        # Obtener una lista de todos los puertos disponibles
        puertos = [port.device for port in serial.tools.list_ports.comports()]
        self.puertospermitidos = []

        for puerto in puertos:
            try:
                # Intentar abrir el puerto serie
                with serial.Serial(puerto, 9600, timeout=2) as ser:
                    self.puertospermitidos.append(puerto)
            except serial.SerialException:
                print("No hay conexión en el puerto:", puerto)

        if value == 1:
            self.seleccionar_puerto['values'] = self.puertospermitidos
            messagebox.showinfo(
                title="Pytuino",
                message=f"Se ha actualizado la lista de puertos, se han encontrado: {len(self.puertospermitidos)}"
            )
    def modeAdmin(self):
        self.adminpass = None
        admin = loginadmin(self)
        admin.wait_window()
        db = PytuinoDB()
        if db.comprobarPass(self.datosuser[1],self.adminpass):
            self.opcionesAdmin = Menu(self.barraMenu, tearoff=False)
            self.opcionesAdmin.add_command(label="Administracion de modulos",image=self.ledimg,compound=LEFT,command=self.adminleds)
            # self.opcionesAdmin.add_command(label="Cambiar Contraseña",image=self.ledmotor,compound=LEFT)
            # self.opcionesAdmin.add_command(label="Salir del modo Administrador",image=self.ledmotor,compound=LEFT)
            self.barraMenu.add_cascade(label="Administrador", menu=self.opcionesAdmin)
        else:
            messagebox.showerror("PytuinoError","La contraseña es incorrecta :)")
    def adminleds(self):
        al = Admin()
        al.grab_set()
        al.wait_window()
# app = menuPrincipal((1, 'Albert', '30506910', 1, 'Administrador'))
# app.mainloop()