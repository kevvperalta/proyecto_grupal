# prueba_final.py
import mysql.connector

print("🔍 Probando conexión a Railway...")

# INTENTO 1: Sin SSL
print("\n1. Probando SIN SSL...")
config_no_ssl = {
    'host': 'mainline.proxy.rlwy.net',
    'user': 'root',
    'password': 'AOXQANSeJeMBwCDcjIiEoUATkeWNhCOV',
    'database': 'railway',
    'port': 52017,
    'ssl_disabled': True
}

try:
    conn = mysql.connector.connect(**config_no_ssl)
    cursor = conn.cursor()
    cursor.execute("SELECT '✅ CONEXIÓN SIN SSL EXITOSA' as mensaje")
    print(cursor.fetchone()[0])
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error sin SSL: {e}")
    
    # INTENTO 2: Con SSL
    print("\n2. Probando CON SSL...")
    config_ssl = config_no_ssl.copy()
    config_ssl['ssl_disabled'] = False
    
    try:
        conn = mysql.connector.connect(**config_ssl)
        cursor = conn.cursor()
        cursor.execute("SELECT '✅ CONEXIÓN CON SSL EXITOSA' as mensaje")
        print(cursor.fetchone()[0])
        cursor.close()
        conn.close()
    except Exception as e2:
        print(f"❌ Error con SSL: {e2}")