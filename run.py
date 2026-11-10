"""Local entry point: python run.py. No external database server needed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from panviz import create_app

app = create_app({"DISTRICT_FILTER_ENABLED": "--baseline" not in sys.argv})
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
