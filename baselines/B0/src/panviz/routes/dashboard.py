"""Dashboard: every metric comes from persisted accepted/rejected rows."""
from collections import Counter
from flask import Blueprint, render_template
from ..db import get_db
from ..services.consolidation_service import active_filters, accepted_records, consolidate, filter_options
from ..services.export_service import reconcile

bp = Blueprint("dashboard", __name__)

@bp.get("/")
def index():
    db = get_db()
    db.execute("BEGIN")  # Consistent read snapshot across metrics and groups.
    filters = active_filters()
    records = accepted_records(db, filters)
    groups = consolidate(db, filters)
    total = reconcile(groups, len(records))
    districts = Counter(row["distrito"] for row in records)
    weeks = Counter(row["semana_iso"] for row in records)
    ages = Counter(row["grupo_etario"] for row in records)
    charts = {"weeks": dict(sorted(weeks.items())), "districts": dict(sorted(districts.items())), "ages": dict(sorted(ages.items()))}
    latest = db.execute("SELECT * FROM batches ORDER BY id DESC LIMIT 1").fetchone()
    return render_template("dashboard.html", title="Dashboard", subtitle="Una visión clara de la vigilancia respiratoria", filters=filters, options=filter_options(db), records=records, total=total, districts=districts, establishments=len({r["establecimiento"] for r in records}), weeks=len(weeks), charts=charts, latest=latest)
