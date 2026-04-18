from datetime import date
from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class ListenerService:
    
    def create_listener(self, name: str, email: str, sub_status: str = 'Бесплатно'):
        existing = db.execute_query(
            "SELECT ID_Listener FROM Listeners WHERE Email = %s",
            (email,), fetch_one=True
        )
        if existing:
            raise ValidationError("Email already exists")
        
        result = db.execute_query(
            """
            INSERT INTO Listeners (Name, Email, Reg_Date, Sub_Status)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Listener
            """,
            (name, email, date.today(), sub_status),
            fetch_one=True
        )
        return result['id_listener']
    
    def get_listener(self, listener_id: int):
        result = db.execute_query(
            "SELECT * FROM Listeners WHERE ID_Listener = %s",
            (listener_id,), fetch_one=True
        )
        if not result:
            raise NotFoundError(f"Listener {listener_id} not found")
        return result
    
    def get_all_listeners(self):
        return db.execute_query(
            "SELECT * FROM Listeners ORDER BY Reg_Date DESC",
            fetch_all=True
        )
    
    def update_subscription_status(self, listener_id: int, new_status: str):
        if new_status not in ('Бесплатно', 'Премиум'):
            raise ValidationError("Invalid subscription status")
        
        rows = db.execute_query(
            "UPDATE Listeners SET Sub_Status = %s WHERE ID_Listener = %s",
            (new_status, listener_id)
        )
        if rows == 0:
            raise NotFoundError(f"Listener {listener_id} not found")
        return True
    
    def get_listener_subscriptions(self, listener_id: int):
        return db.execute_query(
            """
            SELECT a.Nickname, a.Email, s.Type, s.Start_Date, s.End_Date
            FROM Subscriptions s
            JOIN Authors a ON s.ID_Author = a.ID_Author
            WHERE s.ID_Listener = %s
            ORDER BY s.Start_Date DESC
            """,
            (listener_id,), fetch_all=True
        )
    
    def get_listening_history(self, listener_id: int, limit: int = 50):
        return db.execute_query(
            """
            SELECT e.Title, p.Title as Podcast, l.Listen_Date, l.Duration_Listened
            FROM Listening l
            JOIN Episodes e ON l.ID_Episode = e.ID_Episode
            JOIN Podcasts p ON e.ID_Podcast = p.ID_Podcast
            WHERE l.ID_Listener = %s
            ORDER BY l.Listen_Date DESC
            LIMIT %s
            """,
            (listener_id, limit), fetch_all=True
        )
    
    def delete_listener(self, listener_id: int):
        rows = db.execute_query(
            "DELETE FROM Listeners WHERE ID_Listener = %s",
            (listener_id,)
        )
        if rows == 0:
            raise NotFoundError(f"Listener {listener_id} not found")
        return True
    
    def get_listeners_paginated(self, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        data = db.execute_query(
            """
            SELECT * FROM Listeners 
            ORDER BY Reg_Date DESC 
            LIMIT %s OFFSET %s
            """,
            (size, offset),
            fetch_all=True
        )
        total = db.execute_query(
            "SELECT COUNT(*) as count FROM Listeners",
            fetch_one=True
        )
        return {
            "page": page,
            "size": size,
            "total": total['count'],
            "items": data
        }