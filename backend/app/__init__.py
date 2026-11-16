from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from flask import Flask, Response, g

from app.api import api
from app.errors import register_error_handlers


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(MAX_CONTENT_LENGTH=1024 * 1024)
    app.config.from_prefixed_env(prefix="NUBMARK")
    if test_config is not None:
        app.config.update(test_config)

    @app.before_request
    def assign_request_id() -> None:
        g.request_id = str(uuid4())

    @app.after_request
    def include_request_id(response: Response) -> Response:
        response.headers["X-Request-ID"] = g.request_id
        return response

    register_error_handlers(app)
    app.register_blueprint(api, url_prefix="/api/v1")
    return app
