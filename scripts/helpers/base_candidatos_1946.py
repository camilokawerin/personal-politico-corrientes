# -*- coding: utf-8 -*-
"""
Módulo principal para la generación del informe de candidatos peronistas de 1946.
Este módulo coordina la generación del informe, importando las funcionalidades
específicas de los módulos auxiliares.
"""
import os
import sys

# Fix path to properly import modules regardless of how the script is run
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(module_path)
sys.path.insert(0, project_root)

from scripts.commons.data_retrieval import (
    obtener_candidatos_1946,
    obtener_trayectoria,
    obtener_detalle_trayectoria_candidatos_peronistas
)
from scripts.helpers.analisis_candidatos_1946 import procesar_datos_candidatos
from scripts.helpers.html_candidatos_1946 import generar_informe_html_candidatos_1946
from scripts.helpers.tablas_candidatos_1946 import generar_tabla_candidatos

def generar_informe_candidatos_1946():
    """
    Función principal que coordina la generación del informe de candidatos
    peronistas de 1946.
    
    Returns:
        bool: True si el informe se generó correctamente, False en caso contrario
    """
    print("Generando informe de candidatos peronistas de 1946...")
    
    # Obtener datos de candidatos
    print("1. Obteniendo candidatos peronistas de 1946...")
    candidatos = obtener_candidatos_1946()
    candidatos_con_experiencia = obtener_detalle_trayectoria_candidatos_peronistas()
    
    if not candidatos:
        print("No se encontraron candidatos peronistas de 1946 para analizar.")
        return False
    
    print(f"✓ Se encontraron {len(candidatos)} candidatos en 1946.")
    
    # Procesar datos de cada candidato
    print("2. Procesando datos de candidatos...")
    candidatos_data = procesar_datos_candidatos(candidatos, candidatos_con_experiencia, obtener_trayectoria)
    
    # Generar informe HTML
    print("3. Generando informe HTML...")
    html_content = generar_informe_html_candidatos_1946(candidatos_data)
    
    # Guardar informe HTML
    print("4. Guardando informe...")
    informe_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "informes")
    if not os.path.exists(informe_dir):
        os.makedirs(informe_dir)
    
    informe_path = os.path.join(informe_dir, "candidatos_1946_trayectorias.html")
    with open(informe_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print(f"✓ Informe de candidatos de 1946 generado exitosamente en: {informe_path}")
    return True

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_candidatos_1946()
