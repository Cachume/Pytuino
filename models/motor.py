from tkinter import *
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import time

class VentanaMotor(Toplevel):

    grafica = False
    arduino = False
    def __init__(self):
        super().__init__()
        self.title("Motor temperatura")
        self.geometry("900x500")
        self.resizable(0,0)
        #Frame opciones
        self.info = Frame(self, width=250, height=300, bg="#008184")
        self.info.place(x=600, y=40)
        Label(self.info, text="Informacion del motor", bg="#008184",fg="#ffffff").place(y=5,x=20)
        Label(self.info, text="Temperatura Actual:         °C",bg="#008184",fg="#ffffff", font=("Open Sans",11,"bold")).place(y=45,x=20)
        self.tempm = Label(self.info, text="0",bg="#008184",fg="#ffd948", font=("Open Sans",11,"bold"))
        self.tempm.place(y=45,x=185)
        Label(self.info, text="Estado Actual:     ",bg="#008184",fg="#ffffff", font=("Open Sans",11,"bold")).place(y=70,x=20)
        self.estado = Label(self.info, text="",bg="#008184",fg="#00FF00", font=("Open Sans",11,"bold"))
        self.estado.place(y=70,x=130)
        Label(self.info, text="Velocidad Actual:     ",bg="#008184",fg="#ffffff", font=("Open Sans",11,"bold")).place(y=95,x=20)
        self.velocidad = Label(self.info, text="0",bg="#008184",fg="#00FF00", font=("Open Sans",11,"bold"))
        self.velocidad.place(y=95,x=160)

        self.velocidada = IntVar()

        Label(self.info, text="Selecciona las RPM del motor:",bg="#008184",fg="#ffffff", font=("Open Sans",11,"bold")).place(y=170,x=13)
        self.vela = Radiobutton(self.info, text="0", variable=self.velocidada, state="disable", value=0, bg="#008184",font=("Open Sans",10,"bold"),command = self.setSpeed)
        self.vela.place(y=200, x=30)
        self.velm = Radiobutton(self.info, text="1", variable=self.velocidada, state="disable", value=1, bg="#008184",font=("Open Sans",10,"bold"),command = self.setSpeed)
        self.velm.place(y=200, x=100)
        self.velal = Radiobutton(self.info, text="2", variable=self.velocidada, state="disable", value=2, bg="#008184",font=("Open Sans",10,"bold"),command = self.setSpeed)
        self.velal.place(y=200, x=170)


        # Configurar la figura de Matplotlib
        self.widmat()
        # Crear el botón para agregar valores a la gráfica
        self.add_button = Button(self.info, text="Conectar Motor",bg="#ffd948",border=0,fg="#ffffff",font=("Open Sans",10,"bold"),command=self.iniciarf)
        self.add_button.place(y=250,x=70)
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def iniciarf(self):
        if not self.arduino:
            try:
                self.ser = serial.Serial("COM3", 9600, timeout=1)
                time.sleep(2)
                comando="Motor/0/3"
                self.ser.write(comando.encode())
                self.arduino = True
                for wi in [self.vela,self.velm,self.velal]:
                    wi.config(state="normal")
                self.grafica = not self.grafica
                if self.grafica:
                    self.update_graph()
            except:
                messagebox.showerror("Pytuino", "Error al conectar el arduino")
        else:
            self.grafica = not self.grafica
            self.arduino = False
            self.ser.close()
            for wi in [self.vela,self.velm,self.velal]:
                    wi.config(state="disable")
            if self.grafica:
                self.update_graph()

    def setSpeed(self):
        speed = self.velocidada.get()
        if speed == 1 and self.tempi <89:
            self.MessageforArduino("Motor/1/"+self.led)
            self.velocidad.config(text="1")
        elif speed == 2 and self.tempi <89:
            self.MessageforArduino("Motor/2/"+self.led)
            self.velocidad.config(text="2")
        elif speed == 0:
            self.MessageforArduino("Motor/0/"+self.led)
            self.velocidad.config(text="0")

    def refresh_ui(self, temp):
        velac = self.velocidada.get()
        if temp <=50:
            self.tempm.config(text=str(temp),fg="#00FF00")
            self.estado.config(text="Bueno",fg="#00FF00")
            self.led = "2"
        elif temp >50 and temp <=90:
            self.tempm.config(text=str(temp),fg="#ffd948")
            self.estado.config(text="Medio",fg="#ffd948")
            self.led = "1"
        elif temp >90:
            self.tempm.config(text=str(temp),fg="red")
            self.estado.config(text="Critico",fg="red")
            self.led = "0"
            if(velac == 1 or velac == 2):
                self.velocidada.set(0)
                self.setSpeed()
                messagebox.showinfo("Pytuino Motor","El motor tiene una temperatura alta, se detendra mientras la temperatura desciende")

    def update_graph(self):
        if self.grafica:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("Temperatura:"):
                    value = float(line.split(":")[1].strip().split()[0])
                    self.tempi = value
                    self.refresh_ui(int(value))
                    self.x_data.append(len(self.x_data) + 1)
                    self.y_data.append(value)
                    self.line.set_data(self.x_data, self.y_data)
                    self.ax.set_xlim(0, len(self.x_data) + 1)
                    self.ax.set_ylim(min(self.y_data) - 1, max(self.y_data) + 1)
                    self.canvas.draw()
            except Exception as e:
                print(f"Error reading line: {e}")
            # Programar la siguiente actualización
            self.after(1000, self.update_graph)  # Llamar de nuevo a update_graph después de 2000 ms

    def on_closing(self):
        # Cerrar recursos
        # self.ser.close()
        self.destroy()
        self.quit()  

    def widmat(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Temperatura del Motor")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.line, = self.ax.plot([], [], 'r-', label="Temperatura")
        self.ax.legend()

        self.x_data = [0]
        self.y_data = [0]

        # Crear el canvas de Matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(y=40,x=40)

    def MessageforArduino(self, comando):
        time.sleep(1)
        self.ser.write(comando.encode())

# if __name__ == "__main__":
#     app = SimpleGraphApp()
#     app.mainloop()
