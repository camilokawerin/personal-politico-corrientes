# -*- coding: utf-8 -*-
"""
Análisis de datos para el informe de candidatos de 1946.
Este módulo contiene funciones para analizar y procesar los datos
de los candidatos peronistas de 1946.
"""
from collections import Counter
from scripts.helpers.utilidades_candidatos_1946 import categorizar_partido

def procesar_datos_candidatos(candidatos, candidatos_con_experiencia, obtener_trayectoria):
    """
    Procesa los datos de los candidatos y obtiene información adicional
    
    Args:
        candidatos (list): Lista de candidatos de la consulta básica
        candidatos_con_experiencia (list): Datos adicionales de candidatos con experiencia previa
        obtener_trayectoria (function): Función para obtener la trayectoria completa
        
    Returns:
        list: Lista de candidatos con datos procesados
    """
    candidatos_data = []
    
    # Creamos un diccionario con la información de experiencia previa
    experiencia_previa = {}
    for c in candidatos_con_experiencia:
        id_persona = c['ID_Persona']
        # Un candidato tiene experiencia previa si tiene candidaturas anteriores a 1946
        tiene_experiencia = c.get('Cantidad_Candidaturas_Previas', 0) > 0
        experiencia_previa[id_persona] = {
            'tiene_experiencia_previa': tiene_experiencia,
            'cantidad_candidaturas': c.get('Cantidad_Candidaturas_Previas', 0),
            'partidos_previos': c.get('Partidos_Previos', ''),
            'cargos_previos': c.get('Cargos_Previos', ''),
            'primer_anno': c.get('Anno_Primera_Candidatura', 0)
        }
    
    for candidato in candidatos:
        # Verificar las claves disponibles y usar las correctas
        # Comprobar si tenemos nombre y apellido o nombre_completo
        id_persona = candidato.get('ID_Persona')
        
        if 'Nombre_Completo' in candidato:
            nombre_completo = candidato['Nombre_Completo']
        elif 'Nombre' in candidato and 'Apellido' in candidato:
            nombre_completo = candidato['Nombre'] + ' ' + candidato['Apellido']
        else:
            # Si no hay nombre, usar un valor por defecto
            nombre_completo = f"Candidato ID {id_persona}"
        
        # Obtener trayectoria completa
        trayectoria = obtener_trayectoria(id_persona)
        
        # Datos de experiencia previa
        exp_previa = experiencia_previa.get(id_persona, {})
        tiene_experiencia = exp_previa.get('tiene_experiencia_previa', False)
        partidos_previos = exp_previa.get('partidos_previos', '')
        cargos_previos = exp_previa.get('cargos_previos', '')
        
        # Clasificar en períodos históricos
        periodo_historico = ""
        if tiene_experiencia:
            primer_anno = exp_previa.get('primer_anno', 0)
            if 1900 <= primer_anno <= 1915:
                periodo_historico = "1900-1915"
            elif 1916 <= primer_anno <= 1930:
                periodo_historico = "1916-1930"
            elif 1931 <= primer_anno <= 1942:
                periodo_historico = "1931-1942"
            elif 1943 <= primer_anno <= 1945:
                periodo_historico = "1943-1945"
        
        # Clasificar tipo de cargo previo
        tipo_cargo_previo = "Ninguno"
        if cargos_previos:
            cargos_lower = cargos_previos.lower()
            if "diputado nacional" in cargos_lower:
                tipo_cargo_previo = "Diputado Nacional"
            elif "senador provincial" in cargos_lower:
                tipo_cargo_previo = "Senador Provincial"
            elif "diputado provincial" in cargos_lower:
                tipo_cargo_previo = "Diputado Provincial"
            elif "elector nacional" in cargos_lower:
                tipo_cargo_previo = "Elector Nacional"
            elif "elector provincial" in cargos_lower:
                tipo_cargo_previo = "Elector Provincial"
            else:
                tipo_cargo_previo = "Otros Cargos"
        
        # Guardar datos procesados - usar .get() para acceder a las claves de forma segura
        candidato_info = {
            'id_persona': id_persona,
            'nombre_completo': nombre_completo,
            'partido': candidato.get('Partido', ''),
            'cargo': candidato.get('Cargo', ''),
            'ambito': candidato.get('Ambito', ''),
            'electo': 'Sí' if candidato.get('Electo') == 1 else 'No',
            'tiene_experiencia_previa': tiene_experiencia,
            'partidos_previos': partidos_previos,
            'cargos_previos': cargos_previos,
            'periodo_historico': periodo_historico,
            'tipo_cargo_previo': tipo_cargo_previo if tiene_experiencia else None,
            'trayectoria': trayectoria
        }
        
        candidatos_data.append(candidato_info)
    
    return candidatos_data

def analizar_partidos_previos(candidatos):
    """
    Analiza y cuenta los partidos previos de los candidatos, agrupando por persona
    y seleccionando el partido más representativo para cada una según las siguientes prioridades:
    1. Si tiene partidos radicales, autonomistas o liberales, prioriza estos
    2. Si no, toma el más reciente
    
    Args:
        candidatos (list): Lista de candidatos con experiencia previa
        
    Returns:
        Counter: Contador con la distribución de partidos previos (un partido por persona)
    """
    contador_partidos = Counter()
    personas_procesadas = set()
    
    for c in candidatos:
        id_persona = c.get('id_persona')
        
        # Evitar contar la misma persona más de una vez
        if id_persona in personas_procesadas:
            continue
            
        if c.get('partidos_previos'):
            # Dividir los partidos separados por comas
            partidos = [p.strip() for p in c['partidos_previos'].split(', ') if p.strip()]
            
            if partidos:
                # Buscar primero partidos de las familias principales (radical, autonomista, liberal)
                partido_seleccionado = None
                
                # Prioridad 1: Buscar partidos radicales
                for partido in partidos:
                    if 'radical' in partido.lower():
                        partido_seleccionado = partido
                        break
                
                # Prioridad 2: Si no hay radicales, buscar autonomistas
                if not partido_seleccionado:
                    for partido in partidos:
                        if 'autonom' in partido.lower():
                            partido_seleccionado = partido
                            break
                
                # Prioridad 3: Si no hay radicales ni autonomistas, buscar liberales
                if not partido_seleccionado:
                    for partido in partidos:
                        if 'liberal' in partido.lower():
                            partido_seleccionado = partido
                            break
                
                # Prioridad 4: Si no hay ninguno de los anteriores, tomar el más reciente (primero en la lista)
                if not partido_seleccionado:
                    partido_seleccionado = partidos[0]
                
                contador_partidos[partido_seleccionado] += 1
                personas_procesadas.add(id_persona)
    
    return contador_partidos

def analizar_categorias_partidos(contador_partidos):
    """
    Agrupa los partidos por familias políticas
    
    Args:
        contador_partidos (Counter): Contador con la distribución de partidos
        
    Returns:
        dict: Diccionario con el conteo por categoría política
    """
    categorias = {
        "Radicales": 0,
        "Autonomistas": 0,
        "Liberales": 0,
        "Otros": 0
    }
    
    for partido, cantidad in contador_partidos.items():
        categoria = categorizar_partido(partido)
        categorias[categoria] += cantidad
    
    return categorias

def analizar_periodos_historicos(candidatos):
    """
    Analiza la distribución de candidatos por períodos históricos
    
    Args:
        candidatos (list): Lista de candidatos con experiencia previa
        
    Returns:
        dict: Diccionario con el conteo por período histórico
    """
    periodos = {
        "1900-1915": 0,
        "1916-1930": 0,
        "1931-1942": 0,
        "1943-1945": 0
    }
    
    # Usar un conjunto para evitar contar la misma persona más de una vez
    personas_contadas = set()
    
    for c in candidatos:
        if not c.get('tiene_experiencia_previa'):
            continue
            
        id_persona = c['id_persona']
        
        # Evitar contar la misma persona más de una vez
        if id_persona in personas_contadas:
            continue
            
        periodo = c.get('periodo_historico')
        if periodo in periodos:
            periodos[periodo] += 1
            personas_contadas.add(id_persona)
    
    return periodos

def analizar_cargos_previos(candidatos):
    """
    Analiza la distribución de candidatos por tipo de cargo previo
    
    Args:
        candidatos (list): Lista de candidatos con experiencia previa
        
    Returns:
        dict: Diccionario con el conteo por tipo de cargo
    """
    cargos = {
        "Diputado Nacional": 0,
        "Senador Provincial": 0,
        "Diputado Provincial": 0,
        "Elector Nacional": 0,
        "Elector Provincial": 0,
        "Otros Cargos": 0
    }
    
    # Usar un conjunto para evitar contar la misma persona más de una vez
    personas_contadas = set()
    
    for c in candidatos:
        if not c.get('tiene_experiencia_previa'):
            continue
            
        id_persona = c['id_persona']
        
        # Evitar contar la misma persona más de una vez
        if id_persona in personas_contadas:
            continue
            
        tipo_cargo = c.get('tipo_cargo_previo')
        if tipo_cargo in cargos:
            cargos[tipo_cargo] += 1
            personas_contadas.add(id_persona)
    
    return cargos
