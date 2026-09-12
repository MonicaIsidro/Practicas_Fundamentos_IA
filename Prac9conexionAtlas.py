import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

def conectar_mongodb():

    mensaje = entrada_mensaje.get().strip()

    if mensaje == "":
        messagebox.showwarning(
            "Dato faltante",
            "Por favor, escribe un mensaje."
        )
        return

    print("Conectando hacia MongoDB Atlas...")

    uri = os.getenv("MONGO_ATLAS_URI")

    if not uri:
        messagebox.showerror(
            "Error",
            "No se encontró MONGO_ATLAS_URI en el archivo .env"
        )
        return

    try:

        cliente = MongoClient(uri)

        cliente.admin.command("ping")

        print("¡Hay conexión a MongoDB Atlas!")

        # ====================================
        # Bd y coleccion

        db = cliente["Monica_Isidro"]
        coleccion = db["Libro"]

        dato = {
            "mensaje": mensaje
        }

        resultado = coleccion.insert_one(dato)

        print("¡Conexión correcta a MongoDB Atlas!")
        print(
            f"Dato insertado con id: {resultado.inserted_id}"
        )

        resultado_texto.config(
            text=(
                "¡Conexión correcta a MongoDB Atlas!\n\n"
                f"Dato insertado correctamente.\n"
                f"ID: {resultado.inserted_id}"
            )
        )

        messagebox.showinfo(
            "Éxito",
            "El dato fue insertado correctamente en MongoDB Atlas."
        )

        # Limpiar el campo
        entrada_mensaje.delete(0, tk.END)

        # Cerrar conexión
        cliente.close()

    except Exception as e:

        print("Error:")
        print(e)

        resultado_texto.config(
            text=f"Error al conectar con MongoDB Atlas:\n\n{e}"
        )

        messagebox.showerror(
            "Error de conexión",
            f"No fue posible conectarse a MongoDB Atlas.\n\n{e}"
        )


# = ventana =

ventana = tk.Tk()

ventana.title("MongoDB Atlas")
ventana.geometry("600x450")
ventana.resizable(False, False)


titulo = tk.Label(
    ventana,
    text="Conexión a MongoDB Atlas",
    font=("Arial", 22, "bold")
)

titulo.pack(pady=30)


subtitulo = tk.Label(
    ventana,
    text="Base de datos: Monica_Isidro\nColección: Libro",
    font=("Arial", 12)
)

subtitulo.pack(pady=10)


etiqueta = tk.Label(
    ventana,
    text="Ingresa el mensaje que deseas guardar:",
    font=("Arial", 13)
)

etiqueta.pack(pady=15)


entrada_mensaje = tk.Entry(
    ventana,
    width=45,
    font=("Arial", 12)
)

entrada_mensaje.pack(pady=5)

#botonparalaconexion

boton = tk.Button(
    ventana,
    text="Conectar e insertar",
    command=conectar_mongodb,
    font=("Arial", 13, "bold"),
    width=20
)

boton.pack(pady=25)


# =======resultado==========

resultado_texto = tk.Label(
    ventana,
    text="Esperando conexión...",
    font=("Arial", 11),
    wraplength=500,
    justify="center"
)

resultado_texto.pack(pady=15)


ventana.mainloop()
