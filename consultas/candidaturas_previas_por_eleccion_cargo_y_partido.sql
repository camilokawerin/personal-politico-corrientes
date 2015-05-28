# Devuelve un cuadro con los siguientes datos:
#
# Anno   Cargo            Total     Candidatura   Laborista     Radical       Peronista      Otros
#                                   previa                      (J. R.)
# 1946   Diputado prov.   x         x             x             x             x              x
# 1946   Senador prov.    x         x             x             x             x              x
# 1946   Diputado nac.    x         x             x             x             x              x
# 1948   [...] 
# 1951
# 1954
#

SELECT `Todos`.`Anno`, `Todos`.`Cargo`, `Todos`.`Total`, 
  `Candidatura_laborista`.`Total` AS `Laborista`,
  `Candidatura_radical`.`Total` AS `Radical (J. R.)`,
  `Candidatura_peronista`.`Total` AS `Peronista`,
  `Candidatura_otros`.`Total` AS `Otros`
FROM (

  SELECT `Anno`, `Cargo`, `Partidos`, COUNT( * ) AS `Total`
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
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`

) AS `Todos`

LEFT JOIN (
  SELECT  `Anno`, `Cargo`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`,
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
    AND `Anno` <=1955
    AND `T`.`Electo` =1
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
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`, `Partidos_previos`
) AS `Candidatura_laborista` 
ON `Todos`.`Anno` = `Candidatura_laborista`.`Anno`
AND  `Todos`.`Cargo` = `Candidatura_laborista`.`Cargo`
AND `Candidatura_laborista`.`Partidos_previos` = 'Laborista'

LEFT JOIN (
  SELECT  `Anno`, `Cargo`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`,
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
    AND `Anno` <=1955
    AND `T`.`Electo` =1
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
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`, `Partidos_previos`
) AS `Candidatura_radical` 
ON `Todos`.`Anno` = `Candidatura_radical`.`Anno`
AND  `Todos`.`Cargo` = `Candidatura_radical`.`Cargo`
AND `Candidatura_radical`.`Partidos_previos` = 'Radical (J. R.)'

LEFT JOIN (
  SELECT  `Anno`, `Cargo`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`,
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
    AND `Anno` <=1955
    AND `T`.`Electo` =1
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
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`, `Partidos_previos`
) AS `Candidatura_peronista` 
ON `Todos`.`Anno` = `Candidatura_peronista`.`Anno`
AND  `Todos`.`Cargo` = `Candidatura_peronista`.`Cargo`
AND `Candidatura_peronista`.`Partidos_previos` = 'Peronista'

LEFT JOIN (
  SELECT  `Anno`, `Cargo`, `Partidos`, `Partidos_previos`, COUNT( * ) AS `Total`
  FROM (
    SELECT  DISTINCT `T`.`ID_Persona`,
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`,
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
    AND `Anno` <=1955
    AND `T`.`Electo` =1
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
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  AND `Partidos_previos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`, `Partidos_previos`
) AS `Candidatura_otros` 
ON `Todos`.`Anno` = `Candidatura_otros`.`Anno`
AND  `Todos`.`Cargo` = `Candidatura_otros`.`Cargo`
AND `Candidatura_otros`.`Partidos_previos` = 'Otros'

ORDER BY `Todos`.`Anno`, 
  CASE `Todos`.`Cargo` 
    WHEN 'Diputado Nacional' THEN 3
    WHEN 'Senador Provincial' THEN 2 
    ELSE 1 
  END;