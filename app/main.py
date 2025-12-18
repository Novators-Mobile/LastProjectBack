from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.router import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(
        title="LastProjectBack",
        version="0.1.0",
        description="Backend API для системы генерации вариантов генплана площадки.",
        openapi_tags=[
            {"name": "Площадки", "description": "Управление площадками и границами."},
            {"name": "Загрузки", "description": "Загрузка и управление файлами проекта."},
            {
                "name": "Зоны ограничений",
                "description": "Создание и редактирование зон ограничений.",
            },
            {"name": "Слои анализа", "description": "Запуск анализа и получение слоёв."},
            {
                "name": "Объекты",
                "description": "Создание и список объектов производственной схемы.",
            },
            {
                "name": "Правила",
                "description": "Оптимизационные правила взаимодействия объектов и сетей.",
            },
            {"name": "Генерация", "description": "Запуск генерации и получение вариантов."},
        ],
    )
    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )

        for methods in schema.get("paths", {}).values():
            for op in methods.values():
                if not isinstance(op, dict):
                    continue
                responses = op.get("responses") or {}
                for resp in responses.values():
                    if not isinstance(resp, dict):
                        continue
                    if resp.get("description") == "Successful Response":
                        resp["description"] = "Успешный ответ"
                    if resp.get("description") == "Validation Error":
                        resp["description"] = "Ошибка валидации"

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_app()
