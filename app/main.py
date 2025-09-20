from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional, Dict, Any
from sqlmodel import select
from .db import init_db, get_session
from .models import Event, CowrieEvent
from .utils import gen_event_id, extract_params, to_snippet
from .detect import analyze
from .pcap_ingest import parse_pcap_to_events
import io, csv, os, datetime

app = FastAPI(title="URL Attack Detector MVP")

# ✅ Fixed paths (correct relative to container)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize DB
init_db()


def upsert_event_dict(ev: Dict[str, Any]):
    ev = ev.copy()
    ev.setdefault("event_id", gen_event_id())
    ev.setdefault("headers", {})
    if ev.get("url") and (ev.get("params") is None or ev.get("params") == {}):
        try:
            ev["params"] = extract_params(ev["url"])
        except Exception:
            ev["params"] = {}
    if ev.get("body") and not ev.get("body_snippet"):
        ev["body_snippet"] = to_snippet(ev.get("body"))
    atype, conf = analyze(ev)
    ev["attack_type"] = atype
    ev["attack_confidence"] = conf
    with get_session() as s:
        s.add(Event(**ev))
        s.commit()


def correlate_honeypot(window_seconds: int = 3600):
    with get_session() as s:
        cowries = s.exec(select(CowrieEvent)).all()
        events = s.exec(select(Event)).all()
        for ce in cowries:
            for ev in events:
                if ev.src_ip == ce.src_ip:
                    try:
                        t_ev = datetime.datetime.fromisoformat(ev.timestamp.replace("Z", "+00:00"))
                        t_ce = datetime.datetime.fromisoformat(ce.timestamp.replace("Z", "+00:00"))
                        if abs((t_ev - t_ce).total_seconds()) <= window_seconds:
                            ev.honeypot_correlated = True
                            ev.honeypot_session = ce.session
                            if ce.event.lower().endswith("success"):
                                ev.is_success = True
                    except Exception:
                        pass
        s.commit()


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    attack_type: Optional[str] = None,
    ip: Optional[str] = None,
    success: Optional[bool] = None,
):
    with get_session() as s:
        stmt = select(Event)
        if attack_type:
            stmt = stmt.where(Event.attack_type == attack_type)
        if ip:
            stmt = stmt.where(Event.src_ip == ip)
        if success is not None:
            stmt = stmt.where(Event.is_success == success)
        rows = s.exec(stmt.order_by(Event.id.desc()).limit(500)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "rows": rows, "filters": {"attack_type": attack_type, "ip": ip, "success": success}},
    )


@app.get("/events")
def get_events(
    attack_type: Optional[str] = None,
    ip: Optional[str] = None,
    success: Optional[bool] = None,
):
    with get_session() as s:
        stmt = select(Event)
        if attack_type:
            stmt = stmt.where(Event.attack_type == attack_type)
        if ip:
            stmt = stmt.where(Event.src_ip == ip)
        if success is not None:
            stmt = stmt.where(Event.is_success == success)
        return s.exec(stmt.order_by(Event.id.desc()).limit(1000)).all()


@app.get("/export.csv")
def export_csv(
    attack_type: Optional[str] = None,
    ip: Optional[str] = None,
    success: Optional[bool] = None,
):
    with get_session() as s:
        stmt = select(Event)
        if attack_type:
            stmt = stmt.where(Event.attack_type == attack_type)
        if ip:
            stmt = stmt.where(Event.src_ip == ip)
        if success is not None:
            stmt = stmt.where(Event.is_success == success)
        rows = s.exec(stmt.order_by(Event.id.desc())).all()
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(
        ["timestamp", "src_ip", "dst_ip", "method", "url", "attack_type", "confidence", "is_success", "honeypot_session"]
    )
    for r in rows:
        w.writerow(
            [r.timestamp, r.src_ip, r.dst_ip, r.method, r.url, r.attack_type, r.attack_confidence, r.is_success, r.honeypot_session]
        )
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")


@app.get("/export.json")
def export_json(
    attack_type: Optional[str] = None,
    ip: Optional[str] = None,
    success: Optional[bool] = None,
):
    rows = get_events(attack_type, ip, success)
    return JSONResponse(content=[r.model_dump() for r in rows])


@app.post("/ingest/http")
async def ingest_http(payload: List[Dict[str, Any]]):
    for ev in payload:
        upsert_event_dict(ev)
    return {"status": "ok", "ingested": len(payload)}


@app.post("/ingest/cowrie")
async def ingest_cowrie(payload: List[Dict[str, Any]]):
    with get_session() as s:
        for ev in payload:
            ce = CowrieEvent(
                **{
                    "timestamp": ev.get("timestamp") or ev.get("time") or "",
                    "src_ip": ev.get("src_ip") or ev.get("peerIP") or ev.get("ip") or "",
                    "event": ev.get("event") or ev.get("message") or "",
                    "username": ev.get("username") or ev.get("user"),
                    "password": ev.get("password") or ev.get("pass"),
                    "session": ev.get("session"),
                }
            )
            s.add(ce)
        s.commit()
    correlate_honeypot()
    return {"status": "ok", "ingested": len(payload)}


@app.post("/ingest/pcap")
async def ingest_pcap(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    p = os.path.join("uploads", file.filename)
    with open(p, "wb") as f:
        f.write(await file.read())
    events = parse_pcap_to_events(p)
    for ev in events:
        upsert_event_dict(ev)
    correlate_honeypot()
    return {"status": "ok", "pcap_events": len(events)}

@app.get("/cowrie", response_class=HTMLResponse)
def cowrie_index(request: Request, ip: Optional[str] = None, success: Optional[bool] = None):
    with get_session() as s:
        stmt = select(CowrieEvent)
        if ip:
            stmt = stmt.where(CowrieEvent.src_ip == ip)
        if success is not None:
            if success:
                stmt = stmt.where(CowrieEvent.event.ilike("%success"))
            else:
                stmt = stmt.where(CowrieEvent.event.ilike("%fail%"))
        rows = s.exec(stmt.order_by(CowrieEvent.id.desc()).limit(500)).all()
    return templates.TemplateResponse("cowrie.html", {"request": request, "rows": rows, "filters": {"ip": ip, "success": success}})

@app.get("/cowrie/export.csv")
def export_cowrie_csv():
    with get_session() as s:
        rows = s.exec(select(CowrieEvent).order_by(CowrieEvent.id.desc())).all()
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["timestamp","src_ip","event","username","password","session"])
    for r in rows:
        w.writerow([r.timestamp, r.src_ip, r.event, r.username, r.password, r.session])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")

@app.get("/cowrie/export.json")
def export_cowrie_json():
    with get_session() as s:
        rows = s.exec(select(CowrieEvent).order_by(CowrieEvent.id.desc())).all()
    return JSONResponse(content=[r.model_dump() for r in rows])

@app.get("/cowrie", response_class=HTMLResponse)
def cowrie_index(
    request: Request,
    ip: Optional[str] = None,
    event: Optional[str] = None,
):
    with get_session() as s:
        stmt = select(CowrieEvent)
        if ip:
            stmt = stmt.where(CowrieEvent.src_ip == ip)
        if event:
            stmt = stmt.where(CowrieEvent.event == event)
        rows = s.exec(stmt.order_by(CowrieEvent.id.desc()).limit(500)).all()
    return templates.TemplateResponse(
        "cowrie.html",
        {"request": request, "rows": rows, "filters": {"ip": ip, "event": event}},
    )


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


