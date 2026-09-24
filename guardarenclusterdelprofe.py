#practica mejorada 11
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# ==========================================
# 1. MÓDULO DE LÓGICA DEL AGENTE
# ==========================================
class AgenteClimatizacion:
    """Agente Reactivo Simple que toma decisiones según el entorno."""
    
    def tomar_decision(self, temperatura: float, humedad: float) -> str:
        """Aplica las reglas condición-acción."""
        if temperatura > 30 and humedad > 70:
            return "Encender aire acondicionado (Modo Deshumidificador)"
        elif temperatura > 30:
            return "Encender ventilador"
        elif temperatura < 18:
            return "Encender calefacción"
        else:
            return "Mantener sistema apagado"


# ==========================================
# 2. MÓDULO DE ALMACENAMIENTO (MONGODB ATLAS)
# ==========================================
class ClusterMongoDB:
    """Gestor de conexión y persistencia hacia el Cluster de MongoDB Atlas."""
    
    def __init__(self, db_name="Monica_Isidro", collection_name="Climatizacion"):
        load_dotenv()
        self.uri = os.getenv("MONGO_ATLAS_URI")
        self.db_name = db_name
        self.collection_name = collection_name

    def _conectar(self):
        """Método auxiliar para validar la URI e instanciar el cliente."""
        if not self.uri:
            raise ValueError("No se encontró 'MONGO_ATLAS_URI' en el archivo .env")
        
        cliente = MongoClient(self.uri)
        # Verifica si el cluster responde
        cliente.admin.command("ping")
        return cliente, cliente[self.db_name][self.collection_name]

    def guardar_registro(self, temperatura: float, humedad: float, accion: str) -> dict:
        """Inserta una lectura y acción en la colección del Cluster."""
        cliente, coleccion = self._conectar()
        try:
            documento = {
                "temperatura": temperatura,
                "humedad": humedad,
                "accion": accion,
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            resultado = coleccion.insert_one(documento)
            documento["_id"] = str(resultado.inserted_id)
            return documento
        finally:
            cliente.close()

    def obtener_historial(self, limite=15):
        """Obtiene los últimos registros guardados en MongoDB Atlas."""
        cliente, coleccion = self._conectar()
        try:
            # Trae los registros ordenados del más reciente al más antiguo
            registros = list(coleccion.find().sort("_id", -1).limit(limite))
            return registros
        finally:
            cliente.close()


# ==========================================
# 3. INTERFAZ GRÁFICA (TKINTER)
# ==========================================
class ClimatizacionApp(tk.Tk):
    def __init__(self, agente: AgenteClimatizacion, cluster: ClusterMongoDB):
        super().__init__()
        self.agente = agente
        self.cluster = cluster

        self.title("Sistema de Climatización conexion a MongoDB Atlas")
        self.geometry("680x560")
        self.resizable(False, False)

        self._crear_componentes()
        self._cargar_historial_inicial()

    def _crear_componentes(self):
        # Encabezado de la ventana
        lbl_titulo = ttk.Label(
            self, 
            text="Agente Climatizador", 
            font=("Arial", 16, "bold")
        )
        lbl_titulo.pack(pady=10)

        lbl_subtitulo = ttk.Label(
            self, 
            text=f"Base de Datos: {self.cluster.db_name} | Colección: {self.cluster.collection_name}",
            font=("Arial", 9, "italic")
        )
        lbl_subtitulo.pack(pady=2)

        # Panel de Lecturas (Percepción)
        frame_input = ttk.LabelFrame(self, text=" Percepciones del Entorno ", padding=15)
        frame_input.pack(fill="x", padx=20, pady=10)

        ttk.Label(frame_input, text="Temperatura (°C):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_temp = ttk.Entry(frame_input, width=12)
        self.entry_temp.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_input, text="Humedad (%):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_hum = ttk.Entry(frame_input, width=12)
        self.entry_hum.grid(row=1, column=1, padx=10, pady=5)

        btn_evaluar = ttk.Button(
            frame_input, 
            text=" Guardar ", 
            command=self._procesar_y_guardar
        )
        btn_evaluar.grid(row=0, column=2, rowspan=2, padx=20, pady=5, sticky="nesw")

        # Panel de Decisión del Agente
        frame_resultado = ttk.LabelFrame(self, text=" Acción Decidida ", padding=10)
        frame_resultado.pack(fill="x", padx=20, pady=5)

        self.lbl_accion = ttk.Label(
            frame_resultado, 
            text="Esperando percepciones...", 
            font=("Arial", 10, "bold"), 
            foreground="#1d4ed8"
        )
        self.lbl_accion.pack(anchor="w")

        # Panel del Historial guardado en el Cluster (Treeview)
        frame_tabla = ttk.LabelFrame(self, text=" Historial en MongoDB Atlas ", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("Fecha/Hora", "Temp (°C)", "Humedad (%)", "Acción Realizada", "ID MongoDB")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tabla.heading("Fecha/Hora", text="Fecha/Hora")
        self.tabla.heading("Temp (°C)", text="Temp")
        self.tabla.heading("Humedad (%)", text="Humedad")
        self.tabla.heading("Acción Realizada", text="Acción Realizada")
        self.tabla.heading("ID MongoDB", text="ID MongoDB")

        self.tabla.column("Fecha/Hora", width=130, anchor="center")
        self.tabla.column("Temp (°C)", width=60, anchor="center")
        self.tabla.column("Humedad (%)", width=70, anchor="center")
        self.tabla.column("Acción Realizada", width=230, anchor="w")
        self.tabla.column("ID MongoDB", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _procesar_y_guardar(self):
        """Valida entradas, ejecuta la decisión del agente e inserta en MongoDB Atlas."""
        # 1. Validar Entradas
        try:
            temp = float(self.entry_temp.get().strip())
            hum = float(self.entry_hum.get().strip())
        except ValueError:
            messagebox.showerror("Dato Inválido", "Por favor, ingresa números válidos en temperatura y humedad.")
            return

        # 2. Tomar Decisión
        accion = self.agente.tomar_decision(temp, hum)
        self.lbl_accion.config(text=f"Acción: {accion}")

        # 3. Insertar en MongoDB Atlas
        try:
            doc = self.cluster.guardar_registro(temp, hum, accion)
            
            # Insertar en la tabla de la interfaz
            self.tabla.insert("", 0, values=(
                doc["fecha_hora"],
                f"{doc['temperatura']} °C",
                f"{doc['humedad']} %",
                doc["accion"],
                doc["_id"]
            ))

            messagebox.showinfo(
                "Éxito", 
                f"Lectura y decisión guardadas correctamente en MongoDB Atlas.\nID: {doc['_id']}"
            )

            # Limpiar campos de entrada
            self.entry_temp.delete(0, tk.END)
            self.entry_hum.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(
                "Error de Conexión", 
                f"No fue posible guardar en MongoDB Atlas:\n\n{e}"
            )

    def _cargar_historial_inicial(self):
        """Consulta los registros previamente guardados en el Cluster al abrir la app."""
        try:
            registros = self.cluster.obtener_historial()
            for reg in registros:
                self.tabla.insert("", tk.END, values=(
                    reg.get("fecha_hora", "N/A"),
                    f"{reg.get('temperatura', 0)} °C",
                    f"{reg.get('humedad', 0)} %",
                    reg.get("accion", "N/A"),
                    str(reg.get("_id", ""))
                ))
        except Exception as e:
            print(f"Advertencia al cargar historial inicial: {e}")


# ==========================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ==========================================
if __name__ == "__main__":
    agente = AgenteClimatizacion()
    
    # Se usa la Base de Datos 'Monica_Isidro' y la colección 'Climatizacion'
    # (puedes cambiar "Climatizacion" por "Libro" si requieres la misma colección exacta)
    cluster = ClusterMongoDB(db_name="Monica_Isidro", collection_name="Climatizacion")
    
    app = ClimatizacionApp(agente, cluster)
    app.mainloop()