#temperatura y humedad guradar en el cluster tk

class AgenteClimatizacion: #separa las percepciones, la logica de decision y la ejecución en metodos limpios.
def __init__(self):
    self.temperatura = 0.0
    self.humedad = 0.0
    self.accion = ""
def percibir(self):
    """Captura los datos del entorno con validación de entradas."""
    self.temperatura = self._leer_float("Temperatura actual (°C): ")
    self.humedad = self._leer_float("Humedad actual (%): ")
def tomar_decision(self):
    """Aplica la regla condición-acción basada en la percepción."""
    if self.temperatura > 30 and self.humedad > 70:
        self.accion = "Encender aire acondicionado (Modo Deshumidificador)"
    elif self.temperatura > 30:
        self.accion = "Encender ventilador"
    elif self.temperatura < 18:
        self.accion = "Encender calefacción"
    else:
        self.accion = "Mantener sistema apagado"
def mostrar_resultado(self):
"""Muestra el estado del agente y la acción a realizar."""
print("
--- RESUMEN DEL AGENTE ---")
print(f"Percepción -> Temp: {self.temperatura}°C | Humedad: {self.humedad}%")
print(f"Acción -> {self.accion}")
def _leer_float(self, mensaje):
"""Método auxiliar para evitar que el programa truque si se ingresa texto."""
while True:
try:
return float(input(mensaje))
except ValueError:
print("Error: Por favor, ingresa un número válido.")
--- EJECUCIÓN DEL AGENTE ---
if __name__ == "__main__":
agente = AgenteClimatizacion()
agente.percibir()
agente.tomar_decision()
agente.mostrar_resultado()


#Abstracción: Se modeló el agente como un Agente Reactivo Simple usando una clase (AgenteClimatizacion),
#reflejando mejor el concepto teórico de la práctica.
#Validación de entradas: El método _leer_float evita que el programa se cierre si el usuario escribe
#caracteres no numéricos.
#Escalabilidad: Si en el futuro necesitas agregar más sensores (como calidad de aire o luz),
#solo debes extender el método percibir() y agregar condiciones en tomar_decision().