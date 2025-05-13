"""
Generador de informes sobre trayectorias completas de legisladores peronistas.
Este módulo se encarga de generar informes sobre las trayectorias completas 
de todos los legisladores peronistas electos entre 1946 y 1955.
"""
import os
import sys
# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.commons.db_utils import ejecutar_consulta
from scripts.commons.data_retrieval import (
    obtener_legisladores_peronistas,
    obtener_trayectoria
)
from scripts.commons.html_utils import generar_encabezado_html, generar_pie_html

def generar_informe_html_legisladores_peronistas(legisladores_data):
    """Genera un informe HTML con las trayectorias completas de los legisladores peronistas"""
    html = generar_encabezado_html("Trayectorias de Legisladores Peronistas (1946-1955)")
    
    # Resumen
    html += f"""
    <div class="summary">
        <h2>Resumen</h2>
        <p>Total de legisladores peronistas analizados: <strong>{len(legisladores_data)}</strong></p>
        <p>Este informe muestra la trayectoria política completa de cada legislador, incluyendo su actividad tanto antes como después de su afiliación al peronismo.</p>
    </div>
    """
    
    # Detalle de trayectorias por legislador
    for legislador_info in legisladores_data:
        nombre_completo = legislador_info['nombre_completo']
        partido_original = legislador_info['partido']
        trayectoria = legislador_info['trayectoria']
        
        if not trayectoria:
            continue
            
        html += f"""
        <div class="card">
            <h2>{nombre_completo} <small>({partido_original})</small></h2>
            <table>
                <tr>
                    <th>Año</th>
                    <th>Cargo</th>
                    <th>Partido</th>
                    <th>Electo</th>
                    <th>Período</th>
                    <th>Observaciones</th>
                </tr>
        """
        
        for cargo in trayectoria:
            # Determinar si es un cargo del periodo peronista o experiencia previa/posterior
            es_peronista = cargo['Partido'] in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista'] and cargo['Año'] >= 1946 and cargo['Año'] <= 1955
            es_experiencia_previa = cargo['Año'] < 1946
            
            row_class = ""
            if es_peronista:
                row_class = "class='partido-peronista'"
            elif es_experiencia_previa:
                row_class = "class='experiencia-previa'"
            
            html += f"""
                <tr {row_class}>
                    <td>{cargo.get('Año', '')}</td>
                    <td>{cargo.get('Cargo', '')}</td>
                    <td>{cargo.get('Partido', '')}</td>
                    <td>{cargo.get('Electo', '')}</td>
                    <td>{cargo.get('Período', '')}</td>
                    <td>{cargo.get('Observaciones', '')}</td>
                </tr>
            """
        
        html += """
            </table>
        </div>
        """
    
    # Cerrar el HTML
    html += generar_pie_html()
    
    return html

def generar_informe_trayectorias_completas():
    """Genera el informe de trayectorias completas de legisladores peronistas"""
    print("Generando informe de trayectorias completas de legisladores peronistas...")
    
    # Obtener legisladores peronistas (1946-1955)
    print("1. Obteniendo legisladores peronistas (1946-1955)...")
    legisladores = obtener_legisladores_peronistas()
    print(f"✓ Se encontraron {len(legisladores)} legisladores.")
    
    if not legisladores:
        print("No se encontraron legisladores peronistas para analizar.")
        return False    
        
    # Obtener trayectorias para cada legislador
    print("2. Procesando datos de legisladores...")
    legisladores_data = []
    
    for legislador in legisladores:
        id_persona = legislador['ID_Persona']
        nombre_completo = legislador['Nombre_Completo']
        
        # Obtener trayectoria completa
        trayectoria = obtener_trayectoria(id_persona)
        
        if trayectoria:
            # Identificamos el partido peronista del legislador durante el período 1946-1955
            partidos_peronistas = [cargo['Partido'] for cargo in trayectoria 
                                if cargo['Partido'] in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista'] 
                                and cargo['Año'] >= 1946 and cargo['Año'] <= 1955
                                and cargo['Electo'] == 'Sí']
            
            partido = "Peronista" if not partidos_peronistas else partidos_peronistas[0]
            
            legislador_info = {
                'id_persona': id_persona,
                'nombre_completo': nombre_completo,
                'partido': partido,
                'trayectoria': trayectoria
            }
            legisladores_data.append(legislador_info)
    
    if not legisladores_data:
        print("ERROR: No se pudieron generar datos de trayectorias para los legisladores.")
        return False
        
    # Generar informe HTML de legisladores peronistas
    print("3. Generando informe HTML...")    
    html_content = generar_informe_html_legisladores_peronistas(legisladores_data)
    
    # Guardar informe HTML
    print("4. Guardando informe...")
    output_path = r"c:\Users\camil\Code\personal-politico-corrientes\informes\trayectorias_legisladores_peronistas.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Informe de trayectorias completas generado exitosamente en: {output_path}")
    return True

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_trayectorias_completas()
