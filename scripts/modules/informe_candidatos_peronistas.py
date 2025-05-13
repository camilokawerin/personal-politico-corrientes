"""
Generador de informes sobre todos los candidatos peronistas entre 1946 y 1955.
Este módulo se encarga de generar informes y estadísticas sobre todos los 
candidatos que participaron en elecciones por partidos peronistas.
"""
import os
import sys
from datetime import datetime
from collections import Counter, defaultdict
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
from scripts.commons.html_utils import generar_encabezado_html, generar_pie_html

def generar_informe_html_candidatos_peronistas(candidatos_data, datos_partidos_previos, detalle_trayectorias, ruta_grafico_partidos=None, ruta_grafico_periodos=None):
    """Genera un informe HTML con los datos de todos los candidatos peronistas entre 1946 y 1955"""
    # Calcular estadísticas para el resumen
    total_candidatos = len(candidatos_data)
    candidatos_con_experiencia = [c for c in candidatos_data if c.get('tiene_experiencia_previa', False)]
    total_con_experiencia = len(candidatos_con_experiencia)
    porcentaje_con_experiencia = (total_con_experiencia / total_candidatos) * 100 if total_candidatos > 0 else 0
    
    # Calcular promedio de candidaturas previas
    promedio_candidaturas = 0
    antiguedad_promedio = 0
    if detalle_trayectorias:
        suma_candidaturas = sum(item['Cantidad_Candidaturas_Previas'] for item in detalle_trayectorias)
        promedio_candidaturas = suma_candidaturas / len(detalle_trayectorias)
        
        # Calcular antigüedad promedio (años entre primera candidatura y entrada al peronismo)
        suma_antiguedad = sum(item['Anno_Peronista'] - item['Anno_Primera_Candidatura'] for item in detalle_trayectorias)
        antiguedad_promedio = suma_antiguedad / len(detalle_trayectorias)
    
    # Analizar periodos históricos
    periodos = {
        "1900-1915": 0,
        "1916-1930": 0,
        "1931-1942": 0,
        "1943-1945": 0
    }
    
    if detalle_trayectorias:
        # Usamos un conjunto para rastrear IDs de persona ya contadas en cada período
        personas_contadas = {periodo: set() for periodo in periodos.keys()}
        
        for candidato in detalle_trayectorias:
            anno = candidato['Anno_Primera_Candidatura']
            id_persona = candidato['ID_Persona']
            
            if 1900 <= anno <= 1915 and id_persona not in personas_contadas["1900-1915"]:
                periodos["1900-1915"] += 1
                personas_contadas["1900-1915"].add(id_persona)
            elif 1916 <= anno <= 1930 and id_persona not in personas_contadas["1916-1930"]:
                periodos["1916-1930"] += 1
                personas_contadas["1916-1930"].add(id_persona)
            elif 1931 <= anno <= 1942 and id_persona not in personas_contadas["1931-1942"]:
                periodos["1931-1942"] += 1
                personas_contadas["1931-1942"].add(id_persona)
            elif 1943 <= anno <= 1945 and id_persona not in personas_contadas["1943-1945"]:
                periodos["1943-1945"] += 1
                personas_contadas["1943-1945"].add(id_persona)
    
    # Generar el contenido HTML
    html = """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trayectorias Previas de Candidatos Peronistas (1946-1955)</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            h1, h2, h3, h4 { color: #333; }
            h2 { margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
            h3 { margin-top: 25px; padding: 5px; }
            h4 { margin-top: 15px; border-left: 3px solid #4CAF50; padding-left: 10px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .summary-box { margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; }
            .chart-container { margin: 20px 0; text-align: center; }
            .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .grid-container-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
            .electo { color: #008800; font-weight: bold; }
            .no-electo { color: #880000; }
            .sin-experiencia { color: #999; font-style: italic; }
            .candidato-electo { font-weight: bold; }
            .stat-highlight { font-weight: bold; color: #0066cc; }
            .tipo-cargo-section { margin-top: 30px; border-top: 1px dashed #999; padding-top: 20px; }
            .section-title { padding: 10px; text-align: left; border: none; margin-bottom: 0; margin-top: 0; }
            .candidate-section { background-color: white; padding: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
            @media (max-width: 768px) { 
                .grid-container { grid-template-columns: 1fr; } 
                .grid-container-3 { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <h1>Trayectorias Previas de Candidatos Peronistas (1946-1955)</h1>
        <p>Informe generado el: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
        <p>Este informe analiza la experiencia política previa de todos los candidatos peronistas 
        que participaron en elecciones entre 1946 y 1955, permitiendo visualizar sus trayectorias
        políticas y patrones de experiencia previa.</p>
        
        <div class="grid-container">
            <div class="summary-box">
                <h3>Resumen General</h3>
                <p><strong>Total de candidatos peronistas:</strong> """ + str(total_candidatos) + """</p>
                <p><strong>Candidatos con experiencia política previa:</strong> """ + str(total_con_experiencia) + """ (""" + f"{porcentaje_con_experiencia:.1f}%" + """)</p>
                <p><strong>Promedio de candidaturas previas:</strong> """ + f"{promedio_candidaturas:.2f}" + """</p>
                <p><strong>Antigüedad política promedio:</strong> """ + f"{antiguedad_promedio:.1f} años" + """</p>
            </div>
            
            <div class="summary-box">
                <h3>Periodos Históricos de Experiencia Previa</h3>
                <p><strong>1900-1915:</strong> """ + str(periodos["1900-1915"]) + """ candidatos</p>
                <p><strong>1916-1930:</strong> """ + str(periodos["1916-1930"]) + """ candidatos</p>
                <p><strong>1931-1942:</strong> """ + str(periodos["1931-1942"]) + """ candidatos</p>
                <p><strong>1943-1945:</strong> """ + str(periodos["1943-1945"]) + """ candidatos</p>
            </div>
        </div>
    """
    
    # Agregar gráficos si están disponibles
    html += """
    <div class="grid-container">
    """
    
    if ruta_grafico_partidos:
        html += f"""
            <div class="chart-container">
                <h2>Procedencia Partidaria</h2>
                <img src="{os.path.basename(ruta_grafico_partidos)}" alt="Gráfico de partidos previos" style="max-width: 100%;">
            </div>
        """
    
    if ruta_grafico_periodos:
        html += f"""
            <div class="chart-container">
                <h2>Distribución Temporal</h2>
                <img src="{os.path.basename(ruta_grafico_periodos)}" alt="Gráfico de períodos temporales" style="max-width: 100%;">
            </div>
        """
        
    html += "</div>"
    
    # Agregar tabla con detalle de estadísticas por partido
    if datos_partidos_previos:
        html += f"""
        <h2>Distribución por Partido Previo</h2>
        <table>
            <tr>
                <th>Partido Previo</th>
                <th>Cantidad de Candidatos</th>
                <th>Porcentaje</th>
                <th>Año Más Antiguo</th>
                <th>Año Más Reciente</th>
            </tr>
        """
        
        for partido in datos_partidos_previos:
            porcentaje = (partido['Cantidad_Candidatos'] / total_con_experiencia) * 100 if total_con_experiencia > 0 else 0
            html += f"""
            <tr>
                <td>{partido['Partido_Previo']}</td>
                <td>{partido['Cantidad_Candidatos']}</td>
                <td>{porcentaje:.2f}%</td>
                <td>{partido['Anno_Min']}</td>
                <td>{partido['Anno_Max']}</td>
            </tr>
            """
        
        html += "</table>"
    
    # Análisis de experiencia previa por periodo histórico
    periodos_detalle = {
        "1900-1915": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1916-1930": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1931-1942": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1943-1945": {"candidatos": [], "partidos": Counter(), "personas": set()}
    }
    
    if detalle_trayectorias:
        for candidato in detalle_trayectorias:
            if candidato['Cantidad_Candidaturas_Previas'] > 0:
                anno = candidato['Anno_Primera_Candidatura']
                id_persona = candidato['ID_Persona']
                
                if 1900 <= anno <= 1915:
                    periodo = "1900-1915"
                elif 1916 <= anno <= 1930:
                    periodo = "1916-1930"
                elif 1931 <= anno <= 1942:
                    periodo = "1931-1942"
                elif 1943 <= anno <= 1945:
                    periodo = "1943-1945"
                else:
                    continue
                
                # Solo agregar si no hemos procesado ya a esta persona en este período
                if id_persona not in periodos_detalle[periodo]["personas"]:
                    periodos_detalle[periodo]["candidatos"].append(candidato)
                    periodos_detalle[periodo]["personas"].add(id_persona)
                    
                    # Usar el partido principal para el conteo de partidos
                    if candidato.get('Partido_Principal'):
                        periodos_detalle[periodo]["partidos"][candidato['Partido_Principal']] += 1
                    # Si no hay partido principal pero hay partidos previos como string, usar el primero
                    elif candidato.get('Partidos_Previos'):
                        primer_partido = candidato['Partidos_Previos'].split(', ')[0]
                        periodos_detalle[periodo]["partidos"][primer_partido] += 1

    # Sección análisis por periodos históricos
    html += """
    <h2>Análisis por Periodos Históricos</h2>
    <div class="grid-container">
    """
    
    for periodo, datos in periodos_detalle.items():
        if not datos["candidatos"]:
            continue
            
        total_periodo = len(datos["candidatos"])
        porcentaje = (total_periodo / total_con_experiencia) * 100 if total_con_experiencia > 0 else 0
        
        html += f"""
        <div class="summary-box tipo-cargo-section">
            <h3>Periodo {periodo}</h3>
            <p><strong>Total candidatos:</strong> {total_periodo} <span class="stat-highlight">({porcentaje:.1f}%)</span></p>
            
            <h4>Partidos políticos principales</h4>
            <table>
                <tr>
                    <th>Partido</th>
                    <th>Candidatos</th>
                    <th>Porcentaje</th>
                </tr>
        """
        
        # Listar partidos más comunes para este periodo
        for partido, cantidad in datos["partidos"].most_common(5):  # Top 5
            porc_partido = (cantidad / total_periodo) * 100 if total_periodo > 0 else 0
            html += f"""
                <tr>
                    <td>{partido}</td>
                    <td>{cantidad}</td>
                    <td>{porc_partido:.1f}%</td>
                </tr>
            """
        
        html += """
            </table>
        </div>
        """
    
    html += "</div>"  # Cierra grid-container
    
    # Agrupar candidatos por tipo de cargo
    grupos_cargo = {}
    candidatos_por_cargo = {}
    if detalle_trayectorias:
        # Diccionario para rastrear si ya contamos a una persona en un tipo de cargo
        personas_contadas_por_cargo = {}
        
        for candidato in detalle_trayectorias:
            cargo = candidato['Cargo_Peronista']
            ambito = candidato['Ambito_Peronista']
            id_persona = candidato['ID_Persona']
            tipo_cargo = ""
            
            if cargo == "Diputado" and ambito == "Nacional":
                tipo_cargo = "Diputados Nacionales"
            elif cargo == "Senador" and ambito == "Provincial":
                tipo_cargo = "Senadores Provinciales"
            elif cargo == "Diputado" and ambito == "Provincial":
                tipo_cargo = "Diputados Provinciales"
            elif cargo == "Elector" and ambito == "Provincial":
                tipo_cargo = "Electores Provinciales"
            else:
                tipo_cargo = f"{cargo}s {ambito}s" # Categoría genérica
            
            # Inicializar estructuras si no existen
            if tipo_cargo not in grupos_cargo:
                grupos_cargo[tipo_cargo] = []
                candidatos_por_cargo[tipo_cargo] = set()
                personas_contadas_por_cargo[tipo_cargo] = set()
            
            # Solo agregar si esta persona no ha sido contada para este tipo de cargo
            if id_persona not in personas_contadas_por_cargo[tipo_cargo]:
                grupos_cargo[tipo_cargo].append(candidato)
                candidatos_por_cargo[tipo_cargo].add(id_persona)
                personas_contadas_por_cargo[tipo_cargo].add(id_persona)

    # Calcular estadísticas detalladas por tipo de cargo
    estadisticas_por_cargo = calcular_estadisticas_partido_previo_por_tipo_cargo(grupos_cargo, detalle_trayectorias)
    
    # Ordenar los tipos de cargo según la especificación
    orden_tipos_cargo = {
        "Diputados Nacionales": 1,
        "Senadores Provinciales": 2,
        "Diputados Provinciales": 3,
        "Electores Provinciales": 4
    }
    
    tipos_cargo_ordenados = sorted(
        estadisticas_por_cargo.keys(),
        key=lambda x: orden_tipos_cargo.get(x, 99)  # Si no está en el orden definido, irá al final
    )
    
    # Añadir sección de estadísticas por tipo de cargo
    html += """
    <h2>Análisis por Tipo de Cargo</h2>
    <div class="grid-container">
    """
    
    for tipo_cargo in tipos_cargo_ordenados:
        stats = estadisticas_por_cargo[tipo_cargo]
        html += f"""
        <div class="summary-box tipo-cargo-section">
            <h3>{tipo_cargo}</h3>
            <p><strong>Total candidatos:</strong> {stats['total_candidatos']}</p>
            <p><strong>Con experiencia previa:</strong> {stats['con_experiencia_previa']} <span class="stat-highlight">({stats['porcentaje_con_experiencia']:.1f}%)</span></p>
            
            <h4>Procedencia Partidaria Principal</h4>
            <table>
                <tr>
                    <th>Partido Previo</th>
                    <th>Candidatos</th>
                    <th>Porcentaje</th>
                </tr>
        """
        
        # Mostrar los partidos previos más comunes para este tipo de cargo
        partidos_ordenados = sorted(stats['partidos_previos'].items(), 
                                   key=lambda x: x[1]['cantidad'], 
                                   reverse=True)
        
        for partido, partido_stats in partidos_ordenados:
            html += f"""
            <tr>
                <td>{partido}</td>
                <td>{partido_stats['cantidad']}</td>
                <td>{partido_stats['porcentaje']:.1f}%</td>
            </tr>
            """
        
        html += """
            </table>
        </div>
        """
    
    html += "</div>"  # Cierra grid-container para análisis por tipo de cargo
    
    # Definición unificada de la función para asignar tipos de cargo
    def asignar_tipo_cargo(candidato_info):
        """
        Determina el tipo de cargo de un candidato según su trayectoria política.
        """
        # Por defecto asignamos a Otros Cargos y luego revisamos si hay trayectoria específica
        resultado = "Otros Cargos"
        
        # Primero verificamos si el candidato tiene información directa de cargo peronista
        if 'primer_anno' in candidato_info:
            # Recorremos la trayectoria buscando candidaturas peronistas
            for registro in candidato_info.get('trayectoria', []):
                # Verificar si es una entrada peronista
                if registro.get('Partido') in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista'] and \
                   registro.get('Año') == candidato_info['primer_anno']:
                    
                    cargo = registro.get('Cargo', '')
                    
                    # Extraer cargo y ámbito de la cadena si viene en formato combinado
                    cargo_parts = cargo.split(' ')
                    cargo_nombre = cargo_parts[0] if cargo_parts else ''
                    ambito = cargo_parts[1] if len(cargo_parts) > 1 else ''
                    
                    if cargo_nombre == 'Diputado' and ambito == 'Nacional':
                        return "Diputados Nacionales"
                    elif cargo_nombre == 'Senador' and ambito == 'Provincial':
                        return "Senadores Provinciales"
                    elif cargo_nombre == 'Diputado' and ambito == 'Provincial':
                        return "Diputados Provinciales"
                    elif cargo_nombre == 'Elector' and ambito == 'Provincial':
                        return "Electores Provinciales"
    
        # Si no encontramos información específica, recorremos toda la trayectoria
        for registro in candidato_info.get('trayectoria', []):
            cargo = registro.get('Cargo', '')
            
            if 'Diputado Nacional' in cargo:
                return "Diputados Nacionales"
            elif 'Senador Provincial' in cargo:
                return "Senadores Provinciales"
            elif 'Diputado Provincial' in cargo:
                return "Diputados Provinciales"
            elif 'Elector Provincial' in cargo:
                return "Electores Provinciales"
        
        return resultado
    
    # Generar el listado completo de candidatos directamente a partir de candidatos_data
    # Crear un diccionario agrupando los candidatos por tipo de cargo
    candidatos_por_cargo = {
        "Diputados Nacionales": [],
        "Senadores Provinciales": [],
        "Diputados Provinciales": [],
        "Electores Provinciales": [],
        "Otros Cargos": []
    }
    
    # Agrupar los candidatos por tipo de cargo
    for candidato in candidatos_data:
        tipo_cargo = asignar_tipo_cargo(candidato)
        candidatos_por_cargo[tipo_cargo].append(candidato)
    
    # Ordenar cada grupo por nombre
    for tipo, lista in candidatos_por_cargo.items():
        candidatos_por_cargo[tipo] = sorted(lista, key=lambda x: x['nombre_completo'])
      # Orden predefinido para los tipos de cargo
    tipos_cargo_ordenados = [
        "Diputados Nacionales",
        "Senadores Provinciales",
        "Diputados Provinciales", 
        "Electores Provinciales",
        "Otros Cargos"
    ]
    
    # Generar tabla consolidada con todos los candidatos en una única vista
    html += generar_tabla_candidatos(candidatos_data)
    
    # Cerrar el HTML
    html += """
    </body>
    </html>
    """
    
    return html

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

def calcular_estadisticas_partido_previo_por_tipo_cargo(grupos_cargo, detalle_trayectorias):
    """Calcula estadísticas detalladas por tipo de cargo"""
    estadisticas_por_cargo = {}
    
    for tipo_cargo, candidatos in grupos_cargo.items():
        if candidatos:
            # Contar candidatos únicos basados en ID_Persona
            candidatos_unicos = {c['ID_Persona'] for c in candidatos}
            total_candidatos = len(candidatos_unicos)
            
            # Contar candidatos únicos con experiencia previa
            con_experiencia_previa = {c['ID_Persona'] for c in candidatos if c['Cantidad_Candidaturas_Previas'] > 0}
            total_con_experiencia = len(con_experiencia_previa)
            
            # Iniciar estadísticas para este tipo de cargo
            estadisticas_por_cargo[tipo_cargo] = {
                'total_candidatos': total_candidatos,
                'con_experiencia_previa': total_con_experiencia,
                'partidos_previos': {}
            }
            
            # Calcular porcentaje con experiencia
            estadisticas_por_cargo[tipo_cargo]['porcentaje_con_experiencia'] = (
                total_con_experiencia / total_candidatos * 100
            ) if total_candidatos > 0 else 0
            
            # Calcular partidos previos más comunes usando el partido principal
            partidos_previos = {}
            personas_por_partido = {}
            
            for c in candidatos:
                if c['Cantidad_Candidaturas_Previas'] > 0:
                    id_persona = c['ID_Persona']
                    
                    # Determinar el partido principal a contar
                    partido_a_contar = None
                    
                    # Usar el partido principal si está disponible
                    if c.get('Partido_Principal'):
                        partido_a_contar = c['Partido_Principal']
                    # Si no hay partido principal pero hay partidos previos, usar el primero
                    elif c.get('Partidos_Previos'):
                        partido_a_contar = c['Partidos_Previos'].split(', ')[0]
                    
                    if partido_a_contar:
                        # Inicializar el diccionario para este partido si no existe
                        if partido_a_contar not in partidos_previos:
                            partidos_previos[partido_a_contar] = 0
                            personas_por_partido[partido_a_contar] = set()
                        
                        # Solo contar si esta persona no ha sido contada para este partido
                        if id_persona not in personas_por_partido[partido_a_contar]:
                            partidos_previos[partido_a_contar] += 1
                            personas_por_partido[partido_a_contar].add(id_persona)
            
            # Transferir los datos de conteo al diccionario de estadísticas
            for partido, cantidad in partidos_previos.items():
                estadisticas_por_cargo[tipo_cargo]['partidos_previos'][partido] = {
                    'cantidad': cantidad,
                    'porcentaje': (cantidad / total_con_experiencia * 100) if total_con_experiencia > 0 else 0
                }
    
    return estadisticas_por_cargo

def generar_tabla_candidatos(candidatos_data):
    """Genera una tabla HTML consolidada con los datos de todos los candidatos peronistas"""
    # Esta función no debería usar self.asignar_tipo_cargo directamente
    html = """
    <h2>Listado Completo de Candidatos</h2>
    <div class="candidate-section">
        <table>
            <tr>
                <th rowspan="2">#</th>
                <th rowspan="2">Nombre</th>
                <th colspan="3" style="border-bottom: 2px solid #4CAF50; background-color: #e8f5e9;">Trayectoria Peronista</th>
                <th colspan="5" style="border-bottom: 2px solid #2196F3; background-color: #e3f2fd;">Trayectoria Previa</th>
            </tr>
            <tr>
                <th>Cargos</th>
                <th>Candidaturas</th>
                <th>Primera candidatura peronista</th>
                <th>Partidos Previos</th>
                <th>Cargos Previos</th>
                <th>Candidaturas Previas</th>
                <th>Primera Candidatura</th>
                <th>Experiencia (años)</th>
            </tr>
    """
    
    # Definir orden para tipos de cargo
    orden_tipos = {
        "Diputados Nacionales": 1,
        "Senadores Provinciales": 2,
        "Diputados Provinciales": 3, 
        "Electores Provinciales": 4,
        "Otros Cargos": 5
    }    
    
    # En base a cargos en trayectoria, determinar tipo de cargo
    def determinar_tipo_cargo(candidato):
        resultado = "Otros Cargos"
        
        # Primero buscamos el cargo más prioritario (en orden)
        for registro in candidato.get('trayectoria', []):
            # El campo 'Cargo' contiene tanto el cargo como el ámbito (por ejemplo, "Diputado Provincial")
            cargo_completo = registro.get('Cargo', registro.get('cargo', ''))
            
            # Si el cargo está en formato de texto, procesarlo
            if isinstance(cargo_completo, str):
                cargo_lower = cargo_completo.lower().strip()
                
                # Para ser más robustos, comprobamos varias posibles formas de escribir los cargos
                # Diputados Nacionales (mayor prioridad)
                if any(term in cargo_lower for term in ['diputado nacional', 'diputados nacionales', 'diputado nac']):
                    return "Diputados Nacionales"
                
                # Senadores Provinciales
                if any(term in cargo_lower for term in ['senador provincial', 'senadores provinciales', 'senador prov']):
                    return "Senadores Provinciales"
                
                # Diputados Provinciales
                if any(term in cargo_lower for term in ['diputado provincial', 'diputados provinciales', 'diputado prov']):
                    return "Diputados Provinciales"
                
                # Electores Provinciales
                if any(term in cargo_lower for term in ['elector provincial', 'electores provinciales', 'elector prov']):
                    return "Electores Provinciales"
                
                # Verificar componentes por separado en caso de variaciones en el formato
                if 'diputado' in cargo_lower and ('nacional' in cargo_lower or 'nación' in cargo_lower or 'nacion' in cargo_lower):
                    return "Diputados Nacionales"
                elif 'senador' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                    return "Senadores Provinciales"
                elif 'diputado' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                    return "Diputados Provinciales"
                elif 'elector' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                    return "Electores Provinciales"
        
        # Si no encontramos uno de los tipos principales, devolvemos "Otros Cargos"
        return resultado
    
    # Ordenar candidatos por tipo de cargo y nombre
    candidatos_ordenados = []
    for candidato in candidatos_data:
        tipo_cargo = determinar_tipo_cargo(candidato)
        # Agregar el tipo cargo para facilitar ordenamiento y mostrar en tabla
        candidato['tipo_cargo'] = tipo_cargo
        candidatos_ordenados.append(candidato)
    
    # Ordenar por tipo de cargo y nombre
    candidatos_ordenados = sorted(candidatos_ordenados, 
                                 key=lambda c: (orden_tipos.get(c['tipo_cargo'], 999), c['nombre_completo']))
    
    # Generar tabla con numeración
    for i, candidato in enumerate(candidatos_ordenados, 1):
        tipo_cargo = candidato['tipo_cargo']
        # Construir lista de todos los cargos en los que participó en partidos peronistas
        cargos_lista = []
        if candidato.get('trayectoria'):
            for registro in candidato['trayectoria']:
                # Solo considerar cargos de partidos peronistas
                if registro.get('Partido') in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']:
                    cargo_text = registro.get('Cargo', '')
                    
                    # Determinar si fue electo en este cargo específico
                    electo_valor = registro.get('Electo', '')
                    es_electo_en_cargo = False
                    
                    if isinstance(electo_valor, str):
                        electo_valor = electo_valor.lower().strip()
                        if electo_valor in ['sí', 'si', 's', 'yes', 'y', '1', 'true', 'verdadero', 'v']:
                            es_electo_en_cargo = True
                    elif isinstance(electo_valor, (int, bool)) and electo_valor:
                        es_electo_en_cargo = True
                        
                    # Añadir indicador de electo si corresponde
                    if es_electo_en_cargo:
                        cargo_text += " (*)"
                        
                    if cargo_text and cargo_text not in [c.replace(" (*)", "") for c in cargos_lista]:
                        cargos_lista.append(cargo_text)
        
        # Si no hay cargos específicos, usar el tipo de cargo general
        if not cargos_lista:
            if tipo_cargo == "Diputados Nacionales":
                cargos_lista.append("Diputado Nacional")
            elif tipo_cargo == "Senadores Provinciales":
                cargos_lista.append("Senador Provincial")
            elif tipo_cargo == "Diputados Provinciales":
                cargos_lista.append("Diputado Provincial")
            elif tipo_cargo == "Electores Provinciales":
                cargos_lista.append("Elector Provincial")
            else:
                cargos_lista.append("Otro Cargo")
          # Concatenar todos los cargos
        cargos_concatenados = ", ".join(cargos_lista)
        
        # Contar el número total de candidaturas peronistas
        num_candidaturas = sum(
            1 for registro in candidato.get('trayectoria', [])
            if registro.get('Partido') in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']
        )
        
        # Obtener datos de experiencia previa
        primera_candidatura = ""
        experiencia_anos = ""
        cargos_previos = ""
        
        # Manejar valores nulos/vacíos
        partidos_previos = candidato.get('partidos_previos', '')
        if partidos_previos == '-' or partidos_previos == 'None' or partidos_previos is None:
            partidos_previos = ''
            
        # Extraer información sobre cargos previos y primera candidatura
        if candidato.get('tiene_experiencia_previa', False):
            # Buscar el año de la primera candidatura y cargos previos
            primer_anno_peronista = candidato.get('primer_anno', 0)
            cargos_previos_lista = []
            candidaturas_previas = 0
            
            for registro in candidato.get('trayectoria', []):
                anno = registro.get('Año', 0)
                if anno < primer_anno_peronista and registro.get('Partido') not in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']:
                    # Incrementar contador de candidaturas previas
                    candidaturas_previas += 1
                    
                    # Actualizar primera candidatura
                    if not primera_candidatura or anno < int(primera_candidatura):
                        primera_candidatura = str(anno)
                    
                    # Agregar cargo previo
                    cargo_text = registro.get('Cargo', '')
                    electo_valor = registro.get('Electo', '')
                    es_electo = False
                    
                    if isinstance(electo_valor, str):
                        es_electo = electo_valor.lower().strip() in ['sí', 'si', 's', 'yes', 'y', '1', 'true', 'verdadero', 'v']
                    elif isinstance(electo_valor, (int, bool)):
                        es_electo = bool(electo_valor)
                        
                    if es_electo:
                        cargo_text += " (*)"
                        
                    if cargo_text not in cargos_previos_lista:
                        cargos_previos_lista.append(cargo_text)
            
            # Calcular años de experiencia
            if primera_candidatura and primer_anno_peronista > 0:
                experiencia_anos = primer_anno_peronista - int(primera_candidatura)
            
            # Concatenar todos los cargos previos
            cargos_previos = ", ".join(cargos_previos_lista)
        else:
            candidaturas_previas = 0
        
        html += f"""
            <tr>
                <td>{i}</td>
                <td>{candidato['nombre_completo']}</td>
                <td>{cargos_concatenados}</td>
                <td>{num_candidaturas}</td>
                <td>{candidato['primer_anno']}</td>
                <td>{partidos_previos}</td>
                <td>{cargos_previos}</td>
                <td>{candidaturas_previas}</td>
                <td>{primera_candidatura}</td>
                <td>{experiencia_anos}</td>
            </tr>
        """
    
    html += """
        </table>
    </div>
    """
    
    return html

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_candidatos_peronistas()
