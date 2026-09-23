import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi

# 1. Configurar conexión con timeout de 5 segundos para no congelar la app
URI = "TU_CADENA_DE_CONEXION_DE_ATLAS"

try:
    client = MongoClient(
        URI, 
        tlsCAFile=certifi.where(), 
        serverSelectionTimeoutMS=5000  # Tiempo límite si falla la red
    )
    db = client["tu_base_datos"]
    coleccion = db["tu_coleccion"]
except Exception as e:
    print(f"Error inicial de configuración: {e}")

def enviar():
    texto = entrada_texto.get().strip()

    # Validar que no se envíen textos vacíos
    if not texto:
        messagebox.showwarning("Aviso", "Escribe un mensaje antes de enviar.")
        return

    # 2. Capturar el error con try / except
    try:
        resultado = coleccion.insert_one({"mensaje": texto})
        messagebox.showinfo("Éxito", f"Guardado con ID: {resultado.inserted_id}")
        entrada_texto.delete(0, tk.END)  # Limpiar el campo tras enviar

    except PyMongoError as e:
        # Muestra una ventana de error en lugar de hacer colapsar Tkinter
        messagebox.showerror("Error de MongoDB", f"No se pudo conectar a la base de datos:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

# Interfaz Tkinter
root = tk.Tk()
root.title("Ejemplo de Envío")
root.geometry("300x150")

entrada_texto = tk.Entry(root, width=30)
entrada_texto.pack(pady=20)

boton_enviar = tk.Button(root, text="Enviar a MongoDB", command=enviar)
boton_enviar.pack()

root.mainloop()