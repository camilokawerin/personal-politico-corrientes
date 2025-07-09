"""
Data retrieval functions to get information from the database.
"""
from scripts.commons.db_utils import ejecutar_consulta

def obtener_legisladores_peronistas():
    """Obtiene los legisladores electos por partidos peronistas entre 1946 y 1955"""
    query = """
    SELECT DISTINCT 
        `ID_Persona`, 
        CONCAT(`Nombre`, ' ', `Apellido`) AS `Nombre_Completo`
    FROM `Listado` 
    WHERE `Electo` = 1 
    AND `Anno` BETWEEN 1946 AND 1955
    AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    AND `Cargo` IN ('Diputado', 'Senador')
    AND `Ambito` = 'Provincial'
    GROUP BY `ID_Persona`
    ORDER BY `Apellido`, `Nombre`;
    """
    return ejecutar_consulta(query)

def generar_consulta_trayectoria(id_persona):
    """Genera una consulta SQL para obtener la trayectoria de un legislador por su ID"""
    query = f"""
    SELECT 
      CONCAT(`Nombre`, ' ', `Apellido`) AS `Nombre_Completo`,
      `Anno` AS `Año`,
      CONCAT(`Cargo`, ' ', `Ambito`) AS `Cargo`,
      `Partido` AS `Partido`,
      CASE 
        WHEN `Electo` = 1 THEN 'Sí'
        ELSE 'No'
      END AS `Electo`,
      CONCAT(
        CASE WHEN `Inicio_mandato` IS NOT NULL THEN `Inicio_mandato` ELSE '-' END,
        ' a ',
        CASE WHEN `Fin_mandato` IS NOT NULL THEN `Fin_mandato` ELSE '-' END
      ) AS `Período`,
      `Observaciones` AS `Observaciones`
    FROM `Listado`
    WHERE `ID_Persona` = {id_persona}
    ORDER BY `Anno` ASC;
    """
    return query

def obtener_trayectoria(id_persona):
    """Obtiene la trayectoria completa de un legislador por su ID"""
    query = generar_consulta_trayectoria(id_persona)
    return ejecutar_consulta(query)

def obtener_estadisticas_trayectoria_interpartidaria():
    """Obtiene estadísticas de legisladores que cambiaron desde otros partidos al peronismo"""
    query = """
    SELECT 
        L2.`Partido` AS `Partido_Previo`,
        COUNT(DISTINCT peronistas.`ID_Persona`) AS `Cantidad_Legisladores`,
        MIN(L2.`Anno`) AS `Anno_Min`,
        MAX(L2.`Anno`) AS `Anno_Max`
    FROM 
        (
            -- Subconsulta: Legisladores peronistas y su primer año
            SELECT DISTINCT 
                L.`ID_Persona`,
                (SELECT MIN(`Anno`) 
                FROM `Listado` 
                WHERE `ID_Persona` = L.`ID_Persona` 
                AND `Electo` = 1 
                AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
                AND `Cargo` IN ('Diputado', 'Senador')
                AND `Ambito` = 'Provincial') AS `Primer_Anno_Peronista`
            FROM `Listado` L
            WHERE `Electo` = 1 
            AND `Anno` BETWEEN 1946 AND 1955
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND `Cargo` IN ('Diputado', 'Senador')
            AND `Ambito` = 'Provincial'
        ) AS peronistas
    JOIN `Listado` L2 ON peronistas.`ID_Persona` = L2.`ID_Persona`
        AND L2.`Anno` < peronistas.`Primer_Anno_Peronista`
        AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    GROUP BY L2.`Partido`
    ORDER BY `Cantidad_Legisladores` DESC;
    """
    return ejecutar_consulta(query)

def obtener_estadisticas_cargos_previos():
    """Obtiene estadísticas de los cargos previos ocupados por legisladores peronistas"""
    query = """
    SELECT 
        CONCAT(L2.`Cargo`, ' ', L2.`Ambito`) AS `Cargo_Previo`,
        COUNT(DISTINCT peronistas.`ID_Persona`) AS `Cantidad_Legisladores`,
        MIN(L2.`Anno`) AS `Anno_Min`,
        MAX(L2.`Anno`) AS `Anno_Max`,
        COUNT(DISTINCT CASE WHEN L2.`Electo` = 1 THEN peronistas.`ID_Persona` ELSE NULL END) AS `Total_Electos`
    FROM 
        (
            -- Subconsulta: Legisladores peronistas y su primer año
            SELECT DISTINCT 
                L.`ID_Persona`,
                (SELECT MIN(`Anno`) 
                FROM `Listado` 
                WHERE `ID_Persona` = L.`ID_Persona` 
                AND `Electo` = 1 
                AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
                AND `Cargo` IN ('Diputado', 'Senador')
                AND `Ambito` = 'Provincial') AS `Primer_Anno_Peronista`
            FROM `Listado` L
            WHERE `Electo` = 1 
            AND `Anno` BETWEEN 1946 AND 1955
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND `Cargo` IN ('Diputado', 'Senador')
            AND `Ambito` = 'Provincial'
        ) AS peronistas
    JOIN `Listado` L2 ON peronistas.`ID_Persona` = L2.`ID_Persona`
        AND L2.`Anno` < peronistas.`Primer_Anno_Peronista`
        AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    GROUP BY L2.`Cargo`, L2.`Ambito`
    ORDER BY `Cantidad_Legisladores` DESC;
    """
    return ejecutar_consulta(query)

def obtener_detalle_trayectoria_interpartidaria():
    """Obtiene el detalle de legisladores que cambiaron desde otros partidos al peronismo"""
    query = """
    SELECT DISTINCT
        peronistas.`ID_Persona`,
        CONCAT(L1.`Nombre`, ' ', L1.`Apellido`) AS `Nombre_Completo`,
        L1.`Partido` AS `Partido_Peronista`,
        L1.`Anno` AS `Anno_Peronista`,        GROUP_CONCAT(DISTINCT L2.`Partido` ORDER BY L2.`Anno` DESC SEPARATOR ', ') AS `Partidos_Previos`,
        GROUP_CONCAT(DISTINCT CONCAT(L2.`Cargo`, ' ', L2.`Ambito`, 
            CASE WHEN L2.`Electo` = 1 THEN ' (*)' ELSE '' END) 
            ORDER BY L2.`Anno` DESC SEPARATOR ', ') AS `Cargos_Previos`,
        COUNT(DISTINCT L2.`id`) AS `Cantidad_Candidaturas_Previas`,
        MIN(L2.`Anno`) AS `Anno_Primera_Candidatura`,
        MAX(L2.`Anno`) AS `Anno_Ultima_Candidatura`
    FROM 
        (
            -- Subconsulta: Legisladores peronistas y su primer año
            SELECT DISTINCT 
                L.`ID_Persona`,
                (SELECT MIN(`Anno`) 
                FROM `Listado` 
                WHERE `ID_Persona` = L.`ID_Persona` 
                AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
                AND `Cargo` IN ('Diputado', 'Senador')
                AND `Ambito` = 'Provincial') AS `Primer_Anno_Peronista`
            FROM `Listado` L
            WHERE `Electo` = 1 
            AND `Anno` BETWEEN 1946 AND 1955
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND `Cargo` IN ('Diputado', 'Senador')
            AND `Ambito` = 'Provincial'
            GROUP BY L.`ID_Persona`
        ) AS peronistas    JOIN `Listado` L1 ON peronistas.`ID_Persona` = L1.`ID_Persona` 
        AND L1.`Anno` = peronistas.`Primer_Anno_Peronista`
        AND L1.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    JOIN `Listado` L2 ON peronistas.`ID_Persona` = L2.`ID_Persona`
        AND L2.`Anno` < peronistas.`Primer_Anno_Peronista`
        AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    GROUP BY peronistas.`ID_Persona`
    ORDER BY `Cantidad_Candidaturas_Previas` DESC;
    """
    return ejecutar_consulta(query)

def obtener_candidatos_1946():
    """
    Obtiene todos los candidatos de partidos peronistas de 1946
    
    Returns:
        list: Lista de candidatos con sus datos básicos
    """
    # Verificamos primero el formato de los datos devueltos para ver la estructura correcta
    consulta = """
        SELECT l.ID_Persona, CONCAT(l.Nombre, ' ', l.Apellido) AS Nombre_Completo, 
               l.Partido, l.Cargo, l.Ambito, l.Electo
        FROM listado l
        WHERE l.Anno = 1946 
        AND l.Partido IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)')
        GROUP BY l.ID_Persona
        ORDER BY l.ID_Persona
    """
    
    return ejecutar_consulta(consulta)

def obtener_todos_candidatos_peronistas():
    """Obtiene todos los candidatos de partidos peronistas entre 1946 y 1955 (no solo electos)"""
    query = """
    SELECT DISTINCT
        `ID_Persona`,
        CONCAT(`Nombre`, ' ', `Apellido`) AS `Nombre_Completo`,
        (SELECT `Partido` FROM `Listado` L2 WHERE L2.`ID_Persona` = L.`ID_Persona` 
         AND L2.`Anno` = MIN(L.`Anno`) AND L2.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
         LIMIT 1) AS `Partido`,
        MIN(`Anno`) AS `Primer_Anno_Peronista`
    FROM `Listado` L
    WHERE `Anno` BETWEEN 1946 AND 1955
    AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    GROUP BY `ID_Persona`
    ORDER BY `Primer_Anno_Peronista`, `Apellido`, `Nombre`;
    """
    return ejecutar_consulta(query)

def obtener_detalle_trayectoria_candidatos_peronistas():
    """Obtiene el detalle de todos los candidatos peronistas, con o sin experiencia política previa"""
    query = """
    WITH CandidatosPeor AS (
        -- Subconsulta: Candidatos peronistas y su primer año
        SELECT DISTINCT 
            L.`ID_Persona`,
            (SELECT MIN(`Anno`) 
            FROM `Listado` 
            WHERE `ID_Persona` = L.`ID_Persona` 
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Primer_Anno_Peronista`
        FROM `Listado` L
        WHERE `Anno` BETWEEN 1946 AND 1955
        AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    ),
    PartidosPrevios AS (
        -- Obtener todos los partidos previos por cada persona
        SELECT 
            CP.`ID_Persona`,
            L2.`Partido`,
            L2.`Anno`,
            -- Prioridad para selección de partido
            CASE 
                WHEN L2.`Partido` IN ('Radical Antipersonalista', 'Radical Personalista', 'Autonomista', 'Liberal') THEN 1
                WHEN L2.`Partido` LIKE '%Radical%' OR L2.`Partido` LIKE '%Autonomista%' OR L2.`Partido` LIKE '%Liberal%' THEN 2
                ELSE 3
            END as Prioridad
        FROM CandidatosPeor CP
        JOIN `Listado` L2 ON CP.`ID_Persona` = L2.`ID_Persona`
            AND L2.`Anno` < CP.`Primer_Anno_Peronista`
            AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    ),
    TrayectoriaPrincipal AS (
        SELECT 
            CP.`ID_Persona`,
            L1.`Nombre`, 
            L1.`Apellido`,
            L1.`Partido` AS `Partido_Peronista`,
            L1.`Anno` AS `Anno_Peronista`,
            L1.`Cargo` AS `Cargo_Peronista`,
            L1.`Ambito` AS `Ambito_Peronista`,
            L1.`Electo` AS `Electo_Peronista`,
            -- Seleccionar partido previo principal según las reglas de prioridad
            (SELECT `Partido` FROM PartidosPrevios PP 
             WHERE PP.`ID_Persona` = CP.`ID_Persona` 
             ORDER BY PP.Prioridad, PP.`Anno` DESC LIMIT 1) AS `Partido_Principal`,
            -- Para conservar todos los partidos previos para análisis
            GROUP_CONCAT(DISTINCT PP.`Partido` ORDER BY PP.`Anno` DESC SEPARATOR ', ') AS `Partidos_Previos`,
            -- Información de cargos
            GROUP_CONCAT(DISTINCT CONCAT(L2.`Cargo`, ' ', L2.`Ambito`,
                CASE WHEN L2.`Electo` = 1 THEN ' (*)' ELSE '' END) 
                ORDER BY L2.`Anno` DESC SEPARATOR ', ') AS `Cargos_Previos`,
            COUNT(DISTINCT L2.`id`) AS `Cantidad_Candidaturas_Previas`,
            MIN(IFNULL(L2.`Anno`, L1.`Anno`)) AS `Anno_Primera_Candidatura`,
            MAX(IFNULL(L2.`Anno`, L1.`Anno`)) AS `Anno_Ultima_Candidatura`
        FROM CandidatosPeor CP
        JOIN `Listado` L1 ON CP.`ID_Persona` = L1.`ID_Persona` 
            AND L1.`Anno` = CP.`Primer_Anno_Peronista`
            AND L1.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
        LEFT JOIN `Listado` L2 ON CP.`ID_Persona` = L2.`ID_Persona`
            AND L2.`Anno` < CP.`Primer_Anno_Peronista`
            AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
        LEFT JOIN PartidosPrevios PP ON CP.`ID_Persona` = PP.`ID_Persona`
        GROUP BY CP.`ID_Persona`, L1.`Nombre`, L1.`Apellido`, L1.`Partido`, L1.`Anno`, L1.`Cargo`, L1.`Ambito`, L1.`Electo`
    )
    
    SELECT DISTINCT
        `ID_Persona`,
        CONCAT(`Nombre`, ' ', `Apellido`) AS `Nombre_Completo`,
        `Partido_Peronista`,
        `Anno_Peronista`,
        `Cargo_Peronista`,
        `Ambito_Peronista`,
        `Electo_Peronista`,
        COALESCE(`Partido_Principal`, '') AS `Partido_Principal`,
        `Partidos_Previos`,
        `Cargos_Previos`,
        `Cantidad_Candidaturas_Previas`,
        `Anno_Primera_Candidatura`,
        `Anno_Ultima_Candidatura`
    FROM TrayectoriaPrincipal
    ORDER BY `Cantidad_Candidaturas_Previas` DESC, `Nombre_Completo`;
    """
    result = ejecutar_consulta(query)
    return result

def obtener_detalle_trayectoria_candidatos_1946():
    """Obtiene el detalle de todos los candidatos de 1946, con o sin experiencia política previa"""
    query = """
    WITH Candidatos1946 AS (
        -- Subconsulta: Candidatos de 1946
        SELECT DISTINCT 
            L.`ID_Persona`,
            L.`Nombre`,
            L.`Apellido`,
            L.`Partido`,
            L.`Cargo`,
            L.`Ambito`,
            L.`Electo`
        FROM `Listado` L
        WHERE L.`Anno` = 1946
        AND L.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)')
    ),
    PartidosPrevios AS (
        -- Obtener todos los partidos previos por cada persona
        SELECT 
            C.`ID_Persona`,
            L2.`Partido`,
            L2.`Anno`,
            -- Prioridad para selección de partido
            CASE 
                WHEN L2.`Partido` IN ('Radical Antipersonalista', 'Radical Personalista', 'Autonomista', 'Liberal') THEN 1
                WHEN L2.`Partido` LIKE '%Radical%' OR L2.`Partido` LIKE '%Autonomista%' OR L2.`Partido` LIKE '%Liberal%' THEN 2
                ELSE 3
            END as Prioridad
        FROM Candidatos1946 C
        JOIN `Listado` L2 ON C.`ID_Persona` = L2.`ID_Persona`
            AND L2.`Anno` < 1946
            AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    )
    
    SELECT DISTINCT
        C.`ID_Persona`,
        CONCAT(C.`Nombre`, ' ', C.`Apellido`) AS `Nombre_Completo`,
        C.`Partido` AS `Partido_Peronista`,
        1946 AS `Anno_Peronista`,
        C.`Cargo` AS `Cargo_Peronista`,
        C.`Ambito` AS `Ambito_Peronista`,
        C.`Electo` AS `Electo_Peronista`,
        -- Seleccionar partido previo principal según las reglas de prioridad
        (SELECT `Partido` FROM PartidosPrevios PP 
         WHERE PP.`ID_Persona` = C.`ID_Persona` 
         ORDER BY PP.Prioridad, PP.`Anno` DESC LIMIT 1) AS `Partido_Principal`,
        -- Para conservar todos los partidos previos para análisis
        (SELECT GROUP_CONCAT(DISTINCT PP.`Partido` ORDER BY PP.`Anno` DESC SEPARATOR ', ')
         FROM PartidosPrevios PP
         WHERE PP.`ID_Persona` = C.`ID_Persona`) AS `Partidos_Previos`,
        -- Información de cargos
        (SELECT GROUP_CONCAT(DISTINCT CONCAT(L2.`Cargo`, ' ', L2.`Ambito`,
            CASE WHEN L2.`Electo` = 1 THEN ' (*)' ELSE '' END) 
            ORDER BY L2.`Anno` DESC SEPARATOR ', ')
         FROM `Listado` L2
         WHERE L2.`ID_Persona` = C.`ID_Persona`
         AND L2.`Anno` < 1946
         AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Cargos_Previos`,
        (SELECT COUNT(DISTINCT L2.`id`)
         FROM `Listado` L2
         WHERE L2.`ID_Persona` = C.`ID_Persona`
         AND L2.`Anno` < 1946
         AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Cantidad_Candidaturas_Previas`,
        (SELECT MIN(L2.`Anno`)
         FROM `Listado` L2
         WHERE L2.`ID_Persona` = C.`ID_Persona`
         AND L2.`Anno` < 1946
         AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Anno_Primera_Candidatura`,
        (SELECT MAX(L2.`Anno`)
         FROM `Listado` L2
         WHERE L2.`ID_Persona` = C.`ID_Persona`
         AND L2.`Anno` < 1946
         AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Anno_Ultima_Candidatura`
    FROM Candidatos1946 C
    ORDER BY `Cantidad_Candidaturas_Previas` DESC, `Nombre_Completo`;
    """
    result = ejecutar_consulta(query)
    return result

def obtener_estadisticas_partidos_previos_candidatos():
    """Obtiene estadísticas de partidos previos de todos los candidatos peronistas"""
    query = """
    WITH CandidatosPeor AS (
        -- Obtener la primera candidatura peronista para cada persona
        SELECT DISTINCT 
            L.`ID_Persona`,
            (SELECT MIN(`Anno`) 
            FROM `Listado` 
            WHERE `ID_Persona` = L.`ID_Persona` 
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')) AS `Primer_Anno_Peronista`
        FROM `Listado` L
        WHERE `Anno` BETWEEN 1946 AND 1955
        AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    ),
    PartidosPrevios AS (
        -- Obtener todos los partidos previos por cada persona
        SELECT 
            CP.`ID_Persona`,
            L2.`Partido`,
            L2.`Anno`,
            -- Prioridad para selección de partido
            CASE 
                WHEN L2.`Partido` IN ('Radical Antipersonalista', 'Radical Personalista', 'Autonomista', 'Liberal') THEN 1
                WHEN L2.`Partido` LIKE '%Radical%' OR L2.`Partido` LIKE '%Autonomista%' OR L2.`Partido` LIKE '%Liberal%' THEN 2
                ELSE 3
            END as Prioridad
        FROM CandidatosPeor CP
        JOIN `Listado` L2 ON CP.`ID_Persona` = L2.`ID_Persona`
            AND L2.`Anno` < CP.`Primer_Anno_Peronista`
            AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    ),
    RankedPartidos AS (
        -- Asignar un rango a cada partido por persona según prioridad
        SELECT 
            `ID_Persona`,
            `Partido`,
            `Anno`,
            ROW_NUMBER() OVER(PARTITION BY `ID_Persona` ORDER BY Prioridad, `Anno` DESC) as Rango
        FROM PartidosPrevios
    ),
    PartidoSeleccionado AS (
        -- Seleccionar solo el partido de mayor prioridad para cada persona
        SELECT 
            `ID_Persona`,
            `Partido` as Partido_Seleccionado,
            MIN(`Anno`) as `Anno_Min`,
            MAX(`Anno`) as `Anno_Max`
        FROM RankedPartidos 
        WHERE Rango = 1
        GROUP BY `ID_Persona`, `Partido`
    )
    -- Contar personas únicas por partido seleccionado
    SELECT 
        Partido_Seleccionado AS `Partido_Previo`,
        COUNT(DISTINCT `ID_Persona`) AS `Cantidad_Candidatos`,
        MIN(`Anno_Min`) AS `Anno_Min`,
        MAX(`Anno_Max`) AS `Anno_Max`
    FROM PartidoSeleccionado
    GROUP BY Partido_Seleccionado
    ORDER BY `Cantidad_Candidatos` DESC;
    """
    return ejecutar_consulta(query)

def obtener_legisladores_peronistas_con_experiencia_otros_partidos():
    """Obtiene los legisladores peronistas que fueron candidatos por otros partidos antes de ser electos como peronistas"""
    query = """
    SELECT DISTINCT
        L1.`ID_Persona`,
        CONCAT(L1.`Nombre`, ' ', L1.`Apellido`) AS `Nombre_Completo`
    FROM `Listado` L1
    WHERE L1.`Electo` = 1 
    AND L1.`Anno` BETWEEN 1946 AND 1955
    AND L1.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    AND L1.`Cargo` IN ('Diputado', 'Senador')
    AND L1.`Ambito` = 'Provincial'
    AND EXISTS (
        SELECT 1 
        FROM `Listado` L2 
        WHERE L2.`ID_Persona` = L1.`ID_Persona` 
        AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
        AND L2.`Anno` < (
            SELECT MIN(L3.`Anno`)
            FROM `Listado` L3
            WHERE L3.`ID_Persona` = L1.`ID_Persona`
            AND L3.`Electo` = 1
            AND L3.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND L3.`Cargo` IN ('Diputado', 'Senador')
            AND L3.`Ambito` = 'Provincial'
        )
    )
    ORDER BY `Nombre_Completo`;
    """
    return ejecutar_consulta(query)

def obtener_cargos_peronistas():
    """Obtiene los cargos ocupados durante el peronismo (1946-1955) por cada legislador"""
    query = """
    SELECT 
        peronistas.`ID_Persona`,
        GROUP_CONCAT(
            DISTINCT CONCAT(
                L.`Cargo`, ' ', L.`Ambito`,
                CASE WHEN L.`Electo` = 1 THEN ' (*)' ELSE '' END
            )
            ORDER BY L.`Anno`, L.`Cargo`
            SEPARATOR ', '
        ) AS `Cargos_Peronismo`,
        COUNT(DISTINCT L.`id`) AS `Cantidad_Candidaturas_Peronistas`
    FROM 
        (
            -- Subconsulta: Legisladores peronistas (solo obtenemos el ID, sin filtrar por fecha)
            SELECT DISTINCT 
                L.`ID_Persona`
            FROM `Listado` L
            WHERE `Electo` = 1 
            AND `Anno` BETWEEN 1946 AND 1955
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND `Cargo` IN ('Diputado', 'Senador')
            AND `Ambito` = 'Provincial'
        ) AS peronistas
    JOIN `Listado` L ON peronistas.`ID_Persona` = L.`ID_Persona`
        AND L.`Anno` BETWEEN 1946 AND 1955
        AND L.`Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
    GROUP BY peronistas.`ID_Persona`;
    """
    return ejecutar_consulta(query)

def obtener_personas_por_cargo_previo(cargo_previo):
    """Obtiene los IDs de las personas que ocuparon un cargo previo específico"""
    query = f"""
    SELECT DISTINCT peronistas.`ID_Persona`
    FROM 
        (
            -- Subconsulta: Legisladores peronistas y su primer año
            SELECT DISTINCT 
                L.`ID_Persona`,
                (SELECT MIN(`Anno`) 
                FROM `Listado` 
                WHERE `ID_Persona` = L.`ID_Persona` 
                AND `Electo` = 1 
                AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
                AND `Cargo` IN ('Diputado', 'Senador')
                AND `Ambito` = 'Provincial') AS `Primer_Anno_Peronista`
            FROM `Listado` L
            WHERE `Electo` = 1 
            AND `Anno` BETWEEN 1946 AND 1955
            AND `Partido` IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
            AND `Cargo` IN ('Diputado', 'Senador')
            AND `Ambito` = 'Provincial'
        ) AS peronistas
    JOIN `Listado` L2 ON peronistas.`ID_Persona` = L2.`ID_Persona`
        AND L2.`Anno` < peronistas.`Primer_Anno_Peronista`
        AND L2.`Partido` NOT IN ('Laborista Correntino', 'Radical (Junta Reorganizadora)', 'Peronista')
        AND CONCAT(L2.`Cargo`, ' ', L2.`Ambito`) = '{cargo_previo}'
    """
    resultados = ejecutar_consulta(query)
    return [resultado['ID_Persona'] for resultado in resultados]
