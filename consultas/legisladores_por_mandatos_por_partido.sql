# Devuelve un cuadro con los siguientes datos:
#
# Partido       Total   Ocuparon      Ocuparon      Ocuparon
#                       1 cargo       2 cargos      3 cargos
# Autonomi...   x       x             x             x
# Radicales     x       x             x             x
# Peronistas    x       x             x             x
#

SELECT `Todos`.`Partidos`, `Todos`.`Total`, 
  `Con_1_cargo`.`Total` AS `Ocuparon 1 cargo`, 
  `Con_2_cargos`.`Total` AS `Ocuparon 2 cargos`,
  `Con_3_cargos`.`Total` AS `Ocuparon 3 cargos`
FROM (
  SELECT CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`,  `Partido`
    FROM  `Listado` AS  `T` 
    WHERE  `Anno` >=1946
    AND `Anno` <=1955
    AND  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Todos`

LEFT JOIN (
  SELECT  `Partidos`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, 
    COUNT( * ) AS  `Total_mandatos`,
    CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`
    FROM  `Listado` AS  `T` 
    WHERE  `Anno` >=1946
    AND  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Partidos`, `Total_mandatos`
) AS `Con_1_cargo`
ON `Todos`.`Partidos` = `Con_1_cargo`.`Partidos`
AND `Con_1_cargo`.`Total_mandatos` = 1

LEFT JOIN (
  SELECT  `Partidos`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, 
    COUNT( * ) AS  `Total_mandatos`,
    CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`
    FROM  `Listado` AS  `T` 
    WHERE  `Anno` >=1946
    AND  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Partidos`, `Total_mandatos`
) AS `Con_2_cargos`
ON `Todos`.`Partidos` = `Con_2_cargos`.`Partidos`
AND `Con_2_cargos`.`Total_mandatos` = 2

LEFT JOIN (
  SELECT  `Partidos`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, 
    COUNT( * ) AS  `Total_mandatos`,
    CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`
    FROM  `Listado` AS  `T` 
    WHERE  `Anno` >=1946
    AND  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Partidos`, `Total_mandatos`
) AS `Con_3_cargos`
ON `Todos`.`Partidos` = `Con_3_cargos`.`Partidos`
AND `Con_3_cargos`.`Total_mandatos` = 3

ORDER BY CASE `Todos`.`Partidos`
    WHEN 'Autonomista-Liberal' THEN 1
    WHEN 'Radicales' THEN 2
    WHEN 'Peronistas' THEN 3
  END;