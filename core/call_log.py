# core/call_log.py — In-memory ring buffer for recent tool calls (last 50)
import threading
from collections import deque
from typing import Any


class CallLog:
    def __init__(self, maxlen: int = 50):
        self._log: deque = deque(maxlen=maxlen)
        self._lock = threading.Lock()
        self._total_count: int = 0

    def append(self, entry: dict[str, Any]) -> None:
        with self._lock:
            self._log.append(entry)
            self._total_count += 1

    def get_all(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._log)

    @property
    def total_count(self) -> int:
        with self._lock:
            return self._total_count


call_log = CallLog()
