# app/utils/db.py - ACTUALIZAR CON ESTO
import mysql.connector
from ..config import Config

def get_db_connection():
    try:
        config = Config.DB_CONFIG.copy()
        # USAR SSL_DISABLED=True (como en prueba_final.py)
        config['ssl_disabled'] = True
        return mysql.connector.connect(**config)
    except Exception as e:
        print(f"Error DB: {e}")
        return None