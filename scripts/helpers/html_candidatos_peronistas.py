"""
Funciones auxiliares para la generación del informe HTML sobre candidatos peronistas.
"""
import os
from datetime import datetime
from collections import Counter
from scripts.commons.html_utils import formato_decimal
from scripts.helpers.categorias_candidatos_peronistas import categorizar_partido

def generar_informe_html_candidatos_peronistas(candidatos_data, datos_partidos_previos, detalle_trayectorias, ruta_grafico_partidos=None, ruta_grafico_periodos=None):
    """Genera un informe HTML con los datos de todos los candidatos peronistas entre 1946 y 1955"""
    # Importar la función calcular_estadisticas_partido_previo_por_tipo_cargo aquí para evitar la importación circular
    from scripts.helpers.estadisticas_candidatos_peronistas import calcular_estadisticas_partido_previo_por_tipo_cargo
    
    # Calcular estadísticas para el resumen
    total_candidatos = len(candidatos_data)
    # Corregir la verificación para asegurar que el valor es estrictamente True
    candidatos_con_experiencia = [c for c in candidatos_data if c.get('tiene_experiencia_previa') == True]
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
        "1946-1955": 0  # Removed "1943-1945" period as there were no elections
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
            elif 1946 <= anno <= 1955 and id_persona not in personas_contadas["1946-1955"]:
                periodos["1946-1955"] += 1
                personas_contadas["1946-1955"].add(id_persona)

    # Generar el contenido HTML básico
    html = _generar_estructura_basica_html()
    
    # Añadir el resumen general
    html += _generar_seccion_resumen_general(total_candidatos, total_con_experiencia, 
                                            porcentaje_con_experiencia, promedio_candidaturas, 
                                            antiguedad_promedio)
    
    # Añadir gráficos si están disponibles
    html += _generar_seccion_graficos(ruta_grafico_partidos, ruta_grafico_periodos)
    
    # Añadir sección de distribución por partido previo
    html += _generar_seccion_partidos_previos(datos_partidos_previos, total_con_experiencia)
    
    # Añadir sección de distribución por periodos históricos
    html += _generar_seccion_periodos_historicos(detalle_trayectorias, total_con_experiencia)
    
    # Añadir sección de distribución por tipo de cargo previo
    html += _generar_seccion_cargos_previos(detalle_trayectorias)
    
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
    
    # Añadir análisis de periodos históricos y cargos previos a las estadísticas por tipo de cargo
    html += _generar_seccion_analisis_por_tipo_cargo(estadisticas_por_cargo, grupos_cargo)
    
    # Generar tabla consolidada con todos los candidatos en una única vista
    html += generar_tabla_candidatos(candidatos_data)
    
    # Cerrar el HTML
    html += """
    </body>
    </html>
    """
    
    return html

def _generar_estructura_basica_html():
    """Genera la estructura básica del HTML con estilos y encabezado"""
    return """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trayectorias Previas de Candidatos Peronistas (1946-1955)</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            h1, h2, h3, h4 { color: #333; }
            h2 { margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
            h3 { margin-top: 0; padding: 5px; }
            h4 { margin-top: 15px; border-left: 3px solid #4CAF50; padding-left: 10px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            
            /* Estilos para controlar el ancho de columnas */
            .col-nombre { width: 50%; }
            .col-cantidad { width: 15%; }
            .col-porcentaje { width: 15%; }
            .col-año { width: 10%; }
            
            .summary-box { margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; }
            .chart-container { margin: 20px 0; text-align: center; }
            .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .grid-container-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
            .electo { color: #008800; font-weight: bold; }
            .no-electo { color: #880000; }
            .sin-experiencia { color: #999; font-style: italic; }
            .candidato-electo { font-weight: bold; }
            .stat-highlight { font-weight: bold; color: #0066cc; }
            .tipo-cargo-section { padding-top: 15px; }
            .section-title { padding: 10px; text-align: left; border: none; margin-bottom: 0; margin-top: 0; }
            .candidate-section { background-color: white; padding: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
            .full-width-box { margin-bottom: 20px; padding: 20px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; width: 100%; box-sizing: border-box; }
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
    """

def _generar_seccion_resumen_general(total_candidatos, total_con_experiencia, porcentaje_con_experiencia, 
                                    promedio_candidaturas, antiguedad_promedio):
    """Genera la sección de resumen general del informe"""
    return f"""
    <!-- Resumen general -->
    <div class="full-width-box">
        <h3>Resumen General</h3>
        <p><strong>Total de candidatos peronistas:</strong> {total_candidatos}</p>
        <p><strong>Candidatos con experiencia política previa:</strong> {total_con_experiencia} ({formato_decimal(porcentaje_con_experiencia)}%)</p>
        <p><strong>Promedio de candidaturas previas:</strong> {formato_decimal(promedio_candidaturas, 2)}</p>
        <p><strong>Antigüedad política promedio:</strong> {formato_decimal(antiguedad_promedio)} años</p>
    </div>
    """

def _generar_seccion_graficos(ruta_grafico_partidos, ruta_grafico_periodos):
    """Genera la sección con los gráficos del informe"""
    html = """
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
    return html

def _generar_seccion_partidos_previos(datos_partidos_previos, total_con_experiencia):
    """Genera la sección de distribución por partido previo"""
    html = ""
    if datos_partidos_previos:
        html += f"""
        <h2>Distribución por Partido Previo</h2>
        <p>Distribución de candidatos peronistas según el partido político al que pertenecieron previamente.</p>
        <table>
            <tr>
                <th class="col-nombre">Partido Previo</th>
                <th class="col-cantidad">Cantidad de Candidatos</th>
                <th class="col-porcentaje">Porcentaje</th>
                <th class="col-año">Año Más Antiguo</th>
                <th class="col-año">Año Más Reciente</th>
            </tr>
        """
        
        # Variable para calcular el total de candidatos mostrados en la tabla
        total_candidatos_tabla_partidos = 0
        
        for partido in datos_partidos_previos:
            total_candidatos_tabla_partidos += partido['Cantidad_Candidatos']
            porcentaje = (partido['Cantidad_Candidatos'] / total_con_experiencia) * 100 if total_con_experiencia > 0 else 0
            html += f"""
            <tr>
                <td>{partido['Partido_Previo']}</td>
                <td>{partido['Cantidad_Candidatos']}</td>
                <td>{formato_decimal(porcentaje, 2)}%</td>
                <td>{partido['Anno_Min']}</td>
                <td>{partido['Anno_Max']}</td>
            </tr>
            """
        
        # Añadir fila de totales al final de la tabla
        html += f"""
            <tr style="font-weight: bold; background-color: #f2f2f2;">
                <td>Total</td>
                <td>{total_candidatos_tabla_partidos}</td>
                <td>100%</td>
                <td></td>
                <td></td>
            </tr>
        </table>
        """
        
        # Agrupación por familias políticas
        html += _generar_subseccion_familias_politicas(datos_partidos_previos)
    
    return html

def _generar_subseccion_familias_politicas(datos_partidos_previos):
    """Genera la subsección de agrupación por familias políticas"""
    # Agrupar los partidos por categoría
    categorias_partidos = Counter()
    for partido in datos_partidos_previos:
        categoria = categorizar_partido(partido['Partido_Previo'])
        categorias_partidos[categoria] += partido['Cantidad_Candidatos']
    
    # Actualizar la tabla de categorías de partidos
    html = """
    <h3>Agrupación por familias políticas</h3>
    <p>Distribución de candidatos peronistas según la familia política a la que pertenecieron previamente.</p>
    <table>
        <tr>
            <th class="col-nombre">Familia Política</th>
            <th class="col-cantidad">Cantidad de Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
        </tr>
    """
    
    # Mostrar las categorías en orden específico
    orden_categorias = ["Radicales", "Autonomistas", "Liberales", "Otros"]
    total_categorias = sum(categorias_partidos.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias) * 100 if total_categorias > 0 else 0
            html += f"""
            <tr>
                <td>{categoria}</td>
                <td>{cantidad}</td>
                <td>{formato_decimal(porcentaje)}%</td>
            </tr>
            """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_categorias}</td>
            <td>100%</td>
        </tr>
    </table>
    """
    return html

def _generar_seccion_periodos_historicos(detalle_trayectorias, total_con_experiencia):
    """Genera la sección de distribución por periodos históricos"""
    # Análisis de experiencia previa por periodo histórico
    periodos_detalle = {
        "1900-1915": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1916-1930": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1931-1942": {"candidatos": [], "partidos": Counter(), "personas": set()},
        "1946-1955": {"candidatos": [], "partidos": Counter(), "personas": set()}
    }
    
    # Conjunto para rastrear personas que ya han sido asignadas a un periodo
    personas_ya_asignadas = set()
    
    if detalle_trayectorias:
        for candidato in detalle_trayectorias:
            if candidato['Cantidad_Candidaturas_Previas'] > 0:
                anno = candidato['Anno_Primera_Candidatura']
                id_persona = candidato['ID_Persona']
                
                # Verificar si esta persona ya ha sido asignada a un periodo
                if id_persona in personas_ya_asignadas:
                    continue
                
                # Asignar a un periodo basado en la primera candidatura
                if 1900 <= anno <= 1915:
                    periodo = "1900-1915"
                elif 1916 <= anno <= 1930:
                    periodo = "1916-1930"
                elif 1931 <= anno <= 1942:
                    periodo = "1931-1942"
                elif 1946 <= anno <= 1955:
                    periodo = "1946-1955"
                else:
                    continue
                
                # Agregar a este periodo y marcar como ya asignado
                periodos_detalle[periodo]["candidatos"].append(candidato)
                periodos_detalle[periodo]["personas"].add(id_persona)
                personas_ya_asignadas.add(id_persona)
                
                # Usar el partido principal para el conteo de partidos
                if candidato.get('Partido_Principal'):
                    periodos_detalle[periodo]["partidos"][candidato['Partido_Principal']] += 1
                # Si no hay partido principal pero hay partidos previos como string, usar el primero
                elif candidato.get('Partidos_Previos'):
                    primer_partido = candidato['Partidos_Previos'].split(', ')[0]
                    periodos_detalle[periodo]["partidos"][primer_partido] += 1

    # Generar HTML para la sección de periodos históricos
    html = f"""
    <h2>Distribución por Periodos Históricos</h2>
    <p>Distribución de candidatos peronistas según el periodo en que tuvieron su primera participación política previa.</p>
    <table>
        <tr>
            <th class="col-nombre">Periodo Histórico</th>
            <th class="col-cantidad">Cantidad de Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
            <th>Partidos Principales</th>
        </tr>
    """
    
    # Ordenar los periodos para que se muestren cronológicamente
    periodos_orden = ["1900-1915", "1916-1930", "1931-1942", "1946-1955"]
    
    # Variable para calcular el total de candidatos mostrados en la tabla
    total_candidatos_tabla_periodos = 0
    
    for periodo in periodos_orden:
        datos = periodos_detalle.get(periodo, {"candidatos": [], "partidos": Counter(), "personas": set()})
        total_periodo = len(datos["personas"])
        total_candidatos_tabla_periodos += total_periodo
        
        if total_periodo == 0:
            continue
            
        porcentaje = (total_periodo / total_con_experiencia) * 100 if total_con_experiencia > 0 else 0
        
        # Obtener los partidos más comunes para este periodo (máximo 3)
        partidos_principales = []
        for partido, cantidad in datos["partidos"].most_common(3):
            partidos_principales.append(f"{partido} ({cantidad})")
        
        partidos_texto = ", ".join(partidos_principales)
        
        html += f"""
        <tr>
            <td><strong>{periodo}</strong></td>
            <td>{total_periodo}</td>
            <td>{formato_decimal(porcentaje)}%</td>
            <td>{partidos_texto}</td>
        </tr>
    """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_candidatos_tabla_periodos}</td>
            <td>100%</td>
            <td></td>
        </tr>
    </table>
    """
    
    return html

def _generar_seccion_cargos_previos(detalle_trayectorias):
    """Genera la sección de análisis por tipo de cargo previo"""
    # Diccionario para categorías de cargo (siguiendo la jerarquía especificada)
    cargos_jerarquia = {
        "Diputado Nacional": {"peso": 5, "candidatos": [], "personas": set()},
        "Senador Provincial": {"peso": 4, "candidatos": [], "personas": set()},
        "Diputado Provincial": {"peso": 3, "candidatos": [], "personas": set()},
        "Elector Nacional": {"peso": 2, "candidatos": [], "personas": set()},
        "Elector Provincial": {"peso": 1, "candidatos": [], "personas": set()},
        "Otros Cargos": {"peso": 0, "candidatos": [], "personas": set()}  # Categoría para otros cargos
    }
    
    # Conjunto para rastrear personas ya asignadas a un cargo
    personas_ya_asignadas_cargo = set()
    
    if detalle_trayectorias:
        for candidato in detalle_trayectorias:
            if candidato['Cantidad_Candidaturas_Previas'] > 0:
                id_persona = candidato['ID_Persona']
                
                # Verificar si esta persona ya ha sido asignada a un cargo
                if id_persona in personas_ya_asignadas_cargo:
                    continue
                
                # Obtener todos los cargos previos como una lista
                cargos_previos = candidato.get('Cargos_Previos', '')
                if not cargos_previos:
                    continue
                
                # Buscar el cargo de mayor jerarquía
                cargo_asignado = None
                
                # Verificar cada tipo de cargo específicamente en los cargos previos
                if "Diputado Nacional" in cargos_previos:
                    cargo_asignado = "Diputado Nacional"
                elif "Senador Provincial" in cargos_previos:
                    cargo_asignado = "Senador Provincial"
                elif "Diputado Provincial" in cargos_previos:
                    cargo_asignado = "Diputado Provincial"
                elif "Elector Nacional" in cargos_previos:
                    cargo_asignado = "Elector Nacional"
                elif "Elector Provincial" in cargos_previos:
                    cargo_asignado = "Elector Provincial"
                else:
                    cargo_asignado = "Otros Cargos"
                
                # Asignar al cargo correspondiente
                if cargo_asignado:
                    cargos_jerarquia[cargo_asignado]["candidatos"].append(candidato)
                    cargos_jerarquia[cargo_asignado]["personas"].add(id_persona)
                    personas_ya_asignadas_cargo.add(id_persona)
    
    # Calcular el número real de candidatos únicos con experiencia previa
    personas_con_experiencia_previa = set()
    for candidato in detalle_trayectorias:
        if candidato['Cantidad_Candidaturas_Previas'] > 0:
            personas_con_experiencia_previa.add(candidato['ID_Persona'])
    
    # Número real de candidatos únicos con experiencia previa
    total_personas_con_experiencia = len(personas_con_experiencia_previa)
    
    # Generar tabla de cargos previos
    html = f"""
    <h2>Distribución por Tipo de Cargo Previo</h2>
    <p>Distribución de candidatos peronistas según el cargo de mayor jerarquía que ocuparon previamente.</p>
    <table>
        <tr>
            <th class="col-nombre">Cargo Previo</th>
            <th class="col-cantidad">Cantidad de Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
            <th>Partidos Principales</th>
        </tr>
    """
    
    # Ordenar los cargos por jerarquía (mayor a menor)
    cargos_orden = sorted(
        cargos_jerarquia.keys(),
        key=lambda x: cargos_jerarquia[x]["peso"],
        reverse=True
    )
    
    # Variable para calcular el total de candidatos mostrados en la tabla
    total_candidatos_tabla_cargos = 0
    
    for cargo in cargos_orden:
        datos = cargos_jerarquia[cargo]
        total_cargo = len(datos["personas"])
        total_candidatos_tabla_cargos += total_cargo
        
        if total_cargo == 0:
            continue
            
        # Calcular el porcentaje basado en el total real de personas con experiencia previa
        porcentaje = (total_cargo / total_personas_con_experiencia) * 100 if total_personas_con_experiencia > 0 else 0
        
        # Obtener los partidos más comunes para este cargo
        partidos_por_cargo = Counter()
        for candidato in datos["candidatos"]:
            if candidato.get('Partido_Principal'):
                partidos_por_cargo[candidato['Partido_Principal']] += 1
            elif candidato.get('Partidos_Previos'):
                primer_partido = candidato['Partidos_Previos'].split(', ')[0]
                partidos_por_cargo[primer_partido] += 1
        
        # Obtener los partidos más comunes para este cargo (máximo 3)
        partidos_principales = []
        for partido, cantidad in partidos_por_cargo.most_common(3):
            partidos_principales.append(f"{partido} ({cantidad})")
        
        partidos_texto = ", ".join(partidos_principales)
        
        html += f"""
        <tr>
            <td><strong>{cargo}</strong></td>
            <td>{total_cargo}</td>
            <td>{formato_decimal(porcentaje)}%</td>
            <td>{partidos_texto}</td>
        </tr>
    """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_candidatos_tabla_cargos}</td>
            <td>100%</td>
            <td></td>
        </tr>
    </table>
    """
    
    return html

def _generar_seccion_analisis_por_tipo_cargo(estadisticas_por_cargo, grupos_cargo):
    """Genera la sección de análisis por tipo de cargo"""
    # Actualizar función para añadir análisis de periodos históricos y cargos previos
    for tipo_cargo, stats in estadisticas_por_cargo.items():
        # Inicializar estructuras para períodos históricos
        stats['periodos_historicos'] = {
            "1900-1915": 0,
            "1916-1930": 0,
            "1931-1942": 0,
            "1946-1955": 0
        }
        
        # Inicializar estructuras para cargos previos
        stats['cargos_previos'] = {
            "Diputado Nacional": 0,
            "Senador Provincial": 0,
            "Diputado Provincial": 0, 
            "Elector Nacional": 0,
            "Elector Provincial": 0,
            "Otros Cargos": 0
        }
        
        # Solo realizar análisis si hay candidatos con experiencia previa
        if stats['con_experiencia_previa'] > 0:
            # Crear conjuntos para rastrear personas únicas por período y cargo
            personas_por_periodo = {
                "1900-1915": set(),
                "1916-1930": set(),
                "1931-1942": set(),
                "1946-1955": set()
            }
            
            personas_por_cargo_previo = {
                "Diputado Nacional": set(),
                "Senador Provincial": set(),
                "Diputado Provincial": set(), 
                "Elector Nacional": set(),
                "Elector Provincial": set(),
                "Otros Cargos": set()
            }
            
            # Procesar cada candidato del tipo de cargo actual
            for candidato in grupos_cargo[tipo_cargo]:
                if candidato['Cantidad_Candidaturas_Previas'] > 0:
                    id_persona = candidato['ID_Persona']
                    anno = candidato['Anno_Primera_Candidatura']
                    
                    # Asignar a un periodo histórico
                    if 1900 <= anno <= 1915:
                        personas_por_periodo["1900-1915"].add(id_persona)
                    elif 1916 <= anno <= 1930:
                        personas_por_periodo["1916-1930"].add(id_persona)
                    elif 1931 <= anno <= 1942:
                        personas_por_periodo["1931-1942"].add(id_persona)
                    elif 1946 <= anno <= 1955:
                        personas_por_periodo["1946-1955"].add(id_persona)
                    
                    # Asignar a un cargo previo basado en el contenido de Cargos_Previos
                    cargos_previos = candidato.get('Cargos_Previos', '')
                    
                    # Buscar el cargo de mayor jerarquía según la misma lógica de clasificación
                    if "Diputado Nacional" in cargos_previos:
                        personas_por_cargo_previo["Diputado Nacional"].add(id_persona)
                    elif "Senador Provincial" in cargos_previos:
                        personas_por_cargo_previo["Senador Provincial"].add(id_persona)
                    elif "Diputado Provincial" in cargos_previos:
                        personas_por_cargo_previo["Diputado Provincial"].add(id_persona)
                    elif "Elector Nacional" in cargos_previos:
                        personas_por_cargo_previo["Elector Nacional"].add(id_persona)
                    elif "Elector Provincial" in cargos_previos:
                        personas_por_cargo_previo["Elector Provincial"].add(id_persona)
                    else:
                        personas_por_cargo_previo["Otros Cargos"].add(id_persona)
            
            # Actualizar los conteos en las estadísticas
            for periodo, personas in personas_por_periodo.items():
                stats['periodos_historicos'][periodo] = len(personas)
                
            for cargo, personas in personas_por_cargo_previo.items():
                stats['cargos_previos'][cargo] = len(personas)
    
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
    html = """
    <h2>Análisis por Tipo de Cargo</h2>
    <div class="grid-container">
    """
    
    for tipo_cargo in tipos_cargo_ordenados:
        stats = estadisticas_por_cargo[tipo_cargo]
        html += _generar_subseccion_tipo_cargo(tipo_cargo, stats)
    
    # Close the grid-container div
    html += """
    </div>  <!-- Cierre correcto del grid-container para análisis por tipo de cargo -->
    """
    
    return html

def _generar_subseccion_tipo_cargo(tipo_cargo, stats):
    """Genera una subsección HTML para un tipo de cargo específico"""
    # Crear una función auxiliar para generar la subsección
    html = f"""
    <div class="summary-box tipo-cargo-section">
        <h3>{tipo_cargo}</h3>
        <p><strong>Total candidatos:</strong> {stats['total_candidatos']}</p>
        <p><strong>Con experiencia previa:</strong> {stats['con_experiencia_previa']} <span class="stat-highlight">({formato_decimal(stats['porcentaje_con_experiencia'])}%)</span></p>
        
        <h4>Procedencia Partidaria Principal</h4>
        <table>
            <tr>
                <th class="col-nombre">Partido Previo</th>
                <th class="col-cantidad">Candidatos</th>
                <th class="col-porcentaje">Porcentaje</th>
            </tr>
    """
    
    # Mostrar los partidos previos más comunes para este tipo de cargo
    total_candidatos_partidos = 0
    partidos_ordenados = sorted(stats['partidos_previos'].items(), 
                               key=lambda x: x[1]['cantidad'], 
                               reverse=True)
    
    # Crear un contador para las categorías de partidos
    categorias_partidos_cargo = Counter()
    
    for partido, partido_stats in partidos_ordenados:
        total_candidatos_partidos += partido_stats['cantidad']
        html += f"""
        <tr>
            <td>{partido}</td>
            <td>{partido_stats['cantidad']}</td>
            <td>{formato_decimal(partido_stats['porcentaje'])}%</td>
        </tr>
        """
        
        # Categorizar el partido y acumular en el contador
        categoria = categorizar_partido(partido)
        categorias_partidos_cargo[categoria] += partido_stats['cantidad']
    
    # Añadir fila de totales para la tabla de partidos
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_candidatos_partidos}</td>
            <td>100%</td>
        </tr>
    </table>
    """
    
    # Añadir tabla de categorías de partidos
    html += _generar_tabla_categorias_partidos(categorias_partidos_cargo)
    
    # Añadir tabla de periodos históricos
    html += _generar_tabla_periodos_historicos_por_cargo(stats)
    
    # Añadir tabla de cargos previos
    html += _generar_tabla_cargos_previos_por_cargo(stats)
    
    html += "</div>"
    return html

def _generar_tabla_categorias_partidos(categorias_partidos_cargo):
    """Genera una tabla HTML con las categorías de partidos para un tipo de cargo"""
    html = """
    <h4>Agrupación por familias políticas</h4>
    <table>
        <tr>
            <th class="col-nombre">Familia Política</th>
            <th class="col-cantidad">Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
        </tr>
    """
    
    # Mostrar las categorías de partidos en orden específico
    orden_categorias = ["Radicales", "Autonomistas", "Liberales", "Otros"]
    total_categorias_cargo = sum(categorias_partidos_cargo.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_cargo.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias_cargo) * 100 if total_categorias_cargo > 0 else 0
            html += f"""
            <tr>
                <td>{categoria}</td>
                <td>{cantidad}</td>
                <td>{formato_decimal(porcentaje)}%</td>
            </tr>
            """
    
    # Añadir fila de totales para la tabla de categorías
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_categorias_cargo}</td>
            <td>100%</td>
        </tr>
    </table>
    """
    return html

def _generar_tabla_periodos_historicos_por_cargo(stats):
    """Genera una tabla HTML con los períodos históricos para un tipo de cargo"""
    html = """
    <h4>Distribución por Periodos Históricos</h4>
    <table>
        <tr>
            <th class="col-nombre">Periodo</th>
            <th class="col-cantidad">Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
        </tr>
    """
    
    # Mostrar la distribución por períodos históricos
    total_candidatos_periodos = 0
    periodos_orden = ["1900-1915", "1916-1930", "1931-1942", "1946-1955"]
    
    for periodo in periodos_orden:
        cantidad = stats['periodos_historicos'].get(periodo, 0)
        total_candidatos_periodos += cantidad
        if cantidad > 0:
            porcentaje = (cantidad / stats['con_experiencia_previa']) * 100 if stats['con_experiencia_previa'] > 0 else 0
            html += f"""
            <tr>
                <td>{periodo}</td>
                <td>{cantidad}</td>
                <td>{formato_decimal(porcentaje)}%</td>
            </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos históricos
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_candidatos_periodos}</td>
            <td>100%</td>
        </tr>
    </table>
    """
    return html

def _generar_tabla_cargos_previos_por_cargo(stats):
    """Genera una tabla HTML con los cargos previos para un tipo de cargo"""
    html = """
    <h4>Distribución por Tipo de Cargo Previo</h4>
    <table>
        <tr>
            <th class="col-nombre">Cargo Previo</th>
            <th class="col-cantidad">Cantidad de Candidatos</th>
            <th class="col-porcentaje">Porcentaje</th>
        </tr>
    """
    
    # Mostrar la distribución por tipo de cargo previo
    total_candidatos_cargos = 0
    cargos_orden = ["Diputado Nacional", "Senador Provincial", "Diputado Provincial", 
                   "Elector Nacional", "Elector Provincial", "Otros Cargos"]
    
    for cargo in cargos_orden:
        cantidad = stats['cargos_previos'].get(cargo, 0)
        total_candidatos_cargos += cantidad
        if cantidad > 0:
            porcentaje = (cantidad / stats['con_experiencia_previa']) * 100 if stats['con_experiencia_previa'] > 0 else 0
            html += f"""
            <tr>
                <td>{cargo}</td>
                <td>{cantidad}</td>
                <td>{formato_decimal(porcentaje)}%</td>
            </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos previos
    html += f"""
        <tr style="font-weight: bold; background-color: #f2f2f2;">
            <td>Total</td>
            <td>{total_candidatos_cargos}</td>
            <td>100%</td>
        </tr>
    </table>
    """
    return html

def generar_tabla_candidatos(candidatos_data):
    """Genera una tabla HTML consolidada con los datos de todos los candidatos peronistas"""
    # Importar la función determinar_tipo_cargo desde categorias_candidatos_peronistas
    from scripts.helpers.categorias_candidatos_peronistas import determinar_tipo_cargo
    
    html = """
    <h2>Listado Completo de Candidatos</h2>
    <div class="candidate-section">
        <table>
            <tr>
                <th rowspan="2">#</th>
                <th rowspan="2">Nombre</th>
                <th colspan="3" style="border-bottom: 2px solid #4CAF50; background-color: #e8f5e9;">Trayectoria Peronista</th>
                <th colspan="5" style="border-bottom: 2px solid #2196F3; background-color: #e3f2fd;">Trayectoria Previas</th>
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
        candidaturas_previas = ""  # Inicializar como string vacío
        
        # Manejar valores nulos/vacíos
        partidos_previos = candidato.get('partidos_previos', '')
        if partidos_previos == '-' or partidos_previos == 'None' or partidos_previos is None:
            partidos_previos = ''
            
        # Extraer información sobre cargos previos y primera candidatura
        if candidato.get('tiene_experiencia_previa', False):
            # Buscar el año de la primera candidatura y cargos previos
            primer_anno_peronista = candidato.get('primer_anno', 0)
            cargos_previos_lista = []
            candidaturas_previas = 0  # Inicializar contador para candidatos con experiencia
            
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
        
        # Agregar fila para el candidato
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
