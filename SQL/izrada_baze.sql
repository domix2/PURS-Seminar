DROP DATABASE IF EXISTS seminar;
CREATE DATABASE seminar;
USE seminar;
    
CREATE TABLE korisnik (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50) NOT NULL,
    prezime CHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password BINARY(32) NOT NULL
    );

DROP USER IF EXISTS domi;
CREATE USER domi@'%' IDENTIFIED BY '1234';

DROP TABLE korisnik;
    

    
    

