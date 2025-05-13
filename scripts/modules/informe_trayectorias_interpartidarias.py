"""
Generador de informes sobre trayectorias interpartidarias.
Este módulo se encarga de generar informes sobre los legisladores
peronistas que tuvieron trayectorias en otros partidos políticos.
"""
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import shutil
# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.commons.db_utils import ejecutar_consulta
from scripts.commons.data_retrieval import (
    obtener_estadisticas_trayectoria_interpartidaria,
    obtener_detalle_trayectoria_interpartidaria,
    obtener_estadisticas_cargos_previos,
    obtener_cargos_peronistas
)
from scripts.commons.visualization import (
    generar_grafico_partidos_previos,
    generar_grafico_periodos_temporales,
    generar_grafico_cargos_previos,
    analizar_periodos_temporales,
    agrupar_cargos_por_tipo
)
from scripts.commons.html_utils import generar_encabezado_html, generar_pie_html

def generar_informe_html(datos_trayectoria_interpartidaria, detalle_trayectorias, datos_cargos=None, ruta_grafico=None, ruta_grafico_periodos=None, ruta_grafico_cargos=None):
    """Genera un informe HTML con estadísticas de trayectorias interpartidarias"""
    # Calcular total de legisladores con experiencia previa en otros partidos
    total_legisladores = len(detalle_trayectorias) if detalle_trayectorias else 0
    
    # Calcular promedio de candidaturas previas
    promedio_candidaturas = 0
    antiguedad_promedio = 0
    if detalle_trayectorias:
        suma_candidaturas = sum(item['Cantidad_Candidaturas_Previas'] for item in detalle_trayectorias)
        promedio_candidaturas = suma_candidaturas / total_legisladores
        
        # Calcular antigüedad promedio (años entre primera candidatura y entrada al peronismo)
        suma_antiguedad = sum(item['Anno_Peronista'] - item['Anno_Primera_Candidatura'] for item in detalle_trayectorias)
        antiguedad_promedio = suma_antiguedad / total_legisladores

    # Analizar periodos históricos
    periodos = analizar_periodos_temporales(detalle_trayectorias) if detalle_trayectorias else {}
      # Analizar tipos de cargos
    tipos_cargos = agrupar_cargos_por_tipo(datos_cargos, detalle_trayectorias) if datos_cargos and detalle_trayectorias else {}
    
    # Generar el contenido HTML
    html = f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Estadísticas de Legisladores Peronistas (1946-1955)</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            h1, h2 {{ color: #333; }}
            h2 {{ margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .summary-box {{ margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4CAF50; }}
            .chart-container {{ margin: 20px 0; text-align: center; }}
            .grid-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .grid-container-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
            @media (max-width: 768px) {{ 
                .grid-container {{ grid-template-columns: 1fr; }} 
                .grid-container-3 {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <h1>Estadísticas de Legisladores Peronistas con Trayectoria Política Previa</h1>
        <p>Informe generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        
        <div class="grid-container">
            <div class="summary-box">
                <h3>Resumen General</h3>
                <p><strong>Total de legisladores con experiencia previa:</strong> {total_legisladores}</p>
                <p><strong>Promedio de candidaturas previas por legislador:</strong> {promedio_candidaturas:.2f}</p>
                <p><strong>Antigüedad política promedio antes del peronismo:</strong> {antiguedad_promedio:.1f} años</p>
            </div>
            
            <div class="summary-box">
                <h3>Periodos Históricos</h3>
                <p><strong>1900-1915:</strong> {periodos.get("1900-1915", 0)} legisladores</p>
                <p><strong>1916-1930:</strong> {periodos.get("1916-1930", 0)} legisladores</p>
                <p><strong>1931-1942:</strong> {periodos.get("1931-1942", 0)} legisladores</p>
                <p><strong>1943-1945:</strong> {periodos.get("1943-1945", 0)} legisladores</p>
            </div>
        </div>
    
        <div class="summary-box">
            <h3>Distribución por Tipo de Cargo</h3>
            <div class="grid-container">
    """
    
    # Agregar tipos de cargos
    for tipo, cantidad in tipos_cargos.items():
        if cantidad > 0:
            porcentaje = (cantidad / total_legisladores) * 100 if total_legisladores > 0 else 0
            html += f"""
                <div>
                    <p><strong>{tipo}:</strong> {cantidad} legisladores ({porcentaje:.1f}%)</p>
                </div>
            """
    
    html += """
            </div>
        </div>
    """
    
    # Agregar sección de gráficos
    html += """
        <div class="grid-container-3">
    """
    
    # Gráficos
    if ruta_grafico:
        html += f"""
            <div class="chart-container">
                <h2>Procedencia Partidaria</h2>
                <img src="{os.path.basename(ruta_grafico)}" alt="Gráfico de partidos previos" style="max-width: 100%;">
            </div>
        """
    
    if ruta_grafico_periodos:
        html += f"""
            <div class="chart-container">
                <h2>Distribución Temporal</h2>
                <img src="{os.path.basename(ruta_grafico_periodos)}" alt="Gráfico de períodos temporales" style="max-width: 100%;">
            </div>
        """
    
    if ruta_grafico_cargos:
        html += f"""
            <div class="chart-container">
                <h2>Cargos Previos</h2>
                <img src="{os.path.basename(ruta_grafico_cargos)}" alt="Gráfico de cargos previos" style="max-width: 100%;">
            </div>
        """
    
    html += """
        </div>
    """
    
    # Agregar tabla con detalle de estadísticas por partido
    if datos_trayectoria_interpartidaria:
        html += f"""
        <h2>Distribución por Partido Previo</h2>
        <table>
            <tr>
                <th>Partido Previo</th>
                <th>Cantidad de Legisladores</th>
                <th>Porcentaje</th>
                <th>Año Más Antiguo</th>
                <th>Año Más Reciente</th>
            </tr>
        """
        
        for partido in datos_trayectoria_interpartidaria:
            porcentaje = (partido['Cantidad_Legisladores'] / total_legisladores) * 100 if total_legisladores > 0 else 0
            html += f"""
            <tr>
                <td>{partido['Partido_Previo']}</td>
                <td>{partido['Cantidad_Legisladores']}</td>
                <td>{porcentaje:.2f}%</td>
                <td>{partido['Anno_Min']}</td>
                <td>{partido['Anno_Max']}</td>
            </tr>
            """
        
        html += """
        </table>
        """
    
    # Agregar tabla de cargos previos
    if datos_cargos:
        html += f"""
        <h2>Distribución por Cargo Previo</h2>
        <table>
            <tr>
                <th>Cargo Previo</th>
                <th>Cantidad de Legisladores</th>
                <th>Electos</th>
                <th>Año Más Antiguo</th>
                <th>Año Más Reciente</th>
            </tr>
        """
        
        for cargo in datos_cargos:
            html += f"""
            <tr>
                <td>{cargo['Cargo_Previo']}</td>
                <td>{cargo['Cantidad_Legisladores']}</td>
                <td>{cargo['Total_Electos']}</td>
                <td>{cargo['Anno_Min']}</td>
                <td>{cargo['Anno_Max']}</td>
            </tr>
            """
        
        html += """
        </table>
        """
    
    # Agregar tabla con detalle de trayectorias individuales
    if detalle_trayectorias:
        html += f"""        <h2>Detalle de Legisladores con Trayectoria Política Interpartidaria</h2>
        <table>
            <tr>
                <th rowspan="2">Nombre Completo</th>
                <th colspan="3" style="border-bottom: 2px solid #4CAF50; background-color: #e8f5e9;">Trayectoria Peronista</th>
                <th colspan="5" style="border-bottom: 2px solid #2196F3; background-color: #e3f2fd;">Trayectoria Previa</th>
            </tr>
            <tr>
                <th>Cargos Durante Peronismo</th>
                <th>Candidaturas</th>
                <th>Primera candidatura peronista</th>
                <th>Partidos Previos</th>
                <th>Cargos Previos</th>
                <th>Candidaturas Previas</th>
                <th>Primera Candidatura</th>
                <th>Experiencia (años)</th>
            </tr>
        """# Obtener cargos durante peronismo de cada legislador
        cargos_peronistas = {}
        candidaturas_peronistas = {}
        try:
            datos_cargos_peronistas = obtener_cargos_peronistas()
            for cargo in datos_cargos_peronistas:
                cargos_peronistas[cargo['ID_Persona']] = cargo['Cargos_Peronismo']
                candidaturas_peronistas[cargo['ID_Persona']] = cargo['Cantidad_Candidaturas_Peronistas']
        except Exception as e:
            print(f"Error al obtener cargos peronistas: {e}")
            
        for legislador in detalle_trayectorias:
            cargos_peronismo = cargos_peronistas.get(legislador['ID_Persona'], "No disponible")
            cantidad_candidaturas = candidaturas_peronistas.get(legislador['ID_Persona'], 0)
            experiencia_anos = legislador['Anno_Peronista'] - legislador['Anno_Primera_Candidatura']
            
            html += f"""
            <tr>
                <td>{legislador['Nombre_Completo']}</td>
                <td>{cargos_peronismo}</td>
                <td>{cantidad_candidaturas}</td>
                <td>{legislador['Anno_Peronista']}</td>
                <td>{legislador['Partidos_Previos']}</td>
                <td>{legislador['Cargos_Previos']}</td>
                <td>{legislador['Cantidad_Candidaturas_Previas']}</td>
                <td>{legislador['Anno_Primera_Candidatura']}</td>
                <td>{experiencia_anos}</td>
            </tr>
            """
        
        html += """
        </table>
        <p><small>(*) Indica que el legislador fue electo para ese cargo.</small></p>
        """
    
    # Cerrar el HTML
    html += """
    </body>
    </html>
    """
    
    return html

def generar_informe_trayectorias_interpartidarias():
    """Genera el informe completo de trayectorias interpartidarias"""
    print("Generando informe de trayectorias interpartidarias...")
    
    # Obtener datos para el informe
    print("1. Obteniendo datos y estadísticas...")
    datos_trayectoria_interpartidaria = obtener_estadisticas_trayectoria_interpartidaria()
    detalle_trayectorias = obtener_detalle_trayectoria_interpartidaria()
    datos_cargos = obtener_estadisticas_cargos_previos()
    
    if not detalle_trayectorias:
        print("No se encontraron datos para el análisis de trayectorias interpartidarias.")
        return False
      # Generar gráficos para el informe
    print("2. Generando gráficos para el informe...")
      # Asegurarse de que los gráficos se guarden directamente en la carpeta correcta
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar gráfico de partidos previos directamente en la carpeta final
    prefix = ""  # No usar prefijo para que coincida con el informe original
    ruta_grafico = os.path.join(output_dir, "grafico_partidos_previos.png")
    plt.figure(figsize=(12, 8))
    
    # Crear DataFrame para visualizar datos de partidos
    df = pd.DataFrame(datos_trayectoria_interpartidaria)
    df = df.sort_values('Cantidad_Legisladores', ascending=False)
    
    # Crear gráfico
    plt.bar(df['Partido_Previo'], df['Cantidad_Legisladores'], color='skyblue')
    plt.xlabel('Partido')
    plt.ylabel('Cantidad')
    plt.title('Procedencia Partidaria')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfico directamente
    plt.savefig(ruta_grafico)
    plt.close()
    
    print(f"✓ Gráfico guardado en: {ruta_grafico}")
      # Analizar periodos temporales
    periodos = analizar_periodos_temporales(detalle_trayectorias)
    
    # Generar gráfico de periodos directamente en la carpeta final
    ruta_grafico_periodos = os.path.join(output_dir, "grafico_periodos_temporales.png")
    plt.figure(figsize=(10, 6))
    df_periodos = pd.DataFrame(list(periodos.items()), columns=['Periodo', 'Cantidad'])
    plt.bar(df_periodos['Periodo'], df_periodos['Cantidad'], color='lightgreen')
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad')
    plt.title('Distribución Temporal de Experiencia Previa')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(ruta_grafico_periodos)
    plt.close()
    print(f"✓ Gráfico de periodos guardado en: {ruta_grafico_periodos}")
    
    # Generar gráfico de cargos previos directamente en la carpeta final
    ruta_grafico_cargos = os.path.join(output_dir, "grafico_cargos_previos.png")
    if datos_cargos:
        plt.figure(figsize=(12, 8))
        df_cargos = pd.DataFrame(datos_cargos)
        df_cargos = df_cargos.sort_values('Cantidad_Legisladores', ascending=False).head(10)
        plt.bar(df_cargos['Cargo_Previo'], df_cargos['Cantidad_Legisladores'], color='lightcoral')
        plt.xlabel('Cargo')
        plt.ylabel('Cantidad de Legisladores')
        plt.title('Cargos Previos de Legisladores Peronistas')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(ruta_grafico_cargos)
        plt.close()
        print(f"✓ Gráfico de cargos previos guardado en: {ruta_grafico_cargos}")
    
    # Generar informe HTML
    print("3. Generando informe HTML...")
    html_content = generar_informe_html(
        datos_trayectoria_interpartidaria, 
        detalle_trayectorias, 
        datos_cargos,
        ruta_grafico,
        ruta_grafico_periodos,
        ruta_grafico_cargos
    )
      # Guardar informe HTML
    print("4. Guardando informe...")
    output_path = r"c:\Users\camil\Code\personal-politico-corrientes\informes\estadisticas_trayectorias_interpartidarias.html"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Informe de trayectorias interpartidarias generado exitosamente en: {output_path}")
    return True

if __name__ == "__main__":
    # Este código se ejecuta si el archivo se corre directamente
    generar_informe_trayectorias_interpartidarias()
