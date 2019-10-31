CREATE DATABASE IF NOT EXISTS ciab;
USE ciab;
CREATE TABLE IF NOT EXISTS Users (
    ID int NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255),
    company VARCHAR(255),
    balance INTEGER,
    `order` VARCHAR(255),
    embedding TEXT,
    PRIMARY KEY (ID)
);

