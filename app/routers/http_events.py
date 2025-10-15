from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from sqlmodel import select
from ..db import get_session
from ..models import Event
from ..utils import gen_event_id, extract_params, to_snippet
from ..detect import analyze
from ..pcap_ingest import parse_pcap_to_events  # fixed import
import io, csv, tempfile

router = APIRouter()

def upsert_event_dict(ev: dict):
    ev = ev.copy()
    ev.setdefault("event_id", gen_event_id())
    ev.setdefault("headers", {})
    if ev.get("url") and not ev.get("params"):
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

@router.get("/events")
def get_events():
    with get_session() as s:
        return s.exec(select(Event).order_by(Event.id.desc()).limit(1000)).all()

@router.get("/export.csv")
def export_csv():
    with get_session() as s:
        rows = s.exec(select(Event).order_by(Event.id.desc())).all()
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["timestamp","src_ip","dst_ip","method","url","attack_type","confidence","is_success","honeypot_session"])
    for r in rows:
        w.writerow([r.timestamp,r.src_ip,r.dst_ip,r.method,r.url,r.attack_type,r.attack_confidence,r.is_success,r.honeypot_session])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")

@router.get("/export.json")
def export_json():
    with get_session() as s:
        rows = s.exec(select(Event).order_by(Event.id.desc())).all()
    return JSONResponse(content=[r.model_dump() for r in rows])

@router.post("/ingest/http")
async def ingest_http(payload: list[dict]):
    for ev in payload:
        upsert_event_dict(ev)
    return {"status": "ok", "ingested": len(payload)}

@router.post("/upload/pcap")
async def upload_pcap(file: UploadFile = File(...)):
    if not file.filename.endswith(".pcap"):
        return {"error": "Invalid file type. Please upload a .pcap file."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    events = parse_pcap_to_events(tmp_path)
    for ev in events:
        upsert_event_dict(ev)

    return {"status": "ok", "parsed_events": len(events)}
