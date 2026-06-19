from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.relations import router as relations_router
from app.api.v1.moments import router as moments_router
from app.api.v1.elders import router as elders_router
from app.api.v1.ai import router as ai_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.upload import router as upload_router
from app.api.v1.community_auth import router as community_auth_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(relations_router)
api_router.include_router(moments_router)
api_router.include_router(elders_router)
api_router.include_router(ai_router)
api_router.include_router(alerts_router)
api_router.include_router(upload_router)
api_router.include_router(community_auth_router)
