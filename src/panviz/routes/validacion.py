"""R02: rejection inspection with batch and district scope."""
from flask import Blueprint, abort, current_app, render_template, request
from ..db import get_db
from ..services.consolidation_service import rejection_records

bp = Blueprint("validacion", __name__, url_prefix="/validacion")

@bp.get("/")
def index():
    db = get_db()
    district = request.args.get("distrito", "").strip() if current_app.config["DISTRICT_FILTER_ENABLED"] else ""
    batch = request.args.get("lote", "").strip()
    rows = rejection_records(db, district, batch)
    batches = db.execute("SELECT * FROM batches ORDER BY id DESC").fetchall()
    chosen = next((row for row in batches if str(row["id"]) == batch), None)
    if batch and chosen is None:
        abort(404, description="El lote solicitado no existe.")
    districts = [r[0] for r in db.execute("SELECT distrito FROM notifications UNION SELECT distrito FROM rejections WHERE distrito != '' ORDER BY distrito")]
    summary = chosen or {"accepted": sum(r["accepted"] for r in batches), "rejected": sum(r["rejected"] for r in batches)}
    return render_template("validacion.html", title="Validación de datos", subtitle="Cada observación tiene una causa y una solución", rows=rows, batches=batches, batch=batch, district=district, districts=districts, summary=summary)
