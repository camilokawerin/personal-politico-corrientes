# -*- coding: utf-8 -*-
"""
Generador de informes sobre candidatos peronistas de 1946.
Este módulo se encarga de generar informes específicos sobre los candidatos
de los partidos peronistas (Laborista Correntino y Radical Junta Reorganizadora)
en las elecciones de 1946.
"""
import os
import sys

# Fix path to properly import modules regardless of how the script is run
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(module_path)
sys.path.insert(0, project_root)

# Importar la función principal del módulo base
from scripts.helpers.base_candidatos_1946 import generar_informe_candidatos_1946

# Para conservar la compatibilidad con versiones anteriores del código
from scripts.helpers.html_candidatos_1946 import generar_informe_html_candidatos_1946, generar_seccion_cargo
from scripts.helpers.tablas_candidatos_1946 import generar_tabla_candidatos
from scripts.helpers.utilidades_candidatos_1946 import categorizar_partido

# El código principal ahora se encuentra distribuido en los siguientes módulos:
# - base_candidatos_1946.py: Función principal y coordinación
# - analisis_candidatos_1946.py: Funciones de análisis de datos
# - html_candidatos_1946.py: Generación de HTML del informe
# - tablas_candidatos_1946.py: Generación de tablas de candidatos
# - utilidades_candidatos_1946.py: Funciones auxiliares

# El código principal ahora se encuentra distribuido en los siguientes módulos:
# - base_candidatos_1946.py: Función principal y coordinación
# - analisis_candidatos_1946.py: Funciones de análisis de datos
# - html_candidatos_1946.py: Generación de HTML del informe
# - tablas_candidatos_1946.py: Generación de tablas de candidatos
# - utilidades_candidatos_1946.py: Funciones auxiliares

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_candidatos_1946()