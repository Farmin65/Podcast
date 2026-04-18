from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from ..services.listener_service import ListenerService
from ..services.author_service import AuthorService
from ..services.podcast_service import PodcastService
from ..services.episode_service import EpisodeService
from ..services.subscription_service import SubscriptionService
from ..services.payment_service import PaymentService
from ..services.analytics_service import AnalyticsService
from ..auth import get_current_user, get_current_admin

router = APIRouter()

listener_service = ListenerService()
author_service = AuthorService()
podcast_service = PodcastService()
episode_service = EpisodeService()
subscription_service = SubscriptionService()
payment_service = PaymentService()
analytics_service = AnalyticsService()

class ListenerCreate(BaseModel):
    name: str
    email: EmailStr
    sub_status: str = "Бесплатно"

class ListenerUpdate(BaseModel):
    sub_status: str

class AuthorCreate(BaseModel):
    nickname: str
    email: EmailStr
    description: Optional[str] = None

class AuthorRatingUpdate(BaseModel):
    rating: int

class PodcastCreate(BaseModel):
    title: str
    description: Optional[str] = None
    id_author: int

class EpisodeCreate(BaseModel):
    title: str
    duration: Optional[int] = None
    audio_url: Optional[str] = None
    id_podcast: int

class EpisodeListen(BaseModel):
    id_listener: int
    id_episode: int
    duration_listened: int

class CommentCreate(BaseModel):
    id_listener: int
    text: str

class SubscriptionCreate(BaseModel):
    id_listener: int
    id_author: int
    subscription_type: str = "Бесплатно"

class PaymentCreate(BaseModel):
    amount: float
    method: str
    id_subscription: int

@router.get("/")
def root():
    return {
        "name": "Podcast Platform API",
        "version": "1.0.0",
        "endpoints": {
            "listeners": "/listeners",
            "authors": "/authors",
            "podcasts": "/podcasts",
            "episodes": "/episodes",
            "subscriptions": "/subscriptions",
            "payments": "/payments",
            "analytics": "/analytics",
            "docs": "/docs",
            "auth": "/auth/login"
        }
    }

@router.get("/listeners/")
def get_all_listeners(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return listener_service.get_listeners_paginated(page, size)

@router.get("/listeners/{listener_id}")
def get_listener(listener_id: int):
    try:
        return listener_service.get_listener(listener_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/listeners/")
def create_listener(
    listener: ListenerCreate,
    current_user = Depends(get_current_user)
):
    try:
        listener_id = listener_service.create_listener(
            listener.name,
            listener.email,
            listener.sub_status
        )
        return {"id_listener": listener_id, "message": "Слушатель создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/listeners/{listener_id}")
def update_listener_status(
    listener_id: int,
    update: ListenerUpdate,
    current_user = Depends(get_current_user)
):
    try:
        listener_service.update_subscription_status(listener_id, update.sub_status)
        return {"message": "Статус обновлён"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/listeners/{listener_id}/subscriptions")
def get_listener_subscriptions(listener_id: int):
    return listener_service.get_listener_subscriptions(listener_id)

@router.get("/listeners/{listener_id}/history")
def get_listener_history(listener_id: int, limit: int = 50):
    return listener_service.get_listening_history(listener_id, limit)

@router.delete("/listeners/{listener_id}")
def delete_listener(
    listener_id: int,
    current_user = Depends(get_current_admin)
):
    try:
        listener_service.delete_listener(listener_id)
        return {"message": "Слушатель удалён"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/authors/")
def get_all_authors(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return author_service.get_authors_paginated(page, size)

@router.get("/authors/{author_id}")
def get_author(author_id: int):
    try:
        return author_service.get_author(author_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/authors/")
def create_author(
    author: AuthorCreate,
    current_user = Depends(get_current_user)
):
    try:
        author_id = author_service.create_author(
            author.nickname,
            author.email,
            author.description
        )
        return {"id_author": author_id, "message": "Автор создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/authors/{author_id}/rating")
def update_author_rating(
    author_id: int,
    update: AuthorRatingUpdate,
    current_user = Depends(get_current_user)
):
    try:
        author_service.update_rating(author_id, update.rating)
        return {"message": "Рейтинг обновлён"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/authors/{author_id}/podcasts")
def get_author_podcasts(author_id: int):
    return author_service.get_author_podcasts(author_id)

@router.get("/authors/{author_id}/subscribers")
def get_author_subscribers(author_id: int):
    return author_service.get_author_subscribers(author_id)

@router.delete("/authors/{author_id}")
def delete_author(
    author_id: int,
    current_user = Depends(get_current_admin)
):
    try:
        author_service.delete_author(author_id)
        return {"message": "Автор удалён"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/podcasts/")
def get_all_podcasts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return podcast_service.get_podcasts_paginated(page, size)

@router.get("/podcasts/search/")
def search_podcasts(q: str = Query(..., min_length=1)):
    return podcast_service.search_podcasts(q)

@router.get("/podcasts/{podcast_id}")
def get_podcast(podcast_id: int):
    try:
        return podcast_service.get_podcast(podcast_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/podcasts/")
def create_podcast(
    podcast: PodcastCreate,
    current_user = Depends(get_current_user)
):
    try:
        podcast_id = podcast_service.create_podcast(
            podcast.title,
            podcast.id_author,
            podcast.description
        )
        return {"id_podcast": podcast_id, "message": "Подкаст создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/podcasts/{podcast_id}/episodes")
def get_podcast_episodes(podcast_id: int):
    return podcast_service.get_podcast_episodes(podcast_id)

@router.delete("/podcasts/{podcast_id}")
def delete_podcast(
    podcast_id: int,
    current_user = Depends(get_current_admin)
):
    try:
        podcast_service.delete_podcast(podcast_id)
        return {"message": "Подкаст удалён"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/episodes/")
def get_all_episodes():
    return episode_service.get_all_episodes()

@router.get("/episodes/{episode_id}")
def get_episode(episode_id: int):
    try:
        return episode_service.get_episode(episode_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/episodes/")
def create_episode(
    episode: EpisodeCreate,
    current_user = Depends(get_current_user)
):
    try:
        episode_id = episode_service.create_episode(
            episode.title,
            episode.id_podcast,
            episode.duration,
            episode.audio_url
        )
        return {"id_episode": episode_id, "message": "Эпизод создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/episodes/listen/")
def record_listening(listen: EpisodeListen):
    try:
        listen_id = episode_service.record_listening(
            listen.id_listener,
            listen.id_episode,
            listen.duration_listened
        )
        return {"id_listening": listen_id, "message": "Прослушивание записано"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/episodes/{episode_id}/comments")
def get_episode_comments(episode_id: int):
    return episode_service.get_episode_comments(episode_id)

@router.post("/episodes/{episode_id}/comments")
def add_comment(
    episode_id: int,
    comment: CommentCreate,
    current_user = Depends(get_current_user)
):
    try:
        comment_id = episode_service.add_comment(
            comment.id_listener,
            episode_id,
            comment.text
        )
        return {"id_comment": comment_id, "message": "Комментарий добавлен"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscriptions/")
def get_all_subscriptions():
    return subscription_service.get_all_subscriptions()

@router.post("/subscriptions/")
def create_subscription(
    subscription: SubscriptionCreate,
    current_user = Depends(get_current_user)
):
    try:
        sub_id = subscription_service.create_subscription(
            subscription.id_listener,
            subscription.id_author,
            subscription.subscription_type
        )
        return {"id_subscription": sub_id, "message": "Подписка создана"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/subscriptions/{subscription_id}")
def cancel_subscription(
    subscription_id: int,
    current_user = Depends(get_current_user)
):
    try:
        subscription_service.cancel_subscription(subscription_id)
        return {"message": "Подписка отменена"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/payments/")
def get_all_payments(current_user = Depends(get_current_admin)):
    return payment_service.get_all_payments()

@router.post("/payments/")
def create_payment(
    payment: PaymentCreate,
    current_user = Depends(get_current_user)
):
    try:
        payment_id = payment_service.create_payment(
            payment.amount,
            payment.method,
            payment.id_subscription
        )
        return {"id_payment": payment_id, "message": "Платёж создан"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/analytics/popular/")
def get_popular_podcasts(limit: int = 10):
    return analytics_service.get_popular_podcasts(limit)

@router.get("/analytics/top-authors/")
def get_top_authors(limit: int = 10):
    return analytics_service.get_top_authors(limit)

@router.get("/analytics/revenue/")
def get_total_revenue(current_user = Depends(get_current_admin)):
    return analytics_service.get_total_revenue()

@router.get("/analytics/stats/")
def get_platform_stats():
    return analytics_service.get_platform_stats()