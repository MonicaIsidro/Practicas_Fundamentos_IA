# Diagnostico de equipos
# ============================================

import tkinter as tk
from tkinter import messagebox


def realizar_diagnostico():

    electricidad = electricidad_var.get()
    encendido = encendido_var.get()
    imagen = imagen_var.get()

    tipo_equipo = tipo_equipo_var.get()
    estado_equipo = estado_equipo_var.get()

    antiguedad_texto = entrada_antiguedad.get()
    tiempo_texto = entrada_tiempo.get()


    if tipo_equipo == "":
        messagebox.showwarning(
            "Dato faltante",
            "Selecciona el tipo de equipo."
        )
        return

    if estado_equipo == "":
        messagebox.showwarning(
            "Dato faltante",
            "Selecciona el estado del equipo."
        )
        return

    if antiguedad_texto == "" or tiempo_texto == "":
        messagebox.showwarning(
            "Datos faltantes",
            "Ingresa la antigüedad y el tiempo de encendido."
        )
        return

    try:
        antiguedad = int(antiguedad_texto)
        tiempo_encendido = int(tiempo_texto)

    except ValueError:
        messagebox.showerror(
            "Error",
            "La antigüedad y el tiempo deben ser números."
        )
        return


    if antiguedad < 0 or tiempo_encendido < 0:
        messagebox.showerror(
            "Error",
            "Los valores no pueden ser negativos."
        )
        return

    diagnostico = ""

    if electricidad == "no":

        diagnostico = (
            "Revisar alimentación eléctrica."
        )

    elif encendido == "no":

        diagnostico = (
            "Revisar fuente de poder o sistema de alimentación."
        )

    elif imagen == "no":

        diagnostico = (
            "Revisar monitor, pantalla o tarjeta de video."
        )

    else:

        diagnostico = (
            "Funcionamiento básico correcto."
        )

    recomendacion = ""

    # LAPTOP\

    if tipo_equipo == "Laptop":

        if antiguedad > 5:

            recomendacion = (
                "Considerar reemplazo de la laptop "
                "debido a su antigüedad."
            )

        elif estado_equipo == "Golpes":

            recomendacion = (
                "Revisar daños físicos y considerar "
                "reparar o reemplazar la laptop."
            )

        elif estado_equipo == "Sin algunas piezas":

            recomendacion = (
                "Revisar componentes internos y externos "
                "de la laptop."
            )

        elif estado_equipo == "Con polvo":

            recomendacion = (
                "Realizar mantenimiento preventivo "
                "y limpieza del equipo."
            )

        else:

            recomendacion = (
                "Laptop en buen estado."
            )
    # PC

    elif tipo_equipo == "Desktop / PC":

        if antiguedad > 7:

            recomendacion = (
                "Considerar actualización o reemplazo "
                "del equipo por su antigüedad."
            )

        elif estado_equipo == "Golpes":

            recomendacion = (
                "Revisar gabinete y componentes internos "
                "por posibles daños físicos."
            )

        elif estado_equipo == "Sin algunas piezas":

            recomendacion = (
                "Revisar los componentes faltantes "
                "y completar el equipo."
            )

        elif estado_equipo == "Con polvo":

            recomendacion = (
                "Realizar limpieza interna y mantenimiento "
                "preventivo."
            )

        else:

            recomendacion = (
                "PC en buen estado."
            )

    # TABLET

    elif tipo_equipo == "Tablet":

        if antiguedad > 5:

            recomendacion = (
                "Considerar reemplazo de la tablet "
                "por su antigüedad."
            )

        elif estado_equipo == "Golpes":

            recomendacion = (
                "Revisar pantalla, carcasa y componentes "
                "internos por posibles daños."
            )

        elif estado_equipo == "Sin algunas piezas":

            recomendacion = (
                "Revisar los componentes faltantes "
                "de la tablet."
            )

        elif estado_equipo == "Con polvo":

            recomendacion = (
                "Realizar limpieza y mantenimiento "
                "preventivo."
            )

        else:

            recomendacion = (
                "Tablet en buen estado."
            )
    # SERVIDOR

    elif tipo_equipo == "Servidor":

        if antiguedad > 7:

            recomendacion = (
                "Evaluar actualización o reemplazo "
                "del servidor."
            )

        elif estado_equipo == "Golpes":

            recomendacion = (
                "Revisar físicamente el servidor y "
                "sus componentes."
            )

        elif estado_equipo == "Sin algunas piezas":

            recomendacion = (
                "Revisar componentes faltantes y "
                "configuración del servidor."
            )

        elif estado_equipo == "Con polvo":

            recomendacion = (
                "Realizar mantenimiento preventivo "
                "y limpieza del servidor."
            )

        else:

            recomendacion = (
                "Servidor en buen estado."
            )

    if tiempo_encendido >= 4:

        recomendacion += (
            "\n\nAdemás, lleva varias horas intentando "
            "encender el equipo. Se recomienda detener "
            "los intentos y realizar una revisión técnica."
        )

    resultado = (
        "========== DIAGNÓSTICO ==========\n\n"
        f"Tipo de equipo: {tipo_equipo}\n"
        f"Antigüedad: {antiguedad} años\n"
        f"Tiempo intentando encender: "
        f"{tiempo_encendido} horas\n\n"
        f"DIAGNÓSTICO BÁSICO:\n"
        f"{diagnostico}\n\n"
        f"RECOMENDACIÓN:\n"
        f"{recomendacion}"
    )

    resultado_texto.config(
        text=resultado
    )


def limpiar():

    electricidad_var.set("")
    encendido_var.set("")
    imagen_var.set("")
    tipo_equipo_var.set("")
    estado_equipo_var.set("")

    entrada_antiguedad.delete(0, tk.END)
    entrada_tiempo.delete(0, tk.END)

    resultado_texto.config(
        text="Aquí aparecerá el diagnóstico."
    )

ventana = tk.Tk()

ventana.title(
    "Sistema de autorización para examen"
)

ventana.geometry("750x800")

ventana.resizable(False, False)

tk.Label(
    ventana,
    text="SISTEMA DE AUTORIZACIÓN PARA EXAMEN",
    font=("Arial", 20, "bold")
).pack(pady=20)


tk.Label(
    ventana,
    text="¿Hay electricidad?",
    font=("Arial", 12, "bold")
).pack(pady=5)

electricidad_var = tk.StringVar(value="")

frame_electricidad = tk.Frame(ventana)
frame_electricidad.pack()

tk.Radiobutton(
    frame_electricidad,
    text="Sí",
    variable=electricidad_var,
    value="si"
).pack(side="left", padx=15)

tk.Radiobutton(
    frame_electricidad,
    text="No",
    variable=electricidad_var,
    value="no"
).pack(side="left", padx=15)

tk.Label(
    ventana,
    text="¿Enciende el equipo?",
    font=("Arial", 12, "bold")
).pack(pady=5)

encendido_var = tk.StringVar(value="")

frame_encendido = tk.Frame(ventana)
frame_encendido.pack()

tk.Radiobutton(
    frame_encendido,
    text="Sí",
    variable=encendido_var,
    value="si"
).pack(side="left", padx=15)

tk.Radiobutton(
    frame_encendido,
    text="No",
    variable=encendido_var,
    value="no"
).pack(side="left", padx=15)

tk.Label(
    ventana,
    text="¿Muestra imagen?",
    font=("Arial", 12, "bold")
).pack(pady=5)

imagen_var = tk.StringVar(value="")

frame_imagen = tk.Frame(ventana)
frame_imagen.pack()

tk.Radiobutton(
    frame_imagen,
    text="Sí",
    variable=imagen_var,
    value="si"
).pack(side="left", padx=15)

tk.Radiobutton(
    frame_imagen,
    text="No",
    variable=imagen_var,
    value="no"
).pack(side="left", padx=15)

tk.Label(
    ventana,
    text="¿Qué tipo de equipo es?",
    font=("Arial", 12, "bold")
).pack(pady=8)

tipo_equipo_var = tk.StringVar(value="")

tipos = [
    "Laptop",
    "Desktop / PC",
    "Tablet",
    "Servidor"
]

for tipo in tipos:

    tk.Radiobutton(
        ventana,
        text=tipo,
        variable=tipo_equipo_var,
        value=tipo
    ).pack(anchor="center")

tk.Label(
    ventana,
    text="¿Cuál es el estado del equipo?",
    font=("Arial", 12, "bold")
).pack(pady=8)

estado_equipo_var = tk.StringVar(value="")

estados = [
    "Sin algunas piezas",
    "Golpes",
    "No hay problema",
    "Con polvo"
]

for estado in estados:

    tk.Radiobutton(
        ventana,
        text=estado,
        variable=estado_equipo_var,
        value=estado
    ).pack(anchor="center")

frame_datos = tk.Frame(ventana)
frame_datos.pack(pady=10)

tk.Label(
    frame_datos,
    text="Antigüedad (años):"
).grid(row=0, column=0, padx=10)

entrada_antiguedad = tk.Entry(
    frame_datos,
    width=10
)

entrada_antiguedad.grid(row=0, column=1, padx=10)

tk.Label(
    frame_datos,
    text="Tiempo intentando encender (horas):"
).grid(row=0, column=2, padx=10)

entrada_tiempo = tk.Entry(
    frame_datos,
    width=10
)

entrada_tiempo.grid(row=0, column=3, padx=10)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(
    frame_botones,
    text="Realizar diagnóstico",
    command=realizar_diagnostico,
    font=("Arial", 11, "bold"),
    width=20
).grid(row=0, column=0, padx=10)

tk.Button(
    frame_botones,
    text="Limpiar",
    command=limpiar,
    font=("Arial", 11),
    width=12
).grid(row=0, column=1, padx=10)

resultado_texto = tk.Label(
    ventana,
    text="Aquí aparecerá el diagnóstico.",
    font=("Arial", 11),
    justify="left",
    wraplength=650
)

resultado_texto.pack(pady=10)


ventana.mainloop()



#corregir contradicciones e implementar mas opciones para el sistema, que tipo de equipo es

