SELECT DISTINCT CONCAT(`T`.`Apellido`, ' ', `T`.`Nombre`), 
    CONCAT(`T`.`Cargo`, ' ',  `T`.`Ambito`) AS `Cargo`, 
    `T`.`Anno`, 
    `T`.`Partido`,
    CONCAT(`Previos`.`Cargo`, ' ',  `Previos`.`Ambito`) AS `Cargo_previo`,
    `Previos`.`Anno`, 
    `Previos`.`Partido`,
    IF(`Previos`.`Electo` = 1, 'si', 'no') AS `Electo`
    FROM  `Listado`  AS  `T` 
    INNER JOIN  `Listado` AS `Previos` 
      ON `Previos`.`ID_Persona` =  `T`.`ID_Persona` 
    WHERE `T`.`Anno` >=1946
    AND `T`.`Anno` <=1955
    AND `T`.`Electo` =1
    AND (
        (
            `T`.`Cargo` =  'Senador'
            AND `T`.`Ambito` =  'Provincial'
        )
        OR (
            `T`.`Cargo` =  'Diputado'
            AND `T`.`Ambito` =  'Provincial'
        )
        OR (
            `T`.`Cargo` =  'Diputado'
            AND `T`.`Ambito` =  'Nacional'
        )
    )
    AND (
        `T`.`Partido` = 'Laborista Correntino'
        OR `T`.`Partido` = 'Radical (Junta Reorganizadora)'
        OR `T`.`Partido` = 'Peronista'
    )
    AND  `Previos`.`Anno` < `T`.`Anno`  
ORDER BY `T`.`Anno` ASC
