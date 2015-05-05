# Devuelve un cuadro con los siguientes datos:
#
# Periodo       Total   Ocuparon      Diputado      Senador       Diputado      Elector de    Elector de
#                       cargos        provincial    provincial    nacional      gobernador    presidente
# 1919 a 1929   x       x             x             x             x             x             x
# 1931 a 1943   x       x             x             x             x             x             x
# 1946 a 1955   x       x             x             x             x             x             x
#
SELECT `Todos`.`Periodo`, `Todos`.`Total`, 
  IFNULL(`Con_cargo_previo`.`Total`, 0) AS `Ocuparon cargos`, 
  IFNULL(`Diputado_provincial`.`Total`, 0) AS `Diputado provincial`,
  IFNULL(`Senador_provincial`.`Total`, 0) AS `Senador provincial`,
  IFNULL(`Diputado_nacional`.`Total`, 0) AS `Diputado nacional`,
  IFNULL(`Elector_gobernador`.`Total`, 0) AS `Elector de gobernador`,
  IFNULL(`Elector_presidente`.`Total`, 0) AS `Elector de presidente`
FROM (
  SELECT  `Periodo`, COUNT( * ) AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) 
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Todos`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      GROUP BY `T`.`ID_Persona`
    ) 
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Con_cargo_previo` 
ON `Todos`.`Periodo` = `Con_cargo_previo`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    )
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Diputado_provincial` 
ON `Todos`.`Periodo` = `Diputado_provincial`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Senador'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Senador'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Senador'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    )
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Senador_provincial` 
ON `Todos`.`Periodo` = `Senador_provincial`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Diputado'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    )
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Diputado_nacional` 
ON `Todos`.`Periodo` = `Diputado_nacional`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Provincial'
      GROUP BY `T`.`ID_Persona`
    )
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Elector_gobernador` 
ON `Todos`.`Periodo` = `Elector_gobernador`.`Periodo`
LEFT JOIN (
  SELECT  `Periodo`, COUNT( * )  AS `Total`
  FROM (
    (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1919 a 1929' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1919
      AND `T`.`Anno` <=1929
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1919
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1932 a 1942' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1931
      AND `T`.`Anno` <=1943
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1931
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    ) UNION (
      SELECT  `T`.`Nombre` ,  `T`.`Apellido`, '1946 a 1955' AS `Periodo` 
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
      WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
      AND  `Previos`.`Electo` =1
      AND `Previos`.`Cargo` =  'Elector'
      AND  `Previos`.`Ambito` =  'Nacional'
      GROUP BY `T`.`ID_Persona`
    )
  ) AS  `T` 
  GROUP BY  `Periodo`
) AS `Elector_presidente` 
ON `Todos`.`Periodo` = `Elector_presidente`.`Periodo`;
