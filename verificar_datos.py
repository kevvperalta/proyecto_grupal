# verificar_datos.py
import mysql.connector

print("📊 VERIFICANDO DATOS EN LA BASE DE DATOS")
print("="*50)

config = {
    'host': 'mainline.proxy.rlwy.net',
    'user': 'root',
    'password': 'AOXQANSeJeMBwCDcjIiEoUATkeWNhCOV',
    'database': 'railway',
    'port': 52017,
    'ssl_disabled': True
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    
    # 1. Verificar tablas
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    print("\n📋 TABLAS EN LA BASE DE DATOS:")
    for tabla in tablas:
        print(f"   • {list(tabla.values())[0]}")
    
    # 2. Contar libros
    cursor.execute("SELECT COUNT(*) as total FROM Libros")
    total_libros = cursor.fetchone()['total']
    print(f"\n📚 TOTAL DE LIBROS: {total_libros}")
    
    # 3. Mostrar algunos libros
    cursor.execute("SELECT id_libro, titulo, autor, precio FROM Libros LIMIT 5")
    libros = cursor.fetchall()
    
    print("\n📖 MUESTRA DE LIBROS:")
    for libro in libros:
        print(f"   {libro['id_libro']}. {libro['titulo']}")
        print(f"      Autor: {libro['autor']}")
        print(f"      Precio: S/ {libro['precio']}")
        print()
    
    # 4. Verificar estructura de tablas
    print("\n🔍 ESTRUCTURA DE TABLA 'Libros':")
    cursor.execute("DESCRIBE Libros")
    columnas = cursor.fetchall()
    for col in columnas:
        print(f"   {col['Field']} ({col['Type']})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")