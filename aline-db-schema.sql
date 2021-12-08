-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema alinedb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema alinedb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `alinedb` DEFAULT CHARACTER SET utf8mb4 ;
USE `alinedb` ;

-- -----------------------------------------------------
-- Table `alinedb`.`bank`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`bank` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `routing_number` VARCHAR(9) NOT NULL,
  `state` VARCHAR(255) NOT NULL,
  `zipcode` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`branch`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`branch` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `phone` VARCHAR(255) NULL DEFAULT NULL,
  `state` VARCHAR(255) NULL DEFAULT NULL,
  `zipcode` VARCHAR(255) NULL DEFAULT NULL,
  `bank_id` BIGINT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `UK_243da5619wvedk7ah55d50tph` (`phone` ASC),
  INDEX `FKpolhgo6c86h7rrcwvg3hqm32l` (`bank_id` ASC),
  CONSTRAINT `FKpolhgo6c86h7rrcwvg3hqm32l`
    FOREIGN KEY (`bank_id`)
    REFERENCES `alinedb`.`bank` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`applicant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`applicant` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `date_of_birth` DATE NOT NULL,
  `drivers_license` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `gender` VARCHAR(255) NOT NULL,
  `income` INT NOT NULL,
  `last_modified_at` DATETIME NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `mailing_address` VARCHAR(255) NOT NULL,
  `mailing_city` VARCHAR(255) NOT NULL,
  `mailing_state` VARCHAR(255) NOT NULL,
  `mailing_zipcode` VARCHAR(255) NOT NULL,
  `middle_name` VARCHAR(255) NULL DEFAULT NULL,
  `phone` VARCHAR(255) NOT NULL,
  `social_security` VARCHAR(255) NOT NULL,
  `state` VARCHAR(255) NOT NULL,
  `zipcode` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `UK_g8sypjb2jlijcs4k2ga9xf3w3` (`drivers_license` ASC),
  UNIQUE INDEX `UK_6iduje2h6ggdlnmevw2mvolfx` (`email` ASC),
  UNIQUE INDEX `UK_s4gkylihid0qmetrspjnnvy4h` (`phone` ASC),
  UNIQUE INDEX `UK_5p56ol6x0k8os5qytfdswas4u` (`social_security` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`member` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `membership_id` VARCHAR(255) NULL DEFAULT NULL,
  `applicant_id` BIGINT NOT NULL,
  `branch_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `UK_s9bjipf16bofq8s92fj484x7e` (`applicant_id` ASC),
  UNIQUE INDEX `UK_hwbt6hiajpf0qtgxwhlmahbcx` (`membership_id` ASC),
  INDEX `FK1uj76dnpxoa9i8afaaslycb59` (`branch_id` ASC),
  CONSTRAINT `FK1uj76dnpxoa9i8afaaslycb59`
    FOREIGN KEY (`branch_id`)
    REFERENCES `alinedb`.`branch` (`id`),
  CONSTRAINT `FKmhn91ma4lb6uiy6n1ao6tbwkj`
    FOREIGN KEY (`applicant_id`)
    REFERENCES `alinedb`.`applicant` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`account` (
  `account_type` VARCHAR(31) NOT NULL,
  `id` BIGINT NOT NULL,
  `account_number` VARCHAR(255) NULL DEFAULT NULL,
  `balance` INT NOT NULL,
  `status` VARCHAR(255) NULL DEFAULT NULL,
  `available_balance` INT NULL DEFAULT NULL,
  `apy` FLOAT NULL DEFAULT NULL,
  `primary_account_holder_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `UK_66gkcp94endmotfwb8r4ocxm9` (`account_number` ASC),
  INDEX `FK8mr193rmld8wwqn5nlbr8vclx` (`primary_account_holder_id` ASC),
  CONSTRAINT `FK8mr193rmld8wwqn5nlbr8vclx`
    FOREIGN KEY (`primary_account_holder_id`)
    REFERENCES `alinedb`.`member` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`account_holder`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`account_holder` (
  `member_id` BIGINT NOT NULL,
  `account_id` BIGINT NOT NULL,
  PRIMARY KEY (`member_id`, `account_id`),
  INDEX `FKn4212xs4wsfh8cfj9rddju6ic` (`account_id` ASC),
  CONSTRAINT `FKg06e1tl3h06l29ok6lc09l0xh`
    FOREIGN KEY (`member_id`)
    REFERENCES `alinedb`.`member` (`id`),
  CONSTRAINT `FKn4212xs4wsfh8cfj9rddju6ic`
    FOREIGN KEY (`account_id`)
    REFERENCES `alinedb`.`account` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`account_sequence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`account_sequence` (
  `next_val` BIGINT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`application`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`application` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `application_status` VARCHAR(255) NOT NULL,
  `application_type` VARCHAR(255) NOT NULL,
  `primary_applicant_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FKny8me56a33jdg423v5n7j5fpx` (`primary_applicant_id` ASC),
  CONSTRAINT `FKny8me56a33jdg423v5n7j5fpx`
    FOREIGN KEY (`primary_applicant_id`)
    REFERENCES `alinedb`.`applicant` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`application_applicant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`application_applicant` (
  `application_id` BIGINT NOT NULL,
  `applicant_id` BIGINT NOT NULL,
  PRIMARY KEY (`application_id`, `applicant_id`),
  INDEX `FK3iabmdimkfk9q1s3vg0s8hc1q` (`applicant_id` ASC),
  CONSTRAINT `FK3iabmdimkfk9q1s3vg0s8hc1q`
    FOREIGN KEY (`applicant_id`)
    REFERENCES `alinedb`.`applicant` (`id`),
  CONSTRAINT `FKahrhusgia8sp6xy44fbjhc1po`
    FOREIGN KEY (`application_id`)
    REFERENCES `alinedb`.`application` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`merchant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`merchant` (
  `code` VARCHAR(8) NOT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(255) NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `name` VARCHAR(150) NOT NULL,
  `registered_at` DATETIME NULL DEFAULT NULL,
  `state` VARCHAR(255) NULL DEFAULT NULL,
  `zipcode` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`user` (
  `role` VARCHAR(31) NOT NULL,
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `enabled` BIT(1) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `phone` VARCHAR(255) NULL DEFAULT NULL,
  `member_id` BIGINT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `FKtcx8a5i8q7mmh7xl2fi44o8v2` (`member_id` ASC),
  CONSTRAINT `FKtcx8a5i8q7mmh7xl2fi44o8v2`
    FOREIGN KEY (`member_id`)
    REFERENCES `alinedb`.`member` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`one_time_passcode`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`one_time_passcode` (
  `id` INT NOT NULL,
  `checked` BIT(1) NOT NULL,
  `otp` VARCHAR(255) NULL DEFAULT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `UK_7h269l2tqwy5woq1uwxqpu9lb` (`user_id` ASC),
  CONSTRAINT `FKb8d16b0xvwqnabfyxk2kss9aj`
    FOREIGN KEY (`user_id`)
    REFERENCES `alinedb`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`otp_sequence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`otp_sequence` (
  `next_val` BIGINT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`transaction` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `amount` INT NOT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `initial_balance` INT NOT NULL,
  `last_modified` DATETIME NULL DEFAULT NULL,
  `method` VARCHAR(255) NOT NULL,
  `posted_balance` INT NULL DEFAULT NULL,
  `state` VARCHAR(255) NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  `type` VARCHAR(255) NOT NULL,
  `account_id` BIGINT NOT NULL,
  `merchant_code` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK6g20fcr3bhr6bihgy24rq1r1b` (`account_id` ASC),
  INDEX `FKsc1ms700fjxqyq0j4555uc28a` (`merchant_code` ASC),
  CONSTRAINT `FK6g20fcr3bhr6bihgy24rq1r1b`
    FOREIGN KEY (`account_id`)
    REFERENCES `alinedb`.`account` (`id`),
  CONSTRAINT `FKsc1ms700fjxqyq0j4555uc28a`
    FOREIGN KEY (`merchant_code`)
    REFERENCES `alinedb`.`merchant` (`code`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `alinedb`.`user_registration_token`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alinedb`.`user_registration_token` (
  `token` VARCHAR(255) NOT NULL,
  `created` DATETIME NULL DEFAULT NULL,
  `expiration_delay` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`token`),
  UNIQUE INDEX `UK_qf9m08d1bd11csrr3poot0jgd` (`user_id` ASC),
  CONSTRAINT `FKgl6uc7145cqyd47qst0glqwmv`
    FOREIGN KEY (`user_id`)
    REFERENCES `alinedb`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
