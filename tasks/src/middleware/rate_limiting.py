from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Dict, List
import time


class RateLimitMiddleware(BaseHTTPMiddleware): 
    def __init__(self, app: ASGIApp, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next) -> Response:
        ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        if ip not in self.request_counts:
            self.request_counts[ip] = []

        cutoff = current_time - self.window_seconds
        self.request_counts[ip] = [t for t in self.request_counts[ip] if t > cutoff]

        if len(self.request_counts[ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."}
            )

        self.request_counts[ip].append(current_time)

        response = await call_next(request)
        return response