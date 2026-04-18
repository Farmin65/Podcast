from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class AuthorService:
    
    def create_author(self, nickname: str, email: str, description: str = None):
        existing = db.execute_query(
            "SELECT ID_Author FROM Authors WHERE Email = %s OR Nickname = %s",
            (email, nickname), fetch_one=True
        )
        if existing:
            raise ValidationError("Email or nickname already exists")
        
        result = db.execute_query(
            """
            INSERT INTO Authors (Nickname, Email, Description, Rating)
            VALUES (%s, %s, %s, 0)
            RETURNING ID_Author
            """,
            (nickname, email, description),
            fetch_one=True
        )
        return result['id_author']
    
    def get_author(self, author_id: int):
        result = db.execute_query(
            "SELECT * FROM Authors WHERE ID_Author = %s",
            (author_id,), fetch_one=True
        )
        if not result:
            raise NotFoundError(f"Author {author_id} not found")
        return result
    
    def get_all_authors(self):
        return db.execute_query(
            "SELECT * FROM Authors ORDER BY Rating DESC",
            fetch_all=True
        )
    
    def update_rating(self, author_id: int, rating: int):
        if rating < 0 or rating > 5:
            raise ValidationError("Rating must be between 0 and 5")
        
        rows = db.execute_query(
            "UPDATE Authors SET Rating = %s WHERE ID_Author = %s",
            (rating, author_id)
        )
        if rows == 0:
            raise NotFoundError(f"Author {author_id} not found")
        return True
    
    def get_author_podcasts(self, author_id: int):
        return db.execute_query(
            """
            SELECT p.*, COUNT(e.ID_Episode) as episode_count
            FROM Podcasts p
            LEFT JOIN Episodes e ON p.ID_Podcast = e.ID_Podcast
            WHERE p.ID_Author = %s
            GROUP BY p.ID_Podcast
            ORDER BY p.Title
            """,
            (author_id,), fetch_all=True
        )
    
    def get_author_subscribers(self, author_id: int):
        return db.execute_query(
            """
            SELECT l.ID_Listener, l.Name, l.Email, s.Type, s.Start_Date
            FROM Subscriptions s
            JOIN Listeners l ON s.ID_Listener = l.ID_Listener
            WHERE s.ID_Author = %s
            ORDER BY s.Start_Date DESC
            """,
            (author_id,), fetch_all=True
        )
    
    def get_authors_paginated(self, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        data = db.execute_query(
            """
            SELECT * FROM Authors 
            ORDER BY Rating DESC, Nickname 
            LIMIT %s OFFSET %s
            """,
            (size, offset),
            fetch_all=True
        )
        total = db.execute_query(
            "SELECT COUNT(*) as count FROM Authors",
            fetch_one=True
        )
        return {
            "page": page,
            "size": size,
            "total": total['count'],
            "items": data
        }