# Devuelve un cuadro con los siguientes datos:
#
# Anno   Cargo            Total     Candidatura   Candidatura   Candidatura   Candidatura   Candidatura 
#                                   previa        1946 a 1955   1931 a 1942   1919 a 1929   1907 a 1917
# 1946   Diputado prov.   x         x             x             x             x             x
# 1946   Senador prov.    x         x             x             x             x             x
# 1946   Diputado nac.    x         x             x             x             x             x
# 1948   [...] 
# 1951
# 1954
#

SELECT `Todos`.`Anno`, `Todos`.`Cargo`, `Todos`.`Total`, 
  `Candidatura_1946_1955`.`Total` AS `Candidatura 1946 a 1955`, 
  `Candidatura_1931_1942`.`Total` AS `Candidatura 1931 a 1942`,
  `Candidatura_1919_1929`.`Total` AS `Candidatura 1919 a 1929`,
  `Candidatura_1907_1917`.`Total` AS `Candidatura 1907 a 1917`
FROM (
  SELECT `Anno`, `Cargo`, COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`,  
      `Anno`, 
      CONCAT(`Cargo`, ' ',  `Ambito`) AS `Cargo`,
      CASE `Partido` 
        WHEN 'Laborista Correntino' THEN 'Laborista'
        WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
        WHEN 'Peronista' THEN 'Peronista'
      END AS `Partidos`
    FROM  `Listado`
    WHERE  `Anno` >=1946
    AND `Anno` <=1955
    AND  `Electo` =1
    AND (
      (
        `Cargo` =  'Diputado'
        AND `Ambito` =  'Nacional'
      )
      OR (
        `Cargo` =  'Senador'
        AND `Ambito` =  'Provincial'
      )
      OR (
        `Cargo` =  'Diputado'
        AND `Ambito` =  'Provincial'
      )
    )
    GROUP BY `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Anno`, `Cargo`
) AS `Todos`

LEFT JOIN (
  SELECT `Anno`, `Cargo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
      (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Nacional'
      )
      OR (
        `T`.`Cargo` =  'Senador'
        AND `T`.`Ambito` =  'Provincial'
      )
      OR (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Provincial'
      )
    )
    AND  `Previos`.`Anno` >= 1946
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Anno`, `Cargo`
) AS `Candidatura_1946_1955`
ON `Todos`.`Anno` = `Candidatura_1946_1955`.`Anno`
AND `Todos`.`Cargo` = `Candidatura_1946_1955`.`Cargo`

LEFT JOIN (
  SELECT `Anno`, `Cargo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
      (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Nacional'
      )
      OR (
        `T`.`Cargo` =  'Senador'
        AND `T`.`Ambito` =  'Provincial'
      )
      OR (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Provincial'
      )
    )
    AND  `Previos`.`Anno` >= 1931
    AND  `Previos`.`Anno` <= 1942
  ) AS `T`
  GROUP BY `Anno`, `Cargo`
) AS `Candidatura_1931_1942`
ON `Todos`.`Anno` = `Candidatura_1931_1942`.`Anno`
AND `Todos`.`Cargo` = `Candidatura_1931_1942`.`Cargo`

LEFT JOIN (
  SELECT `Anno`, `Cargo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
      (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Nacional'
      )
      OR (
        `T`.`Cargo` =  'Senador'
        AND `T`.`Ambito` =  'Provincial'
      )
      OR (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Provincial'
      )
    )
    AND  `Previos`.`Anno` >= 1919
    AND  `Previos`.`Anno` <= 1929
  ) AS `T`
  GROUP BY `Anno`, `Cargo`
) AS `Candidatura_1919_1929`
ON `Todos`.`Anno` = `Candidatura_1919_1929`.`Anno`
AND `Todos`.`Cargo` = `Candidatura_1919_1929`.`Cargo`

LEFT JOIN (
  SELECT `Anno`, `Cargo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
      (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Nacional'
      )
      OR (
        `T`.`Cargo` =  'Senador'
        AND `T`.`Ambito` =  'Provincial'
      )
      OR (
        `T`.`Cargo` =  'Diputado'
        AND `T`.`Ambito` =  'Provincial'
      )
    )
    AND  `Previos`.`Anno` >= 1907
    AND  `Previos`.`Anno` <= 1917
  ) AS `T`
  GROUP BY `Anno`, `Cargo`
) AS `Candidatura_1907_1917`
ON `Todos`.`Anno` = `Candidatura_1907_1917`.`Anno`
AND `Todos`.`Cargo` = `Candidatura_1907_1917`.`Cargo`

ORDER BY `Todos`.`Anno`, 
  CASE `Todos`.`Cargo` 
    WHEN 'Diputado Nacional' THEN 3
    WHEN 'Senador Provincial' THEN 2 
    ELSE 1 
  END;