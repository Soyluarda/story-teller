from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/api/v1/activities/")
    assert response.status_code == 200


def test_get_activity_by_id():
    response = client.get("/api/v1/activities/1")
    assert response.status_code == 200


# ADD MORE & TEST TO COMPLETE THE TESTS FOR ACTIVITIES.
# MOCK TESTS FOR STRAVA ENDPOINTS.
