import subprocess, json, uuid, binascii
from typing import List, Dict, Any

def parse_pcap_to_events(pcap_path: str) -> List[Dict[str, Any]]:
    events = []
    cmd = ["tshark", "-r", pcap_path, "-Y", "tcp.port==80", "-T", "json"]
    output = subprocess.check_output(cmd)
    packets = json.loads(output)

    for pkt in packets:
        layers = pkt.get("_source", {}).get("layers", {})
        http = layers.get("http", {})
        ip = layers.get("ip", {})
        tcp = layers.get("tcp", {})

        method = http.get("http.request.method")
        uri = http.get("http.request.full_uri") or http.get("http.request.uri")

        # Fallback if tshark didn't decode HTTP
        if not method and "tcp.payload" in tcp:
            try:
                raw_hex = tcp["tcp.payload"].replace(":", "")
                raw_bytes = binascii.unhexlify(raw_hex)
                raw_text = raw_bytes.decode(errors="ignore")
                first_line = raw_text.split("\r\n", 1)[0]
                parts = first_line.split()
                if len(parts) >= 2:
                    method, uri = parts[0], parts[1]
            except Exception:
                continue

        if not method or not uri:
            continue

        headers = {}
        if "http.host" in http:
            headers["Host"] = http["http.host"]
        if "http.user_agent" in http:
            headers["User-Agent"] = http["http.user_agent"]

        events.append({
            "event_id": str(uuid.uuid4()),
            "timestamp": layers.get("frame", {}).get("frame.time"),
            "src_ip": ip.get("ip.src"),
            "dst_ip": ip.get("ip.dst"),
            "method": method,
            "url": uri,
            "headers": headers,
            "body_snippet": None,
            "pcap_path": pcap_path,
        })
    return events
