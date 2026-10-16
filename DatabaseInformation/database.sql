-- This is the Schema used for the website database having a user table where the id is the primary key and the username and email are unique

DROP SCHEMA websiteDatabase;
GO

CREATE SCHEMA websiteDatabase;
GO
USE websiteDatabase;



CREATE TABLE Users (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

