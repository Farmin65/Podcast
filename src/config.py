import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_NAME = os.getenv('DB_NAME', 'podcast_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    API_PORT = int(os.getenv('API_PORT', 8000))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

    @property
    def db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()