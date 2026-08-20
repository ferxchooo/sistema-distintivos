import pandas as pd
from pymongo import MongoClient
import glob
import os

# Tu conexión a la nueva base de datos
MONGO_URI = "mongodb+srv://al222410839_db_user:fernando.123@cluster0.5x95bfb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["portal_distintivos"]
collection = db["registros"]

# Busca TODOS los archivos Excel en la carpeta
archivos_excel = glob.glob("*.xlsx")
total_subidos = 0

print(f"Se encontraron {len(archivos_excel)} archivos. Procesando...")

for archivo in archivos_excel:
    print(f"-> Leyendo: {archivo}")
    try:
        # Lee la hoja de DISTINTIVOS de cada Excel
        df = pd.read_excel(archivo, sheet_name="DISTINTIVOS")
        df.columns = df.columns.str.strip() # Limpia espacios en las columnas
        df = df.fillna("")
        
        registros = df.to_dict(orient="records")
        
        # Sube los datos usando el FOLIO para no duplicar
        for reg in registros:
            folio = str(reg.get("FOLIO", "")).strip()
            if folio: # Solo sube si tiene un folio válido
                collection.update_one(
                    {"FOLIO": folio},
                    {"$set": reg},
                    upsert=True # Crea nuevo si no existe, actualiza si ya existe
                )
                total_subidos += 1
    except Exception as e:
        print(f"No se pudo procesar {archivo} (Asegúrate de que tenga la hoja 'DISTINTIVOS').")

print(f"\n¡Éxito! Base de datos actualizada con {total_subidos} registros procesados.")