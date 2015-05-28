# Devuelve un cuadro con los siguientes datos:
#
# Periodo       Total   Ocuparon      Diputado      Senador       Diputado      Elector de    Elector de
#                       cargos        provincial    provincial    nacional      gobernador    presidente
# 1919 a 1929   x       x             x             x             x             x             x
# 1931 a 1942   x       x             x             x             x             x             x
# 1946 a 1955   x       x             x             x             x             x             x
#

SELECT `Todos`.`Periodo`, `Todos`.`Total`, 
  `Con_cargo_previo`.`Total` AS `Ocuparon cargos`, 
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_nacional`.`Total` AS `Diputado nacional`,
  `Elector_gobernador`.`Total` AS `Elector de gobernador`,
  `Elector_presidente`.`Total` AS `Elector de presidente`
FROM (
  SELECT  `Periodo`, COUNT( * ) AS `Total`
  FROM (
    SELECT DISTINCT `ID_Persona`, 
    CASE 
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`
    WHERE  `Electo` =1
    AND (
      `Cargo` =  'Diputado'
    OR `Cargo` =  'Senador'
    )
    AND `Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Todos`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Con_cargo_previo` 
ON `Todos`.`Periodo` = `Con_cargo_previo`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (

    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
    AND `Previos`.`Cargo` =  'Diputado'
    AND  `Previos`.`Ambito` =  'Provincial'

  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Diputado_provincial` 
ON `Todos`.`Periodo` = `Diputado_provincial`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END  AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
    AND `Previos`.`Cargo` =  'Senador'
    AND  `Previos`.`Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Senador_provincial` 
ON `Todos`.`Periodo` = `Senador_provincial`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END  AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
    AND `Previos`.`Cargo` =  'Diputado'
    AND  `Previos`.`Ambito` =  'Nacional'
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Diputado_nacional` 
ON `Todos`.`Periodo` = `Diputado_nacional`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END  AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
    AND `Previos`.`Cargo` =  'Elector'
    AND  `Previos`.`Ambito` =  'Provincial'
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Elector_gobernador` 
ON `Todos`.`Periodo` = `Elector_gobernador`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN '1919 a 1929'
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN '1931 a 1942'
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN '1946 a 1955'
    END  AS `Periodo` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Electo` =1
    AND (
    `T`.`Cargo` =  'Diputado'
    OR  `T`.`Cargo` =  'Senador'
    )
    AND  `T`.`Ambito` =  'Provincial'
    AND  `Previos`.`Anno` < CASE 
      WHEN `T`.`Anno` >=1919 AND `T`.`Anno` <=1929 THEN 1919
      WHEN `T`.`Anno` >=1931 AND `T`.`Anno` <=1942 THEN 1931
      WHEN `T`.`Anno` >=1946 AND `T`.`Anno` <=1955 THEN 1946
    END
    AND  `Previos`.`Electo` =1
    AND `Previos`.`Cargo` =  'Elector'
    AND  `Previos`.`Ambito` =  'Nacional'
  ) AS  `T` 
  WHERE `Periodo` IS NOT NULL
  GROUP BY  `Periodo`
) AS `Elector_presidente` 
ON `Todos`.`Periodo` = `Elector_presidente`.`Periodo`;
