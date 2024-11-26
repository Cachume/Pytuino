from customtkinter import *
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
from serial import Serial
from pynput import keyboard
import time
class manualMode(CTk):

    Motor = 80
    Motor2 = 40
    Pinza = 20
    def __init__(self,arduino):
        super().__init__()
        self.title("Modo Manual | PyduinoArm")
        self.geometry("800x350")
        self.resizable(0,0)
        self.conexArduino = arduino
        self.logoimagen = CTkImage(dark_image=Image.open("img/pytuino_logo.png"),
                                   light_image=Image.open("img/pytuino_logo.png"),size=(240,80))
        CTkLabel(self, image=self.logoimagen,text="").pack(pady=1)

        self.controlimagen = CTkImage(dark_image=Image.open("img/controles.png"),
                                   light_image=Image.open("img/controles.png"),size=(400,250))

        Feedback_frame = CTkFrame(self, fg_color="#DAF7A6", width=220, height=280)
        Feedback_frame.place(x=30, y=40)
        CTkLabel(Feedback_frame, text="Posiciones Motores", font=("Arial", 16, 'bold'),
                  fg_color="transparent",text_color="black").place(x=30, y=15)
        CTkLabel(Feedback_frame, text="Motor1:", font=("Arial", 15, 'bold'), 
                 fg_color="transparent",text_color="black").place(x=30, y=60)
        self.valmotor = CTkLabel(Feedback_frame, text=str(self.Motor)+"°",font=("Arial", 22),
                                 fg_color="transparent",text_color="black")
        self.valmotor.place(x=60, y=80)
        CTkLabel(Feedback_frame, text="Motor2:", font=("Arial", 15, 'bold'), 
                 fg_color="transparent",text_color="black").place(x=30, y=110)
        self.valmotor2 = CTkLabel(Feedback_frame, text=str(self.Motor2)+"°",font=("Arial", 22),
                                 fg_color="transparent",text_color="black")
        self.valmotor2.place(x=60, y=130)

        CTkLabel(self, text="¿Como usar la grua?", font=("Arial", 15, 'bold'),
                  fg_color="transparent",text_color="white").place(x=540, y=50)
        CTkLabel(self, image=self.controlimagen,text="").place(x=415, y=80)


        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'a':
                if self.Motor > 0:
                    self.Motor -= 20  # Movimiento rápido, ajustar valor según necesidad
                print('Derecha')
                instruccion = "Motor1/" + str(self.Motor)
                self.valmotor.configure(text=str(self.Motor)+"°")
                self.conexArduino.write(instruccion.encode())
            elif key.char == 'd':
                if self.Motor != 180:
                    self.Motor += 20  # Movimiento rápido, ajustar valor según necesidad
                print('Izquierda')
                instruccion = "Motor1/" + str(self.Motor)
                self.valmotor.configure(text=str(self.Motor)+"°")
                self.conexArduino.write(instruccion.encode())
            elif key.char == 's':
                if self.Motor2 != 90:
                    self.Motor2 += 10  # Movimiento rápido, ajustar valor según necesidad
                print('Bajar')
                instruccion = "Motor2/" + str(self.Motor2)
                self.valmotor2.configure(text=str(self.Motor2)+"°")
                self.conexArduino.write(instruccion.encode())
            elif key.char == 'w':
                if self.Motor2 != 20:
                    self.Motor2 -= 10  # Movimiento rápido, ajustar valor según necesidad
                print('Subir')
                instruccion = "Motor2/" + str(self.Motor2)
                self.valmotor2.configure(text=str(self.Motor2)+"°")
                self.conexArduino.write(instruccion.encode())
            elif key.char == 'q':
                print('CerrarPinza')
                instruccion = "Cerrarpinza/1"
                self.conexArduino.write(instruccion.encode())
            elif key.char == 'e':
                print('AbrirPinza')
                instruccion = "Abrirpinza/1"
                self.conexArduino.write(instruccion.encode())
        except AttributeError:
            if key == keyboard.Key.esc:
                self.destroy()
                return False

# arduino = Serial("COM4",9600,timeout=2)
# time.sleep(2)
# arduino.write("ModoManual/0".encode())
# print(arduino.readline().decode('utf-8').strip())
# mp = manualMode(arduino)
# mp.mainloop()