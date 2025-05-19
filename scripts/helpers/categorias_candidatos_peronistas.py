"""
Funciones auxiliares para categorización de candidatos peronistas.
"""

def categorizar_partido(partido):
    """Categoriza un partido según su familia política"""
    partido_lower = partido.lower() if partido else ""
    if 'radical' in partido_lower:
        return 'Radicales'
    elif 'autonomista' in partido_lower:
        return 'Autonomistas'
    elif 'liberal' in partido_lower:
        return 'Liberales'
    else:
        return 'Otros'

def asignar_tipo_cargo(candidato_info):
    """
    Determina el tipo de cargo de un candidato según su trayectoria política.
    """
    # Por defecto asignamos a Otros Cargos y luego revisamos si hay trayectoria específica
    resultado = "Otros Cargos"
    
    # Primero verificamos si el candidato tiene información directa de cargo peronista
    if 'primer_anno' in candidato_info:
        # Recorremos la trayectoria buscando candidaturas peronistas
        for registro in candidato_info.get('trayectoria', []):
            # Verificar si es una entrada peronista
            if registro.get('Partido') in ['Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista'] and \
               registro.get('Año') == candidato_info['primer_anno']:
                
                cargo = registro.get('Cargo', '')
                
                # Extraer cargo y ámbito de la cadena si viene en formato combinado
                cargo_parts = cargo.split(' ')
                cargo_nombre = cargo_parts[0] if cargo_parts else ''
                ambito = cargo_parts[1] if len(cargo_parts) > 1 else ''
                
                if cargo_nombre == 'Diputado' and ambito == 'Nacional':
                    return "Diputados Nacionales"
                elif cargo_nombre == 'Senador' and ambito == 'Provincial':
                    return "Senadores Provinciales"
                elif cargo_nombre == 'Diputado' and ambito == 'Provincial':
                    return "Diputados Provinciales"
                elif cargo_nombre == 'Elector' and ambito == 'Provincial':
                    return "Electores Provinciales"

    # Si no encontramos información específica, recorremos toda la trayectoria
    for registro in candidato_info.get('trayectoria', []):
        cargo = registro.get('Cargo', '')
        
        if 'Diputado Nacional' in cargo:
            return "Diputados Nacionales"
        elif 'Senador Provincial' in cargo:
            return "Senadores Provinciales"
        elif 'Diputado Provincial' in cargo:
            return "Diputados Provinciales"
        elif 'Elector Provincial' in cargo:
            return "Electores Provinciales"
    
    return resultado

def determinar_tipo_cargo(candidato):
    """Determina el tipo de cargo principal de un candidato basado en su trayectoria"""
    resultado = "Otros Cargos"
    
    # Primero buscamos el cargo más prioritario (en orden)
    for registro in candidato.get('trayectoria', []):
        # El campo 'Cargo' contiene tanto el cargo como el ámbito (por ejemplo, "Diputado Provincial")
        cargo_completo = registro.get('Cargo', registro.get('cargo', ''))
        
        # Si el cargo está en formato de texto, procesarlo
        if isinstance(cargo_completo, str):
            cargo_lower = cargo_completo.lower().strip()
            
            # Para ser más robustos, comprobamos varias posibles formas de escribir los cargos
            # Diputados Nacionales (mayor prioridad)
            if any(term in cargo_lower for term in ['diputado nacional', 'diputados nacionales', 'diputado nac']):
                return "Diputados Nacionales"
            
            # Senadores Provinciales
            if any(term in cargo_lower for term in ['senador provincial', 'senadores provinciales', 'senador prov']):
                return "Senadores Provinciales"
            
            # Diputados Provinciales
            if any(term in cargo_lower for term in ['diputado provincial', 'diputados provinciales', 'diputado prov']):
                return "Diputados Provinciales"
            
            # Electores Provinciales
            if any(term in cargo_lower for term in ['elector provincial', 'electores provinciales', 'elector prov']):
                return "Electores Provinciales"
            
            # Verificar componentes por separado en caso de variaciones en el formato
            if 'diputado' in cargo_lower and ('nacional' in cargo_lower or 'nación' in cargo_lower or 'nacion' in cargo_lower):
                return "Diputados Nacionales"
            elif 'senador' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                return "Senadores Provinciales"
            elif 'diputado' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                return "Diputados Provinciales"
            elif 'elector' in cargo_lower and ('provincial' in cargo_lower or 'provincia' in cargo_lower):
                return "Electores Provinciales"
    
    # Si no encontramos uno de los tipos principales, devolvemos "Otros Cargos"
    return resultado
