-- Crear base de datos
CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de prueba
INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', 'admin123'),
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'mypassword'),
('bob_wilson', 'bob@example.com', 'secret456'),
('alice_brown', 'alice@example.com', 'pass789'),
('charlie_davis', 'charlie@example.com', 'qwerty123'),
('diana_miller', 'diana@example.com', 'letmein'),
('edward_jones', 'edward@example.com', 'password1'),
('fiona_garcia', 'fiona@example.com', 'welcome123'),
('george_martinez', 'george@example.com', 'abc123');

-- Crear tabla adicional con información sensible
CREATE TABLE IF NOT EXISTS sensitive_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    credit_card VARCHAR(16),
    ssn VARCHAR(11),
    secret_key VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insertar datos sensibles de ejemplo
INSERT INTO sensitive_data (user_id, credit_card, ssn, secret_key) VALUES
(1, '4532123456789012', '123-45-6789', 'ADMIN_SECRET_KEY_2024'),
(2, '5425123456789012', '234-56-7890', 'USER_SECRET_KEY_ABC'),
(3, '4916123456789012', '345-67-8901', 'PRIVATE_KEY_XYZ123'),
(4, '6011123456789012', '456-78-9012', 'CONFIDENTIAL_DATA_456'),
(5, '3782123456789012', '567-89-0123', 'SECRET_TOKEN_789');

-- Mostrar información de las tablas creadas
SELECT 'Database initialized successfully!' as status;
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as total_sensitive_records FROM sensitive_data;
