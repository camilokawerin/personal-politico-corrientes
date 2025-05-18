"""
Visualization utilities for generating graphs and charts.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def generar_grafico_periodos_temporales(periodos, prefix=''):
    """Genera un gráfico de barras de los periodos temporales"""
    # Crear DataFrame para facilitar la visualización
    df = pd.DataFrame(list(periodos.items()), columns=['Periodo', 'Cantidad'])
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(df['Periodo'], df['Cantidad'], color='lightgreen')
    plt.xlabel('Periodo')
    plt.ylabel('Cantidad')
    plt.title('Distribución Temporal de Experiencia Previa')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Guardar gráfico
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{prefix}grafico_periodos_temporales.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"✓ Gráfico de periodos temporales guardado en: {output_path}")
    
    return output_path

def generar_grafico_partidos_previos(datos_trayectoria_interpartidaria, prefix=''):
    """Genera un gráfico de barras de los partidos previos"""
    if not datos_trayectoria_interpartidaria:
        return None
    
    # Crear DataFrame para facilitar la visualización
    df = pd.DataFrame(datos_trayectoria_interpartidaria)
    
    # Determinar la columna de cantidad según el tipo de datos
    cantidad_col = 'Cantidad_Legisladores' if 'Cantidad_Legisladores' in df.columns else 'Cantidad_Candidatos'
    
    # Ordenar por cantidad (de mayor a menor)
    df = df.sort_values(cantidad_col, ascending=False)
    
    # Limitar a los 10 partidos más frecuentes para mejor visualización
    if len(df) > 10:
        df = df.head(10)
    
    # Crear gráfico
    plt.figure(figsize=(12, 8))
    plt.bar(df['Partido_Previo'], df[cantidad_col], color='skyblue')
    plt.xlabel('Partido')
    plt.ylabel('Cantidad')
    plt.title('Procedencia Partidaria')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfico
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{prefix}grafico_partidos_previos.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"✓ Gráfico guardado en: {output_path}")
    
    return output_path

def generar_grafico_cargos_previos(datos_cargos, prefix=''):
    """Genera un gráfico de barras de los cargos previos"""
    if not datos_cargos:
        return None
    
    # Crear DataFrame para facilitar la visualización
    df = pd.DataFrame(datos_cargos)
    
    # Limitar a los 10 cargos más frecuentes para mejor visualización
    df = df.sort_values('Cantidad_Legisladores', ascending=False).head(10)
    
    # Crear gráfico
    plt.figure(figsize=(12, 8))
    plt.bar(df['Cargo_Previo'], df['Cantidad_Legisladores'], color='lightcoral')
    plt.xlabel('Cargo')
    plt.ylabel('Cantidad de Legisladores')
    plt.title('Cargos Previos de Legisladores Peronistas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfico
    output_dir = r"c:\Users\camil\Code\personal-politico-corrientes\informes"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{prefix}grafico_cargos_previos.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"✓ Gráfico de cargos previos guardado en: {output_path}")
    
    return output_path

def analizar_periodos_temporales(detalle_trayectorias):
        """Analiza los periodos temporales de las candidaturas previas"""
        # Definir los periodos históricos
        periodos = {
            "1900-1915": 0,
            "1916-1930": 0,
            "1931-1942": 0,
            "1946-1955": 0  # Removed "1943-1945" period as there were no elections in Latin America during this time
        }
        
        # Rastrear personas ya contadas en algún período
        personas_contadas = set()
        
        # Contar personas únicas según su primera candidatura
        for legislador in detalle_trayectorias:
            id_persona = legislador.get('ID_Persona')
            
            # Si ya contamos a esta persona, continuamos
            if id_persona in personas_contadas:
                continue
                
            primera_anno = legislador.get('Anno_Primera_Candidatura', 0)
            
            # Solo considerar candidatos con experiencia política previa
            if legislador.get('Cantidad_Candidaturas_Previas', 0) > 0:
                if 1900 <= primera_anno <= 1915:
                    periodos["1900-1915"] += 1
                    personas_contadas.add(id_persona)
                elif 1916 <= primera_anno <= 1930:
                    periodos["1916-1930"] += 1
                    personas_contadas.add(id_persona)
                elif 1931 <= primera_anno <= 1942:
                    periodos["1931-1942"] += 1
                    personas_contadas.add(id_persona)
                elif 1946 <= primera_anno <= 1955:
                    periodos["1946-1955"] += 1
                    personas_contadas.add(id_persona)
        
        return periodos
