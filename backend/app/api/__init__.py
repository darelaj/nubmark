from flask import Blueprint

api = Blueprint("api", __name__)


@api.get("/health")
def health() -> dict[str, str]:
    """Liveness only; database readiness is not checked."""
    return {"status": "ok"}
