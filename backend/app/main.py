from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import dashboard, leads
from app.core.config import get_settings
from app.scheduler.jobs import create_scheduler

settings = get_settings()
scheduler = create_scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


fastapi_app = FastAPI(title="Cafés Lisboa — Lead Automation", lifespan=lifespan)

fastapi_app.include_router(leads.router, prefix="/api")
fastapi_app.include_router(dashboard.router, prefix="/api")


@fastapi_app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


app = CORSMiddleware(
    app=fastapi_app,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
