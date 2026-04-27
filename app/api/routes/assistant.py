from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.assistant import AssistantRequest, AssistantResponse
from app.services.recommendation import RecommendationService

router = APIRouter()


@router.post("/assistant/query", response_model=AssistantResponse)
def assistant_query(
    payload: AssistantRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RecommendationService(db=db)
    return service.recommend(payload=payload, username=current_user.username)
