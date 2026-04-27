from fastapi.testclient import TestClient

from app.main import app


def test_login_and_assistant_query():
    with TestClient(app) as client:
        token_response = client.post(
            "/v1/auth/token",
            data={"username": "demo", "password": "ChangeMe123!"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert token_response.status_code == 200
        access_token = token_response.json()["access_token"]

        me_response = client.get(
            "/v1/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "demo"

        assistant_response = client.post(
            "/v1/assistant/query",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "user_id": "demo",
                "query": "Show me gritty sci-fi thrillers with AI themes",
                "context": {"preferred_genres": ["sci-fi", "thriller"], "excluded_ratings": ["G"]},
            },
        )
        assert assistant_response.status_code == 200
        body = assistant_response.json()
        assert "results" in body
        assert len(body["results"]) >= 1
