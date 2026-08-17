from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.audience import Audience
from app.models.growth import Growth

from app.schemas.audience import AudienceCreate, AudienceUpdate
from app.schemas.growth import GrowthCreate, GrowthUpdate

from app.services.audience_service import (
    get_audience_report,
    get_growth_report,
    get_audience_trends,
)


router = APIRouter(
    tags=["Audience"]
)


# ============================================================
# AUDIENCE CRUD
# ============================================================

@router.post("/audience")
def create_audience(
    audience_data: AudienceCreate,
    db: Session = Depends(get_db)
):
    audience = Audience(
        **audience_data.model_dump()
    )

    db.add(audience)
    db.commit()
    db.refresh(audience)

    return {
        "message": "Audience record created successfully",
        "data": audience
    }


@router.get("/audience")
def get_all_audience(
    db: Session = Depends(get_db)
):
    audience = db.query(Audience).all()

    return {
        "total": len(audience),
        "data": audience
    }


@router.get("/audience/{id}")
def get_audience_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    audience = (
        db.query(Audience)
        .filter(Audience.id == id)
        .first()
    )

    if not audience:
        raise HTTPException(
            status_code=404,
            detail="Audience record not found"
        )

    return {
        "data": audience
    }


@router.put("/audience/{id}")
def update_audience(
    id: int,
    audience_data: AudienceUpdate,
    db: Session = Depends(get_db)
):
    audience = (
        db.query(Audience)
        .filter(Audience.id == id)
        .first()
    )

    if not audience:
        raise HTTPException(
            status_code=404,
            detail="Audience record not found"
        )

    update_data = audience_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(audience, key, value)

    db.commit()
    db.refresh(audience)

    return {
        "message": "Audience record updated successfully",
        "data": audience
    }


@router.delete("/audience/{id}")
def delete_audience(
    id: int,
    db: Session = Depends(get_db)
):
    audience = (
        db.query(Audience)
        .filter(Audience.id == id)
        .first()
    )

    if not audience:
        raise HTTPException(
            status_code=404,
            detail="Audience record not found"
        )

    db.delete(audience)
    db.commit()

    return {
        "message": "Audience record deleted successfully"
    }


# ============================================================
# GROWTH CRUD
# ============================================================

@router.post("/growth")
def create_growth(
    growth_data: GrowthCreate,
    db: Session = Depends(get_db)
):
    growth = Growth(
        **growth_data.model_dump()
    )

    db.add(growth)
    db.commit()
    db.refresh(growth)

    return {
        "message": "Growth record created successfully",
        "data": growth
    }


@router.get("/growth")
def get_all_growth(
    db: Session = Depends(get_db)
):
    growth = (
        db.query(Growth)
        .order_by(Growth.date.asc())
        .all()
    )

    return {
        "total": len(growth),
        "data": growth
    }


# ============================================================
# ANALYTICS
# ============================================================

@router.get("/analytics/audience")
def audience_analytics(
    db: Session = Depends(get_db)
):
    return get_audience_report(db)


@router.get("/analytics/growth")
def growth_analytics(
    db: Session = Depends(get_db)
):
    return get_growth_report(db)


@router.get("/analytics/audience-trends")
def audience_trends(
    db: Session = Depends(get_db)
):
    return get_audience_trends(db)