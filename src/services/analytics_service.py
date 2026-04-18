from ..database.connection import db

class AnalyticsService:
    
    def get_popular_podcasts(self, limit: int = 10):
        return db.execute_query(
            """
            SELECT p.Title, a.Nickname, COUNT(l.ID_Listening) as listen_count
            FROM Podcasts p
            JOIN Authors a ON p.ID_Author = a.ID_Author
            JOIN Episodes e ON p.ID_Podcast = e.ID_Podcast
            LEFT JOIN Listening l ON e.ID_Episode = l.ID_Episode
            GROUP BY p.ID_Podcast, p.Title, a.Nickname
            ORDER BY listen_count DESC
            LIMIT %s
            """,
            (limit,), fetch_all=True
        )
    
    def get_top_authors(self, limit: int = 10):
        return db.execute_query(
            """
            SELECT a.Nickname, a.Rating, COUNT(s.ID_Listener) as subscribers
            FROM Authors a
            LEFT JOIN Subscriptions s ON a.ID_Author = s.ID_Author
            GROUP BY a.ID_Author, a.Nickname, a.Rating
            ORDER BY subscribers DESC
            LIMIT %s
            """,
            (limit,), fetch_all=True
        )
    
    def get_total_revenue(self):
        return db.execute_query(
            """
            SELECT COALESCE(SUM(Amount), 0) as total
            FROM Payments
            """,
            fetch_one=True
        )
    
    def get_revenue_by_method(self):
        return db.execute_query(
            """
            SELECT Method, COUNT(*) as count, SUM(Amount) as total
            FROM Payments
            GROUP BY Method
            """,
            fetch_all=True
        )
    
    def get_daily_stats(self):
        return db.execute_query(
            """
            SELECT 
                DATE(Listen_Date) as day,
                COUNT(*) as listens,
                COUNT(DISTINCT ID_Listener) as unique_listeners
            FROM Listening
            GROUP BY DATE(Listen_Date)
            ORDER BY day DESC
            LIMIT 30
            """,
            fetch_all=True
        )
    
    def get_listener_stats(self, listener_id: int):
        return db.execute_query(
            """
            SELECT * FROM listener_activity 
            WHERE ID_Listener = %s
            """,
            (listener_id,), fetch_one=True
        )
    
    def get_author_analytics(self, author_id: int):
        return db.execute_query(
            """
            SELECT * FROM author_analytics 
            WHERE ID_Author = %s
            """,
            (author_id,), fetch_one=True
        )