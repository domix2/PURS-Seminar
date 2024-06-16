DROP DATABASE IF EXISTS seminar;
CREATE DATABASE seminar;
USE seminar;
    
CREATE TABLE korisnik(
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50) NOT NULL,
    prezime CHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) 
    );

DROP USER IF EXISTS domi;
CREATE USER domi@'%' IDENTIFIED BY '1234';

DROP TABLE korisnik;
    
CREATE TABLE temperatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    datetime DATETIME,
    value FLOAT,
    FOREIGN KEY (username) REFERENCES korisnik(username),
    INDEX fk_temperatura_korisnik_idx (username)
);

CREATE TABLE vlaga (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    datetime DATETIME,
    value FLOAT,
    FOREIGN KEY (username) REFERENCES korisnik(username),
    INDEX fk_vlaga_korisnik_idx (username)
);

CREATE INDEX idx_korisnik_username ON korisnik(username);
DROP INDEX idx_korisnik_username ON korisnik;

CREATE TABLE izmjereni_rezultati ( 
		id INT AUTO_INCREMENT PRIMARY KEY,
        Temperatura FLOAT,
        Vlaga FLOAT,
        Vrijeme TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

