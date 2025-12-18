from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AuthDep, DBSession
from app.schemas.rules import RuleCreate, RuleOut
from app.services.rules import create_rule, list_rules
from app.services.sites import get_site

router = APIRouter()


@router.post(
    "/{site_id}/rules",
    response_model=RuleOut,
    summary="Создать оптимизационное правило",
    description="Создаёт оптимизационное правило взаимодействия объектов или сетей.",
)
def create_rule_endpoint(site_id: UUID, payload: RuleCreate, db: DBSession, _: AuthDep) -> RuleOut:
    get_site(db, site_id)
    rule = create_rule(db, site_id=site_id, data=payload.model_dump())
    return RuleOut.model_validate(rule)


@router.get(
    "/{site_id}/rules",
    response_model=list[RuleOut],
    summary="Список правил",
    description="Возвращает список оптимизационных правил для площадки.",
)
def list_rules_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> list[RuleOut]:
    get_site(db, site_id)
    rules = list_rules(db, site_id)
    return [RuleOut.model_validate(r) for r in rules]
