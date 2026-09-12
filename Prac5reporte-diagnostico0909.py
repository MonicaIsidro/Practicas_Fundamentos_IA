# PRACTICA 09/09/2026
# SISTEMA DE DIAGNÓSTICO

import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime


numero = random.randint(1, 100)
numero_Reporte = "R" + str(numero)

fecha_hora = datetime.now()
fecha = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
hora = fecha_hora.strftime("%H:%M")


#principal

ventana = tk.Tk()
ventana.title("Portal de ayuda - Diagnóstico de equipos")
ventana.geometry("700x650")
ventana.resizable(False, False)


# ===============funciones

def limpiar_ventana():
    """Elimina los elementos de la ventana."""
    for widget in ventana.winfo_children():
        widget.destroy()


def iniciar_diagnostico():
    """Obtiene los datos del usuario y muestra la selección de equipo."""

    nombre = entrada_nombre.get().strip().lower()
    direccion = entrada_direccion.get().strip().lower()

    if nombre == "" or direccion == "":
        messagebox.showwarning(
            "Datos incompletos",
            "Por favor, ingresa tu nombre y dirección."
        )
        return

    mostrar_equipos(nombre, direccion)


def mostrar_equipos(nombre, direccion):
    """Muestra las opciones de equipos."""

    limpiar_ventana()

    titulo = tk.Label(
        ventana,
        text="Tipo de equipo que posees",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=30)

    equipo_var = tk.StringVar(value="")

    opciones = [
        ("Laptop", "1"),
        ("PC", "2"),
        ("Tablet", "3"),
        ("Servidor", "4")
    ]

    for texto, valor in opciones:
        tk.Radiobutton(
            ventana,
            text=texto,
            variable=equipo_var,
            value=valor,
            font=("Arial", 14)
        ).pack(anchor="w", padx=250, pady=8)

    def seleccionar_equipo():

        opcion = equipo_var.get()

        if opcion == "":
            messagebox.showwarning(
                "Selección",
                "Selecciona un tipo de equipo."
            )
            return

        if opcion == "1":
            equipo = "Laptop"
        elif opcion == "2":
            equipo = "PC"
        elif opcion == "3":
            equipo = "Tablet"
        elif opcion == "4":
            equipo = "Servidor"

        mostrar_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            0
        )

    tk.Button(
        ventana,
        text="Continuar",
        command=seleccionar_equipo,
        font=("Arial", 13, "bold"),
        width=15
    ).pack(pady=35)


#diagnostica
def mostrar_pregunta(nombre, direccion, equipo, opcion, paso):

    limpiar_ventana()

    # preguntad lapto

    if opcion == "1":

        preguntas = [
            ("¿La laptop enciende?", "enciende"),
            ("¿El cargador está conectado correctamente?", "cargador"),
            ("¿La batería muestra alguna señal de carga?", "bateria"),
            ("¿La pantalla muestra imagen?", "imagen"),
            ("¿La laptop funciona demasiado lento?", "lento")
        ]

        # Guardamos respuestas
        if not hasattr(ventana, "respuestas"):
            ventana.respuestas = {}

        if paso >= len(preguntas):
            resultado_laptop(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        pregunta, clave = preguntas[paso]

        # Saltar preguntas que no correspondan
        if paso == 1 and ventana.respuestas.get("enciende") != "n":
            mostrar_pregunta(
                nombre, direccion, equipo, opcion, 3
            )
            return

        if paso == 2 and ventana.respuestas.get("cargador") != "n":
            mostrar_pregunta(
                nombre, direccion, equipo, opcion, 4
            )
            return

        if paso == 3 and ventana.respuestas.get("bateria") != "s":
            resultado_laptop(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        if paso == 4 and ventana.respuestas.get("imagen") != "s":
            resultado_laptop(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        mostrar_interfaz_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            paso,
            pregunta,
            clave,
            len(preguntas)
        )

    # PREGUNTAS PC

    elif opcion == "2":

        preguntas = [
            ("¿La PC enciende?", "enciende"),
            ("¿La PC recibe corriente?", "corriente"),
            ("¿El monitor muestra imagen?", "imagen"),
            ("¿La PC se reinicia inesperadamente?", "reinicia")
        ]

        if not hasattr(ventana, "respuestas"):
            ventana.respuestas = {}

        if paso >= len(preguntas):
            resultado_pc(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        pregunta, clave = preguntas[paso]

        if paso == 1 and ventana.respuestas.get("enciende") != "n":
            mostrar_pregunta(
                nombre, direccion, equipo, opcion, 2
            )
            return

        if paso == 2 and ventana.respuestas.get("corriente") != "s":
            resultado_pc(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        if paso == 3 and ventana.respuestas.get("imagen") != "s":
            resultado_pc(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        mostrar_interfaz_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            paso,
            pregunta,
            clave,
            len(preguntas)
        )

    # PREGUNTAS TABLET

    elif opcion == "3":

        preguntas = [
            ("¿La tablet enciende?", "enciende"),
            ("¿La tablet muestra que está cargando?", "carga"),
            ("¿La pantalla táctil funciona correctamente?", "pantalla"),
            ("¿La tablet tiene problemas para conectarse a Internet?", "internet")
        ]

        if not hasattr(ventana, "respuestas"):
            ventana.respuestas = {}

        if paso >= len(preguntas):
            resultado_tablet(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        pregunta, clave = preguntas[paso]

        if paso == 1 and ventana.respuestas.get("enciende") != "n":
            mostrar_pregunta(
                nombre, direccion, equipo, opcion, 2
            )
            return

        if paso == 2 and ventana.respuestas.get("carga") != "s":
            resultado_tablet(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        if paso == 3 and ventana.respuestas.get("pantalla") != "s":
            resultado_tablet(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        mostrar_interfaz_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            paso,
            pregunta,
            clave,
            len(preguntas)
        )

    # PREGUNTAS SERVIDOR

    elif opcion == "4":

        preguntas = [
            ("¿El servidor está disponible?", "disponible"),
            ("¿El servidor tiene conexión de red?", "red"),
            ("¿El servicio que necesitas funciona correctamente?", "servicio")
        ]

        if not hasattr(ventana, "respuestas"):
            ventana.respuestas = {}

        if paso >= len(preguntas):
            resultado_servidor(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        pregunta, clave = preguntas[paso]

        if paso == 1 and ventana.respuestas.get("disponible") != "n":
            mostrar_pregunta(
                nombre, direccion, equipo, opcion, 2
            )
            return

        if paso == 2 and ventana.respuestas.get("red") != "s":
            resultado_servidor(
                nombre,
                direccion,
                equipo,
                ventana.respuestas
            )
            return

        mostrar_interfaz_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            paso,
            pregunta,
            clave,
            len(preguntas)
        )


# INTERFAZ DE PREGUNTA

def mostrar_interfaz_pregunta(
    nombre,
    direccion,
    equipo,
    opcion,
    paso,
    pregunta,
    clave,
    total
):

    titulo = tk.Label(
        ventana,
        text=f"Diagnóstico - {equipo}",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=35)

    etiqueta = tk.Label(
        ventana,
        text=pregunta,
        font=("Arial", 15),
        wraplength=600
    )
    etiqueta.pack(pady=30)

    tk.Label(
        ventana,
        text=f"Pregunta {paso + 1} de {total}",
        font=("Arial", 11)
    ).pack(pady=5)

    frame = tk.Frame(ventana)
    frame.pack(pady=30)

    def responder(valor):

        ventana.respuestas[clave] = valor

        mostrar_pregunta(
            nombre,
            direccion,
            equipo,
            opcion,
            paso + 1
        )

    tk.Button(
        frame,
        text="Sí",
        command=lambda: responder("s"),
        font=("Arial", 14, "bold"),
        width=10
    ).grid(row=0, column=0, padx=20)

    tk.Button(
        frame,
        text="No",
        command=lambda: responder("n"),
        font=("Arial", 14, "bold"),
        width=10
    ).grid(row=0, column=1, padx=20)

# RESULTADO LAPTOP
def resultado_laptop(nombre, direccion, equipo, respuestas):

    if respuestas.get("enciende") == "n":

        if respuestas.get("cargador") == "n":
            diagnostico = "El problema podría estar relacionado con la conexión del cargador."
            recomendacion = "Verifica que el cargador esté conectado correctamente."

        elif respuestas.get("bateria") == "n":
            diagnostico = "Posible problema con la batería o el cargador."
            recomendacion = "Probar otro cargador o revisar la batería."

        else:
            diagnostico = "La laptop recibe energía, pero no logra iniciar."
            recomendacion = "Revisar el sistema de encendido."

    elif respuestas.get("imagen") == "n":

        diagnostico = "Posible problema de pantalla o conexión de video."
        recomendacion = "Revisar la pantalla y sus conexiones."

    elif respuestas.get("lento") == "s":

        diagnostico = "Posible falta de memoria o exceso de programas ejecutándose."
        recomendacion = "Revisar memoria RAM y programas en segundo plano."

    else:

        diagnostico = "No se encontró una falla evidente."
        recomendacion = "Continuar monitoreando el funcionamiento."

    mostrar_reporte(
        nombre,
        direccion,
        equipo,
        diagnostico,
        recomendacion
    )

# RESULTADO PC

def resultado_pc(nombre, direccion, equipo, respuestas):

    if respuestas.get("enciende") == "n":

        if respuestas.get("corriente") == "n":
            diagnostico = "Posible problema con la alimentación eléctrica."
            recomendacion = "Revisar cable, conexión eléctrica y fuente de poder."

        else:
            diagnostico = "La PC recibe corriente pero no inicia."
            recomendacion = "Revisar la fuente de poder y componentes internos."

    elif respuestas.get("imagen") == "n":

        diagnostico = "Posible problema de conexión de video."
        recomendacion = "Revisar cables, monitor y tarjeta gráfica."

    elif respuestas.get("reinicia") == "s":

        diagnostico = "Posible problema de temperatura o alimentación."
        recomendacion = "Revisar temperatura y fuente de poder."

    else:

        diagnostico = "No se encontró una falla evidente."
        recomendacion = "Continuar monitoreando el equipo."

    mostrar_reporte(
        nombre,
        direccion,
        equipo,
        diagnostico,
        recomendacion
    )


# RESULTADO TABLET

def resultado_tablet(nombre, direccion, equipo, respuestas):

    if respuestas.get("enciende") == "n":

        if respuestas.get("carga") == "n":
            diagnostico = "Posible problema con batería, cargador o puerto de carga."
            recomendacion = "Revisar cargador y puerto de carga."

        else:
            diagnostico = "La tablet recibe energía pero no inicia."
            recomendacion = "Intentar reiniciar el dispositivo."

    elif respuestas.get("pantalla") == "n":

        diagnostico = "Posible problema con la pantalla táctil."
        recomendacion = "Reiniciar el dispositivo y comprobar nuevamente."

    elif respuestas.get("internet") == "s":

        diagnostico = "Posible problema con la conexión Wi-Fi."
        recomendacion = "Revisar la conexión y reiniciar el router."

    else:

        diagnostico = "No se encontró una falla evidente."
        recomendacion = "Continuar monitoreando el dispositivo."

    mostrar_reporte(
        nombre,
        direccion,
        equipo,
        diagnostico,
        recomendacion
    )

# RESULTADO SERVIDOR

def resultado_servidor(nombre, direccion, equipo, respuestas):

    if respuestas.get("disponible") == "n":

        if respuestas.get("red") == "n":
            diagnostico = "Posible problema de conexión de red."
            recomendacion = "Revisar cables y configuración de red."

        else:
            diagnostico = "El servidor tiene conexión pero no está disponible."
            recomendacion = "Revisar los servicios del servidor."

    elif respuestas.get("servicio") == "n":

        diagnostico = "Posible problema en el servicio o aplicación."
        recomendacion = "Revisar el estado del servicio."

    else:

        diagnostico = "El servidor y sus servicios funcionan correctamente."
        recomendacion = "Continuar monitoreando el funcionamiento."

    mostrar_reporte(
        nombre,
        direccion,
        equipo,
        diagnostico,
        recomendacion
    )


# MOSTRAR REPORTE

def mostrar_reporte(
    nombre,
    direccion,
    equipo,
    diagnostico,
    recomendacion
):

    limpiar_ventana()

    tk.Label(
        ventana,
        text="REPORTE DE DIAGNÓSTICO",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    texto = f"""
Número de reporte: {numero_Reporte}

Nombre: {nombre}

Dirección: {direccion}

Equipo: {equipo}

Fecha: {fecha}

Hora: {hora}

----------------------------------------

DIAGNÓSTICO:

{diagnostico}

RECOMENDACIÓN:

{recomendacion}
"""

    tk.Label(
        ventana,
        text=texto,
        font=("Arial", 12),
        justify="left",
        wraplength=620
    ).pack(pady=15)

    tk.Button(
        ventana,
        text="Nuevo diagnóstico",
        command=nuevo_diagnostico,
        font=("Arial", 12, "bold"),
        width=20
    ).pack(pady=15)

    tk.Button(
        ventana,
        text="Salir",
        command=ventana.destroy,
        font=("Arial", 12),
        width=20
    ).pack(pady=5)

# NUEVO DIAGNÓSTICO

def nuevo_diagnostico():

    global numero_Reporte, fecha, hora

    numero = random.randint(1, 100)
    numero_Reporte = "R" + str(numero)

    fecha_hora = datetime.now()
    fecha = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
    hora = fecha_hora.strftime("%H:%M")

    if hasattr(ventana, "respuestas"):
        del ventana.respuestas

    crear_inicio()


# PANTALLA INICIAL

def crear_inicio():

    limpiar_ventana()

    tk.Label(
        ventana,
        text="================================",
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        ventana,
        text="Bienvenido a este portal de ayuda",
        font=("Arial", 20, "bold")
    ).pack(pady=5)

    tk.Label(
        ventana,
        text="para resolver conflictos con tus equipos",
        font=("Arial", 13)
    ).pack(pady=5)

    tk.Label(
        ventana,
        text="Datos de usuario",
        font=("Arial", 17, "bold")
    ).pack(pady=25)

    tk.Label(
        ventana,
        text="Nombre:"
    ).pack()

    global entrada_nombre

    entrada_nombre = tk.Entry(
        ventana,
        width=40,
        font=("Arial", 12)
    )
    entrada_nombre.pack(pady=8)

    tk.Label(
        ventana,
        text="Dirección:"
    ).pack()

    global entrada_direccion

    entrada_direccion = tk.Entry(
        ventana,
        width=40,
        font=("Arial", 12)
    )
    entrada_direccion.pack(pady=8)

    tk.Button(
        ventana,
        text="Iniciar diagnóstico",
        command=iniciar_diagnostico,
        font=("Arial", 13, "bold"),
        width=20
    ).pack(pady=30)

crear_inicio()

ventana.mainloop()

