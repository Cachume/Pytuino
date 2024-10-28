import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import PhotoImage, messagebox
from models.register import VentanaRegistro
from libs.pydb import PytuinoDB
from models.menup import menuPrincipal

class myApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pytuino | Inicio de Sesión")
        self.geometry("450x400")
        self.resizable(0, 0)

        # Cargar la imagen usando PIL y luego convertirla a PhotoImage
        icono_img = Image.open("img/logos/logoapp.png")
        icono = ImageTk.PhotoImage(icono_img)
        self.iconphoto(True, icono)

        # Etiqueta de bienvenida
        logo_img = Image.open("img/pytuino_logo.png")
        self.logoimagen = ImageTk.PhotoImage(logo_img)
        self.logoapp = ctk.CTkLabel(self, image=self.logoimagen)
        self.logoapp.pack(pady=10)

        texto = ctk.CTkLabel(self, text="Bienvenido al sistema Pytuino", font=("Arial", 13, "bold"))
        texto.pack()

        # Etiqueta y campo de entrada para el usuario
        textus = ctk.CTkLabel(self, text="Ingresa tu usuario:", font=("Arial", 11, "bold"))
        textus.place(y=170, x=70)

        self.user = ctk.CTkEntry(self, width=200)
        self.user.place(y=195, x=70)

        # Etiqueta y campo de entrada para la contraseña
        textp = ctk.CTkLabel(self, text="Ingresa tu contraseña:", font=("Arial", 11, "bold"))
        textp.place(y=220, x=70)

        self.passwo = ctk.CTkEntry(self, show="*", width=200)
        self.passwo.place(y=245, x=70)

        # Botón de inicio de sesión
        boton_ingresar = ctk.CTkButton(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        boton_ingresar.place(y=300, x=70)

        boton_registrarme = ctk.CTkButton(self, text="Registrarme", command=self.salir)
        boton_registrarme.place(y=300, x=210)

    def iniciar_sesion(self):
        users = self.user.get()
        passw = self.passwo.get()
        query = PytuinoDB().loginUser(users, passw)
        if query:
            messagebox.showinfo(title='Verificación exitosa', message="Has iniciado sesión correctamente.")
            rol = query[3]
            print(f"Rol del usuario: {rol}")
            print(query)
            self.destroy()
            mp = menuPrincipal(query)
            mp.mainloop()
        else:
            messagebox.showerror(title='Verificación fallida', message="Usuario o contraseña incorrectos.")

    def salir(self):
        self.destroy()
        ventanar = VentanaRegistro()
        ventanar.grab_set()
        ventanar.wait_window()
        self.__init__()

App = myApp()
App.mainloop()
