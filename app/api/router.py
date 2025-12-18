from fastapi import APIRouter

from app.api.routes.generation import router as generation_router
from app.api.routes.layers import router as layers_router
from app.api.routes.planned_objects import router as planned_objects_router
from app.api.routes.restriction_zones import router as restriction_zones_router
from app.api.routes.rules import router as rules_router
from app.api.routes.sites import router as sites_router
from app.api.routes.uploads import router as uploads_router

api_router = APIRouter()

api_router.include_router(sites_router, prefix="/sites", tags=["Площадки"])
api_router.include_router(uploads_router, prefix="/sites", tags=["Загрузки"])
api_router.include_router(restriction_zones_router, prefix="/sites", tags=["Зоны ограничений"])
api_router.include_router(layers_router, prefix="/sites", tags=["Слои анализа"])
api_router.include_router(planned_objects_router, prefix="/sites", tags=["Объекты"])
api_router.include_router(rules_router, prefix="/sites", tags=["Правила"])
api_router.include_router(generation_router, prefix="/sites", tags=["Генерация"])
