"""
HTML generation utilities for creating reports.
"""
from datetime import datetime

def generar_encabezado_html(titulo):
    """
    Genera el encabezado estándar para un informe HTML
    """
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            h1 {{ color: #333; }}
            h2 {{ color: #555; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .card {{ background-color: #fff; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .summary {{ background-color: #f8f9fa; padding: 15px; margin-bottom: 20px; border-left: 4px solid #007bff; }}
            .timestamp {{ color: #666; font-size: 0.9em; font-style: italic; margin-bottom: 15px; }}
            .experiencia-previa {{ background-color: #e6f7ff; }}
            .partido-peronista {{ background-color: #ffebcc; }}
            img {{ max-width: 100%; height: auto; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .volver-link {{ display: inline-block; margin-top: 30px; margin-bottom: 20px; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; }}
            .volver-link:hover {{ background-color: #45a049; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <p class="timestamp">Informe generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
    """

def generar_pie_html():
    """
    Genera el pie estándar para un informe HTML
    """
    return """
        <a href="index.html" class="volver-link">Volver al índice</a>
        <footer style="margin-top: 50px; text-align: center; font-size: 0.9em; color: #666; border-top: 1px solid #ccc; padding-top: 20px;">
            <p>Proyecto de Personal Político de Corrientes - Generado mediante scripts de análisis de datos</p>
        </footer>
    </body>
    </html>
    """

def generar_pagina_index():
    """
    Genera una página de índice para todos los informes
    """
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Índice de Informes Estadísticos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; background-color: #f8f9fa; }
            h1 { color: #333; }
            .report-card { 
                background-color: #fff; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 15px 0; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                transition: transform 0.2s;
            }
            .report-card:hover { 
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
            }
            .report-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
                gap: 20px; 
                margin-top: 30px;
            }
            .report-card h3 { margin-top: 0; color: #0066cc; }
            .timestamp { color: #666; font-size: 0.9em; font-style: italic; margin-bottom: 15px; }
            .report-link { 
                display: inline-block; 
                margin-top: 15px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
            }
            .report-link:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>Índice de Informes Estadísticos</h1>
        <p class="timestamp">Última actualización: """ + fecha_actual + """</p>
          <div class="report-grid">
            <div class="report-card">
                <h3>Trayectorias Completas de Legisladores</h3>
                <p>Registro completo de las carreras políticas de todos los legisladores peronistas electos entre 1946 y 1955, incluyendo su experiencia antes, durante y después de su afiliación peronista.</p>
                <p><strong>Contenido:</strong></p>
                <ul>
                    <li>Historial político completo de cada legislador</li>
                    <li>Información sobre cargos, elecciones y partidos</li>
                    <li>Períodos de mandato y observaciones</li>
                </ul>
                <a href="trayectorias_legisladores_peronistas.html" class="report-link">Ver informe</a>
            </div>
            
            <div class="report-card">
                <h3>Trayectorias Interpartidarias</h3>
                <p>Este informe presenta estadísticas detalladas sobre los legisladores peronistas que tuvieron experiencia política previa en otros partidos entre 1946 y 1955.</p>
                <p><strong>Contenido:</strong></p>
                <ul>
                    <li>Distribución por partido de origen</li>
                    <li>Análisis temporal de la experiencia previa</li>
                    <li>Listado detallado de legisladores con trayectoria interpartidaria</li>
                </ul>
                <a href="estadisticas_trayectorias_interpartidarias.html" class="report-link">Ver informe</a>
            </div>
            
            <div class="report-card">
                <h3>Todos los Candidatos Peronistas (1946-1955)</h3>
                <p>Análisis completo de todos los candidatos de partidos peronistas entre 1946 y 1955, incluyendo trayectorias previas y estadísticas generales.</p>
                <p><strong>Contenido:</strong></p>
                <ul>
                    <li>Estadísticas de procedencia partidaria</li>
                    <li>Experiencia política previa por periodos</li>
                    <li>Listado detallado de candidatos con trayectorias interpartidarias</li>
                </ul>
                <a href="todos_candidatos_peronistas.html" class="report-link">Ver informe</a>
            </div>

            <div class="report-card">
                <h3>Candidatos Peronistas de 1946</h3>
                <p>Análisis detallado de los candidatos de los partidos Laborista Correntino y Radical (Junta Reorganizadora) en las elecciones de 1946, con enfoque en sus trayectorias políticas previas.</p>
                <p><strong>Contenido:</strong></p>
                <ul>
                    <li>Comparativa entre partidos peronistas</li>
                    <li>Estadísticas por tipo de candidatura</li>
                    <li>Listado completo de candidatos y sus antecedentes</li>
                </ul>
                <a href="candidatos_1946_trayectorias.html" class="report-link">Ver informe</a>
            </div>
        </div>
        
        <footer style="margin-top: 50px; text-align: center; font-size: 0.9em; color: #666; border-top: 1px solid #ccc; padding-top: 20px;">
            <p>Proyecto de Personal Político de Corrientes - Generado mediante scripts de análisis de datos</p>
        </footer>
    </body>
    </html>
    """
    
    # Guardar archivo index.html
    import os
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
    
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Página índice generada exitosamente en: {index_path}")
    
    return index_path
