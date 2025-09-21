#!/usr/bin/env python3
import re
import sys
from collections import Counter

LOG_PATH = sys.argv[1] if len(sys.argv) > 1 else "/cowrie/data/log/cowrie.session.log"
RE_CMD = re.compile(r"src=(?P<src>[\d\.]+).+cmd=(?P<cmd>.+)$")

def parse(path):
    ip_counts = Counter()
    cmd_counts = Counter()
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = RE_CMD.search(line)
                if not m:
                    continue
                ip = m.group("src")
                cmd = m.group("cmd").strip()
                ip_counts[ip] += 1
                cmd_counts[cmd] += 1
    except FileNotFoundError:
        print("Log file not found:", path)
    return ip_counts, cmd_counts

if __name__ == "__main__":
    ips, cmds = parse(LOG_PATH)
    print("Top attacker IPs:")
    for ip, c in ips.most_common(10):
        print(f"  {ip}: {c}")
    print("\nTop commands:")
    for cmd, c in cmds.most_common(20):
        print(f"  {c:4d}  {cmd}")
