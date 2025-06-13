from fastapi.testclient import TestClient
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.main import app

client = TestClient(app)


def test_create_record():
    response = client.post("/records/", json={"name": "Test", "description": "desc"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["description"] == "desc"
    assert "id" in data


def test_read_records():
    client.post("/records/", json={"name": "Item1"})
    response = client.get("/records/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_and_delete_record():
    resp = client.post("/records/", json={"name": "to_update"})
    record_id = resp.json()["id"]

    update_resp = client.put(f"/records/{record_id}", json={"name": "updated", "description": "new"})
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "updated"

    delete_resp = client.delete(f"/records/{record_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["ok"] is True
