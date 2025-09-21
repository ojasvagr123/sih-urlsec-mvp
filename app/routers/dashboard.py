from fastapi import APIRouter, Request
from sqlmodel import select
from ..db import get_session
from ..models import Event
from collections import Counter
import datetime

router = APIRouter()

@router.get("/", response_class="HTMLResponse")
def index(request: Request):
    with get_session() as s:
        rows = s.exec(select(Event).order_by(Event.id.desc()).limit(500)).all()

        # Stats
        total_events = len(s.exec(select(Event)).all())
        honeypot_hits = len(s.exec(select(Event).where(Event.honeypot_correlated == True)).all())
        successful_attacks = len(s.exec(select(Event).where(Event.is_success == True)).all())

        ip_list = [e.src_ip for e in s.exec(select(Event.src_ip)).all()]
        top_attackers = Counter(ip_list).most_common(5)

        type_list = [e.attack_type for e in s.exec(select(Event.attack_type)).all() if e.attack_type]
        attack_types = Counter(type_list).most_common(5)

    return request.app.state.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rows": rows,
            "stats": {
                "total": total_events,
                "honeypot": honeypot_hits,
                "success": successful_attacks,
                "top_attackers": top_attackers,
                "attack_types": attack_types,
            },
            "filters": {},
        },
    )
