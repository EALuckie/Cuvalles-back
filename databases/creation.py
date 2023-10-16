"""
CREATE TABLE `Thesis`.`Usuarios` (`iD_Usuarios` INT NOT NULL , `Nombres` VARCHAR(45) NOT NULL , `Ap_paterno` VARCHAR(45) NOT NULL , `Ap_materno` VARCHAR(45) NOT NULL , `Email` VARCHAR(20) NOT NULL , `Tipo_usuario` INT NOT NULL , `Foto_perfil` VARCHAR(45) NOT NULL ) ENGINE = InnoDB COMMENT = 'Subject to change';

CREATE TABLE `Thesis`.`Tipo_usuario` (`iD_Tipo` INT NOT NULL , `Tipo` VARCHAR(10) NOT NULL ) ENGINE = InnoDB;

"""