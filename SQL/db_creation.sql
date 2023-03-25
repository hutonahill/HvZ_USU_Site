-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema hvz
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema hvz
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hvz` DEFAULT CHARACTER SET utf8mb3 ;
USE `hvz` ;

-- -----------------------------------------------------
-- Table `hvz`.`equipment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`equipment` ;

CREATE TABLE IF NOT EXISTS `hvz`.`equipment` (
  `equipment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `equipment_name` VARCHAR(45) NOT NULL,
  `equipment_discription` VARCHAR(75) NULL DEFAULT NULL,
  PRIMARY KEY (`equipment_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`equipment_players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`equipment_players` ;

CREATE TABLE IF NOT EXISTS `hvz`.`equipment_players` (
  `equipment_id` INT UNSIGNED NOT NULL,
  `player_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`equipment_id`, `player_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hvz`.`games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`games` ;

CREATE TABLE IF NOT EXISTS `hvz`.`games` (
  `game_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(45) NOT NULL,
  `game_start_time` VARCHAR(45) NULL DEFAULT NULL,
  `is_game_active` ENUM('y', 'n') NOT NULL DEFAULT 'n',
  `is_safe_active` ENUM('y', 'n') NOT NULL DEFAULT 'n',
  `game_email_key` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE INDEX `game_name` (`game_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`lore` (
  `lore_id` INT UNSIGNED NOT NULL,
  `lore_address` VARCHAR(45) NOT NULL,
  `release_time` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`lore_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players` ;

-- Create the `players` table
CREATE TABLE IF NOT EXISTS `hvz`.`players` (
  `player_id` INT(7) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(45) NOT NULL,
  
  -- Define the `a_number` column, which should start with an 'a' (upper or lower) and followed by 8 digits
  `a_number` VARCHAR(45) NOT NULL CHECK (a_number REGEXP '^[aA][0-9]{8}$'),

  `callsign` VARCHAR(45) NULL DEFAULT NULL,
  `fname` VARCHAR(45) NOT NULL,
  `lname` VARCHAR(45) NOT NULL,
  `discord_id` VARCHAR(45) NULL DEFAULT NULL,
  -- Define the `email` column, which should not be null and should be in proper email format
  `email` VARCHAR(45) NOT NULL CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
  
  -- Define the `phone_number` column, which can be null and should contain 10 digits
  `phone_number` VARCHAR(10) NULL DEFAULT NULL CHECK (phone_number REGEXP '^[0-9]{10}$'),
  
  `twoFA_key` VARCHAR(45) NULL DEFAULT NULL,
  `contact_method` ENUM('text', 'email', 'discord', 'all') NOT NULL DEFAULT 'email',
  
  PRIMARY KEY (`player_id`),
  
  UNIQUE INDEX `user_id` (`user_id` ASC) VISIBLE
)
-- Define the engine and character set
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hvz`.`states`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`states` ;

CREATE TABLE IF NOT EXISTS `hvz`.`states` (
  `state_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `state` VARCHAR(45) NOT NULL,
  `state_discription` VARCHAR(75) NULL DEFAULT NULL,
  PRIMARY KEY (`state_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`players_games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players_games` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players_games` (
  `player_id` INT UNSIGNED NOT NULL,
  `game_id` INT UNSIGNED NOT NULL,
  `state_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`player_id`, `game_id`),
  INDEX `fk_players_games_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_players_games_players1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_players_games_states1_idx` (`state_id` ASC) VISIBLE,
  CONSTRAINT `fk_players_games_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `hvz`.`games` (`game_id`),
  CONSTRAINT `fk_players_games_players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `hvz`.`players` (`player_id`),
  CONSTRAINT `fk_players_games_states1`
    FOREIGN KEY (`state_id`)
    REFERENCES `hvz`.`states` (`state_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`players_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players_lore` (
  `player_id` INT NOT NULL,
  `lore_id` INT NOT NULL,
  PRIMARY KEY (`player_id`, `lore_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`roles` ;

CREATE TABLE IF NOT EXISTS `hvz`.`roles` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(45) NOT NULL,
  `perm_file_path` VARCHAR(75) NOT NULL,
  `role_discription` VARCHAR(75) NULL DEFAULT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `role_name` (`role_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`roles_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`roles_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`roles_lore` (
  `role_id` INT UNSIGNED NOT NULL,
  `lore_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`role_id`, `lore_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`states_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`states_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`states_lore` (
  `state_id` INT UNSIGNED NOT NULL,
  `lore_id` INT NOT NULL,
  PRIMARY KEY (`state_id`, `lore_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `hvz`.`tag_registry`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_registry` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_registry` (
  `human_id` INT UNSIGNED NOT NULL,
  `zombie_id` INT UNSIGNED NOT NULL DEFAULT 0000001,
  `game_id` INT UNSIGNED NOT NULL,
  `location_exact` VARCHAR(45) NULL DEFAULT NULL,
  `location_discription` VARCHAR(45) NULL DEFAULT NULL,
  `time` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`human_id`, `zombie_id`, `game_id`),
  INDEX `fk_tag_registry_players1_idx` (`zombie_id` ASC) VISIBLE,
  INDEX `fk_tag_registry_players_idx` (`human_id` ASC) VISIBLE,
  INDEX `fk_tag_registry_games1_idx` (`game_id` ASC) VISIBLE,
  CONSTRAINT `fk_tag_registry_players`
    FOREIGN KEY (`human_id`)
    REFERENCES `hvz`.`players` (`player_id`),
  CONSTRAINT `fk_tag_registry_players1`
    FOREIGN KEY (`zombie_id`)
    REFERENCES `hvz`.`players` (`player_id`),
  CONSTRAINT `fk_tag_registry_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `hvz`.`games` (`game_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
