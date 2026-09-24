#CRUD EN MONGO
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# 1. MÓDULO DE LÓGICA DEL AGENTE
class AgenteClimatizacion:
    """Agente que toma decisiones según el entorno."""

    def tomar_decision(self, temperatura: float, humedad: float) -> str:
        """Aplica las reglas condición-acción."""

        if temperatura > 30 and humedad > 70:
            return "Encender aire acondicionado (Modo Deshumidificador)" #Reducir la humedad
        elif temperatura > 30:
            return "Encender ventilador"
        elif temperatura < 18:
            return "Encender calefacción"
        else:
            return "Mantener sistema apagado"

# 2. MONGODB ATLAS
class ClusterMongoDB:
    """Gestor de conexión y operaciones CRUD con MongoDB Atlas."""

    def __init__(
        self,
        db_name="Monica_Isidro",
        collection_name="Climatizacion"
    ):
        load_dotenv()

        self.uri = os.getenv("MONGO_ATLAS_URI")
        self.db_name = db_name
        self.collection_name = collection_name

    def _conectar(self):
        """Conecta con MongoDB Atlas y devuelve."""

        if not self.uri:
            raise ValueError(
                "No se encontró 'MONGO_ATLAS_URI' en el archivo .env"
            )

        cliente = MongoClient(self.uri)

        # Verificar conexión
        cliente.admin.command("ping")

        coleccion = cliente[self.db_name][self.collection_name]

        return cliente, coleccion

    # ==========================================
    # CREATE - CREAR
    # ==========================================
    def guardar_registro(
        self,
        temperatura: float,
        humedad: float,
        accion: str
    ) -> dict:
        """Inserta un nuevo registro."""

        cliente, coleccion = self._conectar()

        try:
            documento = {
                "temperatura": temperatura,
                "humedad": humedad,
                "accion": accion,
                "fecha_hora": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            resultado = coleccion.insert_one(documento)

            documento["_id"] = str(resultado.inserted_id)

            return documento

        finally:
            cliente.close()

    # ==========================================
    # READ - LEER
    # ==========================================
    def obtener_historial(self, limite=100):
        """Obtiene los registros de MongoDB."""

        cliente, coleccion = self._conectar()

        try:
            registros = list(
                coleccion.find()
                .sort("_id", -1)
                .limit(limite)
            )

            return registros

        finally:
            cliente.close()

    # ==========================================
    # READ - OBTENER UNO
    # ==========================================
    def obtener_registro(self, id_registro):
        """Obtiene un registro específico por su ID."""

        cliente, coleccion = self._conectar()

        try:
            registro = coleccion.find_one(
                {"_id": ObjectId(id_registro)}
            )

            return registro

        finally:
            cliente.close()

    # ==========================================
    # UPDATE - ACTUALIZAR
    # ==========================================
    def actualizar_registro(
        self,
        id_registro,
        temperatura: float,
        humedad: float,
        accion: str
    ):
        """Actualiza temperatura, humedad y acción."""

        cliente, coleccion = self._conectar()

        try:
            resultado = coleccion.update_one(
                {"_id": ObjectId(id_registro)},
                {
                    "$set": {
                        "temperatura": temperatura,
                        "humedad": humedad,
                        "accion": accion,
                        "fecha_hora": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    }
                }
            )

            return resultado.modified_count

        finally:
            cliente.close()

    # ==========================================
    # DELETE - ELIMINAR
    # ==========================================
    def eliminar_registro(self, id_registro):
        """Elimina un registro por su ID."""

        cliente, coleccion = self._conectar()

        try:
            resultado = coleccion.delete_one(
                {"_id": ObjectId(id_registro)}
            )

            return resultado.deleted_count

        finally:
            cliente.close()

# 3. INTERFAZ GRÁFICA
class ClimatizacionApp(tk.Tk):

    def __init__(
        self,
        agente: AgenteClimatizacion,
        cluster: ClusterMongoDB
    ):
        super().__init__()

        self.agente = agente
        self.cluster = cluster

        # ID del registro actualmente seleccionado
        self.id_seleccionado = None

        self.title(
            "Sistema de Climatización - MongoDB Atlas"
        )

        self.geometry("850x650")
        self.config(bg="lightblue") #Poner el color
        self.resizable(False, False)

        self._crear_componentes()
        self._cargar_historial_inicial()

    # ==========================================
    # CREAR INTERFAZ
    # ==========================================
    def _crear_componentes(self):

        # --------------------------------------
        # ENCABEZADO
        # --------------------------------------
        lbl_titulo = ttk.Label(
            self,
            text="Agente Climatizador",
            font=("Arial", 18, "bold")
        )

        lbl_titulo.pack(pady=10)

        # lbl_subtitulo = ttk.Label(
        #     self,
        #     text=(
        #         f"Base de Datos: {self.cluster.db_name} | "
        #         f"Colección: {self.cluster.collection_name}"
        #     ),
        #     font=("Arial", 9, "italic")
        # )

      #  lbl_subtitulo.pack(pady=2)

        # --------------------------------------
        # PANEL DE ENTRADAS
        # --------------------------------------
        frame_input = ttk.LabelFrame(
            self,
            text=" Percepciones del Entorno ",
            padding=15
        )

        frame_input.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            frame_input,
            text="Temperatura (°C):"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_temp = ttk.Entry(
            frame_input,
            width=15
        )

        self.entry_temp.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        ttk.Label(
            frame_input,
            text="Humedad (%):"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_hum = ttk.Entry(
            frame_input,
            width=15
        )

        self.entry_hum.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # --------------------------------------
        # BOTONES CRUD
        # --------------------------------------

        frame_botones = ttk.Frame(frame_input)

        frame_botones.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=20
        )

        self.btn_guardar = tk.Button(
            frame_botones,
            text="Guardar",
            bg="violet",
            fg="blue",
            command=self._crear_registro
        )

        self.btn_guardar.grid(
            row=0,
            column=0,
            padx=5,
            pady=3
        )

        self.btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar",
            bg="orange",
            command=self._actualizar_registro
        )

        self.btn_actualizar.grid(
            row=0,
            column=1,
            padx=5,
            pady=3
        )

        self.btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            bg="red",
            fg="white",
            command=self._eliminar_registro
        )

        self.btn_eliminar.grid(
            row=1,
            column=0,
            padx=5,
            pady=3
        )

        self.btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            bg="blue",
            fg="white",
            command=self._limpiar_campos
        )

        self.btn_limpiar.grid(
            row=1,
            column=1,
            padx=5,
            pady=3
        )

        # --------------------------------------
        # ACCIÓN DEL AGENTE
        # --------------------------------------
        frame_resultado = ttk.LabelFrame(
            self,
            text=" Acción Decidida ",
            padding=10
        )

        frame_resultado.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.lbl_accion = ttk.Label(
            frame_resultado,
            text="Esperando percepciones...",
            font=("Arial", 10, "bold")
        )

        self.lbl_accion.pack(
            anchor="w"
        )

        # --------------------------------------
        # HISTORIAL
        # --------------------------------------
        frame_tabla = ttk.LabelFrame(
            self,
            text=" Historial en MongoDB Atlas ",
            padding=10
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columnas = (
            "Fecha/Hora",
            "Temp",
            "Humedad",
            "Acción",
            "ID MongoDB"
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tabla.heading(
            "Fecha/Hora",
            text="Fecha/Hora"
        )

        self.tabla.heading(
            "Temp",
            text="Temp"
        )

        self.tabla.heading(
            "Humedad",
            text="Humedad"
        )

        self.tabla.heading(
            "Acción",
            text="Acción Realizada"
        )

        self.tabla.heading(
            "ID MongoDB",
            text="ID MongoDB"
        )

        self.tabla.column(
            "Fecha/Hora",
            width=130,
            anchor="center"
        )

        self.tabla.column(
            "Temp",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "Humedad",
            width=80,
            anchor="center"
        )

        self.tabla.column(
            "Acción",
            width=300,
            anchor="w"
        )

        self.tabla.column(
            "ID MongoDB",
            width=220,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscroll=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # --------------------------------------
        # EVENTO DE SELECCIÓN
        # --------------------------------------
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_registro
        )

    # ==========================================
    # CREATE (CREAR)
    # ==========================================
    def _crear_registro(self):

        try:
            temp = float(
                self.entry_temp.get().strip()
            )

            hum = float(
                self.entry_hum.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Dato inválido",
                "Ingresa números válidos en temperatura y humedad."
            )

            return

        # Validar rangos
        if not -100 <= temp <= 100:
            messagebox.showerror(
                "Temperatura inválida",
                "La temperatura debe estar entre -100 y 100 °C."
            )
            return

        if not 0 <= hum <= 100:
            messagebox.showerror(
                "Humedad inválida",
                "La humedad debe estar entre 0 y 100 %."
            )
            return

        # El agente toma la decisión
        accion = self.agente.tomar_decision(
            temp,
            hum
        )

        self.lbl_accion.config(
            text=f"Acción: {accion}"
        )

        try:

            doc = self.cluster.guardar_registro(
                temp,
                hum,
                accion
            )

            self.tabla.insert(
                "",
                0,
                values=(
                    doc["fecha_hora"],
                    f"{doc['temperatura']} °C",
                    f"{doc['humedad']} %",
                    doc["accion"],
                    doc["_id"]
                )
            )

            messagebox.showinfo(
                "Registro creado",
                "La lectura fue guardada correctamente."
            )

            self._limpiar_campos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No fue posible guardar el registro:\n\n{e}"
            )

    # ==========================================
    # READ (LEER)
    # ==========================================
    def _cargar_historial_inicial(self):

        try:

            registros = self.cluster.obtener_historial()

            for reg in registros:

                self.tabla.insert(
                    "",
                    tk.END,
                    values=(
                        reg.get(
                            "fecha_hora",
                            "N/A"
                        ),
                        f"{reg.get('temperatura', 0)} °C",
                        f"{reg.get('humedad', 0)} %",
                        reg.get(
                            "accion",
                            "N/A"
                        ),
                        str(
                            reg.get(
                                "_id",
                                ""
                            )
                        )
                    )
                )

        except Exception as e:

            messagebox.showwarning(
                "Advertencia",
                f"No fue posible cargar el historial:\n\n{e}"
            )

    # ==========================================
    # READ (SELECCIONAR)
    # ==========================================
    def _seleccionar_registro(self, event=None):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        item = self.tabla.item(
            seleccion[0]
        )

        valores = item["values"]

        if not valores:
            return

        # Guardar ID seleccionado
        self.id_seleccionado = str(
            valores[4]
        )

        # Mostrar datos en los campos
        temperatura = str(
            valores[1]
        ).replace(" °C", "")

        humedad = str(
            valores[2]
        ).replace(" %", "")

        self.entry_temp.delete(
            0,
            tk.END
        )

        self.entry_temp.insert(
            0,
            temperatura
        )

        self.entry_hum.delete(
            0,
            tk.END
        )

        self.entry_hum.insert(
            0,
            humedad
        )

        self.lbl_accion.config(
            text=f"Registro seleccionado: {self.id_seleccionado}"
        )

    # ==========================================
    # UPDATE (ACTUALIZAR)
    # ==========================================
    def _actualizar_registro(self):

        if not self.id_seleccionado:

            messagebox.showwarning(
                "Selecciona un registro",
                "Selecciona primero un registro de la tabla."
            )

            return

        try:

            temp = float(
                self.entry_temp.get().strip()
            )

            hum = float(
                self.entry_hum.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Dato inválido",
                "Ingresa números válidos."
            )

            return

        if not -100 <= temp <= 100:

            messagebox.showerror(
                "Temperatura inválida",
                "La temperatura debe estar entre -100 y 100 °C."
            )

            return

        if not 0 <= hum <= 100:

            messagebox.showerror(
                "Humedad inválida",
                "La humedad debe estar entre 0 y 100 %."
            )

            return

        # Recalcular la decisión del agente
        accion = self.agente.tomar_decision(
            temp,
            hum
        )

        try:

            modificados = self.cluster.actualizar_registro(
                self.id_seleccionado,
                temp,
                hum,
                accion
            )

            if modificados == 0:

                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró el registro o no hubo cambios."
                )

                return

            # Actualizar la fila visualmente
            seleccion = self.tabla.selection()

            self.tabla.item(
                seleccion[0],
                values=(
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    f"{temp} °C",
                    f"{hum} %",
                    accion,
                    self.id_seleccionado
                )
            )

            self.lbl_accion.config(
                text=f"Acción: {accion}"
            )

            messagebox.showinfo(
                "Registro actualizado",
                "El registro fue actualizado correctamente."
            )

            self._limpiar_campos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No fue posible actualizar el registro:\n\n{e}"
            )

    # ==========================================
    # DELETE (ELIMINAR)
    # ==========================================
    def _eliminar_registro(self):

        if not self.id_seleccionado:

            messagebox.showwarning(
                "Selecciona un registro",
                "Selecciona primero un registro de la tabla."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este registro?"
        )

        if not confirmar:
            return

        try:

            eliminados = self.cluster.eliminar_registro(
                self.id_seleccionado
            )

            if eliminados == 0:

                messagebox.showwarning(
                    "No encontrado",
                    "El registro no existe en MongoDB."
                )

                return

            # Eliminar de la tabla
            seleccion = self.tabla.selection()

            if seleccion:
                self.tabla.delete(
                    seleccion[0]
                )

            messagebox.showinfo(
                "Registro eliminado",
                "El registro fue eliminado correctamente."
            )

            self._limpiar_campos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No fue posible eliminar el registro:\n\n{e}"
            )

    # ==========================================
    # LIMPIAR CAMPOS
    # ==========================================
    def _limpiar_campos(self):

        self.entry_temp.delete(
            0,
            tk.END
        )

        self.entry_hum.delete(
            0,
            tk.END
        )

        self.id_seleccionado = None

        self.lbl_accion.config(
            text="Esperando percepciones..."
        )

        # Quitar selección
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

# 4. PUNTO DE ENTRADA
if __name__ == "__main__":

    agente = AgenteClimatizacion()

    cluster = ClusterMongoDB(
        db_name="Monica_Isidro",
        collection_name="Climatizacion"
    )

    app = ClimatizacionApp(
        agente,
        cluster
    )

    app.mainloop()