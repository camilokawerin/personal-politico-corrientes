# -*- coding: utf-8 -*-
"""
Utilidades para el informe de candidatos de 1946.
Funciones auxiliares que apoyan la generación de informes de candidatos peronistas de 1946.
"""
import os
import sys

def categorizar_partido(partido):
    """
    Categoriza un partido político en una de las familias políticas principales:
    Radicales, Autonomistas, Liberales, Otros
    
    Args:
        partido (str): Nombre del partido a categorizar
        
    Returns:
        str: Categoría a la que pertenece el partido
    """
    partido_lower = partido.lower() if partido else ''
    
    # Partidos Radicales
    if 'radical' in partido_lower:
        return "Radicales"
    
    # Partido Autonomista
    elif 'autonom' in partido_lower:
        return "Autonomistas"
    
    # Partido Liberal
    elif 'liberal' in partido_lower:
        return "Liberales"
    
    # Cualquier otro partido que no entre en las categorías anteriores
    else:
        return "Otros"

def get_prioridad_partido(partido):
    """
    Asigna una prioridad numérica a un partido político según su relevancia.
    Valores más bajos indican mayor prioridad.
    
    Args:
        partido (str): Nombre del partido
        
    Returns:
        int: Valor de prioridad (menor número = mayor prioridad)
    """
    partido_lower = partido.lower()
    
    # Principales partidos con nombres exactos tienen máxima prioridad
    if partido in ['Radical Antipersonalista', 'Radical Personalista', 'Autonomista', 'Liberal']:
        return 1
    # Contiene nombres genéricos de los principales partidos
    elif ('radical' in partido_lower or 'autonomista' in partido_lower or 'liberal' in partido_lower):
        return 2
    # Cualquier otro partido
    else:
        return 3
