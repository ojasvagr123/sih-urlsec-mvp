# SIH URL Security MVP

Minimal deployed solution to ingest HTTP events, Cowrie honeypot logs, and PCAPs, run rule-based detections, correlate with honeypot, and provide a web UI with filters and CSV/JSON export.

## Quick start

```bash
# 1) Build and run
docker compose up --build -d

# 2) Open UI
open http://localhost:8000

# 3) Ingest sample HTTP event
curl -X POST http://localhost:8000/ingest/http -H "Content-Type: application/json" -d '[
  {"timestamp":"2025-09-14T17:13:27Z","src_ip":"1.2.3.4","dst_ip":"127.0.0.1",
   "method":"GET","url":"/index.php?id=1 OR 1=1",
   "headers":{"User-Agent":"sqlmap/1.6"}}
]'

# 4) Ingest Cowrie JSON events (from your honeypot)
curl -X POST http://localhost:8000/ingest/cowrie -H "Content-Type: application/json" -d '[
  {"timestamp":"2025-09-14T17:13:20Z","src_ip":"1.2.3.4","event":"login.failed","username":"root","password":"toor","session":"abc"},
  {"timestamp":"2025-09-14T17:20:00Z","src_ip":"1.2.3.4","event":"login.success","username":"root","password":"admin","session":"abc"}
]'

# 5) Upload a PCAP
curl -F "file=@/path/to/your.pcap" http://localhost:8000/ingest/pcap
