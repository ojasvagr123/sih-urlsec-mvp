import os, uuid
from typing import List, Dict, Any
import pyshark

def parse_pcap_to_events(pcap_path: str) -> List[Dict[str, Any]]:
    events = []
    cap = pyshark.FileCapture(pcap_path, display_filter="http", keep_packets=False)
    try:
        for pkt in cap:
            try:
                http = pkt.http
            except AttributeError:
                continue
            method = getattr(http, "request_method", None)
            uri = getattr(http, "request_full_uri", None) or getattr(http, "request_uri", None)
            if not method or not uri:
                continue
            src_ip = getattr(pkt.ip, "src", None) if hasattr(pkt, "ip") else None
            dst_ip = getattr(pkt.ip, "dst", None) if hasattr(pkt, "ip") else None
            headers = {}
            host = getattr(http, "host", None)
            if host: headers["Host"] = host
            ua = getattr(http, "user_agent", None)
            if ua: headers["User-Agent"] = ua
            body_snippet = None
            try:
                if hasattr(http, "file_data"):
                    body_snippet = str(getattr(http, "file_data"))[:200]
            except Exception:
                body_snippet = None
            events.append({
                "event_id": str(uuid.uuid4()),
                "timestamp": getattr(pkt, "sniff_time", None).isoformat() if hasattr(pkt, "sniff_time") else None,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "method": str(method),
                "url": str(uri),
                "headers": headers,
                "body_snippet": body_snippet,
                "pcap_path": pcap_path
            })
    finally:
        try: cap.close()
        except Exception: pass
    return events
