from tkinter import *
from tkinter import messagebox

class Posicionamiento(Toplevel):
    
    def __init__(self, parent):
        super().__init__()
        self.principal = parent
        self.title("Posicionamiento | Pyduino")
        self.geometry("560x300")
        self.resizable(0, 0)
        self.config(bg="#ffffff")

        # Frame inicial para seleccionar el modo
        self.frame_seleccion_modo = Frame(self, bg="#ffffff")
        self.frame_seleccion_modo.pack(fill=BOTH, expand=True)

        # Imágenes
        self.img_manual = PhotoImage(file="img/manual.png")
        self.img_automatico = PhotoImage(file="img/auto.png")
        self.img_caja = PhotoImage(file="img/caja2.png")

        # Interfaz de selección de modo
        label = Label(self.frame_seleccion_modo, text="Selecciona el Modo de Posicionamiento", 
                      font=("Open Sans", 13, "bold"), bg="#ffffff")
        label.pack(padx=20, pady=20)

        # Botón Manual
        boton_manual = Button(self.frame_seleccion_modo, text="Manual", cursor="hand2", borderwidth=1, relief="solid",
                              font=("Open Sans", 12, "bold"), image=self.img_manual, compound=TOP,
                              command=lambda: self.seleccionar_modo("Manual"), width=150)
        boton_manual.pack(side=LEFT, padx=45, pady=3)

        # Botón Automático
        boton_automatico = Button(self.frame_seleccion_modo, text="Automático", cursor="hand2", borderwidth=1, relief="solid",
                                  font=("Open Sans", 12, "bold"), image=self.img_automatico, compound=TOP,
                                  command=lambda: self.seleccionar_modo("Automatico"), width=150)
        boton_automatico.pack(side=RIGHT, padx=45, pady=3)

        # Frame para mostrar objetos en modo Automático
        self.frame_objetos = Frame(self, bg="#f0f0f0")

        # Título en el frame de objetos
        label_objetos = Label(self.frame_objetos, text="Objetos disponibles para transporte", 
                              font=("Open Sans", 12, "bold"), bg="#f0f0f0")
        label_objetos.pack(pady=10)
        posx =40
        posy=50
        i = 0
        # Lista de objetos
        objetos = ["Caja Pequeña", "Caja Mediana", "Caja Grande"]
        for objeto in objetos:
            if i==3:
                posy=150
                posx=40
            lbl_objeto = Button(self.frame_objetos, text=objeto, font=("Open Sans", 10),compound=TOP ,bg="#ffffff", width=120, image=self.img_caja,
                                cursor="hand2", borderwidth=1, relief="solid", command=lambda objeto=objeto: self.seleccionar_material(objeto))
            lbl_objeto.place(y=posy,x=posx)
            posx += 180
            i+=1

        # Botón para volver al menú de selección de modo
        boton_volver = Button(self.frame_objetos, text="Volver", command=self.mostrar_seleccion_modo, 
                              font=("Open Sans", 10, "bold"), bg="#B9770E", fg="#ffffff")
        boton_volver.place(x=260,y=260)

    def seleccionar_modo(self, modo):
        messagebox.showinfo("Modo Seleccionado", f"Modo {modo} seleccionado")
        self.principal.modoposicionamiento = modo

        if modo == "Automatico":
            self.mostrar_objetos()

    def seleccionar_material(self, material):
        self.principal.tipotransporte = material
        print(material)
        self.destroy()

    def mostrar_objetos(self):
        # Oculta el frame de selección de modo y muestra el de objetos
        self.frame_seleccion_modo.pack_forget()
        self.frame_objetos.pack(fill=BOTH, expand=True)

    def mostrar_seleccion_modo(self):
        # Oculta el frame de objetos y muestra el de selección de modo
        self.frame_objetos.pack_forget()
        self.frame_seleccion_modo.pack(fill=BOTH, expand=True)
