"""R01-R02: two-stage import; confirmation revalidates under a write lock."""
import secrets
from pathlib import Path
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, session, url_for
from werkzeug.utils import secure_filename
from ..db import get_db
from ..services.csv_service import CsvError, analyze_existing, process_import

bp = Blueprint("importacion", __name__, url_prefix="/importacion")

def render_import(**kwargs):
    batches = get_db().execute("SELECT * FROM batches ORDER BY id DESC LIMIT 20").fetchall()
    return render_template("importacion.html", title="Importar datos", subtitle="De archivos dispersos a información confiable", batches=batches, **kwargs)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_import()
    upload = request.files.get("archivo")
    if not upload or not upload.filename or not upload.filename.lower().endswith(".csv"):
        return render_import(error="Selecciona un archivo con extensión .csv."), 400
    payload = upload.read()
    db = get_db()
    try:
        result = analyze_existing(db, payload, current_app.config["MAX_CSV_ROWS"])
    except CsvError as error:
        return render_import(error=str(error)), 400
    filename = secure_filename(upload.filename)[:120] or "notificaciones.csv"
    token = secrets.token_urlsafe(24)
    with db:
        db.execute("DELETE FROM previews WHERE created_at < strftime('%Y-%m-%dT%H:%M:%SZ','now','-1 hour')")
        previous = session.get("preview_token")
        if previous:
            db.execute("DELETE FROM previews WHERE token=?", (previous,))
        db.execute("INSERT INTO previews(token,filename,payload) VALUES (?,?,?)", (token, filename, payload))
    session["preview_token"] = token
    preview_rows = [dict(row, estado="Válido", motivo="Sin observaciones") for row in result["accepted"][:20]]
    preview_rows += [dict(row["datos"], estado="Rechazado", motivo=row["motivo"]) for row in result["rejected"][:20]]
    return render_import(preview=result, preview_rows=preview_rows, token=token, filename=filename)

@bp.post("/confirmar")
def confirm():
    token = request.form.get("token", "")
    if not token or not secrets.compare_digest(token, session.get("preview_token", "")):
        abort(400, description="La vista previa no corresponde a esta sesión. Vuelve a cargar el CSV.")
    db = get_db()
    try:
        with db:
            db.execute("BEGIN IMMEDIATE")
            pending = db.execute("SELECT * FROM previews WHERE token=? AND created_at >= strftime('%Y-%m-%dT%H:%M:%SZ','now','-1 hour')", (token,)).fetchone()
            if not pending:
                abort(409, description="La vista previa venció o ya fue procesada. Vuelve a cargar el archivo.")
            result = process_import(db, pending["payload"], pending["filename"], max_rows=current_app.config["MAX_CSV_ROWS"])
            db.execute("DELETE FROM previews WHERE token=?", (token,))
    except CsvError as error:
        abort(400, description=str(error))
    session.pop("preview_token", None)
    flash(f'Lote #{result["batch_id"]} procesado: {len(result["accepted"])} aceptados y {len(result["rejected"])} rechazados.', "success")
    return redirect(url_for("validacion.index", lote=result["batch_id"]))

@bp.get("/ejemplo.csv")
def example():
    sample = Path(current_app.root_path).parents[1] / "datos" / "entrada" / "notificaciones_iras.csv"
    return send_file(sample, mimetype="text/csv", as_attachment=True, download_name=sample.name)
