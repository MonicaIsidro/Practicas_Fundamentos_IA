import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def main():
    print("Conectando hacia MongoDB Atlas...")

    uri = os.getenv("MONGO_ATLAS_URI")

    try:
        # Conectarse al cluster de Atlas
        cliente = MongoClient(uri)

        cliente.admin.command("ping")
        print("¡Hay conexión a MongoDB Atlas!")
        
        # base de datos y la colección
        db = cliente["Monica_Isidro"]
        coleccion = db["Libro"]
        
        # Insertar dato sencillo
        dato = {
            "mensaje": "Colores"
        }
        
        resultado = coleccion.insert_one(dato)
        
        print("¡Conexión correcta a MongoDB Atlas!")
        print(f"Dato insertado con id: {resultado.inserted_id}")
        
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    main()


####################################333333

