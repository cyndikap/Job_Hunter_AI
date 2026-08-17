from __future__ import annotations

from statistics import mean
from typing import Any


class LLMMonitoring:
    def __init__(self) -> None:
        self.requests = 0
        self.errors = 0
        self.fallbacks = 0
        self.response_times_ms: list[float] = []

    def record_request(self, provider: str | None = None, duration_ms: float | None = None) -> dict[str, Any]:
        self.requests += 1
        if duration_ms is not None:
            self.response_times_ms.append(float(duration_ms))
        return self.snapshot()

    def record_error(self, error: str | None = None) -> dict[str, Any]:
        self.errors += 1
        return self.snapshot()

    def record_fallback(self) -> dict[str, Any]:
        self.fallbacks += 1
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        avg_response_ms = round(mean(self.response_times_ms), 2) if self.response_times_ms else 0.0
        return {
            "requests": self.requests,
            "errors": self.errors,
            "fallbacks": self.fallbacks,
            "average_response_time_ms": avg_response_ms,
            "error_rate": round((self.errors / self.requests) * 100, 2) if self.requests else 0.0,
        }
