# LastProjectBack

## Запуск (Docker)

1. Скопируйте переменные окружения из `.env.example` в `.env` (опционально).
2. Запустите (профиль prod):

`docker compose --profile prod up --build`

Для разработки (автоперезапуск при изменениях):

`docker compose --profile dev up --build`

API будет доступен на `http://localhost:8000`.

Документация:

- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Миграции

Для применения миграций внутри контейнера:

`docker compose exec api alembic upgrade head`

Для dev-профиля:

`docker compose exec api-dev alembic upgrade head`

## Запуск (локально)

1. Установите зависимости:

`python -m pip install -e ".[dev]"`

2. Установите переменные окружения (минимум `DATABASE_URL`).
3. Примените миграции:

`alembic upgrade head`

4. Запустите сервер:

`uvicorn app.main:app --reload`

## Тесты и линтинг

- Тесты: `pytest`
- Линтер: `ruff check .`

## Аутентификация

По умолчанию аутентификация отключена переменной `AUTH_DISABLED=true`.

Если `AUTH_DISABLED=false`, то каждый запрос должен содержать заголовок:

- `Authorization: Bearer <ACCESS_TOKEN>`

## Сценарий работы (по UI)

Ниже приведён рекомендуемый порядок вызовов API для типового сценария.

1) Создать площадку

- Вариант A (JSON):

`POST /api/sites`

```bash
curl -X POST http://localhost:8000/api/sites \
  -H "Content-Type: application/json" \
  -d '{"name":"Лесозавод №2"}'
```

Ответ:

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "created_at": "2025-01-01T00:00:00Z",
  "name": "Лесозавод №2"
}
```

- Вариант B (с файлами одним запросом):

`POST /api/sites/with-uploads` (multipart/form-data)

```bash
curl -X POST http://localhost:8000/api/sites/with-uploads \
  -F "name=Лесозавод №2" \
  -F "boundary_file=@site.dxf" \
  -F "terrain_file=@dem.tif" \
  -F "existing_file=@existing.dwg"
```

Ответ:

```json
{
  "site": {
    "id": "00000000-0000-0000-0000-000000000000",
    "created_at": "2025-01-01T00:00:00Z",
    "name": "Лесозавод №2"
  },
  "uploads": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "created_at": "2025-01-01T00:00:00Z",
      "site_id": "00000000-0000-0000-0000-000000000000",
      "upload_type": "boundary",
      "status": "uploaded",
      "filename": "site.dxf",
      "content_type": "application/octet-stream",
      "storage_path": "storage/..."
    }
  ]
}
```

2) Загрузить файлы (если не использовали вариант B)

- `POST /api/sites/{site_id}/uploads/boundary`
- `POST /api/sites/{site_id}/uploads/terrain`
- `POST /api/sites/{site_id}/uploads/existing` (опционально)

Пример:

```bash
curl -X POST http://localhost:8000/api/sites/{site_id}/uploads/boundary \
  -F "file=@site.dxf"
```

3) Задать границу площадки (GeoJSON)

`PUT /api/sites/{site_id}/boundary`

```bash
curl -X PUT http://localhost:8000/api/sites/{site_id}/boundary \
  -H "Content-Type: application/json" \
  -d '{"geojson":{"type":"Polygon","coordinates":[[[0,0],[0,10],[10,10],[10,0],[0,0]]]}}'
```

4) Запустить анализ

`POST /api/sites/{site_id}/analyze` (возвращает `202`)

```bash
curl -X POST http://localhost:8000/api/sites/{site_id}/analyze
```

5) Зоны ограничений (GeoJSON)

- Создать: `POST /api/sites/{site_id}/restriction-zones`
- Обновить: `PUT /api/sites/{site_id}/restriction-zones/{zone_id}`
- Удалить: `DELETE /api/sites/{site_id}/restriction-zones/{zone_id}`

6) Объекты и правила

- Объекты: `POST /api/sites/{site_id}/planned-objects`, `GET /api/sites/{site_id}/planned-objects`
- Правила: `POST /api/sites/{site_id}/rules`, `GET /api/sites/{site_id}/rules`

7) Генерация и просмотр вариантов

- Запуск: `POST /api/sites/{site_id}/generation-runs` (возвращает `202`)
- Статус: `GET /api/sites/{site_id}/generation-runs/{run_id}`
- Решения: `GET /api/sites/{site_id}/generation-runs/{run_id}/solutions`

8) Сводка статусов для UI

`GET /api/sites/{site_id}/summary`

Ответ включает наличие границы, счётчики загрузок, статусы анализа, последний запуск генерации и количество решений.

## Полный список эндпоинтов (с примерами)

Площадки

- `POST /api/sites`
  - `curl -X POST http://localhost:8000/api/sites -H "Content-Type: application/json" -d "{\"name\":\"Проект\"}"`
- `POST /api/sites/with-uploads`
  - `curl -X POST http://localhost:8000/api/sites/with-uploads -F "name=Проект" -F "boundary_file=@site.dxf" -F "terrain_file=@dem.tif"`
- `GET /api/sites`
  - `curl http://localhost:8000/api/sites`
- `GET /api/sites/{site_id}`
  - `curl http://localhost:8000/api/sites/{site_id}`
- `PATCH /api/sites/{site_id}`
  - `curl -X PATCH http://localhost:8000/api/sites/{site_id} -H "Content-Type: application/json" -d "{\"name\":\"Новое имя\"}"`
- `DELETE /api/sites/{site_id}`
  - `curl -X DELETE http://localhost:8000/api/sites/{site_id}`
- `PUT /api/sites/{site_id}/boundary`
  - `curl -X PUT http://localhost:8000/api/sites/{site_id}/boundary -H "Content-Type: application/json" -d "{\"geojson\":{\"type\":\"Polygon\",\"coordinates\":[[[0,0],[0,1],[1,1],[1,0],[0,0]]]}}"`
- `GET /api/sites/{site_id}/boundary`
  - `curl http://localhost:8000/api/sites/{site_id}/boundary`
- `GET /api/sites/{site_id}/summary`
  - `curl http://localhost:8000/api/sites/{site_id}/summary`

Загрузки

- `POST /api/sites/{site_id}/uploads/boundary`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/uploads/boundary -F "file=@site.dxf"`
- `POST /api/sites/{site_id}/uploads/terrain`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/uploads/terrain -F "file=@dem.tif"`
- `POST /api/sites/{site_id}/uploads/existing`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/uploads/existing -F "file=@existing.dwg"`
- `GET /api/sites/{site_id}/uploads`
  - `curl http://localhost:8000/api/sites/{site_id}/uploads`
- `DELETE /api/sites/{site_id}/uploads/{upload_id}`
  - `curl -X DELETE http://localhost:8000/api/sites/{site_id}/uploads/{upload_id}`

Зоны ограничений

- `POST /api/sites/{site_id}/restriction-zones`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/restriction-zones -H "Content-Type: application/json" -d "{\"zone_type\":\"СЗЗ\",\"severity\":\"forbidden\",\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[0,0],[0,2],[2,2],[2,0],[0,0]]]}}"`
- `GET /api/sites/{site_id}/restriction-zones`
  - `curl http://localhost:8000/api/sites/{site_id}/restriction-zones`
- `PUT /api/sites/{site_id}/restriction-zones/{zone_id}`
  - `curl -X PUT http://localhost:8000/api/sites/{site_id}/restriction-zones/{zone_id} -H "Content-Type: application/json" -d "{\"severity\":\"limited\"}"`
- `DELETE /api/sites/{site_id}/restriction-zones/{zone_id}`
  - `curl -X DELETE http://localhost:8000/api/sites/{site_id}/restriction-zones/{zone_id}`

Слои анализа

- `POST /api/sites/{site_id}/analyze`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/analyze`
- `GET /api/sites/{site_id}/layers`
  - `curl http://localhost:8000/api/sites/{site_id}/layers`

Объекты

- `POST /api/sites/{site_id}/planned-objects`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/planned-objects -H "Content-Type: application/json" -d "{\"object_type\":\"warehouse\",\"name\":\"Склад\",\"length_min\":100,\"length_max\":200}"`
- `GET /api/sites/{site_id}/planned-objects`
  - `curl http://localhost:8000/api/sites/{site_id}/planned-objects`

Правила

- `POST /api/sites/{site_id}/rules`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/rules -H "Content-Type: application/json" -d "{\"rule_type\":\"minimize_network_length\",\"weight\":1.0,\"params\":{}}"`
- `GET /api/sites/{site_id}/rules`
  - `curl http://localhost:8000/api/sites/{site_id}/rules`

Генерация

- `POST /api/sites/{site_id}/generation-runs`
  - `curl -X POST http://localhost:8000/api/sites/{site_id}/generation-runs -H "Content-Type: application/json" -d "{\"requested_solutions\":5,\"seed\":123}"`
- `GET /api/sites/{site_id}/generation-runs`
  - `curl http://localhost:8000/api/sites/{site_id}/generation-runs`
- `GET /api/sites/{site_id}/generation-runs/{run_id}`
  - `curl http://localhost:8000/api/sites/{site_id}/generation-runs/{run_id}`
- `GET /api/sites/{site_id}/generation-runs/{run_id}/solutions`
  - `curl http://localhost:8000/api/sites/{site_id}/generation-runs/{run_id}/solutions`
