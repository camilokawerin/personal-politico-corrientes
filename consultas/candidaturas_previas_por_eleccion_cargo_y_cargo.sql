# Devuelve un cuadro con los siguientes datos:
#
# Anno   Cargo            Total     Candidatura   Diputado      Senador       Diputado      Elector de    Elector de
#                                   previa        provincial    provincial    nacional      gobernador    presidente
# 1946   Diputado prov.   x         x             x             x             x             x             x
# 1946   Senador prov.    x         x             x             x             x             x             x
# 1946   Diputado nac.    x         x             x             x             x             x             x
# 1948   [...] 
# 1951
# 1954
#

SELECT `Todos`.`Anno`, `Todos`.`Cargo`, `Todos`.`Total`, 
  `Diputado_nacional`.`Total` AS `Diputado Nacional`, 
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
  `Elector_gobernador`.`Total` AS `Elector de gobernador`,
  `Elector_presidente`.`Total` AS `Elector de presidente`
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
    AND `Electo` =1
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
  WHERE `Partidos` IS NOT NULL
  GROUP BY  `Anno`, `Cargo`

) AS `Todos`

LEFT JOIN (
  SELECT `Anno`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`,
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
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
  ) AS `T`
  WHERE `Partidos` IS NOT NULL
  GROUP BY `Anno`, `Cargo`, `Cargo_previo`
) AS `Diputado_nacional`
ON `Todos`.`Anno` = `Diputado_nacional`.`Anno`
AND `Todos`.`Cargo` = `Diputado_nacional`.`Cargo`
AND `Diputado_nacional`.`Cargo_previo` = 'Diputado Nacional'

LEFT JOIN (
  SELECT `Anno`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
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
  ) AS `T`
  WHERE `Partidos` IS NOT NULL
  GROUP BY `Anno`, `Cargo`, `Cargo_previo`
) AS `Senador_provincial`
ON `Todos`.`Anno` = `Senador_provincial`.`Anno`
AND `Todos`.`Cargo` = `Senador_provincial`.`Cargo`
AND `Senador_provincial`.`Cargo_previo` = 'Senador Provincial'

LEFT JOIN (
  SELECT `Anno`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
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
  ) AS `T`
  WHERE `Partidos` IS NOT NULL
  GROUP BY `Anno`, `Cargo`, `Cargo_previo`
) AS `Diputado_provincial`
ON `Todos`.`Anno` = `Diputado_provincial`.`Anno`
AND `Todos`.`Cargo` = `Diputado_provincial`.`Cargo`
AND `Diputado_provincial`.`Cargo_previo` = 'Diputado Provincial'

LEFT JOIN (
  SELECT `Anno`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
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
  ) AS `T`
  WHERE `Partidos` IS NOT NULL
  GROUP BY `Anno`, `Cargo`, `Cargo_previo`
) AS `Elector_gobernador`
ON `Todos`.`Anno` = `Elector_gobernador`.`Anno`
AND `Todos`.`Cargo` = `Elector_gobernador`.`Cargo`
AND `Elector_gobernador`.`Cargo_previo` = 'Elector Provincial'

LEFT JOIN (
  SELECT `Anno`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    `T`.`Anno`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`, 
    CASE `T`.`Partido` 
      WHEN 'Laborista Correntino' THEN 'Laborista'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Radical (J. R.)'
      WHEN 'Peronista' THEN 'Peronista'
    END AS `Partidos`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
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
  ) AS `T`
  WHERE `Partidos` IS NOT NULL
  GROUP BY `Anno`, `Cargo`, `Cargo_previo`
) AS `Elector_presidente`
ON `Todos`.`Anno` = `Elector_presidente`.`Anno`
AND `Todos`.`Cargo` = `Elector_presidente`.`Cargo`
AND `Elector_presidente`.`Cargo_previo` = 'Elector Nacional'

ORDER BY `Todos`.`Anno`, 
  CASE `Todos`.`Cargo` 
    WHEN 'Diputado Nacional' THEN 3
    WHEN 'Senador Provincial' THEN 2 
    ELSE 1 
  END;