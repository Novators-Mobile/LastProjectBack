from enum import Enum


class UploadType(str, Enum):
    boundary = "boundary"
    terrain = "terrain"
    existing = "existing"


class UploadStatus(str, Enum):
    uploaded = "uploaded"
    processed = "processed"
    failed = "failed"


class RestrictionSeverity(str, Enum):
    forbidden = "forbidden"
    limited = "limited"


class ExistingFeatureType(str, Enum):
    building = "building"
    road = "road"
    power_line = "power_line"
    gas_pipeline = "gas_pipeline"
    pipeline = "pipeline"
    rail = "rail"
    other = "other"


class AnalysisLayerType(str, Enum):
    slope = "slope"
    buildable_areas = "buildable_areas"
    infrastructure_nodes = "infrastructure_nodes"


class PlannedObjectType(str, Enum):
    warehouse = "warehouse"
    open_storage = "open_storage"
    workshop = "workshop"
    loading_ramp = "loading_ramp"
    admin = "admin"
    checkpoint = "checkpoint"
    network = "network"


class OptimizationRuleType(str, Enum):
    near = "near"
    far = "far"
    adjacent = "adjacent"
    perimeter = "perimeter"
    minimize_network_length = "minimize_network_length"


class GenerationStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"

