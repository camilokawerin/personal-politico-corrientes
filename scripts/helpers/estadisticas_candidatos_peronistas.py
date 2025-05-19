"""
Funciones auxiliares para el cálculo de estadísticas de candidatos peronistas.
"""
from collections import Counter
from scripts.commons.html_utils import formato_decimal

def calcular_estadisticas_partido_previo_por_tipo_cargo(grupos_cargo, detalle_trayectorias):
    """Calcula estadísticas detalladas por tipo de cargo"""
    estadisticas_por_cargo = {}
    
    for tipo_cargo, candidatos in grupos_cargo.items():
        if candidatos:
            # Contar candidatos únicos basados en ID_Persona
            candidatos_unicos = {c['ID_Persona'] for c in candidatos}
            total_candidatos = len(candidatos_unicos)
            
            # Contar candidatos únicos con experiencia previa
            con_experiencia_previa = {c['ID_Persona'] for c in candidatos if c['Cantidad_Candidaturas_Previas'] > 0}
            total_con_experiencia = len(con_experiencia_previa)
            
            # Iniciar estadísticas para este tipo de cargo
            estadisticas_por_cargo[tipo_cargo] = {
                'total_candidatos': total_candidatos,
                'con_experiencia_previa': total_con_experiencia,
                'partidos_previos': {}
            }
            
            # Calcular porcentaje con experiencia
            estadisticas_por_cargo[tipo_cargo]['porcentaje_con_experiencia'] = (
                total_con_experiencia / total_candidatos * 100
            ) if total_candidatos > 0 else 0
            
            # Calcular partidos previos más comunes usando el partido principal
            partidos_previos = {}
            personas_por_partido = {}
            
            for c in candidatos:
                if c['Cantidad_Candidaturas_Previas'] > 0:
                    id_persona = c['ID_Persona']
                    
                    # Determinar el partido principal a contar
                    partido_a_contar = None
                    
                    # Usar el partido principal si está disponible
                    if c.get('Partido_Principal'):
                        partido_a_contar = c['Partido_Principal']
                    # Si no hay partido principal pero hay partidos previos, usar el primero
                    elif c.get('Partidos_Previos'):
                        partido_a_contar = c['Partidos_Previos'].split(', ')[0]
                    
                    if partido_a_contar:
                        # Inicializar el diccionario para este partido si no existe
                        if partido_a_contar not in partidos_previos:
                            partidos_previos[partido_a_contar] = 0
                            personas_por_partido[partido_a_contar] = set()
                        
                        # Solo contar si esta persona no ha sido contada para este partido
                        if id_persona not in personas_por_partido[partido_a_contar]:
                            partidos_previos[partido_a_contar] += 1
                            personas_por_partido[partido_a_contar].add(id_persona)
            
            # Transferir los datos de conteo al diccionario de estadísticas
            for partido, cantidad in partidos_previos.items():
                estadisticas_por_cargo[tipo_cargo]['partidos_previos'][partido] = {
                    'cantidad': cantidad,
                    'porcentaje': formato_decimal((cantidad / total_con_experiencia * 100) if total_con_experiencia > 0 else 0)
                }
    
    return estadisticas_por_cargo
