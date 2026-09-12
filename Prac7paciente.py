# PRACTICA / TAREA 11/09/2026
# SISTEMA DE ORIENTACIÓN MÉDICA 

import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime

numero = random.randint(1, 100)
numero_Reporte = "R" + str(numero)

fecha_hora = datetime.now()

fecha = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
hora = fecha_hora.strftime("%H:%M")

def realizar_diagnostico():
#datos paciente
    nombre = entrada_nombre.get().strip().lower()
    edad_texto = entrada_edad.get().strip()
    duracion_texto = entrada_duracion.get().strip()

    if nombre == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa el nombre del paciente."
        )
        return

    if edad_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa la edad del paciente."
        )
        return

    if duracion_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa los días con síntomas."
        )
        return

    try:

        edad = int(edad_texto)
        duracion = int(duracion_texto)

    except ValueError:

        messagebox.showerror(
            "Error",
            "La edad y los días deben ser números."
        )
        return

    if edad < 0 or duracion < 0:

        messagebox.showerror(
            "Error",
            "La edad y la duración no pueden ser negativas."
        )
        return

    fiebre = fiebre_var.get()
    tos = tos_var.get()
    dolor_garganta = garganta_var.get()
    dolor_cabeza = cabeza_var.get()
    cuerpo = cuerpo_var.get()
    congestion = congestion_var.get()
    dificultad_respirar = respirar_var.get()



    sintomas = [
        fiebre,
        tos,
        dolor_garganta,
        dolor_cabeza,
        cuerpo,
        congestion,
        dificultad_respirar
    ]

    if "" in sintomas:

        messagebox.showwarning(
            "Preguntas incompletas",
            "Por favor, responde todas las preguntas de síntomas."
        )
        return


    diagnostico = ""
    recomendacion = ""
    nivel = ""


    if dificultad_respirar == "s":

        diagnostico = (
            "Señales que requieren valoración profesional"
        )

        nivel = "ALTA"

        recomendacion = (
            "Se recomienda buscar atención médica lo antes "
            "posible. Si la dificultad para respirar es intensa "
            "o empeora, debe buscar atención de urgencia."
        )


    elif (
        fiebre == "s"
        and tos == "s"
        and dolor_garganta == "s"
    ):

        diagnostico = "Posible infección respiratoria"

        nivel = "MEDIA"

        recomendacion = (
            "Se recomienda descansar, mantenerse hidratado "
            "y vigilar la evolución de los síntomas. Si los "
            "síntomas empeoran o persisten, se recomienda "
            "valoración profesional."
        )


    elif (
        fiebre == "s"
        and dolor_cabeza == "s"
        and cuerpo == "s"
    ):

        diagnostico = "Posible cuadro similar a gripe"

        nivel = "MEDIA"

        recomendacion = (
            "Se recomienda descanso, hidratación y vigilancia "
            "de los síntomas. Si existe empeoramiento o fiebre "
            "persistente, se recomienda acudir con un profesional "
            "de la salud."
        )


    elif tos == "s" and dolor_garganta == "s":

        diagnostico = (
            "Posible irritación o infección de garganta"
        )

        nivel = "BAJA"

        recomendacion = (
            "Se recomienda mantenerse hidratado, descansar y "
            "evitar factores que puedan irritar la garganta. "
            "Si los síntomas persisten o empeoran, se recomienda "
            "valoración profesional."
        )


    elif congestion == "s" and tos == "s":

        diagnostico = "Posible cuadro de resfriado"

        nivel = "BAJA"

        recomendacion = (
            "Se recomienda descanso, buena hidratación y "
            "vigilancia de los síntomas."
        )


    elif fiebre == "s":

        diagnostico = (
            "Presencia de fiebre sin un patrón definido"
        )

        nivel = "MEDIA"

        recomendacion = (
            "Se recomienda vigilar la temperatura, mantenerse "
            "hidratado y considerar una valoración profesional "
            "para determinar la causa de la fiebre."
        )

    else:

        diagnostico = (
            "No se identificó un patrón específico"
        )

        nivel = "BAJA"

        recomendacion = (
            "Se recomienda continuar observando los síntomas. "
            "Si aparecen nuevos síntomas o existe empeoramiento, "
            "se recomienda consultar a un profesional."
        )

    mostrar_reporte(
        nombre,
        edad,
        duracion,
        fiebre,
        tos,
        dolor_garganta,
        dolor_cabeza,
        cuerpo,
        congestion,
        dificultad_respirar,
        diagnostico,
        nivel,
        recomendacion
    )
#mostrar reporte

def mostrar_reporte(
    nombre,
    edad,
    duracion,
    fiebre,
    tos,
    dolor_garganta,
    dolor_cabeza,
    cuerpo,
    congestion,
    dificultad_respirar,
    diagnostico,
    nivel,
    recomendacion
):

    limpiar_ventana()

    tk.Label(
        ventana,
        text="REPORTE DEL PACIENTE",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    # INFORMACIÓN
    texto = f"""
Número de reporte: {numero_Reporte}

Fecha: {fecha}
Hora: {hora}

Nombre del paciente: {nombre}
Edad: {edad} años
Días con síntomas: {duracion}

--------------------------------------------

SÍNTOMAS REGISTRADOS

Fiebre: {"Sí" if fiebre == "s" else "No"}
Tos: {"Sí" if tos == "s" else "No"}
Dolor de garganta: {"Sí" if dolor_garganta == "s" else "No"}
Dolor de cabeza: {"Sí" if dolor_cabeza == "s" else "No"}
Dolor corporal: {"Sí" if cuerpo == "s" else "No"}
Congestión nasal: {"Sí" if congestion == "s" else "No"}
Dificultad para respirar: {"Sí" if dificultad_respirar == "s" else "No"}

--------------------------------------------

RESULTADO

Orientación:
{diagnostico}

Nivel de atención:
{nivel}

--------------------------------------------

RECOMENDACIÓN

{recomendacion}
"""

    tk.Label(
        ventana,
        text=texto,
        font=("Arial", 11),
        justify="left",
        wraplength=650
    ).pack(pady=10)


    tk.Label(
        ventana,
        text=(
            "AVISO: Esta información es únicamente orientativa "
            "y no sustituye una valoración profesional."
        ),
        font=("Arial", 10, "italic"),
        wraplength=600
    ).pack(pady=10)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=15)


    tk.Button(
        frame_botones,
        text="Nuevo paciente",
        command=crear_inicio,
        font=("Arial", 11, "bold"),
        width=18
    ).grid(row=0, column=0, padx=10)


    tk.Button(
        frame_botones,
        text="Salir",
        command=ventana.destroy,
        font=("Arial", 11),
        width=12
    ).grid(row=0, column=1, padx=10)


def limpiar_ventana():

    for widget in ventana.winfo_children():
        widget.destroy()


def crear_inicio():

    limpiar_ventana()

    # TÍTULO

    tk.Label(
        ventana,
        text="SISTEMA DE ORIENTACIÓN MÉDICA",
        font=("Arial", 22, "bold")
    ).pack(pady=20)


    tk.Label(
        ventana,
        text=(
            "La información proporcionada sirve únicamente "
            "como orientación y no sustituye una valoración "
            "médica profesional."
        ),
        font=("Arial", 10, "italic"),
        wraplength=600
    ).pack(pady=5)

    # DATOS DEL PACIENTE

    tk.Label(
        ventana,
        text="Datos del paciente",
        font=("Arial", 16, "bold")
    ).pack(pady=15)


    tk.Label(
        ventana,
        text="Nombre del paciente:"
    ).pack()

    global entrada_nombre

    entrada_nombre = tk.Entry(
        ventana,
        width=40,
        font=("Arial", 11)
    )

    entrada_nombre.pack(pady=5)

    tk.Label(
        ventana,
        text="Edad:"
    ).pack()

    global entrada_edad

    entrada_edad = tk.Entry(
        ventana,
        width=15,
        font=("Arial", 11)
    )

    entrada_edad.pack(pady=5)

    tk.Label(
        ventana,
        text="¿Cuántos días lleva con los síntomas?"
    ).pack()

    global entrada_duracion

    entrada_duracion = tk.Entry(
        ventana,
        width=15,
        font=("Arial", 11)
    )

    entrada_duracion.pack(pady=5)

    tk.Label(
        ventana,
        text="Síntomas principales",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    global fiebre_var
    global tos_var
    global garganta_var
    global cabeza_var
    global cuerpo_var
    global congestion_var
    global respirar_var

    fiebre_var = tk.StringVar(value="")
    tos_var = tk.StringVar(value="")
    garganta_var = tk.StringVar(value="")
    cabeza_var = tk.StringVar(value="")
    cuerpo_var = tk.StringVar(value="")
    congestion_var = tk.StringVar(value="")
    respirar_var = tk.StringVar(value="")

    crear_pregunta(
        "¿Tiene fiebre?",
        fiebre_var
    )

    crear_pregunta(
        "¿Tiene tos?",
        tos_var
    )

    crear_pregunta(  "¿Tiene dolor de garganta?",  garganta_var
    )

    crear_pregunta(
        "¿Tiene dolor de cabeza?", cabeza_var
    )

    crear_pregunta(
        "¿Tiene dolor muscular o corporal?",cuerpo_var)

    crear_pregunta(
  "¿Tiene congestión nasal?",  congestion_var )

    crear_pregunta( "¿Tiene dificultad para respirar?", respirar_var )

    tk.Button(
        ventana,
        text="Realizar orientación",
        command=realizar_diagnostico,
        font=("Arial", 12, "bold"),
        width=22
    ).pack(pady=20)

def crear_pregunta(texto, variable):

    frame = tk.Frame(ventana)
    frame.pack(pady=2)

    tk.Label(
        frame,
        text=texto,
        width=32,
        anchor="w"
    ).pack(side="left")

    tk.Radiobutton(
        frame,
        text="Sí",
        variable=variable,
        value="s"
    ).pack(side="left", padx=5)

    tk.Radiobutton(
        frame,
        text="No",
        variable=variable,
        value="n"
    ).pack(side="left", padx=5)

ventana = tk.Tk()
ventana.title("Sistema de Orientación Médica")
ventana.geometry("750x800")
ventana.resizable(False, False)
crear_inicio()
ventana.mainloop()