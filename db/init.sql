CREATE DATABASE IF NOT EXISTS mydatabase;

USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id_submission INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stattest VARCHAR(255) NOT NULL,
    bitseq BLOB NOT NULL,
    pvalue VARCHAR(255) NOT NULL,
    significance VARCHAR(255) NOT NULL,
    stat VARCHAR(255) NOT NULL
);
