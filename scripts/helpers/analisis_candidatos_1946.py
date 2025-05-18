# -*- coding: utf-8 -*-
"""
Análisis de datos para el informe de candidatos de 1946.
Este módulo contiene funciones para analizar datos de candidatos
y preparar información para los informes.
"""
from collections import Counter

from scripts.helpers.utilidades_candidatos_1946 import categorizar_partido

def procesar_datos_candidatos(candidatos, candidatos_con_experiencia, obtener_trayectoria):
    """
    Procesa los datos de los candidatos, añadiendo información sobre experiencia previa,
    partidos previos y trayectoria.
    
    Args:
        candidatos (list): Lista de candidatos de las elecciones de 1946
        candidatos_con_experiencia (list): Lista de candidatos con información de experiencia previa
        obtener_trayectoria (function): Función para obtener la trayectoria de un candidato
        
    Returns:
        list: Lista de candidatos con información adicional procesada
    """
    candidatos_data = []
    
    for candidato in candidatos:
        id_persona = candidato['ID_Persona']
        nombre_completo = candidato['Nombre_Completo']
        partido = candidato['Partido']
        cargo = candidato['Cargo']
        ambito = candidato['Ambito']
        electo = 'Sí' if candidato['Electo'] == 1 else 'No'
        
        # Verificamos si tiene experiencia política previa
        # Inicializar a False explícitamente
        tiene_experiencia_previa = False
        partidos_previos = []
        partido_principal = None  # Nuevo campo para almacenar el partido principal según prioridad
        cargos_previos = ""
        
        # Buscamos en el listado de candidatos con experiencia previa
        for exp in candidatos_con_experiencia:
            if exp['ID_Persona'] == id_persona:
                # Solo marcar como True si realmente hay candidaturas previas
                if exp.get('Cantidad_Candidaturas_Previas', 0) > 0:
                    tiene_experiencia_previa = True
                    # Obtener el partido principal (si existe en el resultado)
                    partido_principal = exp.get('Partido_Principal', '')
                    partidos_previos = exp.get('Partidos_Previos', '')
                    if partidos_previos and partidos_previos != 'None':
                        partidos_previos = [p.strip() for p in partidos_previos.split(',') if p.strip()]
                    else:
                        partidos_previos = []
                        
                    # Obtener cargos previos si están disponibles
                    cargos_previos = exp.get('Cargos_Previos', '')
                break
        
        # Ordenar partidos_previos según prioridad (si no hay partido_principal)
        if tiene_experiencia_previa and not partido_principal and partidos_previos:
            from scripts.helpers.utilidades_candidatos_1946 import get_prioridad_partido
            
            # Ordenar por prioridad y obtener el primero como principal
            partidos_ordenados = sorted(partidos_previos, key=get_prioridad_partido)
            if partidos_ordenados:
                partido_principal = partidos_ordenados[0]
        
        candidato_info = {
            'id_persona': id_persona,
            'nombre_completo': nombre_completo,
            'partido': partido,
            'cargo': cargo,
            'ambito': ambito,
            'electo': electo,
            'tiene_experiencia_previa': tiene_experiencia_previa,
            'partido_principal': partido_principal,  # Nuevo campo
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
    
    return candidatos_data

def analizar_partidos_previos(candidatos_con_experiencia):
    """
    Analiza los partidos previos de los candidatos con experiencia política.
    
    Args:
        candidatos_con_experiencia (list): Lista de candidatos con experiencia previa
        
    Returns:
        Counter: Contador con los partidos previos y su frecuencia
    """
    partidos_previos = []
    
    for candidato in candidatos_con_experiencia:
        if candidato.get('partido_principal'):
            partidos_previos.append(candidato['partido_principal'])
        elif candidato.get('partidos_previos'):
            partidos = candidato.get('partidos_previos').split(', ')
            if partidos:
                partidos_previos.append(partidos[0])  # Tomar solo el primer partido
    
    return Counter(partidos_previos)

def analizar_categorias_partidos(contador_partidos):
    """
    Categoriza los partidos políticos en familias políticas.
    
    Args:
        contador_partidos (Counter): Contador con partidos y su frecuencia
        
    Returns:
        Counter: Contador con las categorías de partidos y su frecuencia
    """
    categorias_partidos = Counter()
    
    for partido, cantidad in contador_partidos.items():
        categoria = categorizar_partido(partido)
        categorias_partidos[categoria] += cantidad
    
    return categorias_partidos
