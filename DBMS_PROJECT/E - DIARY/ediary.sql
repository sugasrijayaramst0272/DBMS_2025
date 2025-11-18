CREATE DATABASE ediary;
USE ediary;
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);
CREATE TABLE Diary_Entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(100),
    content TEXT,
    entry_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
