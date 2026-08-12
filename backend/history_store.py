"""
Query history and favorites store.

Persistence is a simple JSON file so no extra infrastructure is
needed; every mutation is written through immediately.
"""
import json
import os
import time
import uuid

HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "data", "history.json"
)


def _load():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def _save(entries):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
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