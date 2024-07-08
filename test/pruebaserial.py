from serial import *

puertos = ["COM1","COM2","COM3","COM4", "COM5"]
puertospermitidos = []

for data in puertos:
    try:
        serial=Serial(data,"9600",timeout=2)
        print("Se ha encontrado conexión en el puerto: " + data)
        puertospermitidos.append(data)
    except:
        print("No hay conexión en el puerto: " + data)

print("Se ha encontrado conexión en los puertos: ")
print(puertospermitidos )