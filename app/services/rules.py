from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.rule import OptimizationRule


def create_rule(db: Session, *, site_id, data) -> OptimizationRule:
    if "rule_type" in data and hasattr(data["rule_type"], "value"):
        data["rule_type"] = data["rule_type"].value
    rule = OptimizationRule(site_id=site_id, **data)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def list_rules(db: Session, site_id) -> list[OptimizationRule]:
    return db.query(OptimizationRule).filter(OptimizationRule.site_id == site_id).all()
