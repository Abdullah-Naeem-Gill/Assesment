from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core_db.database import init_db
from src.routers import task
from src.middleware.rate_limiting import RateLimitMiddleware


app = FastAPI()

app.add_middleware(RateLimitMiddleware, max_requests=10, window_seconds=60)

app.include_router(task.router)
