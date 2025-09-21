from fastapi import APIRouter, UploadFile, File
from ..pcap_ingest import parse_pcap_to_events
import os
from .http_events import upsert_event_dict

router = APIRouter()

@router.post("/ingest/pcap")
async def ingest_pcap(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    p = os.path.join("uploads", file.filename)
    with open(p, "wb") as f:
        f.write(await file.read())
    events = parse_pcap_to_events(p)
    for ev in events:
        upsert_event_dict(ev)
    return {"status": "ok", "pcap_events": len(events)}
