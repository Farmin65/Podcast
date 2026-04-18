CREATE TABLE Users (
    ID_User SERIAL PRIMARY KEY,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password_Hash VARCHAR(255) NOT NULL,
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('admin', 'listener', 'author')),
    ID_Listener INT REFERENCES Listeners(ID_Listener) ON DELETE SET NULL,
    ID_Author INT REFERENCES Authors(ID_Author) ON DELETE SET NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Users (Email, Password_Hash, Role, ID_Listener)
SELECT
    Email,
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeO3oP5hq',
    'listener',
    ID_Listener
FROM Listeners
WHERE Email IN ('ivan@mail.ru', 'alex@mail.ru', 'dmitry@mail.ru');

INSERT INTO Users (Email, Password_Hash, Role, ID_Author)
SELECT
    Email,
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeO3oP5hq',
    'author',
    ID_Author
FROM Authors;