"""
Generador de informes sobre todos los candidatos peronistas entre 1946 y 1955.
Este módulo se encarga de generar informes y estadísticas sobre todos los 
candidatos que participaron en elecciones por partidos peronistas.
"""
import os
import sys
from datetime import datetime
# Add the project root to sys.path
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.dirname(module_path)
sys.path.insert(0, project_root)

from scripts.commons.db_utils import ejecutar_consulta
from scripts.commons.data_retrieval import (
    obtener_todos_candidatos_peronistas,
    obtener_trayectoria,
    obtener_detalle_trayectoria_candidatos_peronistas,
    obtener_estadisticas_partidos_previos_candidatos
)
from scripts.commons.visualization import (
    generar_grafico_partidos_previos,
    generar_grafico_periodos_temporales,
    analizar_periodos_temporales
)
from scripts.commons.html_utils import formato_decimal

# Importar los módulos helpers creados
from scripts.helpers.categorias_candidatos_peronistas import categorizar_partido
from scripts.helpers.html_candidatos_peronistas import (
    generar_informe_html_candidatos_peronistas,
    generar_tabla_candidatos
)
from scripts.helpers.estadisticas_candidatos_peronistas import (
    calcular_estadisticas_partido_previo_por_tipo_cargo
)

def generar_informe_candidatos_peronistas():
    """Genera el informe completo de candidatos peronistas entre 1946 y 1955"""
    print("Generando informe de candidatos peronistas entre 1946 y 1955...")
    
    # Obtener todos los candidatos peronistas
    print("1. Obteniendo candidatos peronistas (1946-1955)...")
    candidatos = obtener_todos_candidatos_peronistas()
    
    if not candidatos:
        print("No se encontraron candidatos peronistas para analizar.")
        return False
    
    print(f"✓ Se encontraron {len(candidatos)} candidatos peronistas.")
    
    # Procesar datos de cada candidato
    print("2. Procesando datos de candidatos...")
    candidatos_data = []
    
    for candidato in candidatos:
        id_persona = candidato['ID_Persona']
        nombre_completo = candidato['Nombre_Completo']
        partido = candidato['Partido']
        primer_anno = candidato['Primer_Anno_Peronista']
        
        # Obtener trayectoria completa
        trayectoria = obtener_trayectoria(id_persona)
        
        # Determinar si tiene experiencia política previa
        tiene_experiencia_previa = False
        partidos_previos = []
        
        # Determinar el cargo peronista principal
        cargo_peronista = None
        ambito_peronista = None
        
        for registro in trayectoria:
            # Buscar el cargo correspondiente a su primera candidatura peronista
            if registro['Año'] == primer_anno and registro['Partido'] in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']:
                cargo_text = registro.get('Cargo', '')
                if ' ' in cargo_text:
                    cargo_parts = cargo_text.split(' ')
                    cargo_peronista = cargo_parts[0]
                    ambito_peronista = cargo_parts[1] if len(cargo_parts) > 1 else ''
            
            # Buscar experiencia previa
            if registro['Año'] < primer_anno and registro['Partido'] not in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']:
                tiene_experiencia_previa = True
                if registro['Partido'] not in partidos_previos:
                    partidos_previos.append(registro['Partido'])
        
        candidato_info = {
            'id_persona': id_persona,
            'nombre_completo': nombre_completo,
            'partido': partido,
            'primer_anno': primer_anno,
            'cargo_peronista': cargo_peronista,
            'ambito_peronista': ambito_peronista,
            'tiene_experiencia_previa': tiene_experiencia_previa,
            'partidos_previos': ", ".join(partidos_previos),
            'trayectoria': trayectoria
        }
        
        candidatos_data.append(candidato_info)
    
    # Obtener detalles de trayectorias previas y estadísticas de partidos
    detalle_trayectorias = obtener_detalle_trayectoria_candidatos_peronistas()
    datos_partidos_previos = obtener_estadisticas_partidos_previos_candidatos()
    
    # Generar gráficos para el informe
    print("3. Generando gráficos para el informe...")
    ruta_grafico_partidos = generar_grafico_partidos_previos(datos_partidos_previos, "todos_candidatos_")
    
    # Analizar periodos temporales
    periodos = analizar_periodos_temporales(detalle_trayectorias)
    ruta_grafico_periodos = generar_grafico_periodos_temporales(periodos, "candidatos_")
    
    # Generar informe HTML
    print("4. Generando informe HTML...")
    html_content = generar_informe_html_candidatos_peronistas(
        candidatos_data,
        datos_partidos_previos,
        detalle_trayectorias,
        ruta_grafico_partidos,
        ruta_grafico_periodos
    )
    
    # Guardar informe HTML con codificación UTF-8
    print("5. Guardando informe...")
    output_path = r"c:\Users\camil\Code\personal-politico-corrientes\informes\todos_candidatos_peronistas.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Añadir metadatos de codificación al inicio del HTML si no existen
    if "<meta charset=" not in html_content:
        html_content = html_content.replace("<!DOCTYPE html>", 
                                         "<!DOCTYPE html>\n<!-- Generado con codificación UTF-8 -->")
        html_content = html_content.replace("<head>", 
                                         "<head>\n    <meta charset=\"UTF-8\">\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">")
    
    # Guardar con codificación UTF-8 explícita
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Informe de candidatos peronistas generado exitosamente en: {output_path}")
    return True

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_candidatos_peronistas()
