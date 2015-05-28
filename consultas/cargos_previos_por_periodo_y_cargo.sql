# Devuelve un cuadro con los siguientes datos:
#
# Periodo        Cargo            Total   Diputado      Diputado      Senador       Diputado      Elector de    Elector de
#                                         nacional      provincial    provincial    nacional      gobernador    presidente
# 1907 a 1917    Diputado prov.   x       x             x             x             x             x             x 
# 1907 a 1917    Senador prov.    x       x             x             x             x             x             x   
# 1907 a 1917    Diputado nac.    x       x             x             x             x             x             x
# 1919 a 1929    [...] 
# 1931 a 1942
# 1946 a 1955
#




SELECT `Todos`.`Periodo`, `Todos`.`Cargo`, `Todos`.`Total`, 
  `Diputado_nacional`.`Total` AS `Diputado Nacional`, 
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
  `Elector_gobernador`.`Total` AS `Elector de gobernador`,
  `Elector_presidente`.`Total` AS `Elector de presidente`
FROM (
  SELECT  `Periodo`, `Cargo`, COUNT( * ) AS `Total`, 
    CASE `Cargo` 
      WHEN 'Diputado Nacional' THEN 3
      WHEN 'Senador Provincial' THEN 2 
      ELSE 1 
    END AS `Orden`
  FROM (
    SELECT DISTINCT `ID_Persona`, 
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`Cargo`, ' ',  `Ambito`) AS `Cargo`
    FROM  `Listado`
    WHERE  `Electo` =1
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
  GROUP BY  `Periodo`, `Cargo`
) AS `Todos`

LEFT JOIN (
  SELECT `Periodo`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1907 AND `T`.`Anno` <=1917 THEN '1907 a 1917'
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
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
    AND  `Previos`.`Electo` =1
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Periodo`, `Cargo`, `Cargo_previo`
) AS `Diputado_nacional`
ON `Todos`.`Periodo` = `Diputado_nacional`.`Periodo`
AND `Todos`.`Cargo` = `Diputado_nacional`.`Cargo`
AND `Diputado_nacional`.`Cargo_previo` = 'Diputado Nacional'

LEFT JOIN (
  SELECT `Periodo`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1907 AND `T`.`Anno` <=1917 THEN '1907 a 1917'
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
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
    AND  `Previos`.`Electo` =1
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Periodo`, `Cargo`, `Cargo_previo`
) AS `Senador_provincial`
ON `Todos`.`Periodo` = `Senador_provincial`.`Periodo`
AND `Todos`.`Cargo` = `Senador_provincial`.`Cargo`
AND `Senador_provincial`.`Cargo_previo` = 'Senador Provincial'

LEFT JOIN (
  SELECT `Periodo`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1907 AND `T`.`Anno` <=1917 THEN '1907 a 1917'
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
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
    AND  `Previos`.`Electo` =1
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Periodo`, `Cargo`, `Cargo_previo`
) AS `Diputado_provincial`
ON `Todos`.`Periodo` = `Diputado_provincial`.`Periodo`
AND `Todos`.`Cargo` = `Diputado_provincial`.`Cargo`
AND `Diputado_provincial`.`Cargo_previo` = 'Diputado Provincial'

LEFT JOIN (
  SELECT `Periodo`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1907 AND `T`.`Anno` <=1917 THEN '1907 a 1917'
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
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
    AND  `Previos`.`Electo` =1
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Periodo`, `Cargo`, `Cargo_previo`
) AS `Elector_presidente`
ON `Todos`.`Periodo` = `Elector_presidente`.`Periodo`
AND `Todos`.`Cargo` = `Elector_presidente`.`Cargo`
AND `Elector_presidente`.`Cargo_previo` = 'Elector Nacional'

LEFT JOIN (
  SELECT `Periodo`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1907 AND `T`.`Anno` <=1917 THEN '1907 a 1917'
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo`, 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
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
    AND  `Previos`.`Electo` =1
    AND  `Previos`.`Anno` < `T`.`Anno`
  ) AS `T`
  GROUP BY `Periodo`, `Cargo`, `Cargo_previo`
) AS `Elector_gobernador`
ON `Todos`.`Periodo` = `Elector_gobernador`.`Periodo`
AND `Todos`.`Cargo` = `Elector_gobernador`.`Cargo`
AND `Elector_gobernador`.`Cargo_previo` = 'Elector Provincial'

WHERE `Todos`.`Periodo` IS NOT NULL
ORDER BY `Todos`.`Periodo`, `Todos`.`Orden`;