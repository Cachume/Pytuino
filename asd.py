import tkinter as tk
from pynput import keyboard
from serial import Serial

class KeyApp:
    Motor1 = 90
    Motor2 = 0
    def __init__(self, root):
        self.root = root
        self.root.title("Teclado y Tkinter")
        try:
            self.arduino = Serial("COM3",9600, timeout=2)
        except:
            print("No se ha conectado a Arduino")
        
        self.label = tk.Label(root, text="Presiona 'a' o 'b' para ejecutar una acción")
        self.label.pack(padx=20, pady=20)
        
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == 'w':
                if not self.Motor2 == 0:
                    self.Motor2 -= 10
                print('Subir')
                instruccion = "Motor2/"+str(self.Motor2)
                self.label.config(text="Acción A ejecutada")
                self.arduino.write(instruccion.encode())
                print(self.Motor2)
            elif key.char == 's':
                if not self.Motor2 == 60:
                    self.Motor2 += 10
                print('Bajar')
                instruccion = "Motor2/"+str(self.Motor2)
                self.label.config(text="Acción B ejecutada")
                self.arduino.write(instruccion.encode())
                print(self.Motor2)
            elif key.char == 'a':
                if not self.Motor1 == 180:
                    self.Motor1 +=10
                print('Izquierda')
                instruccion = "Motor1/"+str(self.Motor1)
                self.label.config(text="Acción B ejecutada")
                self.arduino.write(instruccion.encode())
                
                print(self.Motor1)
            elif key.char == 'd':
                print("Resto motor1")
                if not self.Motor1 == 10:
                    self.Motor1 -=10  
                print('Derecha')
                instruccion = "Motor1/"+str(self.Motor1)
                self.label.config(text="Acción B ejecutada")
                self.arduino.write(instruccion.encode())
                print(self.Motor1)
                     
        except AttributeError:
            if key == keyboard.Key.esc:
                self.label.config(text="Saliendo...")
                return False

    def stop_listener(self):
        self.listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyApp(root)
    root.protocol("WM_DELETE_WINDOW", app.stop_listener)  # Asegura que el listener se detenga al cerrar la ventana
    root.mainloop()
