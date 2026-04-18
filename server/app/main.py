from flask import Flask, send_from_directory
from flask_cors import CORS

from .config import STATIC_DIR
from .routes import api, assets


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(assets, url_prefix="/api/assets")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path: str):
        target = STATIC_DIR / path
        if path and target.exists():
            return send_from_directory(STATIC_DIR, path)
        return send_from_directory(STATIC_DIR, "index.html")

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5001, debug=False)
