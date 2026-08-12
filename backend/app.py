"""
Data AI Agent - FastAPI application.

Serves the chat frontend, streams chat completions over SSE and
exposes endpoints for schema discovery, raw SQL execution, database
listing and query history/favorites.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import stream_chat
from config import DATABASES, database_names
from database_tools import execute_query, get_schema
from history_store import (
    add_entry,
    delete_entry,
    list_entries,
    set_favorite,
)

BACKEND_DIR = Path(__file__).parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

app = FastAPI(title="Data AI Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# Request models
# ------------------------------------------------------------------

class ChatRequest(BaseModel):
    messages: list
    database: str = "grocery"


class QueryRequest(BaseModel):
    sql: str
    database: str = "grocery"


class HistoryRequest(BaseModel):
    question: str
    sql: str = ""
    database: str = "grocery"


# ------------------------------------------------------------------
# Chat
# ------------------------------------------------------------------

@app.post("/api/chat")
def chat(request: ChatRequest):
    """Run the agent and return the full event stream as a single JSON response."""
    if not request.messages or not any(
        (m or {}).get("content") for m in request.messages
    ):
        return {"error": "No message provided."}

    database = (
        request.database
        if request.database in database_names()
        else "grocery"
    )

    events = list(stream_chat(request.messages, database=database))
    return {"events": events}


# ------------------------------------------------------------------
# Databases & schema
# ------------------------------------------------------------------

@app.get("/api/databases")
def databases():
    """List databases the agent can connect to."""
    return [
        {"name": name, "description": info["description"]}
        for name, info in DATABASES.items()
    ]


@app.get("/api/schema")
def schema(database: str = "grocery"):
    """JSON schema representation of a database."""
    return get_schema(database)


@app.post("/api/query")
def query(request: QueryRequest):
    """Run a raw SQL SELECT (used by 'run this query' in the UI)."""
    return execute_query(request.sql, request.database)


# ------------------------------------------------------------------
# History & favorites
# ------------------------------------------------------------------

@app.get("/api/history")
def history(favorites_only: bool = False, database: str = None):
    return list_entries(favorites_only=favorites_only, database=database)


@app.post("/api/history")
def save_history(request: HistoryRequest):
    return add_entry(
        question=request.question,
        sql=request.sql,
        database=request.database,
    )


@app.patch("/api/history/{entry_id}")
def favorite_history(entry_id: str, favorite: bool = True):
    entry = set_favorite(entry_id, favorite)
    if entry is None:
        return {"error": "Entry not found."}, 404
    return entry


@app.delete("/api/history/{entry_id}")
def remove_history(entry_id: str):
    if not delete_entry(entry_id):
        return {"error": "Entry not found."}, 404
    return {"deleted": True}


# ------------------------------------------------------------------
# Frontend
# ------------------------------------------------------------------

@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)