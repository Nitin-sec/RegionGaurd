from .download import router as download_router
from .generate import router as generate_router
from .health import router as health_router
from .web import router as web_router

__all__ = ["download_router", "generate_router", "health_router", "web_router"]
