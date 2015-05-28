# Devuelve un cuadro con los siguientes datos:
#
# Partidos        Cargo            Total   Diputado     Diputado      Senador       Diputado      Elector de    Elector de
#                                          nacional     provincial    provincial    nacional      gobernador    presidente
# Autonomi...     Diputado prov.   x       x            x             x             x             x             x
# Autonomi...     Senador prov.    x       x            x             x             x             x             x
# Autonomi...     Diputado nac.    x       x            x             x             x             x             x
# Radicales       [...]
# Peronistas

SELECT `Todos`.`Partidos`, `Todos`.`Cargo`, `Todos`.`Total`, 
  `Diputado_nacional`.`Total` AS `Diputado Nacional`, 
  `Senador_provincial`.`Total` AS `Senador provincial`,
  `Diputado_provincial`.`Total` AS `Diputado provincial`,
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
    `Cargo`, 
    COUNT( * ) AS `Total`
  FROM (
    SELECT `ID_Persona`,  
      `Partido`, 
      CONCAT(`Cargo`, ' ',  `Ambito`) AS `Cargo`
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
  GROUP BY  `Partidos`, `Cargo`
) AS `Todos`

LEFT JOIN (
  SELECT `Partidos`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE `T`.`Partido` 
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
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND  `T`.`Electo` =1
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
  GROUP BY `Partidos`, `Cargo`, `Cargo_previo`
) AS `Diputado_nacional`
ON `Todos`.`Partidos` = `Diputado_nacional`.`Partidos`
AND `Todos`.`Cargo` = `Diputado_nacional`.`Cargo`
AND `Diputado_nacional`.`Cargo_previo` = 'Diputado Nacional'

LEFT JOIN (
  SELECT `Partidos`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE `T`.`Partido` 
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
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND  `T`.`Electo` =1
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
  GROUP BY `Partidos`, `Cargo`, `Cargo_previo`
) AS `Senador_provincial`
ON `Todos`.`Partidos` = `Senador_provincial`.`Partidos`
AND `Todos`.`Cargo` = `Senador_provincial`.`Cargo`
AND `Senador_provincial`.`Cargo_previo` = 'Senador Provincial'

LEFT JOIN (
  SELECT `Partidos`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE `T`.`Partido` 
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
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND  `T`.`Electo` =1
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
  GROUP BY `Partidos`, `Cargo`, `Cargo_previo`
) AS `Diputado_provincial`
ON `Todos`.`Partidos` = `Diputado_provincial`.`Partidos`
AND `Todos`.`Cargo` = `Diputado_provincial`.`Cargo`
AND `Diputado_provincial`.`Cargo_previo` = 'Diputado Provincial'

LEFT JOIN (
  SELECT `Partidos`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE `T`.`Partido` 
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
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND  `T`.`Electo` =1
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
  GROUP BY `Partidos`, `Cargo`, `Cargo_previo`
) AS `Elector_presidente`
ON `Todos`.`Partidos` = `Elector_presidente`.`Partidos`
AND `Todos`.`Cargo` = `Elector_presidente`.`Cargo`
AND `Elector_presidente`.`Cargo_previo` = 'Elector Nacional'

LEFT JOIN (
  SELECT `Partidos`, `Cargo`, `Cargo_previo`, COUNT(*) AS `Total`
  FROM (
    SELECT DISTINCT `T`.`ID_Persona`, 
    CASE `T`.`Partido` 
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
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS  `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE  `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND  `T`.`Electo` =1
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
  GROUP BY `Partidos`, `Cargo`, `Cargo_previo`
) AS `Elector_gobernador`
ON `Todos`.`Partidos` = `Elector_gobernador`.`Partidos`
AND `Todos`.`Cargo` = `Elector_gobernador`.`Cargo`
AND `Elector_gobernador`.`Cargo_previo` = 'Elector Provincial'

WHERE `Todos`.`Partidos` IS NOT NULL
ORDER BY CASE `Todos`.`Partidos` 
    WHEN 'Peronistas' THEN 3
    WHEN 'Radicales' THEN 2 
    ELSE 1 
  END, 
  CASE `Todos`.`Cargo` 
    WHEN 'Diputado Nacional' THEN 3
    WHEN 'Senador Provincial' THEN 2 
    ELSE 1 
  END;