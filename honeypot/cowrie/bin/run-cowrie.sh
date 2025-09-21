#!/usr/bin/env bash
set -e
# Default to running the simple python server if present, else fallback to loop logger
if [ -x /usr/bin/python3 ] && [ -f /cowrie/python/server.py ]; then
  echo "[cowrie] Running python demo honeypot..."
  exec python3 /cowrie/python/server.py
fi

echo "[cowrie] Running fallback logger..."
mkdir -p /cowrie/data/log
while true; do
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "$ts - session - src=127.0.0.1 - user=demo - cmd=uname -a" >> /cowrie/data/log/cowrie.session.log
  sleep 60
done
