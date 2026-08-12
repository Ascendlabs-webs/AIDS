"""
Query history and favorites store.

Persistence is a simple JSON file so no extra infrastructure is
needed; every mutation is written through immediately.
"""
import json
import os
import tempfile
import time
import uuid

_LOCAL_HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "data", "history.json"
)

# Serverless environments (e.g. Vercel) have a read-only bundle, so fall
# back to the writable temp directory when the local data dir is not writable.
HISTORY_FILE = _LOCAL_HISTORY_FILE


def _resolve_history_file():
    global HISTORY_FILE
    if HISTORY_FILE != _LOCAL_HISTORY_FILE:
        return HISTORY_FILE
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        probe = os.path.join(os.path.dirname(HISTORY_FILE), ".write-test")
        with open(probe, "w", encoding="utf-8"):
            pass
        os.remove(probe)
    except OSError:
        HISTORY_FILE = os.path.join(tempfile.gettempdir(), "daa_history.json")
    return HISTORY_FILE


def _load():
    history_file = _resolve_history_file()
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    if not os.path.exists(history_file):
        return []
    try:
        with open(history_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def _save(entries):
    history_file = _resolve_history_file()
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)


def add_entry(question, sql, database, favorite=False):
    """Record a question + generated SQL pair."""
    entry = {
        "id": str(uuid.uuid4()),
        "question": question,
        "sql": sql,
        "database": database,
        "favorite": favorite,
        "created_at": time.time(),
    }
    entries = _load()
    entries.append(entry)
    _save(entries)
    return entry


def list_entries(favorites_only=False, database=None):
    """List history entries, newest first."""
    entries = _load()
    if favorites_only:
        entries = [e for e in entries if e.get("favorite")]
    if database:
        entries = [e for e in entries if e.get("database") == database]
    return sorted(entries, key=lambda e: e.get("created_at", 0), reverse=True)


def set_favorite(entry_id, favorite):
    """Mark / unmark an entry as favourite. Returns None if not found."""
    entries = _load()
    for entry in entries:
        if entry["id"] == entry_id:
            entry["favorite"] = bool(favorite)
            _save(entries)
            return entry
    return None


def delete_entry(entry_id):
    """Remove an entry. Returns True if deleted."""
    entries = _load()
    remaining = [e for e in entries if e["id"] != entry_id]
    if len(remaining) == len(entries):
        return False
    _save(remaining)
    return True