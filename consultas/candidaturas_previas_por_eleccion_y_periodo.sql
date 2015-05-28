# Devuelve un cuadro con los siguientes datos:
#
# Anno   Partidos          Total     Candidatura   Candidatura   Candidatura   Candidatura   Candidatura 
#                                    previa        1946 a 1955   1931 a 1942   1919 a 1929   1907 a 1917
# 1946   Laborista         x         x             x             x             x             x        
# 1946   Radical (J. R.)   x         x             x             x             x             x        
# 1948   Peronista         x         x             x             x             x             x        
# 1951   Peronista         x         x             x             x             x             x        
# 1954   Peronista         x         x             x             x             x             x             
#

SELECT `Todos`.`Anno`, `Todos`.`Partidos`, `Todos`.`Total`, 
  `Candidatura_previa`.`Total` AS `Candidatura previa a elección`, 
  `Candidatura_1946_1955`.`Total` AS `Candidatura 1946 a 1955`, 
  `Candidatura_1931_1942`.`Total` AS `Candidatura 1931 a 1942`,
  `Candidatura_1919_1929`.`Total` AS `Candidatura 1919 a 1929`,
  `Candidatura_1907_1917`.`Total` AS `Candidatura 1907 a 1917`
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
    AND `T`.`Anno` <=1955
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
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT `T`.`ID_Persona`, 
    `T`.`Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
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
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_previa` 
ON `Todos`.`Anno` = `Candidatura_previa`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_previa`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
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
    AND  `Previos`.`Anno` >= 1946
    AND  `Previos`.`Anno` < `T`.`Anno`
    GROUP BY `T`.`ID_Persona`, `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_1946_1955` 
ON `Todos`.`Anno` = `Candidatura_1946_1955`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_1946_1955`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
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
    AND  `Previos`.`Anno` >= 1931
    AND  `Previos`.`Anno` <= 1942
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_1931_1942` 
ON `Todos`.`Anno` = `Candidatura_1931_1942`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_1931_1942`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
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
    AND  `Previos`.`Anno` >= 1919
    AND  `Previos`.`Anno` <= 1929
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_1919_1929` 
ON `Todos`.`Anno` = `Candidatura_1919_1929`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_1919_1929`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
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
    AND  `Previos`.`Anno` >= 1907
    AND  `Previos`.`Anno` <= 1917
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Candidatura_1907_1917` 
ON `Todos`.`Anno` = `Candidatura_1907_1917`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_1907_1917`.`Partidos`

ORDER BY `Todos`.`Anno`, CASE `Todos`.`Partidos` 
      WHEN 'Laborista' THEN 1
      WHEN 'Radical (J. R.)' THEN 2
      WHEN 'Peronista' THEN 3
    END;