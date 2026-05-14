from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routes import download_router, generate_router, health_router, web_router

app = FastAPI(
    title="RegionGuard",
    description="Local cybersecurity engagement preparation toolkit for deterministic engagement briefs.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(web_router)
app.include_router(generate_router)
app.include_router(health_router)
app.include_router(download_router)
