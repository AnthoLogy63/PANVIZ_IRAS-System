"""R04: reconciled CSV serialization with spreadsheet formula protection."""
import csv
import io
from flask import Response

CONSOLIDATED_FIELDS = ("semana_iso", "establecimiento", "distrito", "grupo_etario", "total")

def safe_cell(value):
    text = str(value) if value is not None else ""
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text

def csv_response(rows, fields, filename):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: safe_cell(row.get(key, "")) for key in fields})
    return Response("\ufeff" + output.getvalue(), content_type="text/csv; charset=utf-8", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

def reconcile(groups, accepted_count):
    total = sum(row["total"] for row in groups)
    if total != accepted_count:
        raise ValueError("La reconciliación falló: el consolidado no coincide con los aceptados.")
    return total
