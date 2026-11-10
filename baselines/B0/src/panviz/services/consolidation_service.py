"""R03-R04 + CR01: shared scoped queries ensure exports match the screen."""
from flask import current_app, request

FILTERS = ("distrito", "semana_iso", "establecimiento", "grupo_etario")

def active_filters():
    values = {key: request.args.get(key, "").strip() for key in FILTERS}
    if not current_app.config["DISTRICT_FILTER_ENABLED"]:
        values["distrito"] = ""
    return values

def where_clause(filters):
    pairs = [(key, filters.get(key)) for key in FILTERS if filters.get(key)]
    return (" WHERE " + " AND ".join(key + " = ?" for key, _ in pairs) if pairs else ""), [value for _, value in pairs]

def consolidate(db, filters=None):
    where, params = where_clause(filters or {})
    return [dict(row) for row in db.execute("SELECT semana_iso, establecimiento, distrito, grupo_etario, COUNT(*) AS total FROM notifications" + where + " GROUP BY semana_iso, establecimiento, distrito, grupo_etario ORDER BY semana_iso, distrito, establecimiento, grupo_etario", params)]

def accepted_records(db, filters=None):
    where, params = where_clause(filters or {})
    return [dict(row) for row in db.execute("SELECT * FROM notifications" + where + " ORDER BY fecha_notificacion DESC, id", params)]

def filter_options(db):
    return {key: [row[0] for row in db.execute(f"SELECT DISTINCT {key} FROM notifications ORDER BY {key}")] for key in FILTERS}

def rejection_records(db, district="", batch=""):
    clauses, params = [], []
    if district:
        clauses.append("r.distrito=?")
        params.append(district)
    if batch:
        clauses.append("r.batch_id=?")
        params.append(batch)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    return [dict(row) for row in db.execute("SELECT r.*, b.filename FROM rejections r JOIN batches b ON b.id=r.batch_id" + where + " ORDER BY r.batch_id DESC, r.row_number", params)]
