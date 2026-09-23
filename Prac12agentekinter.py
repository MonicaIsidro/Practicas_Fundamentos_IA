import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# 1. MÓDULO DE LÓGICA DEL AGENTE
# ==========================================
class ReglaClimatizacion:
    """Representa una regla del sistema para facilitar la extensibilidad."""
    def __init__(self, condicion, accion):
        self.condicion = condicion
        self.accion = accion

class AgenteClimatizacion:
    """Agente reactivo desacoplado de la interfaz de usuario."""
    def __init__(self):
        self.reglas = []
        self._cargar_reglas_base()

    def _cargar_reglas_base(self):
        # Se pueden agregar más reglas (ej. calidad de aire) sin alterar el motor
        self.reglas = [
            ReglaClimatizacion(
                lambda t, h: t > 30 and h > 70, 
                "Encender aire acondicionado (Modo Deshumidificador)"
            ),
            ReglaClimatizacion(
                lambda t, h: t > 30, 
                "Encender ventilador"
            ),
            ReglaClimatizacion(
                lambda t, h: t < 18, 
                "Encender calefacción"
            ),
        ]

    def tomar_decision(self, temperatura: float, humedad: float) -> str:
        """Evalúa las percepciones frente a las reglas registradas."""
        for regla in self.reglas:
            if regla.condicion(temperatura, humedad):
                return regla.accion
        return "Mantener sistema apagado"


# ==========================================
# 2. MÓDULO DE ALMACENAMIENTO EN CLUSTER
# ==========================================
class ClusterStorage:
    """Gestor de persistencia para registrar lecturas y acciones."""
    def __init__(self):
        self.registros = []

    def guardar_registro(self, temperatura: float, humedad: float, accion: str) -> dict:
        registro = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": temperatura,
            "humedad": humedad,
            "accion": accion
        }
        self.registros.append(registro)
        return registro


# ==========================================
# 3. INTERFAZ GRÁFICA (TKINTER)
# ==========================================
class ClimatizacionApp(tk.Tk):
    def __init__(self, agente: AgenteClimatizacion, cluster: ClusterStorage):
        super().__init__()
        self.agente = agente
        self.cluster = cluster

        self.title("Sistema de Climatización Inteligente")
        self.geometry("640x500")
        self.resizable(False, False)

        self._crear_componentes()

    def _crear_componentes(self):
        # Panel de Lectura de Sensores
        frame_input = ttk.LabelFrame(self, text=" Percepciones del Entorno ", padding=15)
        frame_input.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_input, text="Temperatura (°C):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_temp = ttk.Entry(frame_input, width=12)
        self.entry_temp.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_input, text="Humedad (%):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_hum = ttk.Entry(frame_input, width=12)
        self.entry_hum.grid(row=1, column=1, padx=10, pady=5)

        btn_evaluar = ttk.Button(frame_input, text="Procesar y Guardar", command=self._procesar_datos)
        btn_evaluar.grid(row=0, column=2, rowspan=2, padx=20, pady=5, sticky="nesw")

        # Panel de Acción Resultante
        frame_resultado = ttk.LabelFrame(self, text=" Decisión del Agente ", padding=12)
        frame_resultado.pack(fill="x", padx=15, pady=5)

        self.lbl_accion = ttk.Label(
            frame_resultado, 
            text="Esperando lecturas...", 
            font=("Helvetica", 10, "bold"), 
            foreground="#1e40af"
        )
        self.lbl_accion.pack(anchor="w")

        # Panel de Tabla / Historial en Cluster
        frame_tabla = ttk.LabelFrame(self, text=" Historial Guardado en Cluster ", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("Fecha/Hora", "Temp (°C)", "Humedad (%)", "Acción Ejecutada")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)

        self.tabla.heading("Fecha/Hora", text="Fecha/Hora")
        self.tabla.heading("Temp (°C)", text="Temp (°C)")
        self.tabla.heading("Humedad (%)", text="Humedad (%)")
        self.tabla.heading("Acción Ejecutada", text="Acción Ejecutada")

        self.tabla.column("Fecha/Hora", width=140, anchor="center")
        self.tabla.column("Temp (°C)", width=80, anchor="center")
        self.tabla.column("Humedad (%)", width=90, anchor="center")
        self.tabla.column("Acción Ejecutada", width=270, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _procesar_datos(self):
        try:
            temp = float(self.entry_temp.get())
            hum = float(self.entry_hum.get())
        except ValueError:
            messagebox.showerror("Error de Entrada", "Ingresa valores numéricos válidos para temperatura y humedad.")
            return

        # 1. Tomar decisión
        accion = self.agente.tomar_decision(temp, hum)
        self.lbl_accion.config(text=f"Acción: {accion}")

        # 2. Guardar en Cluster
        registro = self.cluster.guardar_registro(temp, hum, accion)

        # 3. Mostrar en la vista del historial
        self.tabla.insert("", 0, values=(
            registro["timestamp"],
            f"{registro['temperatura']} °C",
            f"{registro['humedad']} %",
            registro["accion"]
        ))

        # Limpiar cajas de texto
        self.entry_temp.delete(0, tk.END)
        self.entry_hum.delete(0, tk.END)


if __name__ == "__main__":
    agente = AgenteClimatizacion()
    cluster = ClusterStorage()
    app = ClimatizacionApp(agente, cluster)
    app.mainloop()