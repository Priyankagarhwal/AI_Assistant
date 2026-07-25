from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.api.router import router
from app.core.logger import logger

from app.database.database import engine
from app.database.models import Base

# Create all database tables
Base.metadata.create_all(bind=engine)

# Debug prints
print("=" * 50)
print("Database URL :", engine.url)
print("Tables Found :", Base.metadata.tables.keys())
print("=" * 50)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logger.info("KnowledgeHub AI Backend Started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("KnowledgeHub AI Backend Stopped")