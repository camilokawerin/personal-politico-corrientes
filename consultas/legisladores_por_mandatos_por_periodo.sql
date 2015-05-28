# Devuelve un cuadro con los siguientes datos:
#
# Periodo       Total   Ocuparon      Ocuparon      Ocuparon      Ocuparon
#                       1 cargo       2 cargos      3 cargos      4 cargos
# 1919 a 1929   x       x             x             x             x
# 1931 a 1943   x       x             x             x             x
# 1946 a 1955   x       x             x             x             x
#

SELECT `Todos`.`Periodo`, `Todos`.`Total`, 
  `Con_1_cargo`.`Total` AS `Ocuparon 1 cargo`, 
  `Con_2_cargos`.`Total` AS `Ocuparon 2 cargos`,
  `Con_3_cargos`.`Total` AS `Ocuparon 3 cargos`,
  `Con_4_cargos`.`Total` AS `Ocuparon 4 cargos`
FROM (
  SELECT  `Periodo`, COUNT( * ) AS `Total`
  FROM (
    SELECT DISTINCT `ID_Persona`, 
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
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
  SELECT  `Periodo`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, COUNT( * ) AS  `Total_mandatos`,
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`
    WHERE  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `Periodo`, `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Periodo`, `Total_mandatos`
) AS `Con_1_cargo`
ON `Todos`.`Periodo` = `Con_1_cargo`.`Periodo`
AND `Con_1_cargo`.`Total_mandatos` = 1

LEFT JOIN (
  SELECT  `Periodo`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, COUNT( * ) AS  `Total_mandatos`,
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`
    WHERE  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `Periodo`, `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Periodo`, `Total_mandatos`
) AS `Con_2_cargos`
ON `Todos`.`Periodo` = `Con_2_cargos`.`Periodo`
AND `Con_2_cargos`.`Total_mandatos` = 2

LEFT JOIN (
  SELECT  `Periodo`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, COUNT( * ) AS  `Total_mandatos`,
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`
    WHERE  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `Periodo`, `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Periodo`, `Total_mandatos`
) AS `Con_3_cargos`
ON `Todos`.`Periodo` = `Con_3_cargos`.`Periodo`
AND `Con_3_cargos`.`Total_mandatos` = 3

LEFT JOIN (
  SELECT  `Periodo`, `Total_mandatos` , COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`, COUNT( * ) AS  `Total_mandatos`,
    CASE 
      WHEN `Anno` >=1907 AND `Anno` <=1917 THEN '1907 a 1917'
      WHEN `Anno` >=1919 AND `Anno` <=1929 THEN '1919 a 1929'
      WHEN `Anno` >=1931 AND `Anno` <=1942 THEN '1931 a 1942'
      WHEN `Anno` >=1946 AND `Anno` <=1955 THEN '1946 a 1955'
    END AS `Periodo` 
    FROM  `Listado`
    WHERE  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY  `Periodo`, `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Periodo`, `Total_mandatos`
) AS `Con_4_cargos`
ON `Todos`.`Periodo` = `Con_4_cargos`.`Periodo`
AND `Con_4_cargos`.`Total_mandatos` = 4