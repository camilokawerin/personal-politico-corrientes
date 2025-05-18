# -*- coding: utf-8 -*-
"""
Funciones para generar tablas de candidatos en el informe de 1946.
Este módulo contiene funciones específicas para la generación de tablas
con datos de candidatos en el informe de 1946.
"""

def generar_tabla_candidatos(candidatos):
    """
    Genera una tabla HTML con los datos detallados de los candidatos
    
    Args:
        candidatos (list): Lista de candidatos a mostrar en la tabla
        
    Returns:
        str: HTML de la tabla con todos los datos de los candidatos
    """
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
            # No mostrar "0" cuando no hay candidaturas previas
            candidaturas_previas = ""
        
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
