from uuid import UUID

import pytest
from flask import request

from app import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


def test_health(app):
    with app.test_client() as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}
    assert response.content_type == "application/json"
    assert UUID(response.headers["X-Request-ID"]).version == 4
    assert "Access-Control-Allow-Origin" not in response.headers


@pytest.mark.parametrize(
    ("method", "path", "status", "code"),
    [
        ("GET", "/api/v1/missing", 404, "NOT_FOUND"),
        ("GET", "/health", 404, "NOT_FOUND"),
        ("POST", "/api/v1/health", 405, "METHOD_NOT_ALLOWED"),
    ],
)
def test_http_errors_are_json(app, method, path, status, code):
    with app.test_client() as client:
        response = client.open(path, method=method)

    assert response.status_code == status
    assert response.json["code"] == code
    assert response.json["requestId"] == response.headers["X-Request-ID"]
    assert response.json["message"]
    if status == 405:
        assert "GET" in response.headers["Allow"]


def test_request_ids_are_generated_per_request(app):
    with app.test_client() as client:
        first = client.get("/api/v1/health", headers={"X-Request-ID": "untrusted"})
        second = client.get("/api/v1/health")

    assert UUID(first.headers["X-Request-ID"]).version == 4
    assert first.headers["X-Request-ID"] != second.headers["X-Request-ID"]


def test_internal_error_does_not_expose_exception():
    app = create_app({"TESTING": True, "PROPAGATE_EXCEPTIONS": False})

    @app.get("/failure")
    def failure():
        raise RuntimeError("private implementation detail")

    with app.test_client() as client:
        response = client.get("/failure")

    assert response.status_code == 500
    assert response.json == {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Internal Server Error",
        "requestId": response.headers["X-Request-ID"],
    }
    assert "private implementation detail" not in response.text


def test_environment_config_and_factory_isolation(monkeypatch):
    monkeypatch.setenv("NUBMARK_MAX_CONTENT_LENGTH", "64")
    first = create_app({"TESTING": True, "MAX_CONTENT_LENGTH": 128})
    second = create_app()

    assert first.config["MAX_CONTENT_LENGTH"] == 128
    assert second.config["MAX_CONTENT_LENGTH"] == 64
    assert second.testing is False
    assert second.debug is False


def test_body_size_limit_returns_json(app):
    app.config["MAX_CONTENT_LENGTH"] = 16

    @app.post("/echo")
    def echo():
        return request.get_json()

    with app.test_client() as client:
        response = client.post("/echo", json={"message": "x" * 32})

    assert response.status_code == 413
    assert response.json["code"] == "REQUEST_ENTITY_TOO_LARGE"
    assert response.json["requestId"] == response.headers["X-Request-ID"]
