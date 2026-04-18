CREATE VIEW podcast_stats AS
SELECT 
    p.ID_Podcast,
    p.Title,
    a.Nickname AS author,
    COUNT(DISTINCT e.ID_Episode) AS total_episodes,
    COALESCE(SUM(e.Duration), 0) AS total_duration,
    COUNT(DISTINCT l.ID_Listening) AS total_listens,
    COUNT(DISTINCT s.ID_Listener) AS subscribers_count
FROM Podcasts p
JOIN Authors a ON p.ID_Author = a.ID_Author
LEFT JOIN Episodes e ON p.ID_Podcast = e.ID_Podcast
LEFT JOIN Listening l ON e.ID_Episode = l.ID_Episode
LEFT JOIN Subscriptions s ON a.ID_Author = s.ID_Author
GROUP BY p.ID_Podcast, p.Title, a.Nickname;

CREATE VIEW author_analytics AS
SELECT 
    a.ID_Author,
    a.Nickname,
    a.Rating,
    COUNT(DISTINCT p.ID_Podcast) AS podcasts_count,
    COUNT(DISTINCT e.ID_Episode) AS episodes_count,
    COUNT(DISTINCT s.ID_Listener) AS subscribers,
    COALESCE(SUM(pay.Amount), 0) AS total_revenue
FROM Authors a
LEFT JOIN Podcasts p ON a.ID_Author = p.ID_Author
LEFT JOIN Episodes e ON p.ID_Podcast = e.ID_Podcast
LEFT JOIN Subscriptions s ON a.ID_Author = s.ID_Author
LEFT JOIN Payments pay ON s.ID_Subscription = pay.ID_Subscription
GROUP BY a.ID_Author, a.Nickname, a.Rating;

CREATE VIEW listener_activity AS
SELECT 
    l.ID_Listener,
    l.Name,
    l.Email,
    l.Sub_Status,
    COUNT(DISTINCT s.ID_Author) AS subscriptions_count,
    COUNT(DISTINCT lis.ID_Episode) AS listened_episodes,
    COALESCE(SUM(lis.Duration_Listened), 0) AS total_time_listened
FROM Listeners l
LEFT JOIN Subscriptions s ON l.ID_Listener = s.ID_Listener
LEFT JOIN Listening lis ON l.ID_Listener = lis.ID_Listener
GROUP BY l.ID_Listener, l.Name, l.Email, l.Sub_Status;