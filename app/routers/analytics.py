from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from app.db import engine
from app.models import Event, CowrieEvent

router = APIRouter()

@router.get("/analytics", response_class=JSONResponse)
def get_analytics():
    with Session(engine) as session:
        total_http_events = session.exec(select(func.count(Event.id))).one()
        total_cowrie_events = session.exec(select(func.count(CowrieEvent.id))).one()
        total_attacks = total_http_events + total_cowrie_events

        successful = session.exec(
            select(func.count(Event.id)).where(Event.is_success == True)
        ).one()

        top_attacks = session.exec(
            select(Event.attack_type, func.count(Event.attack_type))
            .where(Event.attack_type.is_not(None))
            .group_by(Event.attack_type)
            .order_by(func.count(Event.attack_type).desc())
            .limit(5)
        ).all()

        top_ips = session.exec(
            select(Event.src_ip, func.count(Event.src_ip))
            .group_by(Event.src_ip)
            .order_by(func.count(Event.src_ip).desc())
            .limit(5)
        ).all()

        last_week = datetime.utcnow() - timedelta(days=7)
        trend = session.exec(
            select(func.substr(Event.timestamp, 1, 10), func.count(Event.id))
            .where(Event.timestamp >= last_week.isoformat())
            .group_by(func.substr(Event.timestamp, 1, 10))
            .order_by(func.substr(Event.timestamp, 1, 10))
        ).all()

        return JSONResponse(
            content={
                "total_attacks": total_attacks,
                "successful_attacks": successful,
                "top_attacks": [{"type": t, "count": c} for t, c in top_attacks],
                "top_ips": [{"ip": ip, "count": c} for ip, c in top_ips],
                "trend": [{"date": d, "count": c} for d, c in trend],
            }
        )
