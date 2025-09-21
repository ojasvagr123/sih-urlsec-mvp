#!/usr/bin/env python3
from pathlib import Path
import threading

class SessionLogger:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def info(self, line: str):
        if not line.endswith("\n"):
            line = line + "\n"
        with self._lock:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line)
