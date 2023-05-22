-- Prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS partnerup_test_db;
CREATE USER IF NOT EXISTS 'partnerup_test'@'localhost' IDENTIFIED BY 'partnerup_test_pwd';
GRANT ALL PRIVILEGES ON `partnerup_test_db`.* TO 'partnerup_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'partnerup_test'@'localhost';
FLUSH PRIVILEGES;