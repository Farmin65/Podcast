from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class PodcastService:
    
    def create_podcast(self, title: str, id_author: int, description: str = None):
        author = db.execute_query(
            "SELECT ID_Author FROM Authors WHERE ID_Author = %s",
            (id_author,), fetch_one=True
        )
        if not author:
            raise ValidationError("Author does not exist")
        
        result = db.execute_query(
            """
            INSERT INTO Podcasts (Title, Description, ID_Author)
            VALUES (%s, %s, %s)
            RETURNING ID_Podcast
            """,
            (title, description, id_author),
            fetch_one=True
        )
        return result['id_podcast']
    
    def get_podcast(self, podcast_id: int):
        result = db.execute_query(
            """
            SELECT p.*, a.Nickname as author_nickname, a.Rating as author_rating
            FROM Podcasts p
            JOIN Authors a ON p.ID_Author = a.ID_Author
            WHERE p.ID_Podcast = %s
            """,
            (podcast_id,), fetch_one=True
        )
        if not result:
            raise NotFoundError(f"Podcast {podcast_id} not found")
        return result
    
    def get_all_podcasts(self):
        return db.execute_query(
            """
            SELECT p.*, a.Nickname as author_nickname
            FROM Podcasts p
            JOIN Authors a ON p.ID_Author = a.ID_Author
            ORDER BY p.Title
            """,
            fetch_all=True
        )
    
    def get_podcast_episodes(self, podcast_id: int):
        return db.execute_query(
            """
            SELECT * FROM Episodes
            WHERE ID_Podcast = %s
            ORDER BY Release_Date DESC
            """,
            (podcast_id,), fetch_all=True
        )
    
    def search_podcasts(self, query: str):
        return db.execute_query(
            """
            SELECT p.*, a.Nickname as author_nickname
            FROM Podcasts p
            JOIN Authors a ON p.ID_Author = a.ID_Author
            WHERE p.Title ILIKE %s OR p.Description ILIKE %s
            """,
            (f'%{query}%', f'%{query}%'), fetch_all=True
        )
    
    def delete_podcast(self, podcast_id: int):
        rows = db.execute_query(
            "DELETE FROM Podcasts WHERE ID_Podcast = %s",
            (podcast_id,)
        )
        if rows == 0:
            raise NotFoundError(f"Podcast {podcast_id} not found")
        return True

    def get_podcasts_paginated(self, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        data = db.execute_query(
            """
            SELECT p.*, a.Nickname as author_nickname
            FROM Podcasts p
            JOIN Authors a ON p.ID_Author = a.ID_Author
            ORDER BY p.Title
            LIMIT %s OFFSET %s
            """,
            (size, offset),
            fetch_all=True
        )
        total = db.execute_query(
            "SELECT COUNT(*) as count FROM Podcasts",
            fetch_one=True
        )
        return {
            "page": page,
            "size": size,
            "total": total['count'],
            "items": data
        }