# Devuelve un cuadro con los siguientes datos:
#
# Anno   Partidos          Total     Candidatura   Diputado      Senador       Diputado      Elector de    Elector de
#                                    previa        provincial    provincial    nacional      gobernador    presidente
# 1946   Laborista         x         x             x             x             x             x             x
# 1946   Radical (J. R.)   x         x             x             x             x             x             x
# 1948   Peronista         x         x             x             x             x             x             x
# 1951   Peronista         x         x             x             x             x             x             x
# 1954   Peronista         x         x             x             x             x             x             x
#

SELECT `Todos`.`Anno`, `Todos`.`Partidos`, `Todos`.`Total`, 
  `Candidatura_previa`.`Total` AS `Candidatura previa`, 
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_nacional`.`Total` AS `Diputado nacional`,
  `Elector_gobernador`.`Total` AS `Elector de gobernador`,
  `Elector_presidente`.`Total` AS `Elector de presidente`
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
    AND `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND `T`.`Ambito` =  'Provincial'
    AND `Previos`.`Anno` < `T`.`Anno`
    AND `Previos`.`Cargo` =  'Diputado'
    AND `Previos`.`Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Diputado_provincial` 
ON `Todos`.`Anno` = `Diputado_provincial`.`Anno`
AND  `Todos`.`Partidos` = `Diputado_provincial`.`Partidos`

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
    AND `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
    AND `Previos`.`Cargo` =  'Senador'
    AND  `Previos`.`Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Senador_provincial` 
ON `Todos`.`Anno` = `Senador_provincial`.`Anno`
AND  `Todos`.`Partidos` = `Senador_provincial`.`Partidos`

LEFT JOIN (
  SELECT DISTINCT `Anno`, `Partidos`, COUNT( * )  AS `Total`
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
    WHERE  `T`.`Anno` >= 1946
    AND `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
    AND `Previos`.`Cargo` =  'Diputado'
    AND  `Previos`.`Ambito` =  'Nacional'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Diputado_nacional` 
ON `Todos`.`Anno` = `Diputado_nacional`.`Anno`
AND  `Todos`.`Partidos` = `Diputado_nacional`.`Partidos`

LEFT JOIN (
  SELECT  `Anno`, `Partidos`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` = 1946 THEN '1946'
      WHEN `T`.`Anno` = 1948 THEN '1948'
      WHEN `T`.`Anno` >=1951 AND `T`.`Anno` <=1955 THEN '1951 a 1955'
    END AS `Anno`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >= 1946
    AND `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
    AND `Previos`.`Cargo` =  'Elector'
    AND  `Previos`.`Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Elector_gobernador` 
ON `Todos`.`Anno` = `Elector_gobernador`.`Anno`
AND  `Todos`.`Partidos` = `Elector_gobernador`.`Partidos`

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
    WHERE  `T`.`Anno` >= 1946
    AND `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < `T`.`Anno`
    AND `Previos`.`Cargo` =  'Elector'
    AND  `Previos`.`Ambito` =  'Nacional'
  ) AS  `T` 
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Partidos`
) AS `Elector_presidente` 
ON `Todos`.`Anno` = `Elector_presidente`.`Anno`
AND  `Todos`.`Partidos` = `Elector_presidente`.`Partidos`

ORDER BY `Todos`.`Anno`, CASE `Todos`.`Partidos` 
      WHEN 'Autonomista-Liberal' THEN 1
      WHEN 'Radicales' THEN 2
      WHEN 'Laborista' THEN 3
      WHEN 'Radical (J. R.)' THEN 3
      WHEN 'Peronista' THEN 3
    END;