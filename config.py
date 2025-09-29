import os
import psycopg2

def conectar():
    """
    Conecta a la base de datos PostgreSQL usando la variable de entorno DATABASE_URL.
    Funciona tanto en Railway como en tu máquina local si defines la variable.
    """
    try:
        # Obtener la URL de la base de datos desde la variable de entorno
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError(
                "❌ La variable de entorno DATABASE_URL no está definida. "
                "En local, define la variable antes de correr la app:\n"
                "set DATABASE_URL=postgresql://usuario:password@host:puerto/base"
            )

        # Conectar a PostgreSQL
        conexion = psycopg2.connect(db_url)
        print("✅ Conexión a PostgreSQL establecida")
        return conexion

    except Exception as error:
        print("❌ Error al conectar a PostgreSQL:", error)
        # Detener la ejecución para evitar errores posteriores
        raise

def desconectar(conexion):
    """
    Cierra la conexión a la base de datos si está abierta.
    """
    if conexion is not None:
        conexion.close()
        print("🔒 Conexión cerrada")

