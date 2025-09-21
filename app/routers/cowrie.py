from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from sqlmodel import select
from ..db import get_session
from ..models import CowrieEvent
import io, csv

router = APIRouter()

@router.get("/cowrie", response_class=HTMLResponse)
def cowrie_index(request: Request):
    with get_session() as s:
        rows = s.exec(select(CowrieEvent).order_by(CowrieEvent.id.desc()).limit(500)).all()
    return request.app.state.templates.TemplateResponse("cowrie.html", {
        "request": request,
        "rows": rows,
        "filters": {}
    })

@router.post("/ingest/cowrie")
async def ingest_cowrie(payload: list[dict]):
    with get_session() as s:
        for ev in payload:
            ce = CowrieEvent(
                timestamp=ev.get("timestamp") or ev.get("time") or "",
                src_ip=ev.get("src_ip") or ev.get("peerIP") or ev.get("ip") or "",
                event=ev.get("event") or ev.get("message") or "",
                username=ev.get("username") or ev.get("user"),
                password=ev.get("password") or ev.get("pass"),
                session=ev.get("session"),
            )
            s.add(ce)
        s.commit()
    return {"status": "ok", "ingested": len(payload)}

@router.get("/cowrie/export.csv")
def export_cowrie_csv():
    with get_session() as s:
        rows = s.exec(select(CowrieEvent).order_by(CowrieEvent.id.desc())).all()
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["timestamp","src_ip","event","username","password","session"])
    for r in rows:
        w.writerow([r.timestamp, r.src_ip, r.event, r.username, r.password, r.session])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")

@router.get("/cowrie/export.json")
def export_cowrie_json():
    with get_session() as s:
        rows = s.exec(select(CowrieEvent).order_by(CowrieEvent.id.desc())).all()
    return JSONResponse(content=[r.model_dump() for r in rows])
