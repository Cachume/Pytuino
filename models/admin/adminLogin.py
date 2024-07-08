from tkinter import *
from tkinter import messagebox, Menu, ttk, Canvas

class loginadmin(Toplevel):

    intentos = 3
    
    def __init__(self,parent):
        super().__init__()
        self.title("Pytuino")
        self.geometry("400x400")
        self.resizable(0,0)
        self.config(bg="#ffffff")
        self.ventanap = parent
        #Widgets Principales
        self.logoimagen = PhotoImage(file="img/pytuino_logo_admin.png")
        self.logoapp= Label(self,image=self.logoimagen,bg="#ffffff").pack(pady=1)
        etiqueta_secundaria = Label(self, text="Ingresa la contraseña de administración", bg="#ffffff", font=("Open Sans",11,"bold"))
        etiqueta_secundaria.pack(pady=20)
        self.passwordEntry = Entry(self, show="*", font=12)
        self.passwordEntry.pack(pady=10)
        Button(self, text="Confirmar", bg="#008184",fg="#ffffff",border=0,font=("Open Sans", 11,"bold"),command=self.enviarcomando).pack(pady=30)
        self.intentosLabel = Label(self, text="Intentos restantes :"+str(self.intentos), bg="#ffffff", font=("Open Sans",12,"bold"))
        self.intentosLabel.pack(pady=30)

    def enviarcomando(self):
        self.ventanap.adminpass = self.passwordEntry.get()
        self.destroy()