from tkinter import *
from tkinter import messagebox
from models.register import VentanaRegistro
from libs.pydb import PytuinoDB
from models.admin.admin import Admin
from models.menup import menuPrincipal
from models.leds import VentanaLeds


class myApp(Tk):

    def __init__(self):
        super().__init__()    
        self.title("Pytuino | Inicio de Sesión")
        self.geometry("450x400")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        icono = PhotoImage(file="img/logos/logoapp.png")
        self.iconphoto(True, icono)
        # Etiqueta de bienvenida
        self.logoimagen = PhotoImage(file="img/pytuino_logo.png")
        self.logoapp= Label(self,image=self.logoimagen,bg="#ffffff").pack(pady=10)
        texto = Label(self, text="Bienvenido al sistema Pytuino",bg="#ffffff",font=("Arial",13,"bold")).pack()

        # Etiqueta y campo de entrada para el usuario
        textus = Label(self, text="Ingresa tu usuario:", bg="#ffffff",font=("Arial",11,"bold")).place(y=170, x=70)
        self.user = Entry(self,bg="#dfdfdf",border=0,width=30,font=("Arial",11))
        self.user.place(y=195, x=70)

        # Etiqueta y campo de entrada para la contraseña
        textp = Label(self, text="Ingresa tu contraseña:", bg="#ffffff",font=("Arial",11,"bold")).place(y=220, x=70)
        self.passwo = Entry(self, show="*",bg="#dfdfdf",border=0,width=30,font=("Arial",11))  
        self.passwo.place(y=245, x=70)

        # Botón de inicio de sesión (por ejemplo)
        boton_ingresar = Button(self, text="Iniciar Sesion",bg="#008184",fg="#ffffff",border=0,font=("Open Sans", 11,"bold") ,command=self.iniciar_sesion)
        boton_ingresar.place(y=300, x=70)
        boton_salir = Button(self, text="Registrarme",bg="#ffd948",fg="#008184",border=0,font=("Open Sans", 11,"bold"), command=self.salir)
        boton_salir.place(y=300, x=210)


    def iniciar_sesion(self):
        users=self.user.get()
        passw=self.passwo.get()
        query = PytuinoDB().loginUser(users,passw)
        if query:
            messagebox.showinfo(title='Verificacion exitosa',message="Has iniciado sesion correctamente.")  
            rol = query[3]
            print(f"Rol del usuario: {rol}")
            print(query)
            self.destroy()
            mp=menuPrincipal(query)
            mp.mainloop()
        else:
            messagebox.showerror(title='Verificacion fallida',message="Usuario o contraseña incorrectos.")
        # ventana_secundaria = VentanaSecundaria(self)
        # ventana_secundaria.grab_set()  
        # ventana_secundaria.wait_window()
        print("Seguimos") 

    def salir(self):
        print("asd")
        self.destroy()
        ventanar = VentanaRegistro()
        ventanar.grab_set()
        ventanar.wait_window()
        self.__init__()

App = myApp()
App.mainloop()