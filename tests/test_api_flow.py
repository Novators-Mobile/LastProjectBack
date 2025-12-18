from uuid import UUID


def test_basic_flow(client):
    r = client.post("/api/sites", json={"name": "Test site"})
    assert r.status_code == 200, r.text
    site = r.json()
    site_id = UUID(site["id"])

    boundary = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
    }
    r = client.put(f"/api/sites/{site_id}/boundary", json={"geojson": boundary})
    assert r.status_code == 200, r.text

    r = client.post(f"/api/sites/{site_id}/analyze")
    assert r.status_code == 202, r.text

    r = client.post(
        f"/api/sites/{site_id}/planned-objects",
        json={
            "object_type": "warehouse",
            "name": "Склад сырья",
            "length_min": 100,
            "length_max": 200,
            "width_min": 48,
            "width_max": 96,
            "height_min": 10,
            "height_max": 12,
        },
    )
    assert r.status_code == 200, r.text

    r = client.post(
        f"/api/sites/{site_id}/rules",
        json={"rule_type": "minimize_network_length", "weight": 1.0, "params": {}},
    )
    assert r.status_code == 200, r.text

    r = client.post(
        f"/api/sites/{site_id}/generation-runs",
        json={"requested_solutions": 5, "seed": 123},
    )
    assert r.status_code == 202, r.text
    run_id = r.json()["id"]

    r = client.get(f"/api/sites/{site_id}/generation-runs/{run_id}")
    assert r.status_code == 200, r.text

    r = client.get(f"/api/sites/{site_id}/generation-runs/{run_id}/solutions")
    assert r.status_code == 200, r.text
    sols = r.json()
    assert len(sols) in (0, 5)


def test_site_with_uploads_flow(client):
    r = client.post(
        "/api/sites/with-uploads",
        data={"name": "Проект с файлами"},
        files={
            "boundary_file": ("boundary.dxf", b"DXF", "application/octet-stream"),
            "terrain_file": ("terrain.tif", b"TIFF", "application/octet-stream"),
            "existing_file": ("existing.dwg", b"DWG", "application/octet-stream"),
        },
    )
    assert r.status_code == 201, r.text
    payload = r.json()
    site_id = UUID(payload["site"]["id"])
    assert len(payload["uploads"]) == 3

    r = client.get(f"/api/sites/{site_id}/summary")
    assert r.status_code == 200, r.text
    summary = r.json()
    assert summary["site"]["id"] == str(site_id)
    assert summary["uploads"]["boundary"] == 1
    assert summary["uploads"]["terrain"] == 1
    assert summary["uploads"]["existing"] == 1

    r = client.get(f"/api/sites/{site_id}/uploads")
    assert r.status_code == 200, r.text
    uploads = r.json()
    assert len(uploads) == 3

    upload_id = uploads[0]["id"]
    r = client.delete(f"/api/sites/{site_id}/uploads/{upload_id}")
    assert r.status_code == 204, r.text

    r = client.get(f"/api/sites/{site_id}/uploads")
    assert r.status_code == 200, r.text
    uploads2 = r.json()
    assert len(uploads2) == 2

    r = client.patch(f"/api/sites/{site_id}", json={"name": "Переименовано"})
    assert r.status_code == 200, r.text
    assert r.json()["name"] == "Переименовано"

    r = client.delete(f"/api/sites/{site_id}")
    assert r.status_code == 204, r.text
