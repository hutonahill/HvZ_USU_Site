-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema hvz
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema hvz
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hvz` DEFAULT CHARACTER SET utf8 ;
USE `hvz` ;

-- -----------------------------------------------------
-- Table `hvz`.`players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players` (
  `player_id` INT NOT NULL,
  `a_number` VARCHAR(45) NOT NULL,
  `callsign` VARCHAR(45) NULL,
  `discord_id` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone_number` VARCHAR(45) NULL,
  `2FA_key` VARCHAR(45) NULL,
  `contact_method` ENUM("text", "email", "discord", "all") NOT NULL DEFAULT 'email',
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`games` ;

CREATE TABLE IF NOT EXISTS `hvz`.`games` (
  `games_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(45) NULL,
  `game_start_time` VARCHAR(45) NULL,
  `is_game_active` ENUM("y", "n") NULL,
  `is_safe_active` ENUM("y", "n") NOT NULL,
  `game_email_key` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`games_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`equipment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`equipment` ;

CREATE TABLE IF NOT EXISTS `hvz`.`equipment` (
  `equipment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `equipment_name` VARCHAR(45) NULL,
  PRIMARY KEY (`equipment_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`tag_codes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_codes` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_codes` (
  `tag_code_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tag_code` VARCHAR(45) NULL,
  PRIMARY KEY (`tag_code_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`states`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`states` ;

CREATE TABLE IF NOT EXISTS `hvz`.`states` (
  `states_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `state` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`states_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`lore` (
  `lore_id` INT NOT NULL,
  `lore_address` VARCHAR(45) NOT NULL,
  `release_time` VARCHAR(45) NULL,
  PRIMARY KEY (`lore_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`tag_registry`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_registry` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_registry` (
  `human_id` INT NOT NULL,
  `zombie_id` INT NOT NULL,
  `games_id` INT UNSIGNED NOT NULL,
  `location_exact` VARCHAR(45) NULL,
  `location_discription` VARCHAR(45) NULL,
  `time` VARCHAR(45) NULL,
  PRIMARY KEY (`human_id`, `zombie_id`, `games_id`),
  INDEX `fk_players_players_players1_idx` (`zombie_id` ASC) VISIBLE,
  INDEX `fk_players_players_players_idx` (`human_id` ASC) VISIBLE,
  INDEX `fk_tag_registry_games1_idx` (`games_id` ASC) VISIBLE,
  CONSTRAINT `fk_players_players_players`
    FOREIGN KEY (`human_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_players_players1`
    FOREIGN KEY (`zombie_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tag_registry_games1`
    FOREIGN KEY (`games_id`)
    REFERENCES `hvz`.`games` (`games_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`players_games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players_games` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players_games` (
  `player_id` INT NOT NULL,
  `games_id` INT UNSIGNED NOT NULL,
  `tag_code_id` INT UNSIGNED NOT NULL,
  `states_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`player_id`, `games_id`, `tag_code_id`, `states_id`),
  INDEX `fk_players_games_games1_idx` (`games_id` ASC) VISIBLE,
  INDEX `fk_players_games_players1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_players_games_tag_codes1_idx` (`tag_code_id` ASC) VISIBLE,
  INDEX `fk_players_games_states1_idx` (`states_id` ASC) VISIBLE,
  CONSTRAINT `fk_players_games_players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_games_games1`
    FOREIGN KEY (`games_id`)
    REFERENCES `hvz`.`games` (`games_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_games_tag_codes1`
    FOREIGN KEY (`tag_code_id`)
    REFERENCES `hvz`.`tag_codes` (`tag_code_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_games_states1`
    FOREIGN KEY (`states_id`)
    REFERENCES `hvz`.`states` (`states_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`tag_codes_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_codes_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_codes_lore` (
  `tag_code_id` INT UNSIGNED NOT NULL,
  `lore_id` INT NOT NULL,
  PRIMARY KEY (`tag_code_id`, `lore_id`),
  INDEX `fk_tag_codes_lore_lore1_idx` (`lore_id` ASC) VISIBLE,
  INDEX `fk_tag_codes_lore_tag_codes1_idx` (`tag_code_id` ASC) VISIBLE,
  CONSTRAINT `fk_tag_codes_lore_tag_codes1`
    FOREIGN KEY (`tag_code_id`)
    REFERENCES `hvz`.`tag_codes` (`tag_code_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tag_codes_lore_lore1`
    FOREIGN KEY (`lore_id`)
    REFERENCES `hvz`.`lore` (`lore_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`states_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`states_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`states_lore` (
  `states_id` INT UNSIGNED NOT NULL,
  `lore_id` INT NOT NULL,
  PRIMARY KEY (`states_id`, `lore_id`),
  INDEX `fk_states_lore_lore1_idx` (`lore_id` ASC) VISIBLE,
  INDEX `fk_states_lore_states1_idx` (`states_id` ASC) VISIBLE,
  CONSTRAINT `fk_states_lore_states1`
    FOREIGN KEY (`states_id`)
    REFERENCES `hvz`.`states` (`states_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_states_lore_lore1`
    FOREIGN KEY (`lore_id`)
    REFERENCES `hvz`.`lore` (`lore_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`players_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players_lore` (
  `player_id` INT NOT NULL,
  `lore_id` INT NOT NULL,
  PRIMARY KEY (`player_id`, `lore_id`),
  INDEX `fk_players_lore_lore1_idx` (`lore_id` ASC) VISIBLE,
  INDEX `fk_players_lore_players1_idx` (`player_id` ASC) VISIBLE,
  CONSTRAINT `fk_players_lore_players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_lore_lore1`
    FOREIGN KEY (`lore_id`)
    REFERENCES `hvz`.`lore` (`lore_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`equipment_players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`equipment_players` ;

CREATE TABLE IF NOT EXISTS `hvz`.`equipment_players` (
  `equipment_id` INT UNSIGNED NOT NULL,
  `player_id` INT NOT NULL,
  PRIMARY KEY (`equipment_id`, `player_id`),
  INDEX `fk_equipment_players_players1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_equipment_players_equipment1_idx` (`equipment_id` ASC) VISIBLE,
  CONSTRAINT `fk_equipment_players_equipment1`
    FOREIGN KEY (`equipment_id`)
    REFERENCES `hvz`.`equipment` (`equipment_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_equipment_players_players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
