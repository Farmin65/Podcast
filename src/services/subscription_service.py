from datetime import date, timedelta
from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class SubscriptionService:
    
    def create_subscription(self, id_listener: int, id_author: int, 
                           subscription_type: str = 'Бесплатно'):
        if subscription_type not in ('Бесплатно', 'Премиум'):
            raise ValidationError("Invalid subscription type")
        
        existing = db.execute_query(
            """
            SELECT ID_Subscription FROM Subscriptions 
            WHERE ID_Listener = %s AND ID_Author = %s
            """,
            (id_listener, id_author), fetch_one=True
        )
        if existing:
            raise ValidationError("Subscription already exists")
        
        end_date = None
        if subscription_type == 'Премиум':
            end_date = date.today() + timedelta(days=365)
        
        result = db.execute_query(
            """
            INSERT INTO Subscriptions (ID_Listener, ID_Author, Type, Start_Date, End_Date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ID_Subscription
            """,
            (id_listener, id_author, subscription_type, date.today(), end_date),
            fetch_one=True
        )
        return result['id_subscription']
    
    def get_subscription(self, subscription_id: int):
        result = db.execute_query(
            """
            SELECT s.*, l.Name as listener_name, a.Nickname as author_nickname
            FROM Subscriptions s
            JOIN Listeners l ON s.ID_Listener = l.ID_Listener
            JOIN Authors a ON s.ID_Author = a.ID_Author
            WHERE s.ID_Subscription = %s
            """,
            (subscription_id,), fetch_one=True
        )
        if not result:
            raise NotFoundError(f"Subscription {subscription_id} not found")
        return result
    
    def cancel_subscription(self, subscription_id: int):
        rows = db.execute_query(
            "DELETE FROM Subscriptions WHERE ID_Subscription = %s",
            (subscription_id,)
        )
        if rows == 0:
            raise NotFoundError(f"Subscription {subscription_id} not found")
        return True
    
    def check_active_subscription(self, id_listener: int, id_author: int):
        result = db.execute_query(
            """
            SELECT * FROM Subscriptions 
            WHERE ID_Listener = %s AND ID_Author = %s
            AND (End_Date IS NULL OR End_Date >= CURRENT_DATE)
            """,
            (id_listener, id_author), fetch_one=True
        )

        def get_all_subscriptions(self):
            return db.execute_query(
                """
                SELECT s.*, l.Name as listener_name, a.Nickname as author_nickname
                FROM Subscriptions s
                JOIN Listeners l ON s.ID_Listener = l.ID_Listener
                JOIN Authors a ON s.ID_Author = a.ID_Author
                ORDER BY s.Start_Date DESC
                """,
                fetch_all=True
            )
        return result is not None