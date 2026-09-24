    #Que pueda seleccionar lo que quiera aparezca la grafica 

import os
from datetime import datetime

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Sistema de Climatización",
    
    layout="wide"
)


# ============================================================
# 1. MÓDULO DE LÓGICA DEL AGENTE
# ============================================================

class AgenteClimatizacion:
    """
    Agente reactivo que toma decisiones
    según temperatura y humedad.
    """

    def tomar_decision(
        self,
        temperatura: float,
        humedad: float
    ) -> str:

        if temperatura > 30 and humedad > 70:
            return "Encender aire acondicionado (Modo Deshumidificador)"

        elif temperatura > 30:
            return "Encender ventilador"

        elif temperatura < 18:
            return "Encender calefacción"

        else:
            return "Mantener sistema apagado"


# ============================================================
# 2. MONGODB ATLAS
# ============================================================

class ClusterMongoDB:
    """
    Gestor de conexión y operaciones CRUD
    con MongoDB Atlas.
    """

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

        if not self.uri:
            raise ValueError(
                "No se encontró 'MONGO_ATLAS_URI' "
                "en el archivo .env"
            )

        cliente = MongoClient(self.uri)

        # Verificar conexión
        cliente.admin.command("ping")

        coleccion = cliente[
            self.db_name
        ][
            self.collection_name
        ]

        return cliente, coleccion

    # ========================================================
    # CREATE
    # ========================================================

    def guardar_registro(
        self,
        temperatura: float,
        humedad: float,
        accion: str
    ) -> dict:

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

            resultado = coleccion.insert_one(
                documento
            )

            documento["_id"] = str(
                resultado.inserted_id
            )

            return documento

        finally:
            cliente.close()

    # ========================================================
    # READ
    # ========================================================

    def obtener_historial(self, limite=100):

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

    # ========================================================
    # READ - UNO
    # ========================================================

    def obtener_registro(self, id_registro):

        cliente, coleccion = self._conectar()

        try:

            registro = coleccion.find_one(
                {
                    "_id": ObjectId(id_registro)
                }
            )

            return registro

        finally:
            cliente.close()

    # ========================================================
    # UPDATE
    # ========================================================

    def actualizar_registro(
        self,
        id_registro,
        temperatura: float,
        humedad: float,
        accion: str
    ):

        cliente, coleccion = self._conectar()

        try:

            resultado = coleccion.update_one(

                {
                    "_id": ObjectId(id_registro)
                },

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

    # ========================================================
    # DELETE
    # ========================================================

    def eliminar_registro(self, id_registro):

        cliente, coleccion = self._conectar()

        try:

            resultado = coleccion.delete_one(
                {
                    "_id": ObjectId(id_registro)
                }
            )

            return resultado.deleted_count

        finally:
            cliente.close()


# ============================================================
# 3. CREAR OBJETOS
# ============================================================

agente = AgenteClimatizacion()

cluster = ClusterMongoDB(
    db_name="Monica_Isidro",
    collection_name="Climatizacion"
)


# ============================================================
# 4. TÍTULO
# ============================================================

st.title("Sistema Inteligente de Climatización")

st.write(
    "Sistema basado en un agente reactivo simple "
    "con almacenamiento de información en MongoDB Atlas."
)


# ============================================================
# 5. CONEXIÓN
# ============================================================

try:

    # Probamos la conexión
    cliente, coleccion = cluster._conectar()
    cliente.close()

    st.success(
        "Conexión con MongoDB Atlas establecida"
    )

except Exception as e:

    st.error(
        f" Error de conexión con MongoDB Atlas:\n\n{e}"
    )

    st.stop()


# ============================================================
# 6. ENTRADA DE DATOS
# ============================================================

st.header("Percepciones del entorno")

col1, col2 = st.columns(2)

with col1:

    temperatura = st.number_input(
        "Temperatura (°C)",
        min_value=-100.0,
        max_value=100.0,
        value=25.0,
        step=0.1
    )

with col2:

    humedad = st.number_input(
        "Humedad (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.1
    )


# ============================================================
# 7. DECISIÓN DEL AGENTE
# ============================================================

accion_agente = agente.tomar_decision(
    temperatura,
    humedad
)

st.subheader("Decisión del agente")

st.info(
    f"El agente recomienda: **{accion_agente}**"
)


# ============================================================
# 8. SELECCIÓN DEL USUARIO
# ============================================================

st.subheader("👤 Selección del usuario")

opciones_accion = [

    "Encender aire acondicionado (Modo Deshumidificador)",

    "Encender ventilador",

    "Encender calefacción",

    "Mantener sistema apagado"
]

accion_usuario = st.selectbox(
    "Selecciona la acción que deseas realizar:",
    opciones_accion
)


# ============================================================
# COMPARACIÓN
# ============================================================

if accion_usuario == accion_agente:

    st.success(
        "La acción seleccionada coincide con "
        "la recomendación del agente."
    )

else:

    st.warning(
        "La acción seleccionada es diferente "
        "a la recomendación del agente."
    )


# ============================================================
# 9. GUARDAR REGISTRO
# ============================================================

st.subheader("Guardar lectura")

if st.button(
    "Guardar registro",
    type="primary"
):

    try:

        documento = cluster.guardar_registro(
            temperatura,
            humedad,
            accion_usuario
        )

        st.success(
            "Registro guardado correctamente."
        )

        st.write(
            f"**ID:** {documento['_id']}"
        )

    except Exception as e:

        st.error(
            f"No fue posible guardar el registro:\n\n{e}"
        )


# ============================================================
# 10. HISTORIAL
# ============================================================

st.header("Historial de climatización")

try:

    registros = cluster.obtener_historial()

except Exception as e:

    st.error(
        f"No fue posible obtener los registros: {e}"
    )

    registros = []


if registros:

    datos_tabla = []

    for registro in registros:

        datos_tabla.append(
            {
                "ID": str(
                    registro.get("_id", "")
                ),

                "Fecha/Hora": registro.get(
                    "fecha_hora",
                    "N/A"
                ),

                "Temperatura (°C)": registro.get(
                    "temperatura",
                    0
                ),

                "Humedad (%)": registro.get(
                    "humedad",
                    0
                ),

                "Acción": registro.get(
                    "accion",
                    "N/A"
                )
            }
        )

    df = pd.DataFrame(datos_tabla)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No existen registros todavía."
    )


# ============================================================
# 11. SELECCIONAR REGISTRO
# ============================================================

st.header("Administrar registro")

if registros:

    ids = [
        str(registro["_id"])
        for registro in registros
    ]

    id_seleccionado = st.selectbox(
        "Selecciona un registro:",
        ids
    )

    registro_seleccionado = cluster.obtener_registro(
        id_seleccionado
    )

    if registro_seleccionado:

        temperatura_actual = registro_seleccionado.get(
            "temperatura",
            0
        )

        humedad_actual = registro_seleccionado.get(
            "humedad",
            0
        )

        accion_actual = registro_seleccionado.get(
            "accion",
            opciones_accion[0]
        )

        col1, col2 = st.columns(2)

        with col1:

            nueva_temperatura = st.number_input(
                "Nueva temperatura",
                min_value=-100.0,
                max_value=100.0,
                value=float(temperatura_actual),
                step=0.1,
                key="temp_update"
            )

        with col2:

            nueva_humedad = st.number_input(
                "Nueva humedad",
                min_value=0.0,
                max_value=100.0,
                value=float(humedad_actual),
                step=0.1,
                key="hum_update"
            )

        nueva_accion = st.selectbox(
            "Nueva acción:",
            opciones_accion,
            index=(
                opciones_accion.index(accion_actual)
                if accion_actual in opciones_accion
                else 0
            ),
            key="accion_update"
        )

        col_actualizar, col_eliminar = st.columns(2)

        # ====================================================
        # UPDATE
        # ====================================================

        with col_actualizar:

            if st.button(
                "Actualizar registro",
                use_container_width=True
            ):

                try:

                    modificados = (
                        cluster.actualizar_registro(
                            id_seleccionado,
                            nueva_temperatura,
                            nueva_humedad,
                            nueva_accion
                        )
                    )

                    if modificados > 0:

                        st.success(
                            "Registro actualizado correctamente."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "No hubo cambios en el registro."
                        )

                except Exception as e:

                    st.error(
                        f"Error al actualizar: {e}"
                    )

        # ====================================================
        # DELETE
        # ====================================================

        with col_eliminar:

            if st.button(
                "Eliminar registro",
                use_container_width=True
            ):

                try:

                    eliminados = (
                        cluster.eliminar_registro(
                            id_seleccionado
                        )
                    )

                    if eliminados > 0:

                        st.success(
                            "Registro eliminado correctamente."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "No se encontró el registro."
                        )

                except Exception as e:

                    st.error(
                        f"Error al eliminar: {e}"
                    )


# ============================================================
# 12. GRÁFICAS
# ============================================================

st.header("Gráficas de temperatura y humedad")


if registros:

    datos_grafica = []

    # MongoDB devuelve los más recientes primero.
    # Los invertimos para mostrar la evolución cronológica.

    registros_grafica = list(
        reversed(registros)
    )

    for registro in registros_grafica:

        datos_grafica.append(
            {
                "Fecha/Hora": registro.get(
                    "fecha_hora",
                    ""
                ),

                "Temperatura": registro.get(
                    "temperatura",
                    0
                ),

                "Humedad": registro.get(
                    "humedad",
                    0
                )
            }
        )

    df_grafica = pd.DataFrame(
        datos_grafica
    )

    # ========================================================
    # GRÁFICA DE TEMPERATURA
    # ========================================================

    st.subheader("Temperatura por registro")

    st.line_chart(
        df_grafica.set_index(
            "Fecha/Hora"
        )["Temperatura"]
    )


    # ========================================================
    # GRÁFICA DE HUMEDAD
    # ========================================================

    st.subheader("Humedad por registro")

    st.line_chart(
        df_grafica.set_index(
            "Fecha/Hora"
        )["Humedad"]
    )


    # ========================================================
    # GRÁFICA CONJUNTA
    # ========================================================

    st.subheader(
        "Temperatura y humedad"
    )

    st.line_chart(
        df_grafica.set_index(
            "Fecha/Hora"
        )[[
            "Temperatura",
            "Humedad"
        ]]
    )

else:

    st.info(
        "No hay datos suficientes para generar gráficas."
    )


# ============================================================
# 13. RESUMEN
# ============================================================

st.header("Resumen")

if registros:

    total_registros = len(registros)

    temperaturas = [
        registro.get("temperatura", 0)
        for registro in registros
    ]

    humedades = [
        registro.get("humedad", 0)
        for registro in registros
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total de registros",
            total_registros
        )

    with col2:

        st.metric(
            "Temperatura promedio",
            f"{sum(temperaturas) / len(temperaturas):.2f} °C"
        )

    with col3:

        st.metric(
            "Humedad promedio",
            f"{sum(humedades) / len(humedades):.2f} %"
        )