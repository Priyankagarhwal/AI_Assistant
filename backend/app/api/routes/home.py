from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()


@router.get("/", tags=["Home"])
async def home():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Backend Running 🚀"
    }