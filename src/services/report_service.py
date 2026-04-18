import pandas as pd
from datetime import datetime
from ..database.connection import db

class ReportService:
    
    def generate_listeners_report(self):
        data = db.execute_query(
            """
            SELECT Name, Email, Reg_Date, Sub_Status 
            FROM Listeners 
            ORDER BY Reg_Date DESC
            """,
            fetch_all=True
        )
        df = pd.DataFrame(data)
        filename = f"reports/listeners_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        return filename
    
    def generate_revenue_report(self, start_date: str, end_date: str):
        data = db.execute_query(
            """
            SELECT 
                Date,
                Method,
                Amount,
                l.Name as listener_name,
                a.Nickname as author_nickname
            FROM Payments p
            JOIN Subscriptions s ON p.ID_Subscription = s.ID_Subscription
            JOIN Listeners l ON s.ID_Listener = l.ID_Listener
            JOIN Authors a ON s.ID_Author = a.ID_Author
            WHERE Date BETWEEN %s AND %s
            ORDER BY Date DESC
            """,
            (start_date, end_date), fetch_all=True
        )
        df = pd.DataFrame(data)
        filename = f"reports/revenue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        return filename
    
    def generate_analytics_summary(self):
        os.makedirs("reports", exist_ok=True)
        
        popular = self.get_popular_podcasts_dataframe()
        authors = self.get_authors_dataframe()
        
        filename = f"reports/analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with pd.ExcelWriter(filename) as writer:
            popular.to_excel(writer, sheet_name='Popular Podcasts', index=False)
            authors.to_excel(writer, sheet_name='Top Authors', index=False)
        
        return filename
    
    def get_popular_podcasts_dataframe(self):
        data = db.execute_query(
            """
            SELECT * FROM podcast_stats 
            ORDER BY total_listens DESC 
            LIMIT 50
            """,
            fetch_all=True
        )
        return pd.DataFrame(data)
    
    def get_authors_dataframe(self):
        data = db.execute_query(
            """
            SELECT * FROM author_analytics 
            ORDER BY subscribers DESC
            """,
            fetch_all=True
        )
        return pd.DataFrame(data)