import os
import psycopg2

def conectar():
    try:
        # Railway pone la URL de la DB como variable de entorno DATABASE_URL
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            # Si no existe, usamos tu local (cambia tus datos locales aquí)
            db_url = "postgresql://postgres:tu_clave@localhost:5432/jusweet"
        conexion = psycopg2.connect(db_url)
        print("✅ Conexión a PostgreSQL establecida")
        return conexion
    except Exception as error:
        print("❌ Error al conectar a PostgreSQL:", error)
        return None

def desconectar(conexion):
    if conexion is not None:
        conexion.close()

