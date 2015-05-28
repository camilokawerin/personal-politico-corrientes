# Devuelve un cuadro con los siguientes datos:
#
# Anno   Partidos          Total     Candidatura   Laborista     Radical       Peronista      Otros
#                                    previa                      (J. R.)    
# 1946   Laborista         x         x             x             x             x              x        
# 1946   Radical (J. R.)   x         x             x             x             x              x        
# 1948   Peronista         x         x             x             x             x              x        
# 1951   Peronista         x         x             x             x             x              x        
# 1954   Peronista         x         x             x             x             x              x        
#

SELECT `Todos`.`Anno`, `Todos`.`Partidos`, `Todos`.`Total`, 
  `Candidatura_previa`.`Total` AS `Candidatura previa`, 
  `Candidatura_laborista`.`Total` AS `Laborista`,
  `Candidatura_radical`.`Total` AS `Radical (J. R.)`,
  `Candidatura_peronista`.`Total` AS `Peronista`,
  `Candidatura_otros`.`Total` AS `Otros`
FROM (
  SELECT  `Anno`, `Partidos`, COUNT( * ) AS `Total`
  FROM (
    SELECT DISTINCT `ID_Persona`, 
    `Anno`,
    CASE `Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`
    WHERE  `Anno` >= 1946
    AND `Anno` <=1955
    AND `Electo` =1
    AND (
      `Cargo` =  'Diputado'
    OR `Cargo` =  'Senador'
    )
    AND `Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Todos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  `T`.`ID_Persona`,
    `T`.`Anno`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`,
    CASE `Previos`.`Partido`
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
      ELSE 'Otros'
    END AS `Partidos_previos`
    FROM  `Listado`  AS  `T`
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >= 1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
    GROUP BY `T`.`ID_Persona`, `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_previa` 
ON `Todos`.`Anno` = `Candidatura_previa`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_previa`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`,
    CASE `Previos`.`Partido`
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
      ELSE 'Otros'
    END AS `Partidos_previos`
    FROM  `Listado`  AS  `T`
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >= 1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`, `Partidos_previos`
) AS `Candidatura_laborista` 
ON `Todos`.`Anno` = `Candidatura_laborista`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_laborista`.`Partidos`
AND `Candidatura_laborista`.`Partidos_previos` = 'Laborista'

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`,
    CASE `Previos`.`Partido`
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
      ELSE 'Otros'
    END AS `Partidos_previos`
    FROM  `Listado`  AS  `T`
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >= 1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`, `Partidos_previos`
) AS `Candidatura_radical` 
ON `Todos`.`Anno` = `Candidatura_radical`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_radical`.`Partidos`
AND `Candidatura_radical`.`Partidos_previos` = 'Radical (J. R.)'

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`,
    CASE `Previos`.`Partido`
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
      ELSE 'Otros'
    END AS `Partidos_previos`
    FROM  `Listado`  AS  `T`
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >= 1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`, `Partidos_previos`
) AS `Candidatura_peronista` 
ON `Todos`.`Anno` = `Candidatura_peronista`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_peronista`.`Partidos`
AND `Candidatura_peronista`.`Partidos_previos` = 'Peronista'

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`,
    CASE `Previos`.`Partido`
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
      ELSE 'Otros'
    END AS `Partidos_previos`
    FROM  `Listado`  AS  `T`
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >= 1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`, `Partidos_previos`
) AS `Candidatura_otros` 
ON `Todos`.`Anno` = `Candidatura_otros`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_otros`.`Partidos`
AND `Candidatura_otros`.`Partidos_previos` = 'Otros'
