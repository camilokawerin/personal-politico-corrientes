# Devuelve un cuadro con los siguientes datos:
#
# Anno   Partidos          Total     Candidatura   Autonomista   Liberal       Radical      Radical
#                                    previa                                                 antipers.
# 1946   Laborista         x         x             x             x             x            x
# 1946   Radical (J. R.)   x         x             x             x             x            x
# 1948   Peronista         x         x             x             x             x            x
# 1951   Peronista         x         x             x             x             x            x
# 1954   Peronista         x         x             x             x             x            x
#

SELECT `Todos`.`Anno`, `Todos`.`Partidos`, `Todos`.`Total`, 
  `Candidatura_previa`.`Total` AS `Candidatura previa`, 
  `Candidatura_autonomista`.`Total` AS `Autonomista`,
  `Candidatura_liberal`.`Total` AS `Liberal`,
  `Candidatura_radical`.`Total` AS `Radical`,
  `Candidatura_antipersonalista`.`Total` AS `Radical antipersonalista`
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
      WHEN 'Laborista Correntino' THEN NULL
      WHEN 'Radical (Junta Reorganizadora)' THEN NULL
      WHEN 'Peronista' THEN NULL
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista'
      WHEN 'Liberal Pactista' THEN 'Liberal'
      ELSE `Previos`.`Partido`
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
      WHEN 'Laborista Correntino' THEN NULL
      WHEN 'Radical (Junta Reorganizadora)' THEN NULL
      WHEN 'Peronista' THEN NULL
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista'
      WHEN 'Liberal Pactista' THEN 'Liberal'
      ELSE `Previos`.`Partido`
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
) AS `Candidatura_autonomista` 
ON `Todos`.`Anno` = `Candidatura_autonomista`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_autonomista`.`Partidos`
AND `Candidatura_autonomista`.`Partidos_previos` = 'Autonomista'

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
      WHEN 'Laborista Correntino' THEN NULL
      WHEN 'Radical (Junta Reorganizadora)' THEN NULL
      WHEN 'Peronista' THEN NULL
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista'
      WHEN 'Liberal Pactista' THEN 'Liberal'
      ELSE `Previos`.`Partido`
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
) AS `Candidatura_liberal` 
ON `Todos`.`Anno` = `Candidatura_liberal`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_liberal`.`Partidos`
AND `Candidatura_liberal`.`Partidos_previos` = 'Liberal'

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
      WHEN 'Laborista Correntino' THEN NULL
      WHEN 'Radical (Junta Reorganizadora)' THEN NULL
      WHEN 'Peronista' THEN NULL
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista'
      WHEN 'Liberal Pactista' THEN 'Liberal'
      ELSE `Previos`.`Partido`
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
AND `Candidatura_radical`.`Partidos_previos` = 'Radical'

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
      WHEN 'Laborista Correntino' THEN NULL
      WHEN 'Radical (Junta Reorganizadora)' THEN NULL
      WHEN 'Peronista' THEN NULL
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista'
      WHEN 'Liberal Pactista' THEN 'Liberal'
      ELSE `Previos`.`Partido`
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
) AS `Candidatura_antipersonalista` 
ON `Todos`.`Anno` = `Candidatura_antipersonalista`.`Anno`
AND  `Todos`.`Partidos` = `Candidatura_antipersonalista`.`Partidos`
AND `Candidatura_antipersonalista`.`Partidos_previos` = 'Radical antipersonalista'
