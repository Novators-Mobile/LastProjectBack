from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AuthDep, DBSession
from app.schemas.layers import AnalysisLayerOut
from app.services.analysis import run_analysis
from app.services.layers import list_layers
from app.services.sites import get_site

router = APIRouter()


@router.post(
    "/{site_id}/analyze",
    status_code=202,
    summary="Запустить анализ контекста",
    description="Запускает расчёт слоёв анализа (уклоны, пятна застройки, точки инфраструктуры).",
)
def analyze_site(site_id: UUID, db: DBSession, _: AuthDep) -> None:
    get_site(db, site_id)
    run_analysis(db, site_id=site_id)


@router.get(
    "/{site_id}/layers",
    response_model=list[AnalysisLayerOut],
    summary="Получить слои анализа",
    description="Возвращает список слоёв анализа по площадке.",
)
def get_layers(site_id: UUID, db: DBSession, _: AuthDep) -> list[AnalysisLayerOut]:
    get_site(db, site_id)
    layers = list_layers(db, site_id)
    return [AnalysisLayerOut.model_validate(layer) for layer in layers]
