# -*- coding: utf-8 -*-
"""
Generación de HTML para el informe de candidatos de 1946.
Este módulo contiene funciones específicas para generar el HTML
del informe de candidatos peronistas de 1946.
"""
from datetime import datetime
from collections import Counter

from scripts.commons.html_utils import formato_decimal
from scripts.helpers.utilidades_candidatos_1946 import categorizar_partido
from scripts.helpers.analisis_candidatos_1946 import (
    analizar_partidos_previos, 
    analizar_categorias_partidos,
    analizar_periodos_historicos,
    analizar_cargos_previos
)
from scripts.helpers.tablas_candidatos_1946 import generar_tabla_candidatos

def generar_informe_html_candidatos_1946(candidatos_data):
    """
    Genera el contenido HTML completo del informe de candidatos peronistas de 1946
    
    Args:
        candidatos_data (list): Lista de candidatos con toda su información procesada
        
    Returns:
        str: Contenido HTML del informe
    """
    from datetime import datetime
    
    # Inicializar el HTML con el encabezado y estilos
    html = """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Candidatos Peronistas de 1946 - Trayectorias Previas</title>
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
            .summary-box { margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; }
            .partido-laborista { background-color: #ffebcc; }
            .partido-radical { background-color: #e6f7ff; }
            .candidato-electo { font-weight: bold; }
            .sin-experiencia { color: #999; font-style: italic; }
            .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .tipo-cargo-section { padding-top: 15px; }
            @media (max-width: 768px) { .grid-container { grid-template-columns: 1fr; } }
            .stat-highlight { font-weight: bold; color: #0066cc; }
            .section-title { padding: 10px; text-align: left; border: none; margin-bottom: 0; margin-top: 0; }
            .candidate-section { background-color: white; padding: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
            .full-width-box { margin-bottom: 20px; padding: 20px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; width: 100%; box-sizing: border-box; }
            .col-nombre { width: 50%; }
            .col-cantidad { width: 15%; }
            .col-porcentaje { width: 15%; }
            .col-año { width: 10%; }
        </style>
    </head><body>
        <h1>Candidatos de Partidos Peronistas en las Elecciones de 1946</h1>
        <p>Informe generado el: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
        <p>Este informe analiza la experiencia política previa de los candidatos que participaron en las elecciones de 1946
        por los partidos Laborista Correntino y Radical (Junta Reorganizadora), permitiendo visualizar sus trayectorias
        políticas y procedencia partidaria.</p>
    """
    
    # Analizamos los datos para el resumen
    total_candidatos = len(candidatos_data)
    candidatos_laboristas = [c for c in candidatos_data if c['partido'] == 'Laborista Correntino']
    candidatos_radicales_jr = [c for c in candidatos_data if c['partido'] == 'Radical (Junta Reorganizadora)']
    
    total_electos = sum(1 for c in candidatos_data if c['electo'] == 'Sí')
    total_laboristas_electos = sum(1 for c in candidatos_laboristas if c['electo'] == 'Sí')
    total_radicales_jr_electos = sum(1 for c in candidatos_radicales_jr if c['electo'] == 'Sí')
    
    # Corregir la identificación de candidatos con experiencia previa
    candidatos_con_experiencia = [c for c in candidatos_data if c.get('tiene_experiencia_previa') == True]
    porcentaje_con_experiencia = (len(candidatos_con_experiencia) / total_candidatos) * 100 if total_candidatos > 0 else 0
    
    # Contamos los candidatos con experiencia previa por partido
    laboristas_con_exp = [c for c in candidatos_laboristas if c.get('tiene_experiencia_previa') == True]
    radicales_jr_con_exp = [c for c in candidatos_radicales_jr if c.get('tiene_experiencia_previa') == True]
    
    # Calculamos porcentajes
    porc_laboristas_con_exp = (len(laboristas_con_exp) / len(candidatos_laboristas)) * 100 if len(candidatos_laboristas) > 0 else 0
    porc_radicales_jr_con_exp = (len(radicales_jr_con_exp) / len(candidatos_radicales_jr)) * 100 if len(candidatos_radicales_jr) > 0 else 0
    
    # Resumen general - Usamos full-width-box como en el otro informe
    html += f"""
        <div class="full-width-box">
            <h3>Resumen General</h3>
            <p><strong>Total de candidatos analizados:</strong> {total_candidatos}</p>
            <p><strong>Candidatos con experiencia política previa:</strong> {len(candidatos_con_experiencia)} <span class="stat-highlight">({formato_decimal(porcentaje_con_experiencia)}%)</span></p>
            <p><strong>Total electos:</strong> {total_electos} ({formato_decimal((total_electos/total_candidatos)*100)}%)</p>
        </div>

        <h2>Análisis General (Todos los Candidatos)</h2>
        <div class="full-width-box">
            <p>Esta sección analiza todos los candidatos de partidos peronistas en 1946 sin distinguir entre Laborista Correntino y Radical (Junta Reorganizadora).</p>
            
            <h3>Procedencia Partidaria de Candidatos con Experiencia Previa</h3>
            
            <div class="grid-container">
                <div class="summary-box">
                    <h4>Partidos previos más comunes</h4>
                    <table>
                        <tr>
                            <th>Partido</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Analizar partidos previos de todos los candidatos con experiencia previa
    contador_partidos_todos = analizar_partidos_previos(candidatos_con_experiencia)
    
    # Variable para calcular el total de candidatos mostrados en la tabla
    total_candidatos_tabla_partidos_todos = 0
    
    for partido, cantidad in contador_partidos_todos.most_common():
        total_candidatos_tabla_partidos_todos += cantidad
        porcentaje = (cantidad / len(candidatos_con_experiencia)) * 100 if len(candidatos_con_experiencia) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
        """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
                        <tr style="font-weight: bold; background-color: #f2f2f2;">
                            <td>Total</td>
                            <td>{total_candidatos_tabla_partidos_todos}</td>
                            <td>100%</td>
                        </tr>
                    </table>
                </div>
                
                <div class="summary-box">
                    <h4>Agrupación por familias políticas</h4>
                    <table>
                        <tr>
                            <th>Familia Política</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Crear un contador para las categorías de todos los candidatos
    categorias_partidos_todos = analizar_categorias_partidos(contador_partidos_todos)
    
    # Mostrar las categorías en orden específico
    orden_categorias = ["Radicales", "Autonomistas", "Liberales", "Otros"]
    total_categorias_todos = sum(categorias_partidos_todos.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_todos.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias_todos) * 100 if total_categorias_todos > 0 else 0
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
                            <td>{total_categorias_todos}</td>
                            <td>100%</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <!-- NUEVAS TABLAS: Distribución por períodos históricos y tipos de cargo previo -->
            <div class="grid-container">
                <div class="summary-box">
                    <h4>Distribución por Períodos Históricos</h4>
                    <table>
                        <tr>
                            <th class="col-nombre">Periodo Histórico</th>
                            <th class="col-cantidad">Candidatos</th>
                            <th class="col-porcentaje">Porcentaje</th>
                        </tr>
    """
    
    # Analizar los períodos históricos
    periodos = analizar_periodos_historicos(candidatos_con_experiencia)
    
    # Orden cronológico para los periodos
    periodos_orden = ["1900-1915", "1916-1930", "1931-1942", "1943-1945"]
    total_periodos = sum(periodos.values())
    
    for periodo in periodos_orden:
        cantidad = periodos.get(periodo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_periodos) * 100 if total_periodos > 0 else 0
            html += f"""
                        <tr>
                            <td>{periodo}</td>
                            <td>{cantidad}</td>
                            <td>{formato_decimal(porcentaje)}%</td>
                        </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos
    html += f"""
                        <tr style="font-weight: bold; background-color: #f2f2f2;">
                            <td>Total</td>
                            <td>{total_periodos}</td>
                            <td>100%</td>
                        </tr>
                    </table>
                </div>
                
                <div class="summary-box">
                    <h4>Distribución por Tipo de Cargo Previo</h4>
                    <table>
                        <tr>
                            <th class="col-nombre">Cargo Previo</th>
                            <th class="col-cantidad">Candidatos</th>
                            <th class="col-porcentaje">Porcentaje</th>
                        </tr>
    """
    
    # Analizar los tipos de cargo previo
    cargos_previos = analizar_cargos_previos(candidatos_con_experiencia)
    
    # Orden jerárquico para los cargos
    cargos_orden = ["Diputado Nacional", "Senador Provincial", "Diputado Provincial", 
                    "Elector Nacional", "Elector Provincial", "Otros Cargos"]
    total_cargos = sum(cargos_previos.values())
    
    for cargo in cargos_orden:
        cantidad = cargos_previos.get(cargo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_cargos) * 100 if total_cargos > 0 else 0
            html += f"""
                        <tr>
                            <td>{cargo}</td>
                            <td>{cantidad}</td>
                            <td>{formato_decimal(porcentaje)}%</td>
                        </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos
    html += f"""
                        <tr style="font-weight: bold; background-color: #f2f2f2;">
                            <td>Total</td>
                            <td>{total_cargos}</td>
                            <td>100%</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <h2>Estadísticas Comparativas por Partido (Todos los Candidatos)</h2>
        <div class="grid-container">
    """
    
    # Sección de Laboristas
    html += f"""
            <div class="summary-box partido-laborista">
                <h3>Laborista Correntino</h3>
                <p><strong>Total candidatos:</strong> {len(candidatos_laboristas)}</p>
                <p><strong>Con experiencia previa:</strong> {len(laboristas_con_exp)} <span class="stat-highlight">({formato_decimal(porc_laboristas_con_exp)}%)</span></p>
                
                <h4>Partidos previos más comunes</h4>
                <table>
                    <tr>
                        <th>Partido</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Analizar partidos previos de laboristas
    contador_partidos_laboristas = analizar_partidos_previos(laboristas_con_exp)
    
    # Variable para calcular el total de candidatos mostrados en la tabla
    total_candidatos_tabla_partidos_laboristas = 0
    
    for partido, cantidad in contador_partidos_laboristas.most_common():
        total_candidatos_tabla_partidos_laboristas += cantidad
        porcentaje = (cantidad / len(laboristas_con_exp)) * 100 if len(laboristas_con_exp) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
        """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_candidatos_tabla_partidos_laboristas}</td>
                        <td>100%</td>
                    </tr>
                </table>
    """
    
    # NUEVA TABLA: Agrupación por familias políticas
    # Crear un contador para las categorías
    categorias_partidos_laboristas = analizar_categorias_partidos(contador_partidos_laboristas)
    
    # Agregar tabla de categorías de partidos
    html += """
                <h4>Agrupación por familias políticas</h4>
                <table>
                    <tr>
                        <th>Familia Política</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Mostrar las categorías en orden específico
    total_categorias = sum(categorias_partidos_laboristas.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_laboristas.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias) * 100 if total_categorias > 0 else 0
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
                        <td>{total_categorias}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <!-- NUEVAS TABLAS: Distribución por períodos históricos y tipos de cargo previo para Laboristas -->
                <h4>Distribución por Períodos Históricos</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Periodo Histórico</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los períodos históricos para laboristas
    periodos_lab = analizar_periodos_historicos(laboristas_con_exp)
    total_periodos_lab = sum(periodos_lab.values())
    
    for periodo in periodos_orden:
        cantidad = periodos_lab.get(periodo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_periodos_lab) * 100 if total_periodos_lab > 0 else 0
            html += f"""
                    <tr>
                        <td>{periodo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_periodos_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <h4>Distribución por Tipo de Cargo Previo</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Cargo Previo</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los tipos de cargo previo para laboristas
    cargos_previos_lab = analizar_cargos_previos(laboristas_con_exp)
    total_cargos_lab = sum(cargos_previos_lab.values())
    
    for cargo in cargos_orden:
        cantidad = cargos_previos_lab.get(cargo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_cargos_lab) * 100 if total_cargos_lab > 0 else 0
            html += f"""
                    <tr>
                        <td>{cargo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_cargos_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
            </div>
    """
    
    # Sección de Radicales JR
    html += f"""
            <div class="summary-box partido-radical">
                <h3>Radical (Junta Reorganizadora)</h3>
                <p><strong>Total candidatos:</strong> {len(candidatos_radicales_jr)}</p>
                <p><strong>Con experiencia previa:</strong> {len(radicales_jr_con_exp)} <span class="stat-highlight">({formato_decimal(porc_radicales_jr_con_exp)}%)</span></p>
                
                <h4>Partidos previos más comunes</h4>
                <table>
                    <tr>
                        <th>Partido</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Analizar partidos previos de radicales jr
    contador_partidos_radicales = analizar_partidos_previos(radicales_jr_con_exp)
    
    # Variable para calcular el total de candidatos mostrados en la tabla
    total_candidatos_tabla_partidos_radicales = sum(contador_partidos_radicales.values())
    
    for partido, cantidad in contador_partidos_radicales.most_common():
        porcentaje = (cantidad / len(radicales_jr_con_exp)) * 100 if len(radicales_jr_con_exp) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
        """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_candidatos_tabla_partidos_radicales}</td>
                        <td>100%</td>
                    </tr>
                </table>
    """
    
    # NUEVA TABLA: Agrupación por familias políticas para radicales JR
    # Crear un contador para las categorías
    categorias_partidos_radicales = analizar_categorias_partidos(contador_partidos_radicales)
    
    # Agregar tabla de categorías de partidos
    html += """
                <h4>Agrupación por familias políticas</h4>
                <table>
                    <tr>
                        <th>Familia Política</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Mostrar las categorías en orden específico
    total_categorias_rad = sum(categorias_partidos_radicales.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_radicales.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias_rad) * 100 if total_categorias_rad > 0 else 0
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
                        <td>{total_categorias_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <!-- NUEVAS TABLAS: Distribución por períodos históricos y tipos de cargo previo para Radical JR -->
                <h4>Distribución por Períodos Históricos</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Periodo Histórico</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los períodos históricos para radicales
    periodos_rad = analizar_periodos_historicos(radicales_jr_con_exp)
    total_periodos_rad = sum(periodos_rad.values())
    
    for periodo in periodos_orden:
        cantidad = periodos_rad.get(periodo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_periodos_rad) * 100 if total_periodos_rad > 0 else 0
            html += f"""
                    <tr>
                        <td>{periodo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_periodos_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <h4>Distribución por Tipo de Cargo Previo</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Cargo Previo</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los tipos de cargo previo para radicales
    cargos_previos_rad = analizar_cargos_previos(radicales_jr_con_exp)
    total_cargos_rad = sum(cargos_previos_rad.values())
    
    for cargo in cargos_orden:
        cantidad = cargos_previos_rad.get(cargo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_cargos_rad) * 100 if total_cargos_rad > 0 else 0
            html += f"""
                    <tr>
                        <td>{cargo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_cargos_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
            </div>
        </div>
    """
    
    # Agrupamos candidatos por tipo de cargo
    diputados_nacionales = [c for c in candidatos_data if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional']
    senadores = [c for c in candidatos_data if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial']
    diputados = [c for c in candidatos_data if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial']
    
    # Usar el mismo título de sección que en el otro informe
    html += "<h2>Distribución por Tipo de Cargo</h2>"
    
    # Modificar el orden de las secciones para que coincida con el otro informe
    # Sección de Diputados Nacionales (primero)
    if diputados_nacionales:
        html += generar_seccion_cargo(
            "Diputados Nacionales", 
            diputados_nacionales, 
            [c for c in candidatos_laboristas if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional'],
            [c for c in candidatos_radicales_jr if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional']
        )
    
    # Sección de Senadores Provinciales (segundo)
    html += generar_seccion_cargo(
        "Senadores Provinciales", 
        senadores, 
        [c for c in candidatos_laboristas if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial'],
        [c for c in candidatos_radicales_jr if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial']
    )
    
    # Sección de Diputados Provinciales (tercero)
    html += generar_seccion_cargo(
        "Diputados Provinciales", 
        diputados, 
        [c for c in candidatos_laboristas if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial'],
        [c for c in candidatos_radicales_jr if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial']
    )
    
    # Sección final: Listado de todos los candidatos
    html += """
        <h2>Listado Completo de Candidatos</h2>
        
        <div class="candidate-section">
            <h3 class="section-title">Candidatos Laborista Correntino</h3>
    """
    
    # Tabla de candidatos laboristas
    html += generar_tabla_candidatos(candidatos_laboristas)
    html += """
        </div>
        
        <div class="candidate-section">
            <h3 class="section-title">Candidatos Radical (Junta Reorganizadora)</h3>
    """
    
    # Tabla de candidatos radicales JR
    html += generar_tabla_candidatos(candidatos_radicales_jr)
    html += """
        </div>
    """
    
    # Cerrar el HTML
    html += "</body></html>"
    
    return html

def generar_seccion_cargo(titulo, candidatos, candidatos_laboristas_filtrados, candidatos_radicales_jr_filtrados):
    """
    Genera una sección HTML con estadísticas comparativas para un tipo específico de cargo
    
    Args:
        titulo (str): Título de la sección (tipo de cargo)
        candidatos (list): Lista de candidatos de este tipo de cargo
        candidatos_laboristas_filtrados (list): Candidatos del Partido Laborista para este cargo
        candidatos_radicales_jr_filtrados (list): Candidatos Radicales JR para este cargo
        
    Returns:
        str: HTML de la sección para este tipo de cargo
    """
    # Importaciones necesarias para realizar análisis dentro de la función
    from scripts.helpers.analisis_candidatos_1946 import (
        analizar_partidos_previos, 
        analizar_categorias_partidos,
        analizar_periodos_historicos,
        analizar_cargos_previos
    )
    
    if not candidatos:
        return ""
        
    # Mantener el cálculo de estadísticas para referencia interna
    total = len(candidatos)
    con_experiencia = [c for c in candidatos if c.get('tiene_experiencia_previa') == True]
    porcentaje_exp = (len(con_experiencia) / total) * 100 if total > 0 else 0
    
    # Orden definido para las categorías y periodos
    orden_categorias = ["Radicales", "Autonomistas", "Liberales", "Otros"]
    periodos_orden = ["1900-1915", "1916-1930", "1931-1942", "1943-1945"]
    cargos_orden = ["Diputado Nacional", "Senador Provincial", "Diputado Provincial", 
                    "Elector Nacional", "Elector Provincial", "Otros Cargos"]
    
    # Generar HTML empezando directamente con el título y el grid container
    html = f"""
        <div class="tipo-cargo-section">
            <h3>{titulo}</h3>
            <div class="grid-container">
    """
    
    # Sección para Laboristas de este tipo de cargo
    laboristas_exp = [c for c in candidatos_laboristas_filtrados if c.get('tiene_experiencia_previa') == True]
    porcentaje_lab_exp = (len(laboristas_exp) / len(candidatos_laboristas_filtrados)) * 100 if len(candidatos_laboristas_filtrados) > 0 else 0
    
    html += f"""
                <div class="summary-box partido-laborista">
                    <h3>Laborista Correntino</h3>
                    <p><strong>Total candidatos:</strong> {len(candidatos_laboristas_filtrados)}</p>
                    <p><strong>Con experiencia previa:</strong> {len(laboristas_exp)} <span class="stat-highlight">({formato_decimal(porcentaje_lab_exp)}%)</span></p>
                
                    <h4>Partidos previos más comunes</h4>
                    <table>
                        <tr>
                            <th>Partido</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Recopilamos partidos previos para laboristas
    contador_partidos_lab = analizar_partidos_previos(laboristas_exp)
    
    for partido, cantidad in contador_partidos_lab.most_common():
        porcentaje = (cantidad / len(laboristas_exp)) * 100 if len(laboristas_exp) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
        """
    
    # Añadir fila de totales al final de la tabla
    total_candidatos_tabla_partidos_lab = sum(contador_partidos_lab.values())
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_candidatos_tabla_partidos_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
    """
    
    # NUEVA TABLA: Agrupación por familias políticas
    # Crear un contador para las categorías
    categorias_partidos_lab = analizar_categorias_partidos(contador_partidos_lab)
    
    # Agregar tabla de categorías de partidos
    html += """
                <h4>Agrupación por familias políticas</h4>
                <table>
                    <tr>
                        <th>Familia Política</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Mostrar las categorías en orden específico
    total_categorias_lab = sum(categorias_partidos_lab.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_lab.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias_lab) * 100 if total_categorias_lab > 0 else 0
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
                        <td>{total_categorias_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <!-- NUEVAS TABLAS: Distribución por períodos históricos y tipos de cargo previo -->
                <h4>Distribución por Períodos Históricos</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Periodo Histórico</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los períodos históricos para laboristas
    periodos_lab = analizar_periodos_historicos(laboristas_exp)
    total_periodos_lab = sum(periodos_lab.values())
    
    for periodo in periodos_orden:
        cantidad = periodos_lab.get(periodo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_periodos_lab) * 100 if total_periodos_lab > 0 else 0
            html += f"""
                    <tr>
                        <td>{periodo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_periodos_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <h4>Distribución por Tipo de Cargo Previo</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Cargo Previo</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los tipos de cargo previo para laboristas
    cargos_previos_lab = analizar_cargos_previos(laboristas_exp)
    total_cargos_lab = sum(cargos_previos_lab.values())
    
    for cargo in cargos_orden:
        cantidad = cargos_previos_lab.get(cargo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_cargos_lab) * 100 if total_cargos_lab > 0 else 0
            html += f"""
                    <tr>
                        <td>{cargo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_cargos_lab}</td>
                        <td>100%</td>
                    </tr>
                </table>
                </div>
    """
    
    # Sección para Radicales JR de este tipo de cargo
    radicales_exp = [c for c in candidatos_radicales_jr_filtrados if c.get('tiene_experiencia_previa') == True]
    porcentaje_rad_exp = (len(radicales_exp) / len(candidatos_radicales_jr_filtrados)) * 100 if len(candidatos_radicales_jr_filtrados) > 0 else 0
    
    html += f"""
                <div class="summary-box partido-radical">
                    <h3>Radical (Junta Reorganizadora)</h3>
                    <p><strong>Total candidatos:</strong> {len(candidatos_radicales_jr_filtrados)}</p>
                    <p><strong>Con experiencia previa:</strong> {len(radicales_exp)} <span class="stat-highlight">({formato_decimal(porcentaje_rad_exp)}%)</span></p>
                
                    <h4>Partidos previos más comunes</h4>
                    <table>
                        <tr>
                            <th>Partido</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Recopilamos partidos previos para radicales JR
    contador_partidos_rad = analizar_partidos_previos(radicales_exp)
    
    # Variable para calcular el total de candidatos mostrados en la tabla de partidos de radicales JR
    total_candidatos_tabla_partidos_rad = sum(contador_partidos_rad.values())
    
    for partido, cantidad in contador_partidos_rad.most_common():
        porcentaje = (cantidad / len(radicales_exp)) * 100 if len(radicales_exp) > 0 else 0
        html += f"""
                        <tr>
                            <td>{partido}</td>
                            <td>{cantidad}</td>
                            <td>{formato_decimal(porcentaje)}%</td>
                        </tr>
        """
    
    # Añadir fila de totales al final de la tabla
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_candidatos_tabla_partidos_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
    """
    
    # NUEVA TABLA: Agrupación por familias políticas para radicales JR
    # Crear un contador para las categorías
    categorias_partidos_rad = analizar_categorias_partidos(contador_partidos_rad)
    
    # Agregar tabla de categorías de partidos
    html += """
                <h4>Agrupación por familias políticas</h4>
                <table>
                    <tr>
                        <th>Familia Política</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Mostrar las categorías en orden específico
    total_categorias_rad = sum(categorias_partidos_rad.values())
    
    for categoria in orden_categorias:
        cantidad = categorias_partidos_rad.get(categoria, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_categorias_rad) * 100 if total_categorias_rad > 0 else 0
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
                        <td>{total_categorias_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <!-- NUEVAS TABLAS: Distribución por períodos históricos y tipos de cargo previo -->
                <h4>Distribución por Períodos Históricos</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Periodo Histórico</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los períodos históricos para radicales
    periodos_rad = analizar_periodos_historicos(radicales_exp)
    total_periodos_rad = sum(periodos_rad.values())
    
    for periodo in periodos_orden:
        cantidad = periodos_rad.get(periodo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_periodos_rad) * 100 if total_periodos_rad > 0 else 0
            html += f"""
                    <tr>
                        <td>{periodo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de períodos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_periodos_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
                
                <h4>Distribución por Tipo de Cargo Previo</h4>
                <table>
                    <tr>
                        <th class="col-nombre">Cargo Previo</th>
                        <th class="col-cantidad">Candidatos</th>
                        <th class="col-porcentaje">Porcentaje</th>
                    </tr>
    """
    
    # Analizar los tipos de cargo previo para radicales
    cargos_previos_rad = analizar_cargos_previos(radicales_exp)
    total_cargos_rad = sum(cargos_previos_rad.values())
    
    for cargo in cargos_orden:
        cantidad = cargos_previos_rad.get(cargo, 0)
        if cantidad > 0:
            porcentaje = (cantidad / total_cargos_rad) * 100 if total_cargos_rad > 0 else 0
            html += f"""
                    <tr>
                        <td>{cargo}</td>
                        <td>{cantidad}</td>
                        <td>{formato_decimal(porcentaje)}%</td>
                    </tr>
            """
    
    # Añadir fila de totales para la tabla de cargos
    html += f"""
                    <tr style="font-weight: bold; background-color: #f2f2f2;">
                        <td>Total</td>
                        <td>{total_cargos_rad}</td>
                        <td>100%</td>
                    </tr>
                </table>
            </div>
        </div>
    """
    
    return html
