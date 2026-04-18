INSERT INTO Listeners (Name, Email, Reg_Date, Sub_Status) VALUES
('Иван Петров', 'ivan@mail.ru', '2024-01-15', 'Премиум'),
('Мария Иванова', 'maria@mail.ru', '2024-02-01', 'Бесплатно'),
('Алексей Смирнов', 'alex@mail.ru', '2024-01-20', 'Премиум'),
('Елена Козлова', 'elena@mail.ru', '2024-03-10', 'Бесплатно'),
('Дмитрий Волков', 'dmitry@mail.ru', '2024-02-15', 'Премиум');

INSERT INTO Authors (Nickname, Email, Description, Rating) VALUES
('TechGuru', 'tech@podcast.ru', 'Технологии и программирование', 5),
('MusicMaster', 'music@podcast.ru', 'Все о музыке и исполнителях', 4),
('BizInsider', 'biz@podcast.ru', 'Бизнес и стартапы', 5),
('ScienceDaily', 'science@podcast.ru', 'Научные открытия каждый день', 4),
('HistoryBuff', 'history@podcast.ru', 'Увлекательные исторические факты', 4);

INSERT INTO Podcasts (Title, Description, ID_Author) VALUES
('Python для начинающих', 'Изучаем Python с нуля', 1),
('JavaScript Pro', 'Продвинутое программирование на JS', 1),
('История рока', 'От Beatles до современности', 2),
('Стартап за 30 дней', 'Практическое руководство', 3),
('Квантовая физика', 'Сложное простым языком', 4);

INSERT INTO Episodes (Title, Duration, Release_Date, Audio_URL, ID_Podcast) VALUES
('Введение в Python', 45, '2024-03-01', 'https://cdn.podcast.ru/ep1.mp3', 1),
('Переменные и типы данных', 50, '2024-03-08', 'https://cdn.podcast.ru/ep2.mp3', 1),
('Основы JavaScript', 55, '2024-03-05', 'https://cdn.podcast.ru/ep3.mp3', 2),
('Beatles: Начало', 60, '2024-03-10', 'https://cdn.podcast.ru/ep4.mp3', 3),
('Идея для стартапа', 40, '2024-03-12', 'https://cdn.podcast.ru/ep5.mp3', 4);

INSERT INTO Subscriptions (ID_Listener, ID_Author, Type, Start_Date, End_Date) VALUES
(1, 1, 'Премиум', '2024-01-15', '2025-01-15'),
(1, 2, 'Бесплатно', '2024-02-01', NULL),
(3, 1, 'Премиум', '2024-01-20', '2025-01-20'),
(3, 3, 'Премиум', '2024-02-01', '2025-02-01'),
(5, 4, 'Премиум', '2024-02-15', '2025-02-15');

INSERT INTO Payments (Amount, Date, Method, ID_Subscription) VALUES
(2990.00, '2024-01-15', 'Карта', 1),
(4990.00, '2024-01-20', 'СБП', 3),
(3990.00, '2024-02-01', 'Карта', 4),
(3490.00, '2024-02-15', 'Карта', 5);

INSERT INTO Listening (ID_Listener, ID_Episode, Listen_Date, Duration_Listened) VALUES
(1, 1, '2024-03-01', 45),
(1, 2, '2024-03-08', 50),
(3, 1, '2024-03-02', 30),
(3, 3, '2024-03-06', 55),
(5, 5, '2024-03-12', 40);

INSERT INTO Comments (Text, Date, ID_Listener, ID_Episode) VALUES
('Отличный выпуск!', '2024-03-02', 1, 1),
('Очень познавательно', '2024-03-09', 1, 2),
('Жду продолжения', '2024-03-03', 3, 1),
('Лучший подкаст о JS', '2024-03-07', 3, 3),
('Спасибо за выпуск', '2024-03-13', 5, 5);