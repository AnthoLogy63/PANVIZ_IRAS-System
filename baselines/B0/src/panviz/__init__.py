"""PANVIZ IRAS application factory. Requirements R01-R05 + CR01."""
import hmac
import os
import secrets
import sqlite3
from pathlib import Path
from flask import Flask, abort, render_template, request, session
from werkzeug.exceptions import RequestEntityTooLarge
from .config import Config
from .db import close_db, get_db, init_db

__version__ = "0.1.0"

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    # A persisted local key prevents invalidating previews on restart.
    if not app.config.get("SECRET_KEY"):
        key_path = Path(app.config["DATABASE"]).parent / ".secret_key"
        key_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with key_path.open("x", encoding="utf-8") as handle:
                handle.write(secrets.token_hex(32))
        except FileExistsError:
            pass
        app.config["SECRET_KEY"] = os.environ.get("PANVIZ_SECRET_KEY") or key_path.read_text().strip()
    app.teardown_appcontext(close_db)

    @app.before_request
    def protect_forms():
        session.setdefault("csrf_token", secrets.token_hex(24))
        if request.method == "POST":
            expected = session.get("csrf_token", "")
            received = request.form.get("csrf_token", "")
            if not expected or not hmac.compare_digest(expected, received):
                abort(400, description="El formulario venció. Recarga la página e inténtalo de nuevo.")

    @app.context_processor
    def shared_context():
        return {"version": __version__, "district_filter_enabled": app.config["DISTRICT_FILTER_ENABLED"]}

    @app.after_request
    def response_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(409)
    @app.errorhandler(413)
    def user_error(error):
        message = "El archivo supera el límite de 2 MB." if isinstance(error, RequestEntityTooLarge) else error.description
        return render_template("error.html", message=message, code=error.code), error.code

    @app.errorhandler(sqlite3.OperationalError)
    def storage_error(error):
        app.logger.exception("SQLite operation failed")
        return render_template("error.html", code=503, message="No se pudo acceder al almacenamiento. Vuelve a intentarlo en unos segundos."), 503

    from .routes import dashboard, importacion, validacion, reportes
    for module in (dashboard, importacion, validacion, reportes):
        app.register_blueprint(module.bp)
    with app.app_context():
        init_db()
        if app.config["SEED_DEMO"]:
            from .services.csv_service import process_import
            sample = Path(app.root_path).parents[1] / "datos" / "entrada" / "notificaciones_iras.csv"
            # Serialize first-run seeding across application processes.
            db = get_db()
            with db:
                db.execute("BEGIN IMMEDIATE")
                if not db.execute("SELECT 1 FROM batches LIMIT 1").fetchone():
                    process_import(db, sample.read_bytes(), sample.name, source="demo")
    return app
