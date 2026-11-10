"""Extrae texto y estructura de la plantilla sin modificarla."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
source = ROOT / "TIF-PROYECTO.docx"
output = ROOT / "docs/estructura_plantilla_word.txt"
lines = []
with ZipFile(source) as package:
    for name in package.namelist():
        if name.startswith("word/") and name.endswith(".xml") and (name == "word/document.xml" or "header" in name or "footer" in name or "footnote" in name):
            lines.append("\nPARTE " + name)
            tree = ET.fromstring(package.read(name))
            for index, paragraph in enumerate(tree.findall(".//w:p", NS)):
                text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
                style = paragraph.find("w:pPr/w:pStyle", NS)
                role = style.get("{" + NS["w"] + "}val", "") if style is not None else ""
                if text.strip():
                    lines.append(f"[{index}] [{role}] {text}")
            for section in tree.findall(".//w:sectPr", NS):
                lines.append("SECCION " + ET.tostring(section, encoding="unicode"))
output.write_text("\n".join(lines), encoding="utf-8")
print("Plantilla analizada. Archivo creado:", output)
