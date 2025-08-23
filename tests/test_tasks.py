import pytest


@pytest.mark.anyio
async def test_health(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_create_task(client):
    payload = {"title": "Test task", "description": "Check CRUD"}
    resp = await client.post("/tasks/", json=payload)

    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert "id" in data
    return data


@pytest.mark.anyio
async def test_list_tasks(client):
    for i in range(2):
        await client.post("/tasks/", json={"title": f"Task {i}", "description": "bulk"})

        resp = await client.get("/tasks/?limit=10&offset=0")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert data["total"] >= 2


@pytest.mark.anyio
async def test_get_task(client):
    task = (await client.post("/tasks/", json={"title": "Get me"})).json()
    resp = await client.get(f"/tasks/{task['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == task["id"]


@pytest.mark.anyio
async def test_update_task(client):
    task = (await client.post("/tasks/", json={"title": "Old title"})).json()

    resp = await client.patch(f"/tasks/{task['id']}", json={"title": "New title"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New title"


@pytest.mark.anyio
async def test_delete_task(client):
    task = (await client.post("/tasks/", json={"title": "To delete"})).json()

    resp = await client.delete(f"/tasks/{task['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/tasks/{task['id']}")
    assert resp.status_code == 404
