import hashlib
import json
from pathlib import Path

STATE_DIR = Path("state")
STATE_FILE = STATE_DIR / "page_hashes.json"

def load_state():
    STATE_DIR.mkdir(exist_ok=True)

    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def has_changed(url, html):
    state = load_state()
    new_hash = hashlib.sha256(html.encode()).hexdigest()

    if state.get(url) != new_hash:
        state[url] = new_hash
        save_state(state)
        return True

    return False
