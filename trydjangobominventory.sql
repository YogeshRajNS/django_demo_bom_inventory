CREATE DATABASE bom_inventory_db;
use bom_inventory_db;
CREATE TABLE inventory3_component (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    available_quantity INT NOT NULL
);
INSERT INTO inventory3_component (name, available_quantity) VALUES
('Resistor', 1000),
('Capacitor', 500),
('Diode', 300),
('Transistor', 200);
RENAME TABLE inventory_component TO inventory3_component;
DROP DATABASE bom_inventory_db;  -- Replace with the actual name of your database
