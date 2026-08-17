from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.analytics_service import (
    calculate_engagement_rate,
    get_top_content,
    get_platform_performance,
    get_dashboard_summary,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/content/{content_id}/engagement")
def content_engagement(
    content_id: int,
    db: Session = Depends(get_db)
):
    result = calculate_engagement_rate(db, content_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )

    return result


@router.get("/top-content")
def top_content(
    db: Session = Depends(get_db)
):
    return get_top_content(db)


@router.get("/platform-performance")
def platform_performance(
    db: Session = Depends(get_db)
):
    return get_platform_performance(db)


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    return get_dashboard_summary(db)