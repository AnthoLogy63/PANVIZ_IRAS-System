"""R03-R04 and separately documented CR01 district filtering."""
import json
from flask import Blueprint, current_app, render_template, request
from ..db import get_db
from ..services.consolidation_service import active_filters, accepted_records, consolidate, filter_options, rejection_records
from ..services.export_service import CONSOLIDATED_FIELDS, csv_response, reconcile

bp = Blueprint("reportes", __name__, url_prefix="/reportes")

@bp.get("/")
def index():
    db = get_db()
    db.execute("BEGIN")
    filters = active_filters()
    groups = consolidate(db, filters)
    count = len(accepted_records(db, filters))
    total = reconcile(groups, count)
    return render_template("reportes.html", title="Reportes consolidados", subtitle="Resultados verificables, listos para compartir", groups=groups, total=total, accepted=count, filters=filters, options=filter_options(db))

@bp.get("/consolidado.csv")
def consolidated_csv():
    filters = active_filters()
    db = get_db()
    db.execute("BEGIN")
    groups = consolidate(db, filters)
    reconcile(groups, len(accepted_records(db, filters)))
    return csv_response(groups, CONSOLIDATED_FIELDS, "panviz_consolidado.csv")

@bp.get("/rechazos.csv")
def rejected_csv():
    district = request.args.get("distrito", "").strip() if current_app.config["DISTRICT_FILTER_ENABLED"] else ""
    rows = rejection_records(get_db(), district, request.args.get("lote", "").strip())
    records = [{"lote": row["batch_id"], "archivo": row["filename"], "fila": row["row_number"], "id": row["notification_id"], "motivo": row["reason"], "datos_originales": row["raw_json"]} for row in rows]
    return csv_response(records, ("lote", "archivo", "fila", "id", "motivo", "datos_originales"), "panviz_rechazos.csv")
