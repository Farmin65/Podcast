CREATE TABLE Listeners (
    ID_Listener SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Reg_Date DATE NOT NULL,
    Sub_Status VARCHAR(10) NOT NULL CHECK (Sub_Status IN ('Бесплатно', 'Премиум'))
);

CREATE TABLE Authors (
    ID_Author SERIAL PRIMARY KEY,
    Nickname VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Description TEXT,
    Rating INT CHECK (Rating BETWEEN 0 AND 5)
);

CREATE TABLE Podcasts (
    ID_Podcast SERIAL PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    Description TEXT,
    ID_Author INT REFERENCES Authors(ID_Author) ON DELETE CASCADE
);

CREATE TABLE Episodes (
    ID_Episode SERIAL PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    Duration INT CHECK (Duration > 0),
    Release_Date DATE,
    Audio_URL TEXT,
    ID_Podcast INT REFERENCES Podcasts(ID_Podcast) ON DELETE CASCADE
);

CREATE TABLE Subscriptions (
    ID_Subscription SERIAL PRIMARY KEY,
    ID_Listener INT REFERENCES Listeners(ID_Listener) ON DELETE CASCADE,
    ID_Author INT REFERENCES Authors(ID_Author) ON DELETE CASCADE,
    Type VARCHAR(20) NOT NULL CHECK (Type IN ('Бесплатно', 'Премиум')),
    Start_Date DATE,
    End_Date DATE
);

CREATE TABLE Comments (
    ID_Comment SERIAL PRIMARY KEY,
    Text TEXT NOT NULL,
    Date DATE,
    ID_Listener INT REFERENCES Listeners(ID_Listener) ON DELETE CASCADE,
    ID_Episode INT REFERENCES Episodes(ID_Episode) ON DELETE CASCADE
);

CREATE TABLE Payments (
    ID_Payment SERIAL PRIMARY KEY,
    Amount DECIMAL(10,2) CHECK (Amount > 0),
    Date DATE,
    Method VARCHAR(20) NOT NULL CHECK (Method IN ('СБП', 'Карта')),
    ID_Subscription INT REFERENCES Subscriptions(ID_Subscription) ON DELETE CASCADE
);

CREATE TABLE Listening (
    ID_Listening SERIAL PRIMARY KEY,
    ID_Listener INT REFERENCES Listeners(ID_Listener) ON DELETE CASCADE,
    ID_Episode INT REFERENCES Episodes(ID_Episode) ON DELETE CASCADE,
    Listen_Date DATE,
    Duration_Listened INT CHECK (Duration_Listened >= 0)
);