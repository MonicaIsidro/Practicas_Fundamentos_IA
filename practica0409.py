# =======================Examen 30 de septiembre =========
    #333333333333333333333333333333

# SISTEMA DE AUTORIZACIÓN PARA EXAMEN

electricidad = input(" Hay electricidad s/n: ") == 's'
encendido = input("¿Enciende? (si/no): ") == 's'
imagen = input("¿muestra imagen? (si/no): ") == 's'

tipo_equipo = input("¿Qué tipo de equipo es? (laptop/desktop): ")
estado_equipo = input("¿Cuál es el estado del equipo? (sin algunas piezas/ golpes/ no hay problema/ con polovo): ")
antiguedad = int(input("¿Qué antigüedad tiene el equipo? (años): "))
tiempo_encendido = int(input("¿Cuánto tiempo ha estado intrentando encender el equipo? (horas): "))


if not electricidad:
    print(" Revisar alimentacion")

elif not encendido:
    print(" Revisar fuente de poder")

elif not imagen:
    print(" Revisar monitor o tarjeta de video")

else:
    print(" Funcionamiento basico correcto.")


if tipo_equipo == "laptop":
     if antiguedad > 5:
         print(" Considerar reemplazo de la laptop.")
     elif estado_equipo == "golpes":
         print(" Reparar o reemplazar la laptop.")
     elif estado_equipo == "sin algunas piezas":
         print(" Revisar componentes internos y externos de la laptop.")
     elif estado_equipo  == "con polvo":
          print(" Realizar mantenimiento preventivo del equipo.")
     else:
         print(" Laptop en buen estado.")





#corregir contradicciones e implementar mas opciones para el sistema, que tipo de equipo es

