from flask import Flask, Response, g
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> Response:
        response = error.get_response()
        response.data = app.json.dumps(
            {
                "code": error.name.upper().replace(" ", "_"),
                "message": error.name,
                "requestId": g.request_id,
            }
        )
        response.content_type = "application/json"
        return response
