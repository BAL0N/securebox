DROP DATABASE IF EXISTS automata ;
CREATE DATABASE automata CHARACTER SET utf8 COLLATE utf8_spanish2_ci;
USE automata ;

-- Binary objects
DROP TABLE IF EXISTS bin;
CREATE TABLE IF NOT EXISTS bin (
    id INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
PRIMARY KEY (id));