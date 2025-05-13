"""
Generador de informes sobre candidatos peronistas de 1946.
Este módulo se encarga de generar informes específicos sobre los candidatos
de los partidos peronistas (Laborista Correntino y Radical Junta Reorganizadora)
en las elecciones de 1946.
"""
import os
import sys
from datetime import datetime
from collections import Counter, defaultdict
# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.commons.db_utils import ejecutar_consulta
from scripts.commons.data_retrieval import (
    obtener_candidatos_1946,
    obtener_trayectoria,
    obtener_detalle_trayectoria_candidatos_peronistas
)
from scripts.commons.html_utils import generar_encabezado_html, generar_pie_html

def generar_informe_html_candidatos_1946(candidatos_data):
    """Genera un informe HTML con los datos de los candidatos peronistas de 1946"""
    html = """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Candidatos Peronistas de 1946 - Trayectorias Previas</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
            h1, h2, h3, h4 { color: #333; }            h2 { margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
            h3 { margin-top: 25px; padding: 5px; }
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
            .tipo-cargo-section { margin-top: 30px; border-top: 1px dashed #999; padding-top: 20px; }
            @media (max-width: 768px) { .grid-container { grid-template-columns: 1fr; } }            .stat-highlight { font-size: 1.2em; font-weight: bold; color: #0066cc; }
            .section-title { padding: 10px; text-align: left; 
                         border: none; margin-bottom: 0; margin-top: 0; }
            .candidate-section { background-color: white; padding: 10px; border: 1px solid #ddd; margin-bottom: 20px; }        </style>
    </head><body>
        <h1>Candidatos de Partidos Peronistas en las Elecciones de 1946</h1>
        <p>Informe generado el: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
    """
    
    # Analizamos los datos para el resumen
    total_candidatos = len(candidatos_data)
    candidatos_laboristas = [c for c in candidatos_data if c['partido'] == 'Laborista Correntino']
    candidatos_radicales_jr = [c for c in candidatos_data if c['partido'] == 'Radical (Junta Reorganizadora)']
    
    total_electos = sum(1 for c in candidatos_data if c['electo'] == 'Sí')
    total_laboristas_electos = sum(1 for c in candidatos_laboristas if c['electo'] == 'Sí')
    total_radicales_jr_electos = sum(1 for c in candidatos_radicales_jr if c['electo'] == 'Sí')
    
    candidatos_con_experiencia = [c for c in candidatos_data if c['tiene_experiencia_previa']]
    porcentaje_con_experiencia = (len(candidatos_con_experiencia) / total_candidatos) * 100 if total_candidatos > 0 else 0
    
    # Contamos los candidatos con experiencia previa por partido
    laboristas_con_exp = [c for c in candidatos_laboristas if c['tiene_experiencia_previa']]
    radicales_jr_con_exp = [c for c in candidatos_radicales_jr if c['tiene_experiencia_previa']]
    
    # Calculamos porcentajes
    porc_laboristas_con_exp = (len(laboristas_con_exp) / len(candidatos_laboristas)) * 100 if len(candidatos_laboristas) > 0 else 0
    porc_radicales_jr_con_exp = (len(radicales_jr_con_exp) / len(candidatos_radicales_jr)) * 100 if len(candidatos_radicales_jr) > 0 else 0
    
    # Resumen general
    html += f"""
        <div class="summary-box">
            <h2>Resumen General</h2>
            <p><strong>Total de candidatos analizados:</strong> {total_candidatos}</p>
            <p><strong>Candidatos con experiencia política previa:</strong> {len(candidatos_con_experiencia)} <span class="stat-highlight">({porcentaje_con_experiencia:.1f}%)</span></p>
        </div>

        <h2>Estadísticas Comparativas por Partido (Todos los Candidatos)</h2>
        <div class="grid-container">
    """
    
    # Sección de Laboristas
    html += f"""
            <div class="summary-box partido-laborista">
                <h3>Laborista Correntino</h3>
                <p><strong>Total candidatos:</strong> {len(candidatos_laboristas)}</p>
                <p><strong>Con experiencia previa:</strong> {len(laboristas_con_exp)} <span class="stat-highlight">({porc_laboristas_con_exp:.1f}%)</span></p>
    """
    
    # Analizar partidos previos de laboristas
    partidos_previos_laboristas = []
    for candidato in laboristas_con_exp:
        if candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            partidos_previos_laboristas.extend(partidos)
    
    contador_partidos_laboristas = Counter(partidos_previos_laboristas)
    
    # Mostrar tabla de partidos previos para laboristas
    html += """
                <h4>Partidos previos más comunes</h4>
                <table>
                    <tr>
                        <th>Partido</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    for partido, cantidad in contador_partidos_laboristas.most_common():
        porcentaje = (cantidad / len(laboristas_con_exp)) * 100 if len(laboristas_con_exp) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{porcentaje:.1f}%</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
    """
    
    # Sección de Radicales JR
    html += f"""
            <div class="summary-box partido-radical">
                <h3>Radical (Junta Reorganizadora)</h3>
                <p><strong>Total candidatos:</strong> {len(candidatos_radicales_jr)}</p>
                <p><strong>Con experiencia previa:</strong> {len(radicales_jr_con_exp)} <span class="stat-highlight">({porc_radicales_jr_con_exp:.1f}%)</span></p>
    """
    
    # Analizar partidos previos de radicales jr
    partidos_previos_radicales = []
    for candidato in radicales_jr_con_exp:
        if candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            partidos_previos_radicales.extend(partidos)
    
    contador_partidos_radicales = Counter(partidos_previos_radicales)
    
    # Mostrar tabla de partidos previos para radicales jr
    html += """
                <h4>Partidos previos más comunes</h4>
                <table>
                    <tr>
                        <th>Partido</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    for partido, cantidad in contador_partidos_radicales.most_common():
        porcentaje = (cantidad / len(radicales_jr_con_exp)) * 100 if len(radicales_jr_con_exp) > 0 else 0
        html += f"""
                    <tr>
                        <td>{partido}</td>
                        <td>{cantidad}</td>
                        <td>{porcentaje:.1f}%</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
        </div>
    """
    
    # Agrupamos candidatos por tipo de cargo
    diputados = [c for c in candidatos_data if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial']
    senadores = [c for c in candidatos_data if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial']
    diputados_nacionales = [c for c in candidatos_data if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional']
    
    # Sección de Diputados Provinciales
    html += generar_seccion_cargo(
        "Diputados Provinciales", 
        diputados, 
        [c for c in candidatos_laboristas if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial'],
        [c for c in candidatos_radicales_jr if c['cargo'] == 'Diputado' and c['ambito'] == 'Provincial']
    )
    
    # Sección de Senadores Provinciales
    html += generar_seccion_cargo(
        "Senadores Provinciales", 
        senadores, 
        [c for c in candidatos_laboristas if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial'],
        [c for c in candidatos_radicales_jr if c['cargo'] == 'Senador' and c['ambito'] == 'Provincial']
    )
    
    # Sección de Diputados Nacionales
    if diputados_nacionales:
        html += generar_seccion_cargo(
            "Diputados Nacionales", 
            diputados_nacionales, 
            [c for c in candidatos_laboristas if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional'],
            [c for c in candidatos_radicales_jr if c['cargo'] == 'Diputado' and c['ambito'] == 'Nacional']
        )
    
    # Cerrar las secciones de estadísticas comparativas
    html += """
    </div>
    """
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
    """Genera una sección con estadísticas comparativas por tipo de cargo"""
    if not candidatos:
        return ""
        
    # Calculamos estadísticas generales para este tipo de cargo
    total = len(candidatos)
    con_experiencia = [c for c in candidatos if c['tiene_experiencia_previa']]
    porcentaje_exp = (len(con_experiencia) / total) * 100 if total > 0 else 0
    
    # Recopilamos partidos previos más comunes
    partidos_previos = []
    for candidato in con_experiencia:
        if candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            partidos_previos.extend(partidos)
    
    contador_partidos = Counter(partidos_previos)
    
    html = f"""
        <div class="tipo-cargo-section">
            <h2>Estadísticas Comparativas: {titulo}</h2>
            <div class="summary-box">
                <p><strong>Total candidatos:</strong> {total}</p>
                <p><strong>Con experiencia previa:</strong> {len(con_experiencia)} <span class="stat-highlight">({porcentaje_exp:.1f}%)</span></p>
                
                <h4>Procedencia partidaria principal</h4>
                <table>
                    <tr>
                        <th>Partido Previo</th>
                        <th>Candidatos</th>
                        <th>Porcentaje</th>
                    </tr>
    """
    
    # Generamos filas de la tabla de partidos previos
    for partido, cantidad in contador_partidos.most_common():
        porcentaje = (cantidad / len(con_experiencia)) * 100 if len(con_experiencia) > 0 else 0
        html += f"""
            <tr>
                <td>{partido}</td>
                <td>{cantidad}</td>
                <td>{porcentaje:.1f}%</td>
            </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="grid-container">
    """
    
    # Sección para Laboristas de este tipo de cargo
    laboristas_exp = [c for c in candidatos_laboristas_filtrados if c['tiene_experiencia_previa']]
    porcentaje_lab_exp = (len(laboristas_exp) / len(candidatos_laboristas_filtrados)) * 100 if len(candidatos_laboristas_filtrados) > 0 else 0
    
    html += f"""
                <div class="summary-box partido-laborista">
                    <h3>Laborista Correntino</h3>
                    <p><strong>Total candidatos:</strong> {len(candidatos_laboristas_filtrados)}</p>
                    <p><strong>Con experiencia previa:</strong> {len(laboristas_exp)} <span class="stat-highlight">({porcentaje_lab_exp:.1f}%)</span></p>
                
                    <h4>Partidos previos más comunes</h4>
                    <table>
                        <tr>
                            <th>Partido</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Recopilamos partidos previos para laboristas
    partidos_previos_lab = []
    for candidato in laboristas_exp:
        if candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            partidos_previos_lab.extend(partidos)
    
    contador_partidos_lab = Counter(partidos_previos_lab)
    
    for partido, cantidad in contador_partidos_lab.most_common():
        porcentaje = (cantidad / len(laboristas_exp)) * 100 if len(laboristas_exp) > 0 else 0
        html += f"""
                        <tr>
                            <td>{partido}</td>
                            <td>{cantidad}</td>
                            <td>{porcentaje:.1f}%</td>
                        </tr>
        """
    
    html += """
                    </table>
                </div>
    """
    
    # Sección para Radicales JR de este tipo de cargo
    radicales_exp = [c for c in candidatos_radicales_jr_filtrados if c['tiene_experiencia_previa']]
    porcentaje_rad_exp = (len(radicales_exp) / len(candidatos_radicales_jr_filtrados)) * 100 if len(candidatos_radicales_jr_filtrados) > 0 else 0
    
    html += f"""
                <div class="summary-box partido-radical">
                    <h3>Radical (Junta Reorganizadora)</h3>
                    <p><strong>Total candidatos:</strong> {len(candidatos_radicales_jr_filtrados)}</p>
                    <p><strong>Con experiencia previa:</strong> {len(radicales_exp)} <span class="stat-highlight">({porcentaje_rad_exp:.1f}%)</span></p>
                
                    <h4>Partidos previos más comunes</h4>
                    <table>
                        <tr>
                            <th>Partido</th>
                            <th>Candidatos</th>
                            <th>Porcentaje</th>
                        </tr>
    """
    
    # Recopilamos partidos previos para radicales JR
    partidos_previos_rad = []
    for candidato in radicales_exp:
        if candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            partidos_previos_rad.extend(partidos)
    
    contador_partidos_rad = Counter(partidos_previos_rad)
    
    for partido, cantidad in contador_partidos_rad.most_common():
        porcentaje = (cantidad / len(radicales_exp)) * 100 if len(radicales_exp) > 0 else 0
        html += f"""
                        <tr>
                            <td>{partido}</td>
                            <td>{cantidad}</td>
                            <td>{porcentaje:.1f}%</td>
                        </tr>
        """
    
    html += """
                    </table>
                </div>
            </div>
        </div>
    """
    
    return html

def generar_tabla_candidatos(candidatos):
    """Genera una tabla HTML con los datos de los candidatos"""
    html = """
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
    # Definir orden personalizado para los cargos
    def orden_cargo(candidato):
        cargo = candidato['cargo']
        ambito = candidato['ambito']
        
        # Orden definido: Diputado Nacional, Senador Provincial, Diputado Provincial, Elector Provincial
        if cargo == 'Diputado' and ambito == 'Nacional':
            return 1
        elif cargo == 'Senador' and ambito == 'Provincial':
            return 2
        elif cargo == 'Diputado' and ambito == 'Provincial':
            return 3
        elif cargo == 'Elector' and ambito == 'Provincial':
            return 4
        else:
            # Cualquier otro cargo no especificado va al final
            return 5
    
    # Ordenar candidatos por tipo de cargo y nombre
    candidatos_ordenados = sorted(candidatos, key=lambda c: (orden_cargo(c), c['nombre_completo']))
    
    # Generar tabla con numeración
    for i, candidato in enumerate(candidatos_ordenados, 1):
        # Construir lista de todos los cargos en los que participó en partidos peronistas
        cargos_lista = []
        
        # Obtener el cargo actual (siempre peronista en este informe)
        cargo_actual = f"{candidato['cargo']} {candidato['ambito']}"
        
        # Añadir el cargo actual con indicador de electo si corresponde
        if candidato['electo'] == 'Sí':
            cargos_lista.append(f"{cargo_actual} (*)")
        else:
            cargos_lista.append(cargo_actual)
        
        # Solo buscar otras candidaturas peronistas previas en la trayectoria, si existe
        num_candidaturas_peronistas = 1  # La candidatura actual de 1946
        
        if candidato.get('trayectoria'):
            for registro in candidato.get('trayectoria', []):
                # Solo considerar cargos previos de partidos peronistas que no sea el cargo actual
                if (registro.get('Año', 0) < 1946 and 
                    registro.get('Partido') in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista']):
                    cargo_text = registro.get('Cargo', '')
                    
                    # Añadir indicador de electo si corresponde
                    electo_valor = registro.get('Electo', '')
                    if (isinstance(electo_valor, str) and electo_valor == 'Sí') or (isinstance(electo_valor, (int, bool)) and electo_valor):
                        cargo_text += " (*)"
                    
                    # Verificar si el cargo ya está en la lista
                    if cargo_text and cargo_text not in [c.replace(" (*)", "") for c in cargos_lista]:
                        cargos_lista.append(cargo_text)
                        num_candidaturas_peronistas += 1  # Incrementar contador solo para partidos peronistas
        
        # Concatenar todos los cargos
        cargos_concatenados = ", ".join(cargos_lista)
        
        # Obtener datos de experiencia previa
        primera_candidatura = ""
        experiencia_anos = ""
        cargos_previos = candidato.get('cargos_previos', '')
        
        # Calcular experiencia (años) y primera candidatura
        if candidato.get('tiene_experiencia_previa'):
            # Obtener el año más antiguo en la trayectoria previa
            candidaturas_previas = 0
            for registro in candidato.get('trayectoria', []):
                anno = registro.get('Año', 0)
                if anno < 1946:  # año anterior a 1946 (primera candidatura peronista)
                    candidaturas_previas += 1
                    if not primera_candidatura or anno < int(primera_candidatura):
                        primera_candidatura = str(anno)
                        
            if primera_candidatura:
                experiencia_anos = 1946 - int(primera_candidatura)
        else:
            candidaturas_previas = 0
        
        # Manejar valores nulos/vacíos
        partidos_previos = candidato.get('partidos_previos', '')
        if partidos_previos == '-' or partidos_previos == 'None' or partidos_previos is None:
            partidos_previos = ''
        
        html += f"""
            <tr>
                <td>{i}</td>
                <td>{candidato['nombre_completo']}</td>
                <td>{cargos_concatenados}</td>
                <td>{num_candidaturas_peronistas}</td>
                <td>1946</td>
                <td>{partidos_previos}</td>
                <td>{cargos_previos}</td>
                <td>{candidaturas_previas}</td>
                <td>{primera_candidatura}</td>
                <td>{experiencia_anos}</td>
            </tr>
        """
    
    html += """
        </table>
    """
    
    return html

def generar_informe_candidatos_1946():
    """Genera el informe de candidatos peronistas de 1946"""
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
    candidatos_data = []
    
    for candidato in candidatos:
        id_persona = candidato['ID_Persona']
        nombre_completo = candidato['Nombre_Completo']
        partido = candidato['Partido']
        cargo = candidato['Cargo']
        ambito = candidato['Ambito']
        electo = 'Sí' if candidato['Electo'] == 1 else 'No'
        
        # Verificamos si tiene experiencia política previa
        tiene_experiencia_previa = False
        partidos_previos = []
        cargos_previos = ""
        
        # Buscamos en el listado de candidatos con experiencia previa
        for exp in candidatos_con_experiencia:
            if exp['ID_Persona'] == id_persona:
                tiene_experiencia_previa = True
                partidos_previos = exp.get('Partidos_Previos', '')
                if partidos_previos and partidos_previos != 'None':
                    partidos_previos = partidos_previos.split(', ')
                else:
                    partidos_previos = []
                
                cargos_previos = exp.get('Cargos_Previos', '')
                if cargos_previos == 'None':
                    cargos_previos = ''
                break
        
        candidato_info = {
            'id_persona': id_persona,
            'nombre_completo': nombre_completo,
            'partido': partido,
            'cargo': cargo,
            'ambito': ambito,
            'electo': electo,
            'tiene_experiencia_previa': tiene_experiencia_previa,
            'partidos_previos': ", ".join(partidos_previos) if partidos_previos else "",
            'cargos_previos': cargos_previos if cargos_previos else ""
        }
        
        # Añadir la trayectoria al candidato después de crear toda la información básica
        trayectoria_candidato = []
        
        # Agregar el cargo actual como parte de la trayectoria
        trayectoria_candidato.append({
            'Cargo': f"{cargo} {ambito}",
            'Electo': electo,
            'Partido': partido,
            'Año': 1946  # Año fijo para las elecciones analizadas en este informe
        })
        
        # Si tiene experiencia previa, obtener toda la trayectoria de la base de datos
        if tiene_experiencia_previa:
            trayectoria_previa = obtener_trayectoria(id_persona)
            # Filtrar solo las entradas previas a 1946
            trayectoria_previa = [t for t in trayectoria_previa if t.get('Año', 0) < 1946]
            # Añadir a la lista de trayectoria
            trayectoria_candidato.extend(trayectoria_previa)
        
        candidato_info['trayectoria'] = trayectoria_candidato
        
        candidatos_data.append(candidato_info)
    
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

# Esta función ya no es necesaria ya que la trayectoria se construye directamente en generar_informe_candidatos_1946

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_candidatos_1946()
