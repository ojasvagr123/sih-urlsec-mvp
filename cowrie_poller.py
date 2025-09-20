#!/usr/bin/env python3
import os, time, requests

HONEYPOT_API  = os.environ.get("HONEYPOT_API", "http://13.48.133.89/api/events")
MVP_API       = os.environ.get("MVP_API", "http://api:8000/ingest/cowrie")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))
BATCH_LIMIT   = int(os.environ.get("BATCH_LIMIT", "500"))

def main():
    print("[poller] starting poller loop...", flush=True)
    print(f"[poller] HONEYPOT_API={HONEYPOT_API}", flush=True)
    print(f"[poller] MVP_API={MVP_API}", flush=True)
    seen = set()
    while True:
        try:
            r = requests.get(HONEYPOT_API, timeout=10)
            r.raise_for_status()
            data = r.json().get("events", [])
            new_events = []
            for ev in data:
                ts  = ev.get("timestamp")
                ip  = ev.get("ip")
                eid = ev.get("eventid")
                key = (ts, ip, eid)
                if key in seen:
                    continue
                seen.add(key)
                new_events.append({
                    "timestamp": ts,
                    "src_ip": ip,
                    "event": eid,
                    "message": ev.get("message"),
                    "session": ev.get("sensor")
                })
                if len(new_events) >= BATCH_LIMIT:
                    break
            print(f"[poller] fetched {len(data)} total, {len(new_events)} new", flush=True)
            if new_events:
                try:
                    requests.post(MVP_API, json=new_events, timeout=10)
                    print(f"[poller] Forwarded {len(new_events)} events", flush=True)
                except Exception as e:
                    print("[poller] Post failed:", e, flush=True)
        except Exception as e:
            print("[poller] Fetch failed:", e, flush=True)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
