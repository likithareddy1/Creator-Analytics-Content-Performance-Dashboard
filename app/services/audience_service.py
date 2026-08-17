from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.audience import Audience
from app.models.growth import Growth


def get_total_followers(db: Session):
    return db.query(func.sum(Audience.followers)).scalar() or 0


def get_total_reach(db: Session):
    return db.query(func.sum(Audience.reach)).scalar() or 0


def get_total_impressions(db: Session):
    return db.query(func.sum(Audience.impressions)).scalar() or 0


def get_gender_distribution(db: Session):
    results = (
        db.query(
            Audience.gender,
            func.count(Audience.id)
        )
        .group_by(Audience.gender)
        .all()
    )

    return {
        gender: count
        for gender, count in results
    }


def get_age_distribution(db: Session):
    results = (
        db.query(
            Audience.age_group,
            func.count(Audience.id)
        )
        .group_by(Audience.age_group)
        .all()
    )

    return {
        age_group: count
        for age_group, count in results
    }


def get_top_countries(db: Session):
    results = (
        db.query(
            Audience.country,
            func.count(Audience.id).label("total")
        )
        .group_by(Audience.country)
        .order_by(func.count(Audience.id).desc())
        .all()
    )

    return [
        {
            "country": country,
            "count": total
        }
        for country, total in results
    ]


def get_top_cities(db: Session):
    results = (
        db.query(
            Audience.city,
            func.count(Audience.id).label("total")
        )
        .group_by(Audience.city)
        .order_by(func.count(Audience.id).desc())
        .all()
    )

    return [
        {
            "city": city,
            "count": total
        }
        for city, total in results
    ]


def get_device_distribution(db: Session):
    results = (
        db.query(
            Audience.device_type,
            func.count(Audience.id)
        )
        .group_by(Audience.device_type)
        .all()
    )

    return {
        device: count
        for device, count in results
    }


def get_audience_report(db: Session):
    return {
        "total_followers": get_total_followers(db),
        "total_reach": get_total_reach(db),
        "total_impressions": get_total_impressions(db),
        "gender_distribution": get_gender_distribution(db),
        "age_distribution": get_age_distribution(db),
        "top_countries": get_top_countries(db),
        "top_cities": get_top_cities(db),
        "device_distribution": get_device_distribution(db)
    }


def get_growth_report(db: Session):
    growth_data = (
        db.query(Growth)
        .order_by(Growth.date.desc())
        .limit(30)
        .all()
    )

    growth_data.reverse()

    results = []

    previous_followers = None

    for record in growth_data:
        if previous_followers is None:
            daily_growth = 0
            growth_percentage = 0
        else:
            daily_growth = record.followers - previous_followers

            if previous_followers == 0:
                growth_percentage = 0
            else:
                growth_percentage = (
                    daily_growth / previous_followers
                ) * 100

        results.append({
            "date": record.date,
            "followers": record.followers,
            "daily_growth": daily_growth,
            "growth_percentage": round(
                growth_percentage, 2
            )
        })

        previous_followers = record.followers

    return results


def get_audience_trends(db: Session):
    growth_data = (
        db.query(Growth)
        .order_by(Growth.date.asc())
        .limit(30)
        .all()
    )

    return [
        {
            "date": record.date,
            "followers": record.followers,
            "reach": record.reach
        }
        for record in growth_data
    ]