from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Listener:
    id_listener: Optional[int]
    name: str
    email: str
    reg_date: date
    sub_status: str

@dataclass
class Author:
    id_author: Optional[int]
    nickname: str
    email: str
    description: Optional[str]
    rating: Optional[int]

@dataclass
class Podcast:
    id_podcast: Optional[int]
    title: str
    description: Optional[str]
    id_author: int

@dataclass
class Episode:
    id_episode: Optional[int]
    title: str
    duration: Optional[int]
    release_date: date
    audio_url: Optional[str]
    id_podcast: int

@dataclass
class Subscription:
    id_subscription: Optional[int]
    id_listener: int
    id_author: int
    type: str
    start_date: date
    end_date: Optional[date]

@dataclass
class Comment:
    id_comment: Optional[int]
    text: str
    date: date
    id_listener: int
    id_episode: int

@dataclass
class Payment:
    id_payment: Optional[int]
    amount: float
    date: date
    method: str
    id_subscription: int

@dataclass
class Listening:
    id_listening: Optional[int]
    id_listener: int
    id_episode: int
    listen_date: date
    duration_listened: int