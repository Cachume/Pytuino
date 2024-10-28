from tkinter import *
from pynput import keyboard
from serial import Serial

class KeyApp(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Posicionamiento Manual | Pyduino")
        self.Motor1 = 90
        self.Motor2 = 0

        try:
            self.arduino = Serial("COM3", 9600, timeout=2)
        except:
            print("No se ha conectado a Arduino")

        self.label = Label(self, text="Presiona 'w', 's', 'a' o 'd' para ejecutar una acción")
        self.label.pack(padx=20, pady=20)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'w':
                if self.Motor2 > 0:
                    self.Motor2 -= 10
                print('Subir')
                instruccion = "Motor2/" + str(self.Motor2)
                self.label.config(text="Subir")
                self.arduino.write(instruccion.encode())
                print(self.Motor2)
            elif key.char == 's':
                if self.Motor2 < 60:
                    self.Motor2 += 10
                print('Bajar')
                instruccion = "Motor2/" + str(self.Motor2)
                self.label.config(text="Bajar")
                self.arduino.write(instruccion.encode())
                print(self.Motor2)
            elif key.char == 'a':
                if self.Motor1 < 180:
                    self.Motor1 += 10
                print('Izquierda')
                instruccion = "Motor1/" + str(self.Motor1)
                self.label.config(text="Izquierda")
                self.arduino.write(instruccion.encode())
                print(self.Motor1)
            elif key.char == 'd':
                if self.Motor1 > 10:
                    self.Motor1 -= 10
                print('Derecha')
                instruccion = "Motor1/" + str(self.Motor1)
                self.label.config(text="Derecha")
                self.arduino.write(instruccion.encode())
                print(self.Motor1)
        except AttributeError:
            if key == keyboard.Key.esc:
                self.label.config(text="Saliendo...")
                return False

    def stop_listener(self):
        self.listener.stop()

# Ejemplo de ventana principal que llama a la ventana Toplevel
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    app = KeyApp(root)
    app.protocol("WM_DELETE_WINDOW", app.stop_listener)  # Asegura que el listener se detenga al cerrar la ventana
    root.mainloop()
