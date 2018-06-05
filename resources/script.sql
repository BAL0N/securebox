DROP DATABASE IF EXISTS securebox ;
CREATE DATABASE securebox CHARACTER SET utf8 COLLATE utf8_spanish2_ci;
USE securebox ;

-- Gestión de usuarios
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
    name VARCHAR(20) NOT NULL,
    hash VARCHAR(256) NOT NULL,
    PRIMARY KEY (id));

-- Objetos cifrados
DROP TABLE IF EXISTS secrets;
CREATE TABLE IF NOT EXISTS secrets (
    id INT(11) NOT NULL AUTO_INCREMENT UNIQUE,
    name VARCHAR(100) NOT NULL,
    algorithm VARCHAR(30),
    property INT(11) NOT NULL,
    hash VARCHAR(256) NOT NULL,
    version FLOAT NOT NULL DEFAULT 1.0,
    -- validation VARCHAR(256) NOT NULL,
    cryptedfile longblob,
    cryptedpassword blob,
    cryptedinfo mediumblob,
    site VARCHAR(100) DEFAULT '',
    username VARCHAR(50) DEFAULT '',
    mail VARCHAR(100) DEFAULT '',
    notes TEXT DEFAULT '',
    PRIMARY KEY (id),
    FOREIGN KEY (property) REFERENCES users(id));

INSERT INTO users(name,hash) values('javier', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
INSERT INTO users(name,hash) values('juan', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');