from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_minute: int = 60):
        super().__init__(app)
        self.limit_per_minute = limit_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = [ts for ts in self.requests.get(client_ip, []) if now - ts < 60]
        window.append(now)
        self.requests[client_ip] = window
        if len(window) > self.limit_per_minute:
            return __import__("fastapi").Response(content='{"detail": "Rate limit exceeded"}', status_code=429, media_type="application/json")
        return await call_next(request)


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start = time.time()
        response = await call_next(request)
        elapsed_ms = round((time.time() - start) * 1000, 2)
        print(f"AUDIT {request.method} {request.url.path} status={response.status_code} elapsed_ms={elapsed_ms}")
        return response
