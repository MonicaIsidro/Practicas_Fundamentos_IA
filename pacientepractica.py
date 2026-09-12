3#ractica/tarea 11/09/2026
import random
from datetime import datetime

#Numero de reporte
numero = random.randint(1, 100)

#identificador
numero_Reporte = "R" + str(numero)

#fecha y hora
fecha_hora = datetime.now()

#formato para leer
fecha = fecha_hora.strftime("%d/%m/%Y %H:%M:%S") # el formato puede cambiar todo depende de como se pida
hora = fecha_hora.strftime("%H:%M")

# ==========================================================
# SISTEMA DE ORIENTACIÓN MEDICA
# ==========================================================

print("=" * 60)
print("        SISTEMA DE ORIENTACIÓN MMEDICA")
print("=" * 60)

print("\nBienvenido.")
#print("Este sistema realizará algunas preguntas sobre tus síntomas.")
print("La información proporcionada sirve únicamente como orientación")
print("y no sustituye una valoración médica profesional.\n")


# ----------------------------------------------------------
# 1. DATOS DEL PACIENTE
# ----------------------------------------------------------

nombre = input("Nombre del paciente: ").lower()
edad = int(input("Edad: "))


# ----------------------------------------------------------
# 2. PREGUNTAS INICIALES
# ----------------------------------------------------------

print("\n--- SÍNTOMAS PRINCIPALES ---")

fiebre = input("¿Tiene fiebre? (s/n): ").lower()
tos = input("¿Tiene tos? (s/n): ").lower()
dolor_garganta = input("¿Tiene dolor de garganta? (s/n): ").lower()
dolor_cabeza = input("¿Tiene dolor de cabeza? (s/n): ").lower()
cuerpo = input("¿Tiene dolor muscular o corporal? (s/n): ").lower()
congestion = input("¿Tiene congestión nasal? (s/n): ").lower()


# ----------------------------------------------------------
# 3. PREGUNTAS ADICIONALES
# ----------------------------------------------------------

print("\n--- PREGUNTAS ADICIONALES ---")

dificultad_respirar = input(
    "¿Tiene dificultad para respirar? (s/n): "
).lower()

duracion = int(input(
    "¿Cuántos días lleva con los síntomas?: "
))


# ----------------------------------------------------------
# 4. SISTEMA DE DECISIONES
# ----------------------------------------------------------

diagnostico = ""
recomendacion = ""
nivel = ""


# Situación que requiere mayor atención
if dificultad_respirar == "s":

    diagnostico = "Señales que requieren valoración profesional"
    nivel = "ALTA"
    recomendacion = (
        "Se recomienda buscar atención médica lo antes posible. "
        "Si la dificultad para respirar es intensa o empeora, "
        "debe buscar atención de urgencia."
    )


# Posible cuadro respiratorio
elif fiebre == "s" and tos == "s" and dolor_garganta == "s":

    diagnostico = "Posible infección respiratoria"
    nivel = "MEDIA"
    recomendacion = (
        "Se recomienda descansar, mantenerse hidratado y vigilar "
        "la evolución de los síntomas. Si los síntomas empeoran "
        "o persisten, se recomienda valoración profesional."
    )


# Posible cuadro gripal
elif fiebre == "s" and dolor_cabeza == "s" and cuerpo == "s":

    diagnostico = "Posible cuadro similar a gripe"
    nivel = "MEDIA"
    recomendacion = (
        "Se recomienda descanso, hidratación y vigilancia de los "
        "síntomas. Si existe empeoramiento o fiebre persistente, "
        "se recomienda acudir con un profesional de la salud."
    )


# Irritación o infección de garganta
elif tos == "s" and dolor_garganta == "s":

    diagnostico = "Posible irritación o infección de garganta"
    nivel = "BAJA"
    recomendacion = (
        "Se recomienda mantenerse hidratado, descansar y evitar "
        "factores que puedan irritar la garganta. Si los síntomas "
        "persisten o empeoran, se recomienda valoración profesional."
    )


# Posible resfriado
elif congestion == "s" and tos == "s":

    diagnostico = "Posible cuadro de resfriado"
    nivel = "BAJA"
    recomendacion = (
        "Se recomienda descanso, buena hidratación y vigilancia "
        "de los síntomas."
    )


# Fiebre sin otros patrones
elif fiebre == "s":

    diagnostico = "Presencia de fiebre sin un patrón definido"
    nivel = "MEDIA"
    recomendacion = (
        "Se recomienda vigilar la temperatura, mantenerse hidratado "
        "y considerar una valoración profesional para determinar "
        "la causa de la fiebre."
    )


# Sin patrón identificado
else:

    diagnostico = "No se identificó un patrón específico"
    nivel = "BAJA"
    recomendacion = (
        "Se recomienda continuar observando los síntomas. "
        "Si aparecen nuevos síntomas o existe empeoramiento, "
        "se recomienda consultar a un profesional."
    )


# ----------------------------------------------------------
# 5. REPORTE FINAL
# ----------------------------------------------------------

print("\n")
print("=" * 60)
print("                  REPORTE DEL PACIENTE")
print("=" * 60)

print("Fecha: ", fecha)
print("Hora: ", hora)
print("=" * 60)

print(f"\nNombre del paciente: {nombre}")
print(f"Edad: {edad} años")
print(f"Días con síntomas: {duracion}")

print("\n--- SÍNTOMAS REGISTRADOS ---")

print(f"Fiebre: {'Sí' if fiebre == 's' else 'No'}")
print(f"Tos: {'Sí' if tos == 's' else 'No'}")
print(f"Dolor de garganta: {'Sí' if dolor_garganta == 's' else 'No'}")
print(f"Dolor de cabeza: {'Sí' if dolor_cabeza == 's' else 'No'}")
print(f"Dolor corporal: {'Sí' if cuerpo == 's' else 'No'}")
print(f"Congestión nasal: {'Sí' if congestion == 's' else 'No'}")
print(f"Dificultad para respirar: {'Sí' if dificultad_respirar == 's' else 'No'}")

print("\n--- RESULTADO ---")

print(f"Orientación: {diagnostico}")
print(f"Nivel de atención: {nivel}")

print("\n--- RECOMENDACIÓN ---")

print(recomendacion)

