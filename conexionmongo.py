#practica Conexion local con MONGODB.    11/09/26

from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017")

db = cliente["practicas"]
alumnos = db["alumnos"]

# Insertar datos
datos = [
    {
        "nombre": "Madian",
        "edad": 21,
        "carrera": "Ingeniería"
    },
    {
        "nombre": "Ian",
        "edad": 22,
        "carrera": "Sismologia"
    },
    {
        "nombre": "Amanda",
        "edad": 20,
        "carrera": "Odontologia"
    }
]

resultado = alumnos.insert_many(datos)

print("Documentos insertados:", len(resultado.inserted_ids))

cliente.close()