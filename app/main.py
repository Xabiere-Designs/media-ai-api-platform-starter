from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import assistant, auth, health, users
from app.core.logging import configure_logging, request_logging_middleware
from app.core.metrics import metrics_router
from app.core.settings import settings
from app.db.init_db import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    seed_data()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.middleware("http")(request_logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(metrics_router, tags=["metrics"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["auth"])
app.include_router(users.router, prefix=settings.api_prefix, tags=["users"])
app.include_router(assistant.router, prefix=settings.api_prefix, tags=["assistant"])
