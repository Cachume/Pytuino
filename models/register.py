from tkinter import *
from tkinter import messagebox
from libs.pydb import Pydb
class VentanaRegistro(Tk):
    def __init__(self):
        super().__init__()    
        self.title("Pytuino | Registro")
        self.geometry("450x600")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        # Etiqueta de bienvenida
        self.logoimagen = PhotoImage(file="img/pytuino_logo.png")
        self.logoapp= Label(self,image=self.logoimagen,bg="#ffffff").pack(pady=10)
        texto = Label(self, text="Bienvenido al registro de Pytuino",bg="#ffffff",font=("Arial",13,"bold")).pack()
        # Etiqueta y campo de entrada para los nombres
        textus = Label(self, text="Ingresa tus Nombres:", bg="#ffffff",font=("Arial",11,"bold")).place(y=170, x=70)
        self.names = Entry(self,bg="#dfdfdf",border=0,width=30,font=("Arial",11))
        self.names.place(y=195, x=70)
        # Etiqueta y campo de entrada para el usuario
        textus = Label(self, text="Ingresa tu usuario:", bg="#ffffff",font=("Arial",11,"bold")).place(y=235, x=70)
        self.user = Entry(self,bg="#dfdfdf",border=0,width=30,font=("Arial",11))
        self.user.place(y=260, x=70)
        # Etiqueta y campo de entrada para el usuario
        textus = Label(self, text="Ingresa tu correo electronico:", bg="#ffffff",font=("Arial",11,"bold")).place(y=290, x=70)
        self.email = Entry(self,bg="#dfdfdf",border=0,width=30,font=("Arial",11))
        self.email.place(y=315, x=70)
        # Etiqueta y campo de entrada para el usuario
        textus = Label(self, text="Ingresa tu contraseña:", bg="#ffffff",font=("Arial",11,"bold")).place(y=350, x=70)
        self.passwor = Entry(self,bg="#dfdfdf",show="*",border=0,width=30,font=("Arial",11))
        self.passwor.place(y=375, x=70)

        # Etiqueta y campo de entrada para la contraseña
        textp = Label(self, text="Confirma tu contraseña:", bg="#ffffff",font=("Arial",11,"bold")).place(y=410, x=70)
        self.passwod = Entry(self, show="*",bg="#dfdfdf",border=0,width=30,font=("Arial",11))  
        self.passwod.place(y=440, x=70)

        # Botón de inicio de sesión (por ejemplo)
        boton_ingresar = Button(self, text="Regresar",bg="#008184",fg="#ffffff",border=0,font=("Open Sans", 11,"bold"),command=self.regresar)
        boton_ingresar.place(y=480, x=70)
        boton_salir = Button(self, text="Registrarme",bg="#ffd948",fg="#008184",border=0,font=("Open Sans", 11,"bold"), command=self.registarme)
        boton_salir.place(y=480, x=210)
    
    def registarme(self):
        usuario = self.user.get()
        nombres = self.names.get()
        correo = self.email.get()
        contrasena = self.passwor.get()
        confirmacion_contrasena = self.passwod.get()
        conedb = Pydb()
        if nombres == '' or usuario == '' or correo == '' or contrasena == '' or confirmacion_contrasena == '':
            messagebox.showerror("Error", "Todos los campos son obligatorios. Por favor, completa todos los campos.")
        else:
            messagebox.showinfo("Éxito", "Todos los campos están completos. Puedes proceder.")
            if not conedb.vefuser(usuario) and not conedb.vefmail(correo):
                messagebox.showerror("Pytuino","El correo electronico y el usuario ingresado ya esta en uso")
            elif not conedb.vefuser(usuario):
                messagebox.showerror("Pytuino","El usuario ingresado ya esta en uso")
                return
            elif not conedb.vefmail(correo):
                messagebox.showerror("Pytuino","El correo electronico ingresado ya esta en uso")
                return
            else:
                if conedb.insertUser(usuario,contrasena,nombres,correo):
                    messagebox.showinfo("Pytuino","Te has registrado exitosamente")
                else:
                    messagebox.showerror("Pytuino","Ha ocurrido un error en registrarte, intenta mas tarde")
    
    def regresar(self):
        self.destroy()