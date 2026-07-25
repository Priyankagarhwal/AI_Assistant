from fastapi import APIRouter

from app.api.routes.home import router as home_router
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.workspace import router as workspace_router
from app.api.routes.document import router as document_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.summary import router as summary_router
router = APIRouter()

router.include_router(home_router)
router.include_router(health_router)
router.include_router(upload_router)
router.include_router(chat_router)
router.include_router(workspace_router)
router.include_router(document_router)
router.include_router(dashboard_router)
router.include_router(summary_router)