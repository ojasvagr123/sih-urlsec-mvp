#!/usr/bin/env bash
set -e
echo "[*] Starting honeypot (docker-compose)..."
docker-compose up -d --build
echo "[*] Done. To follow logs: docker logs -f cowrie"
