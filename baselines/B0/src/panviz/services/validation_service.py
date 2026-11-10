"""R02: deterministic quality rules; no clinical interpretation."""
import re
from datetime import date

FIELDS = ("id", "fecha_notificacion", "establecimiento", "distrito", "grupo_etario", "evento")
AGE_GROUPS = ("0-4", "5-11", "12-17", "18-29", "30-59", "60+")

def validate_record(row, seen):
    errors = []
    for field in FIELDS:
        if not row.get(field, "").strip():
            errors.append(f"Campo obligatorio vacío: {field}")
        elif len(row[field]) > 120:
            errors.append(f"Longitud máxima de 120 caracteres: {field}")
        elif any(ord(char) < 32 for char in row[field]):
            errors.append(f"Caracteres de control no permitidos: {field}")
    notification_id = row.get("id", "")
    if notification_id:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", notification_id):
            errors.append("Formato de id inválido: use letras, números, guion o guion bajo (máx. 64)")
        if notification_id.casefold() in seen:
            errors.append("ID de notificación duplicado")
    value = row.get("fecha_notificacion", "")
    if value:
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
                raise ValueError()
            date.fromisoformat(value)
        except ValueError:
            errors.append("Fecha imposible o formato inválido: use AAAA-MM-DD")
    if row.get("grupo_etario") and row["grupo_etario"] not in AGE_GROUPS:
        errors.append("Grupo etario fuera del catálogo: " + ", ".join(AGE_GROUPS))
    if row.get("evento") and row["evento"] != "IRAS":
        errors.append("Evento inválido: únicamente IRAS")
    return errors
