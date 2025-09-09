from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.routes.health import router as health_router
from .api.routes.participants import router as participants_router
from .api.routes.sessions import router as sessions_router
from .api.routes.events import router as events_router
from .db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    # CORS
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Routers
    app.include_router(health_router)
    app.include_router(participants_router, prefix="/api")
    app.include_router(sessions_router, prefix="/api")
    app.include_router(events_router, prefix="/api")

    return app


app = create_app()


