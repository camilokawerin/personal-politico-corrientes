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
        "1943-1945": 0
    }
    
    # Contar legisladores activos en cada periodo
    for legislador in detalle_trayectorias:
        primera_anno = legislador.get('Anno_Primera_Candidatura', 0)
        ultima_anno = legislador.get('Anno_Ultima_Candidatura', 0)
        
        if primera_anno <= 1915 or ultima_anno <= 1915:
            periodos["1900-1915"] += 1
        if (primera_anno >= 1916 and primera_anno <= 1930) or (ultima_anno >= 1916 and ultima_anno <= 1930):
            periodos["1916-1930"] += 1
        if (primera_anno >= 1931 and primera_anno <= 1942) or (ultima_anno >= 1931 and ultima_anno <= 1942):
            periodos["1931-1942"] += 1
        if (primera_anno >= 1943 and primera_anno <= 1945) or (ultima_anno >= 1943 and ultima_anno <= 1945):
            periodos["1943-1945"] += 1
    
    return periodos

def agrupar_cargos_por_tipo(datos_cargos, detalle_trayectorias):
    """
    Agrupa los cargos por tipo (Legislativo, Ejecutivo, etc.) contando personas únicas
    
    Args:
        datos_cargos: Lista de diccionarios con datos de cargos previos
        detalle_trayectorias: Datos detallados de cada legislador para obtener total correcto
    """
    # Definir categorías de cargos
    categorias = {
        'Legislativo': ['Diputado', 'Senador', 'Convencional', 'Concejal'],
        'Ejecutivo': ['Gobernador', 'Intendente', 'Ministro', 'Secretario', 'Presidente'],
        'Judicial': ['Juez', 'Fiscal'],
        'Otros': []
    }
    
    # Crear diccionario para rastrear las personas en cada categoría
    personas_por_categoria = {categoria: set() for categoria in categorias.keys()}
    
    # Recorrer todos los legisladores y sus cargos previos
    for legislador in detalle_trayectorias:
        id_persona = legislador['ID_Persona']
        cargos_previos = legislador['Cargos_Previos'].split(', ')
        
        # Asignar cada persona a las categorías correspondientes a sus cargos
        for cargo_previo in cargos_previos:
            cargo_nombre = cargo_previo.split(' ')[0]  # Extraer nombre del cargo sin ámbito
            
            # Determinar la categoría del cargo
            categoria_asignada = 'Otros'
            for categoria, tipos_cargos in categorias.items():
                if any(tipo in cargo_nombre for tipo in tipos_cargos):
                    categoria_asignada = categoria
                    break
            
            # Registrar que esta persona ocupó un cargo de esta categoría
            personas_por_categoria[categoria_asignada].add(id_persona)
    
    # Contar personas únicas por categoría
    resultados = {categoria: len(personas) for categoria, personas in personas_por_categoria.items()}
        
    return resultados
