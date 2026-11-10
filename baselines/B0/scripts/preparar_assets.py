"""Run manually once to vendor pinned browser dependencies. No Node/npm needed."""
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "chart.umd.js": "https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.js",
    "tailwind.min.css": "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
    "Chart.LICENSE.md": "https://cdn.jsdelivr.net/npm/chart.js@4.4.8/LICENSE.md",
    "Tailwind.LICENSE.txt": "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/LICENSE",
}

def main():
    folder = ROOT / "src" / "panviz" / "static" / "vendor"
    folder.mkdir(parents=True, exist_ok=True)
    for filename, url in ASSETS.items():
        destination = folder / filename
        if destination.exists() and destination.stat().st_size:
            print(f"Ya existe: {filename}")
            continue
        print(f"Descargando {filename}...")
        with urlopen(url, timeout=60) as response:
            data = response.read()
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_bytes(data)
        temporary.replace(destination)
    print("Assets preparados. La aplicación puede usarse sin conexión.")

if __name__ == "__main__":
    main()
