from __future__ import annotations

from typing import Any


def _iter_coords(obj: Any):
    if isinstance(obj, (list, tuple)):
        if len(obj) == 2 and all(isinstance(v, (int, float)) for v in obj):
            yield obj
        else:
            for item in obj:
                yield from _iter_coords(item)


def geojson_bbox(geojson: dict) -> tuple[float, float, float, float]:
    coords = geojson.get("coordinates")
    if coords is None:
        raise ValueError("Invalid GeoJSON: missing coordinates")
    xs: list[float] = []
    ys: list[float] = []
    for x, y in _iter_coords(coords):
        xs.append(float(x))
        ys.append(float(y))
    if not xs:
        raise ValueError("Invalid GeoJSON: empty coordinates")
    return min(xs), min(ys), max(xs), max(ys)

