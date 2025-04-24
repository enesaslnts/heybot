import json
from pathlib import Path

CONTEXT_FILE = Path("context.json")

default_context = {
    "style": "neutral",
    "mode": "default",
    "language": "de"
}

def load_context():
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_context.copy()

def save_context(style, mode, language):
    data = {
        "style": style,
        "mode": mode,
        "language": language
    }
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data
