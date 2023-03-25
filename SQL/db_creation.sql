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
DROP TABLE IF EXISTS `hvz`.`players`;

CREATE TABLE IF NOT EXISTS `hvz`.`players` (
  # player_id column, the primary key, generated by SQL.
  `player_id`  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  # user_id is an ID generated by Firebase. Its unique.
  `user_id` VARCHAR(45) UNIQUE NOT NULL,
  # a_number is a student id number assigned by usu.
  `a_number` VARCHAR(45) NOT NULL,
  # a constreaing requiring a numbers be an a followed by 8 numbers.
  CONSTRAINT valid_a_number CHECK (a_number REGEXP '^[Aa][0-9]{8}$'),
  # callsign, an optional nickname
  `callsign` VARCHAR(45) NULL,
  # the users first name
  `fname` VARCHAR(45) NOT NULL,
  # the users last name
  `lname` VARCHAR(45) NOT NULL,
  # a discord id is somthing we will theoreticly need for discored intagration.
  `discord_id` VARCHAR(45) NULL,
  # email, for contacting people.
  `email` VARCHAR(45) NOT NULL,
  # a constraint requiring the email be in a valid format.
  CONSTRAINT valid_email CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  # phone, for contact via text.
  `phone_number` VARCHAR(10) NULL,
  # a constraint requiring phone numbers be 10 numbers
  CONSTRAINT valid_phone_number CHECK (phone_number REGEXP '^[0-9]{10}$'),
  # two factor auth key, required for a potental feature implimentation of Two factor authentication
  `twoFA_key` VARCHAR(45) NULL,
  # the contact methon the players prefers
  `contact_method` ENUM('text', 'email', 'discord', 'all') NOT NULL DEFAULT 'email',
  # spesify the player_id is the primary key.
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `hvz`.`games`
-- -----------------------------------------------------
# clear the old table
DROP TABLE IF EXISTS `hvz`.`games` ;

# create the table
CREATE TABLE IF NOT EXISTS `hvz`.`games` (
  # new column game_id, the primary key
  `game_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  # the name of the game, public facing
  `game_name` VARCHAR(45) UNIQUE NOT NULL,
  # a time for the game to automaticly start
  `game_start_time` VARCHAR(45) NULL,
  # wther or not the game is active, can people sign up for the game, register or not
  `is_game_active` ENUM("y", "n") NOT NULL DEFAULT "n",
  # make sure only one game is active at a time
  CONSTRAINT chk_is_game_active CHECK (
    (`is_game_active` = 'y' AND (SELECT COUNT(*) FROM games WHERE is_game_active = 'y') = 1)
    OR `is_game_active` = 'n'
   ),
   # are people safe from being tagged? when set to y you cannot tag people
  `is_safe_active` ENUM("y", "n") NOT NULL DEFAULT "n",
  # the gmail key 
  `game_email_key` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`game_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`equipment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`equipment` ;

CREATE TABLE IF NOT EXISTS `hvz`.`equipment` (
  `equipment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `equipment_name` VARCHAR(45) NOT NULL,
  `equipment_discription` VARCHAR(75) NULL,
  PRIMARY KEY (`equipment_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`tag_codes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_codes` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_codes` (
  `tag_code_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tag_code` VARCHAR(45) UNIQUE NOT NULL,
  PRIMARY KEY (`tag_code_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hvz`.`roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`roles`;

CREATE TABLE IF NOT EXISTS `hvz`.`roles`(
	`role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `role_name` VARCHAR(45) UNIQUE NOT NULL,
    # a json discribing the permitions of users with this role
    `perm_file_path` VARCHAR(75) NOT NULL,
    # a discription of the role
    `role_discription` VARCHAR(75) NULL,
    PRIMARY KEY (`role_id`)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`states`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`states` ;

CREATE TABLE IF NOT EXISTS `hvz`.`states` (
  `states_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `state` VARCHAR(45) NOT NULL,
  # a discription of the role
  `state_discription`  VARCHAR(75) NULL,
  PRIMARY KEY (`states_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`lore` (
  `lore_id` INT UNSIGNED NOT NULL,
  # the HTML address of the lore doc
  `lore_address` VARCHAR(45) NOT NULL,
  # a time at which the lore becomes visible 
  `release_time` VARCHAR(45) NULL,
  PRIMARY KEY (`lore_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`tag_registry`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`tag_registry` ;

CREATE TABLE IF NOT EXISTS `hvz`.`tag_registry` (
  # the players_id of the human that got tagged
  `human_id` INT UNSIGNED NOT NULL,
  # the player_id of the zombie that did the tagging
  `zombie_id` INT UNSIGNED NOT NULL,
  # the game the tag was a part of
  `game_id` INT UNSIGNED NOT NULL,
  # gps cordinates spesifying the exact location of the tag
  `location_exact` VARCHAR(45) NULL,
  # a short discription of where the tag took place.
  `location_discription` VARCHAR(45) NULL,
  # The time the tag took place. There should be some kind of override
  `time` VARCHAR(45) NULL,
  # spesify the primary key is a compound key of the human zombie and game ids
  PRIMARY KEY (`human_id`, `zombie_id`, `game_id`),
  INDEX `fk_players_players_players1_idx` (`zombie_id` ASC) VISIBLE,
  INDEX `fk_players_players_players_idx` (`human_id` ASC) VISIBLE,
  INDEX `fk_tag_registry_games1_idx` (`game_id` ASC) VISIBLE,
  # human_id is a foreign key player_id form players table
  CONSTRAINT `fk_players_players_players`
    FOREIGN KEY (`human_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  # zobmie_id is a foreign key player_id form players table
  CONSTRAINT `fk_players_players_players1`
    FOREIGN KEY (`zombie_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  # game_id is a foreign key game_id form games table
  CONSTRAINT `fk_tag_registry_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `hvz`.`games` (`game_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hvz`.`players_games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`players_games` ;

CREATE TABLE IF NOT EXISTS `hvz`.`players_games` (
  # the player that is registering.
  `player_id` INT UNSIGNED NOT NULL,
  # the game they are registering for.
  `game_id` INT UNSIGNED NOT NULL,
  # the tag code they have for this game
  `tag_code_id` INT UNSIGNED NOT NULL,
  # the state they currently have
  `states_id` INT UNSIGNED NOT NULL,
  # ive removed states_id and tage_code_id from the primary key declaration
  # as i only want the combo of player_id and game_id to be unique
  PRIMARY KEY (`player_id`, `game_id`),
  INDEX `fk_players_games_games1_idx` (`game_id` ASC) VISIBLE,
  INDEX `fk_players_games_players1_idx` (`player_id` ASC) VISIBLE,
  INDEX `fk_players_games_tag_codes1_idx` (`tag_code_id` ASC) VISIBLE,
  INDEX `fk_players_games_states1_idx` (`states_id` ASC) VISIBLE,
  CONSTRAINT `fk_players_games_players1`
    FOREIGN KEY (`player_id`)
    REFERENCES `hvz`.`players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_games_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `hvz`.`games` (`game_id`)
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
-- Table `hvz`.`roles_lore`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hvz`.`roles_lore` ;

CREATE TABLE IF NOT EXISTS `hvz`.`roles_lore` (
  `role_id` INT UNSIGNED NOT NULL,
  `lore_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`role_id`, `lore_id`),
  INDEX `fk_tag_codes_lore_lore1_idx` (`lore_id` ASC) VISIBLE,
  INDEX `fk_tag_codes_lore_roles1_idx` (`role_id` ASC) VISIBLE,
  CONSTRAINT `fk_roles_lore_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `hvz`.`roles` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_roles_lore_lore1`
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
  `player_id`  INT UNSIGNED NOT NULL,
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
ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
