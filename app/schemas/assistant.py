from typing import Optional

from pydantic import BaseModel, Field


class AssistantContext(BaseModel):
    preferred_genres: list[str] = Field(default_factory=list)
    excluded_ratings: list[str] = Field(default_factory=list)
    recent_watch_history: list[str] = Field(default_factory=list)


class AssistantRequest(BaseModel):
    user_id: str
    query: str
    context: Optional[AssistantContext] = None


class Recommendation(BaseModel):
    id: str
    title: str
    reason: str


class AssistantResponse(BaseModel):
    results: list[Recommendation]
    cache_hit: bool = False
