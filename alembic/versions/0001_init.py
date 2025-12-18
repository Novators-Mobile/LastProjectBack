"""init

Revision ID: 0001_init
Revises: 
Create Date: 2025-12-18
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sites",
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "site_boundaries",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("geojson", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("site_id"),
    )
    op.create_table(
        "uploads",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("upload_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("filename", sa.String(length=512), nullable=False),
        sa.Column("content_type", sa.String(length=200), nullable=True),
        sa.Column("storage_path", sa.String(length=1024), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_uploads_site_id", "uploads", ["site_id"])
    op.create_table(
        "terrain_models",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("upload_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["upload_id"], ["uploads.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_terrain_models_site_id", "terrain_models", ["site_id"])
    op.create_table(
        "existing_features",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("feature_type", sa.String(length=50), nullable=False),
        sa.Column("geometry", sa.JSON(), nullable=False),
        sa.Column("properties", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_existing_features_site_id", "existing_features", ["site_id"])
    op.create_table(
        "restriction_zones",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("zone_type", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False),
        sa.Column("geometry", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_restriction_zones_site_id", "restriction_zones", ["site_id"])
    op.create_table(
        "analysis_layers",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("layer_type", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_analysis_layers_site_id", "analysis_layers", ["site_id"])
    op.create_table(
        "planned_objects",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("object_type", sa.String(length=50), nullable=False),
        sa.Column("template_key", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("length_min", sa.Float(), nullable=True),
        sa.Column("length_max", sa.Float(), nullable=True),
        sa.Column("width_min", sa.Float(), nullable=True),
        sa.Column("width_max", sa.Float(), nullable=True),
        sa.Column("height_min", sa.Float(), nullable=True),
        sa.Column("height_max", sa.Float(), nullable=True),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_planned_objects_site_id", "planned_objects", ["site_id"])
    op.create_table(
        "optimization_rules",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("rule_type", sa.String(length=50), nullable=False),
        sa.Column("source_object_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("target_object_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("params", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_object_id"], ["planned_objects.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["target_object_id"], ["planned_objects.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_optimization_rules_site_id", "optimization_rules", ["site_id"])
    op.create_table(
        "generation_runs",
        sa.Column("site_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("seed", sa.Integer(), nullable=True),
        sa.Column("requested_solutions", sa.Integer(), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_generation_runs_site_id", "generation_runs", ["site_id"])
    op.create_table(
        "plan_solutions",
        sa.Column("run_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("layout", sa.JSON(), nullable=False),
        sa.Column("thumbnail_url", sa.String(length=1024), nullable=True),
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["generation_runs.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_plan_solutions_run_id", "plan_solutions", ["run_id"])


def downgrade() -> None:
    op.drop_index("ix_plan_solutions_run_id", table_name="plan_solutions")
    op.drop_table("plan_solutions")
    op.drop_index("ix_generation_runs_site_id", table_name="generation_runs")
    op.drop_table("generation_runs")
    op.drop_index("ix_optimization_rules_site_id", table_name="optimization_rules")
    op.drop_table("optimization_rules")
    op.drop_index("ix_planned_objects_site_id", table_name="planned_objects")
    op.drop_table("planned_objects")
    op.drop_index("ix_analysis_layers_site_id", table_name="analysis_layers")
    op.drop_table("analysis_layers")
    op.drop_index("ix_restriction_zones_site_id", table_name="restriction_zones")
    op.drop_table("restriction_zones")
    op.drop_index("ix_existing_features_site_id", table_name="existing_features")
    op.drop_table("existing_features")
    op.drop_index("ix_terrain_models_site_id", table_name="terrain_models")
    op.drop_table("terrain_models")
    op.drop_index("ix_uploads_site_id", table_name="uploads")
    op.drop_table("uploads")
    op.drop_table("site_boundaries")
    op.drop_table("sites")
