
# ============================================
# SISTEMA EXPERTO DE DIAGNÓSTICO
# usuario = paciente
# ============================================

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


print("SISTEMA DE DIAGNÓSTICO")

print("------------------------------------------------------------")
print("Datos de usuario")

nombre = input(" Ingresa tu nombre: ").lower()
direccion = input(" Ingresa tu direccion: ").lower()
edad = input("Ingresa tu edad: ")
tipo_sangre = input("Ingresa tu tipo de sangre: ")
genero = input("Ingresa tu genero: ") 


print("------------------------------------------------------------")

#variables

seguro = input('Usted cuenta con seguro (s/n): ') == 's'
fiebre = input("¿Tiene fiebre? (s/n): ") == 's'
tos = input("¿Tiene tos? (s/n): ") == 's'
dolor = input("¿Tiene dolor de garganta? (s/n): ") == 's'
vomito = input("¿Tiene vómito? (s/n): ") == 's'
sangrado_nasal = input("¿Tiene sangrado nasal? (s/n): ") == 's' 
dolor_estomago = input("¿Tiene dolor de estómago? (s/n): ") == 's'
dolor_cabeza = input("¿Tiene dolor de cabeza? (s/n): ") == 's'
alergias = input("¿Tiene alergias? (s/n): ") == 's'
diarrea = input("¿Tiene diarrea? (s/n): ") == 's'
estornudos = input("¿Tiene estornudos? (s/n): ") == 's'

#########################

##################33

if seguro == 's':
    print("Usted cuenta con seguro, por lo que puede acudir a un centro de salud para una evaluación más precisa.")

else: 
    print("Usted no cuenta con seguro, por lo que se recomienda buscar atención médica en caso de que los síntomas persistan o empeoren.")



###########################3menus
if fiebre == "s" and tos == "s":

    diagnostico = "Posible infección respiratoria"

elif tos == "s" and dolor == "s":

    diagnostico = "Posible irritación respiratoria"

elif fiebre == "s" and sangrado_nasal == 's':

    diagnostico = "Se recomienda valoración profesional"

elif dolor_estomago == 's' or diarrea:
    diagnostico = 'Posiblemente un alimento que ingerio estaba pasado '

elif dolor_cabeza == "s" and estornudos == "s" and fiebre == 's'
    diagnostico = 'Posible resfriado por cambio de clima'

else:

    diagnostico = "No se identificó un diagnostico acertado"






print("\nResultado:")
print(fecha)
print(hora)
print(nombre)

print("--------------------------------------------------------------")
print(diagnostico)
print(seguro)


#Implementación de mejores decisiones para un mejor resultado.