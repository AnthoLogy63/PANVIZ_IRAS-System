"""R01-R02: parse, preview and persist imports in the caller's transaction."""
import csv
import io
import json
import unicodedata
from datetime import date
from .validation_service import FIELDS, validate_record

class CsvError(ValueError):
    """A user-correctable CSV contract violation."""

def normalize_header(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.strip().lower()) if not unicodedata.combining(c))

def analyze_csv(payload, existing_ids=(), max_rows=10000):
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise CsvError("El archivo debe estar codificado en UTF-8.") from error
    if not text.strip() or "\x00" in text:
        raise CsvError("El archivo está vacío o contiene bytes nulos.")
    # The delimiter is defined by the header, not by values in subsequent rows.
    header = text.splitlines()[0]
    delimiter = ";" if header.count(";") > header.count(",") else ","
    try:
        reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True)
        headers = [normalize_header(x) for x in next(reader)]
        if len(set(headers)) != len(headers) or set(headers) != set(FIELDS):
            raise CsvError("Columnas requeridas (sin columnas adicionales): " + ", ".join(FIELDS))
        accepted, rejected = [], []
        seen = {str(x).casefold() for x in existing_ids}
        for values in reader:
            line = reader.line_num  # Physical ending line; multiline quoted records supported.
            if not values or all(not value.strip() for value in values):
                continue
            if len(accepted) + len(rejected) >= max_rows:
                raise CsvError(f"Máximo {max_rows} registros por archivo.")
            row = {name: (values[index].strip() if index < len(values) else "") for index, name in enumerate(headers)}
            reasons = validate_record(row, seen)
            if len(values) != len(headers):
                reasons.append("Número de columnas distinto al encabezado")
            if reasons:
                rejected.append({"fila": line, "id": row["id"], "motivo": "; ".join(reasons), "datos": row})
            else:
                iso_year, iso_week, _ = date.fromisoformat(row["fecha_notificacion"]).isocalendar()
                row["semana_iso"] = f"{iso_year}-W{iso_week:02d}"
                accepted.append(row)
                seen.add(row["id"].casefold())
    except (csv.Error, StopIteration) as error:
        raise CsvError("CSV mal formado: revisa comillas y delimitadores.") from error
    if not accepted and not rejected:
        raise CsvError("El CSV contiene encabezados, pero no contiene registros.")
    return {"accepted": accepted, "rejected": rejected, "total": len(accepted) + len(rejected)}

def analyze_existing(db, payload, max_rows=10000):
    ids = [row[0] for row in db.execute("SELECT id FROM notifications")]
    return analyze_csv(payload, ids, max_rows)

def process_import(db, payload, filename, source="upload", max_rows=10000):
    result = analyze_existing(db, payload, max_rows)
    cursor = db.execute("INSERT INTO batches(filename,accepted,rejected,source) VALUES (?,?,?,?)", (filename, len(result["accepted"]), len(result["rejected"]), source))
    batch_id = cursor.lastrowid
    db.executemany("INSERT INTO notifications(id,fecha_notificacion,establecimiento,distrito,grupo_etario,evento,semana_iso,batch_id) VALUES (?,?,?,?,?,?,?,?)", [tuple(row[key] for key in FIELDS) + (row["semana_iso"], batch_id) for row in result["accepted"]])
    db.executemany("INSERT INTO rejections(batch_id,row_number,notification_id,reason,raw_json,distrito) VALUES (?,?,?,?,?,?)", [(batch_id, row["fila"], row["id"], row["motivo"], json.dumps(row["datos"], ensure_ascii=False), row["datos"]["distrito"]) for row in result["rejected"]])
    return {**result, "batch_id": batch_id}
