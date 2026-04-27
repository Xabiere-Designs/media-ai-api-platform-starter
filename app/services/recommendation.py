import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.media import MediaItem
from app.schemas.assistant import AssistantRequest, AssistantResponse, Recommendation
from app.services.cache import CacheService


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = CacheService()

    def _cache_key(self, payload: AssistantRequest, username: str) -> str:
        raw = f"{username}:{payload.model_dump_json()}"
        return "recommend:" + hashlib.sha256(raw.encode()).hexdigest()

    def recommend(self, payload: AssistantRequest, username: str) -> AssistantResponse:
        cache_key = self._cache_key(payload, username)
        cached = self.cache.get_json(cache_key)
        if cached:
            return AssistantResponse(**cached, cache_hit=True)

        query_text = payload.query.lower()
        preferred = set((payload.context.preferred_genres if payload.context else []) or [])
        excluded = set((payload.context.excluded_ratings if payload.context else []) or [])

        items = self.db.scalars(select(MediaItem)).all()
        ranked: list[tuple[int, MediaItem]] = []

        for item in items:
            score = 0
            genres = set(g.strip().lower() for g in item.genres.split(",") if g.strip())
            if any(token in item.description.lower() for token in query_text.split()):
                score += 3
            if any(token in item.title.lower() for token in query_text.split()):
                score += 2
            if preferred and genres.intersection({g.lower() for g in preferred}):
                score += 4
            if "ai" in query_text and "ai" in item.description.lower():
                score += 2
            if "thriller" in query_text and "thriller" in genres:
                score += 2
            if item.maturity_rating in excluded:
                score -= 10
            ranked.append((score, item))

        ranked.sort(key=lambda pair: (pair[0], pair[1].release_year), reverse=True)
        results = [
            Recommendation(
                id=item.external_id,
                title=item.title,
                reason=f"Matched on theme, genre, and metadata with a score of {score}.",
            )
            for score, item in ranked[:3]
            if score > 0
        ] or [
            Recommendation(
                id=item.external_id,
                title=item.title,
                reason="Fallback recommendation from the seeded catalog.",
            )
            for _, item in ranked[:3]
        ]

        response = AssistantResponse(results=results, cache_hit=False)
        self.cache.set_json(cache_key, response.model_dump(), settings.cache_ttl_seconds)
        return response
