# core/call_log.py — In-memory ring buffer for recent tool calls (last 50)
import threading
from collections import deque
from typing import Any


class CallLog:
    def __init__(self, maxlen: int = 50):
        self._log: deque = deque(maxlen=maxlen)
        self._lock = threading.Lock()

    def append(self, entry: dict[str, Any]) -> None:
        with self._lock:
            self._log.append(entry)

    def get_all(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._log)


call_log = CallLog()
