import pytest

from app.services.geojson import geojson_bbox


def test_geojson_bbox_polygon():
    geojson = {"type": "Polygon", "coordinates": [[[1, 2], [1, 5], [4, 5], [4, 2], [1, 2]]]}
    assert geojson_bbox(geojson) == (1.0, 2.0, 4.0, 5.0)


def test_geojson_bbox_invalid():
    with pytest.raises(ValueError):
        geojson_bbox({"type": "Polygon"})

