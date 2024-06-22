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
    
CREATE TABLE izmjereni_rezultati ( 
		id INT AUTO_INCREMENT PRIMARY KEY,
        Temperatura FLOAT,
        Vlaga FLOAT,
        Vrijeme TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        
DROP TABLE izmjereni_rezultati;