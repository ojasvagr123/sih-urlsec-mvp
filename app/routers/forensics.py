from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.db import engine
from app.models import Event, CowrieEvent

router = APIRouter()

@router.get("/forensics", response_class=JSONResponse)
def list_forensic_events(
    ip: str | None = Query(None, description="Filter by source IP"),
    attack_type: str | None = Query(None, description="Filter by attack type"),
    limit: int = 50,
):
    """List recent attack events with optional filters."""
    with Session(engine) as session:
        stmt = select(Event).order_by(Event.id.desc())

        if ip:
            stmt = stmt.where(Event.src_ip == ip)
        if attack_type:
            stmt = stmt.where(Event.attack_type == attack_type)

        events = session.exec(stmt.limit(limit)).all()

        results = [
            {
                "id": e.id,
                "timestamp": e.timestamp,
                "src_ip": e.src_ip,
                "dst_ip": e.dst_ip,
                "method": e.method,
                "url": e.url,
                "attack_type": e.attack_type,
                "attack_confidence": e.attack_confidence,
                "is_success": e.is_success,
                "honeypot_correlated": e.honeypot_correlated,
            }
            for e in events
        ]

        return JSONResponse(content=results)


@router.get("/forensics/{event_id}", response_class=JSONResponse)
def get_forensic_detail(event_id: int):
    """Return full details for a specific attack event."""
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            return JSONResponse(status_code=404, content={"error": "Event not found"})

        honeypot_hits = session.exec(
            select(CowrieEvent)
            .where(CowrieEvent.src_ip == event.src_ip)
            .order_by(CowrieEvent.id.desc())
            .limit(5)
        ).all()

        detail = {
            "id": event.id,
            "timestamp": event.timestamp,
            "src_ip": event.src_ip,
            "dst_ip": event.dst_ip,
            "method": event.method,
            "url": event.url,
            "params": event.params,
            "headers": event.headers,
            "body_snippet": event.body_snippet,
            "attack_type": event.attack_type,
            "attack_confidence": event.attack_confidence,
            "is_success": event.is_success,
            "honeypot_correlated": event.honeypot_correlated,
            "honeypot_hits": [
                {
                    "timestamp": h.timestamp,
                    "event": h.event,
                    "username": h.username,
                    "password": h.password,
                }
                for h in honeypot_hits
            ],
        }

        return JSONResponse(content=detail)
