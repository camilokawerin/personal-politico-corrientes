# Devuelve un cuadro con los siguientes datos:
#
# Partido       Total   Ocuparon    Fueron        Diputado      Senador       Diputado      Elector de    Elector de
#                       cargos      candidatos    provincial    provincial    nacional      gobernador    presidente
# Autonomi...   x       x           x             x             x             x             x             x
# Radicales     x       x           x             x             x             x             x             x
# Peronistas    x       x           x             x             x             x             x             x
# 

SELECT `Todos`.`Partidos`, `Todos`.`Total`, 
  `Con_cargo_previo`.`Total` AS `Ocuparon cargos`, 
  `Con_candidatura_previa`.`Total` AS `Fueron candidatos`, 
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_nacional`.`Total` AS `Diputado nacional`,
  `Elector_gobernador`.`Total` AS `Elector de gobernador`,
  `Elector_presidente`.`Total` AS `Elector de presidente`
FROM (
  SELECT CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`,  `Partido`
    FROM  `Listado` AS  `T` 
    WHERE  `Anno` >=1946
    AND `Anno` <=1955
    AND  `Electo` =1
    AND (
     `Cargo` =  'Diputado'
    OR  `Cargo` =  'Senador'
    )
    AND  `Ambito` =  'Provincial'
    GROUP BY `ID_Persona`
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Todos`

LEFT JOIN (
  SELECT  CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Con_cargo_previo` 
ON `Todos`.`Partidos` = `Con_cargo_previo`.`Partidos`

LEFT JOIN (
  SELECT  CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido` 
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON  `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
      AND `T`.`Anno` <=1955
      AND  `T`.`Electo` =1
      AND (
      `T`.`Cargo` =  'Diputado'
      OR  `T`.`Cargo` =  'Senador'
      )
      AND  `T`.`Ambito` =  'Provincial'
      AND  `Previos`.`Anno` <1946
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Con_candidatura_previa` 
ON `Todos`.`Partidos` = `Con_candidatura_previa`.`Partidos`

LEFT JOIN (
  SELECT   CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Diputado_provincial` 
ON `Todos`.`Partidos` = `Diputado_provincial`.`Partidos`
LEFT JOIN (
  SELECT   CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Senador_provincial` 
ON `Todos`.`Partidos` = `Senador_provincial`.`Partidos`
LEFT JOIN (
  SELECT   CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Diputado_nacional` 
ON `Todos`.`Partidos` = `Diputado_nacional`.`Partidos`
LEFT JOIN (
  SELECT   CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Elector_gobernador` 
ON `Todos`.`Partidos` = `Elector_gobernador`.`Partidos`
LEFT JOIN (
  SELECT   CASE `Partido` 
      WHEN 'Demócrata Nacional (Autonomista)' THEN 'Autonomista-Liberal'
      WHEN 'Demócrata Nacional (Distrito Corrientes)' THEN 'Autonomista-Liberal'
      WHEN 'Liberal' THEN 'Autonomista-Liberal'
      WHEN 'Radical (Comité Nacional)' THEN 'Radicales'
      WHEN 'Radical Antipersonalista' THEN 'Radicales'
      WHEN 'Radical' THEN 'Radicales'
      WHEN 'Laborista Correntino' THEN 'Peronistas'
      WHEN 'Radical (Junta Reorganizadora)' THEN 'Peronistas'
      WHEN 'Peronista' THEN 'Peronistas'
    END AS `Partidos`, 
    COUNT( * )  AS `Total`
  FROM (
      SELECT DISTINCT `T`.`ID_Persona`, `T`.`Partido`
      FROM  `Listado`  AS  `T` 
      INNER JOIN  `Listado` AS  `Previos` 
        ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
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
  ) AS  `T` 
  GROUP BY  `Partidos`
) AS `Elector_presidente` 
ON `Todos`.`Partidos` = `Elector_presidente`.`Partidos`

ORDER BY CASE `Todos`.`Partidos`
    WHEN 'Autonomista-Liberal' THEN 1
    WHEN 'Radicales' THEN 2
    WHEN 'Peronistas' THEN 3
  END;