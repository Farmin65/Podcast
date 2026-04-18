from datetime import date
from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class EpisodeService:
    
    def create_episode(self, title: str, id_podcast: int, duration: int = None, 
                       audio_url: str = None, release_date: date = None):
        podcast = db.execute_query(
            "SELECT ID_Podcast FROM Podcasts WHERE ID_Podcast = %s",
            (id_podcast,), fetch_one=True
        )
        if not podcast:
            raise ValidationError("Podcast does not exist")
        
        if release_date is None:
            release_date = date.today()
        
        result = db.execute_query(
            """
            INSERT INTO Episodes (Title, Duration, Release_Date, Audio_URL, ID_Podcast)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ID_Episode
            """,
            (title, duration, release_date, audio_url, id_podcast),
            fetch_one=True
        )
        return result['id_episode']
    
    def get_episode(self, episode_id: int):
        result = db.execute_query(
            """
            SELECT e.*, p.Title as podcast_title, a.Nickname as author
            FROM Episodes e
            JOIN Podcasts p ON e.ID_Podcast = p.ID_Podcast
            JOIN Authors a ON p.ID_Author = a.ID_Author
            WHERE e.ID_Episode = %s
            """,
            (episode_id,), fetch_one=True
        )
        if not result:
            raise NotFoundError(f"Episode {episode_id} not found")
        return result
    
    def record_listening(self, id_listener: int, id_episode: int, duration_listened: int):
        listener = db.execute_query(
            "SELECT ID_Listener FROM Listeners WHERE ID_Listener = %s",
            (id_listener,), fetch_one=True
        )
        episode = db.execute_query(
            "SELECT ID_Episode FROM Episodes WHERE ID_Episode = %s",
            (id_episode,), fetch_one=True
        )
        
        if not listener or not episode:
            raise ValidationError("Invalid listener or episode")
        
        result = db.execute_query(
            """
            INSERT INTO Listening (ID_Listener, ID_Episode, Listen_Date, Duration_Listened)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Listening
            """,
            (id_listener, id_episode, date.today(), duration_listened),
            fetch_one=True
        )
        return result['id_listening']
    
    def get_episode_comments(self, episode_id: int):
        return db.execute_query(
            """
            SELECT c.*, l.Name as listener_name
            FROM Comments c
            JOIN Listeners l ON c.ID_Listener = l.ID_Listener
            WHERE c.ID_Episode = %s
            ORDER BY c.Date DESC
            """,
            (episode_id,), fetch_all=True
        )
    
    def add_comment(self, id_listener: int, id_episode: int, text: str):
        if not text or not text.strip():
            raise ValidationError("Comment text cannot be empty")
        
        result = db.execute_query(
            """
            INSERT INTO Comments (Text, Date, ID_Listener, ID_Episode)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Comment
            """,
            (text, date.today(), id_listener, id_episode),
            fetch_one=True
        )

        return result['id_comment']

    def get_all_episodes(self):
        return db.execute_query(
            """
            SELECT e.*, p.Title as podcast_title
            FROM Episodes e
            JOIN Podcasts p ON e.ID_Podcast = p.ID_Podcast
            ORDER BY e.Release_Date DESC
            """,
            fetch_all=True
        )
