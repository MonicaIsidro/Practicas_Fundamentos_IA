#practica 09/09/2026


import random
from datetime import datetime

#Numero de reporte
numero = random.randint(1, 100)

#identificador
numero_Reporte = "R" + str(numero)

#fecha y hora
fecha_hora = datetime.now()

#formato para leer
fecha = fecha_hora.strftime("%d/%m/%Y %H:%M:%S") # el formato puede cambiar todo depende de como se pida
hora = fecha_hora.strftime("%H:%M")

#
print("/n ====")
print("Bienvenido a este portal de ayuda para resolver conflictos con tus equipos")
print("/n ====")
print("Datos de usuario")

nombre = input(" Ingresa tu nombre: ").lower()
direccion = input(" Ingresa tu direccion: ").lower()
#opciones de dipsositivos
print("Tipo de equipo que posees")
print("1. Laptop")
print("2. PC")
print("3. Tablet")
print("4. Servidor")

#1er menu
opcion = input("Selecciona una de las opciones: ")

if opcion == "1":
    print("Has seleccionado Laptop")
elif opcion == "2":
    print("Has seleccionado PC")
elif opcion == "3":
    print("Has seleccionado Tablet")
elif opcion == "4":
    print("Has seleccionado Servidor")
else:
    print("Opción no válida")

print("Seguimiento para tu diagnostico basado al dispositivo que tienes")

#WHILE condicion


\
if opcion == "1":
 print("Preguntas de seguimiento")

  