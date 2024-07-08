from tkinter import *
from tkinter import messagebox, Menu, ttk
from libs.pydb import Pydb
from PIL import Image, ImageTk, ImageSequence

class Admin(Tk):

    def __init__(self):
        super().__init__()   
        self.title("Pytuino | Administrador") 
        self.geometry("700x400")
        barraMenu= Menu(self)
        self.resizable(0,0)
        self.config(menu=barraMenu)
        opcionesMenu = Menu(barraMenu)
        opcionesMenu.add_command(label="Usuarios")
        opcionesMenu.add_command(label="Modulos")
        barraMenu.add_cascade(label="Gestionar", menu=opcionesMenu)

        self.tablasControl = ttk.Notebook(self)
        frameBienvenida = Frame(self.tablasControl, bg="#ffffff")
        frameLed = Frame(self.tablasControl, bg="#ffffff")
        frameMotor = Frame(self.tablasControl, bg="#ffffff")    
        self.tablasControl.add(frameLed, text="Leds")
        self.tablasControl.add(frameMotor, text="Motor")
        self.tablasControl.add(frameBienvenida, text="Bienvenida")
        self.tablasControl.pack(expand=1, fill="both")

        #Widgets Leds
        Label(frameLed, text="Manejo de Leds | Pyduino", font=("Open Sans",11,"bold"),bg="#ffffff").pack(pady=10)
        Label(frameLed, text="Selecciona los leds",bg="#ffffff",font=("Open Sans",11,"bold")).place(x=20,y=60)
        opciones = ["1", "2", "3", "4"]
        ron=20
        self.led_vars = []
        self.leds = []
        for opcion in opciones:
            var = IntVar()
            led = Checkbutton(frameLed, text=opcion, onvalue=1, offvalue=0, variable=var, bg="#ffffff", font=("Open Sans", 8))
            led.place(y=90, x=ron)
            self.leds.append(led)
            self.led_vars.append(var)  # Agrega la variable a la lista
            ron += 70
        Label(frameLed, text="Selecciona la funcion del led:",bg="#ffffff",font=("Open Sans",11,"bold")).place(y=150, x=20)
        valor = StringVar()
        self.seleccionar_funcion = ttk.Combobox(frameLed, width=20, state="readonly" ,textvariable=valor)
        self.seleccionar_funcion['values'] = ('Encender Todos','Izquierda-Derecha', 'Derecha-Izquierda', 'Parpadeo')
        self.seleccionar_funcion.place(y=180, x=30)
        boton_previ = Button(frameLed, text="Previsualizar",bg="#008184",fg="#ffffff",border=0,font=("Open Sans", 10,"bold"),command=self.viewLed)
        boton_previ.place(y=220, x=30)
        boton_add = Button(frameLed, text="Añadir Función",bg="#ffd948",fg="#008184",border=0,font=("Open Sans", 10,"bold"),command=self.addLed)
        boton_add.place(y=220, x=135)
        Label(frameLed, text="Previsualizar Leds",bg="#ffffff",font=("Open Sans",11,"bold")).place(y=120, x=350)
        self.imagenp=PhotoImage(file="img/et/0000.png")
        self.ledimg=Label(frameLed,image=self.imagenp,bg="#ffffff")
        self.ledimg.place(y=150,x=350)

    def addLed(self):
        seleccion = self.seleccionar_funcion.get()
        valores = "".join([str(var.get()) for var in self.led_vars])
        print("Valores de los Checkbutton:", valores)
        funcion = None
        print("Visualizar Leds")
        if seleccion == 'Encender Todos':
            funcion='et'
        elif seleccion == 'Izquierda-Derecha':
            funcion='id'
        elif seleccion == 'Derecha-Izquierda':
            funcion='di'
        elif seleccion == 'Parpadeo':
            funcion='pd'
        else:
            messagebox.showerror("Error", "Selección no válida.")
            return False
        combinacion=funcion+"/"+valores
        dbp=Pydb()
        if dbp.insertLeds(combinacion):
            messagebox.showinfo("Pytuino | Administrador","Se ha añadido exitosamente la nueva instruccion")
        else:
            messagebox.showinfo("Pytuino | Administrador","La instrucción ingresada ya se encuentra en el sistema")

    def viewLed(self):
        seleccion = self.seleccionar_funcion.get()
        valores = "".join([str(var.get()) for var in self.led_vars])
        funcion = None
        print("Visualizar Leds")
        if seleccion == 'Encender Todos':
            funcion='et'
        elif seleccion == 'Izquierda-Derecha':
            funcion='id'
        elif seleccion == 'Derecha-Izquierda':
            funcion='di'
        elif seleccion == 'Parpadeo':
            funcion='pd'
        else:
            messagebox.showerror("Error", "Selección no válida.")
            return False
        self.should_continue = False
        if(funcion == 'pd' or funcion == 'di' or funcion == 'id'):
            imagen="img/"+funcion+"/"+valores+".gif"
            gif = Image.open(imagen)
            frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
            current_frame = 0
            self.should_continue = True
            self.update_animation(self.ledimg, frames, current_frame)
        else:
            self.should_continue = False
            imagen="img/et/"+valores+".png"
            self.imagen = PhotoImage(file=imagen)
            self.ledimg.config(image=self.imagen)
    
    def update_animation(self, label, frames, current_frame):
        if self.should_continue:  # Solo actualiza si should_continue es True
            image = ImageTk.PhotoImage(frames[current_frame])
            label.config(image=image)
            label.image = image
            current_frame = (current_frame + 1) % len(frames)
            label.after(1000, self.update_animation, label, frames, current_frame)
    

# app = Admin()
# app.mainloop()