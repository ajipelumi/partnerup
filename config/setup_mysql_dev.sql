-- Prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS partnerup_dev_db;
CREATE USER IF NOT EXISTS 'partnerup_dev'@'localhost' IDENTIFIED BY 'partnerup_dev_pwd';
GRANT ALL PRIVILEGES ON `partnerup_dev_db`.* TO 'partnerup_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'partnerup_dev'@'localhost';
FLUSH PRIVILEGES;