# Honeypot (Cowrie-like) — Minimal Repo

Minimal example repo that demonstrates running a small Cowrie-like honeypot in Docker on an EC2 instance.

## Contents
- Docker deployment (`docker-compose.yml`, `Dockerfile`)
- Minimal Cowrie config (`cowrie/cowrie.cfg`)
- Demo Python honeypot (`python/`) that logs sessions
- Helper scripts (`start.sh`, `provision.sh`)
- Small parser for quick summaries (`python/parser.py`)

## Quick start
1. Install Docker and Docker Compose.
2. From repo root:
   ```bash
   chmod +x start.sh cowrie/bin/run-cowrie.sh
   ./start.sh

## View Logs
tail -F cowrie/data/log/cowrie.session.log
