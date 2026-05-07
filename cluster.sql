CREATE TABLE `cluster` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `spotter` VARCHAR(32) NOT NULL,
  `freq` DECIMAL(10,1) NOT NULL,
  `dx` VARCHAR(32) NOT NULL,
  `message` TEXT DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX (`dx`),
  INDEX (`spotter`),
  INDEX (`timestamp`)
);