electricidad = input("¿Tiene electricidad? (s/n): ").lower() == "s"

enciende = input("¿El equipo enciende? (s/n): ").lower() == "s"

imagen = input("¿Muestra imagen en la pantalla? (s/n): ").lower() == "s"

dispositivo = input("¿Tiene problemas con algún dispositivo? (s/n): ").lower() == "s"

golpe = input("¿El equipo recibió algún golpe o daño físico recientemente? (s/n): ").lower() == "s"

antiguo = input("¿El equipo es antiguo? (s/n): ").lower() == "s"

version = input("¿Qué versión del sistema utiliza?: ")

sobrecalienta = input("¿El equipo se sobrecalienta? (s/n): ").lower() == "s"

ruido = input("¿El equipo presenta ruidos extraños? (s/n): ").lower() == "s"


if not electricidad:
    print("Diagnóstico: Revisar la conexión eléctrica, el cable de alimentación o el contacto de energía.")

elif not enciende:
    if golpe:
        print("Diagnóstico: El equipo pudo sufrir daños físicos. Revisar la fuente de poder y los componentes internos.")
    elif antiguo:
        print("Diagnóstico: El equipo puede presentar una falla relacionada con el desgaste de sus componentes. Revisar la fuente de poder y componentes internos.")
    else:
        print("Diagnóstico: Revisar la fuente de poder, el botón de encendido y las conexiones internas.")

elif not imagen:
    if golpe:
        print("Diagnóstico: Posible daño en la pantalla, tarjeta gráfica, memoria RAM o conexiones debido al golpe.")
    elif dispositivo:
        print("Diagnóstico: Revisar la conexión del dispositivo de video, tarjeta gráfica y memoria RAM.")
    else:
        print("Diagnóstico: Revisar la pantalla, memoria RAM, tarjeta gráfica y conexiones de video.")

elif dispositivo:
    print("Diagnóstico: Revisar la conexión, controladores y funcionamiento del dispositivo afectado.")

elif sobrecalienta:
    print("Diagnóstico: Revisar el sistema de ventilación, ventiladores, disipador y acumulación de polvo.")

elif ruido:
    print("Diagnóstico: Revisar ventiladores, disco duro y otros componentes mecánicos que puedan estar generando el ruido.")

elif antiguo:
    print("Diagnóstico: El equipo funciona, pero por su antigüedad se recomienda revisar el estado de sus componentes y considerar una actualización.")

else:
    print("Diagnóstico: Funcionamiento básico correcto. No se detectaron problemas evidentes.")