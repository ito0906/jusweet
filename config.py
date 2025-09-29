import os
import psycopg2

def conectar():
    try:
        db_url = os.getenv("DATABASE_URL")  # Render la pone como variable
        conexion = psycopg2.connect(db_url)
        print("✅ Conexión a PostgreSQL establecida")
        return conexion
    except Exception as error:
        print("❌ Error al conectar a PostgreSQL:", error)
        return None

def desconectar(conexion):
    if conexion is not None:
        conexion.close()

