"""
Database utilities for connecting to MySQL and executing queries.
"""
import mysql.connector

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'personal-politico-corrientes'
}

def ejecutar_consulta(query):
    """Ejecuta una consulta SQL y devuelve los resultados"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except Exception as e:
        print(f"ERROR al ejecutar la consulta: {e}")
        print(f"Query: {query[:500]}...")
        return []
