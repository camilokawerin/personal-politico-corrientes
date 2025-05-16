"""
Script principal para generar todos los informes estadísticos.
Este script integra los diferentes módulos de generación de informes
y ejecuta la generación de cada informe de forma secuencial.
"""
import os
import sys
from datetime import datetime

# Añadir el directorio raíz del proyecto al path de Python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Importar los módulos de informes
from scripts.modules import informe_trayectorias_interpartidarias
from scripts.modules import informe_trayectorias_completas
from scripts.modules import informe_candidatos_1946
from scripts.modules import informe_candidatos_peronistas
from scripts.modules import visualizacion_trayectorias_interactivas
from scripts.commons.html_utils import generar_pagina_index

def imprimir_separador(mensaje):
    """Imprime un mensaje destacado en la consola"""
    ancho = 80
    print("\n" + "=" * ancho)
    print(mensaje.center(ancho))
    print("=" * ancho + "\n")

def main():
    """Función principal que ejecuta la generación de todos los informes"""
    inicio = datetime.now()
    
    print("Iniciando generación de informes estadísticos...")
    print(f"Fecha y hora: {inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Crear directorio de informes si no existe
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
      # Lista para registrar los informes generados
    informes_generados = []
      # 1. Generar informe de trayectorias completas de legisladores
    imprimir_separador("GENERANDO INFORME: TRAYECTORIAS COMPLETAS DE LEGISLADORES")
    
    try:
        if informe_trayectorias_completas.generar_informe_trayectorias_completas():
            # El mensaje de éxito ya está en la función generadora
            informes_generados.append("Trayectorias Completas de Legisladores")
        else:
            print("✗ Error al generar el informe de trayectorias completas")
    except Exception as e:
        print(f"✗ Error en la generación del informe de trayectorias completas: {e}")
    
    # 2. Generar informe de trayectorias interpartidarias
    imprimir_separador("GENERANDO INFORME: TRAYECTORIAS INTERPARTIDARIAS")
    
    try:
        if informe_trayectorias_interpartidarias.generar_informe_trayectorias_interpartidarias():
            # El mensaje de éxito ya está en la función generadora
            informes_generados.append("Trayectorias Interpartidarias")
        else:
            print("✗ Error al generar el informe de trayectorias interpartidarias")
    except Exception as e:
        print(f"✗ Error en la generación del informe de trayectorias interpartidarias: {e}")
    
    # 3. Generar informe de todos los candidatos peronistas
    imprimir_separador("GENERANDO INFORME: TODOS LOS CANDIDATOS PERONISTAS")
    
    try:
        if informe_candidatos_peronistas.generar_informe_candidatos_peronistas():
            # El mensaje de éxito ya está en la función generadora
            informes_generados.append("Todos los Candidatos Peronistas")
        else:
            print("✗ Error al generar el informe de todos los candidatos peronistas")
    except Exception as e:
        print(f"✗ Error en la generación del informe de todos los candidatos peronistas: {e}")
    
    # 4. Generar informe de candidatos de 1946
    imprimir_separador("GENERANDO INFORME: CANDIDATOS PERONISTAS DE 1946")
    
    try:
        if informe_candidatos_1946.generar_informe_candidatos_1946():
            # El mensaje de éxito ya está en la función generadora
            informes_generados.append("Candidatos Peronistas de 1946")
        else:
            print("✗ Error al generar el informe de candidatos de 1946")
    except Exception as e:
        print(f"✗ Error en la generación del informe de candidatos de 1946: {e}")
      # 5. Generar visualización interactiva de trayectorias
    imprimir_separador("GENERANDO VISUALIZACIÓN INTERACTIVA DE TRAYECTORIAS")
    
    try:
        if visualizacion_trayectorias_interactivas.generar_visualizacion_interactiva():
            # El mensaje de éxito ya está en la función generadora
            informes_generados.append("Visualización Interactiva de Trayectorias")
        else:
            print("✗ Error al generar la visualización interactiva de trayectorias")
    except Exception as e:
        print(f"✗ Error en la generación de la visualización interactiva de trayectorias: {e}")
    
    # 6. Generar la página de índice
    imprimir_separador("GENERANDO PÁGINA DE ÍNDICE")
    
    try:
        index_path = generar_pagina_index()
    except Exception as e:
        print(f"✗ Error al generar la página de índice: {e}")    # Mostrar resumen final
    fin = datetime.now()
    duracion = fin - inicio
    
    imprimir_separador("RESUMEN DE EJECUCIÓN")
    print(f"Hora de inicio: {inicio.strftime('%H:%M:%S')}")
    print(f"Hora de finalización: {fin.strftime('%H:%M:%S')}")
    print(f"Duración total: {duracion.total_seconds():.2f} segundos")
    print(f"\nInformes generados correctamente: {len(informes_generados)} de 5")
    
    for informe in informes_generados:
        print(f"  - {informe}")
    
    print("\nLos informes se han generado en el directorio:")
    print(output_dir)
    print("\nPuede acceder a todos los informes desde la página index.html")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEjecución interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError general en la ejecución: {e}")
        sys.exit(2)
