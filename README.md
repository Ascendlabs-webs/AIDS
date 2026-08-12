# 🛒 Data AI Agent — Conversational Database Analyst

A hackathon project: an LLM-powered agent that lets non-technical users ask
questions in plain English, query a SQLite database, and see the answers with
interactive charts, diagrams and tables — all inside a ChatGPT-style chat.

![stack](https://img.shields.io/badge/backend-FastAPI%20%2B%20Gemini-7c6cf0)
![stack](https://img.shields.io/badge/frontend-Vanilla%20JS%20(no%20build)-7c6cf0)

---

## ✨ Features

| Area | What you get |
|---|---|
| **Chat interface** | ChatGPT-style UI with **streaming** responses, markdown, session history (persisted in the browser) and suggested prompts |
| **Schema discovery** | `get_schema` tool — tables, columns, types, primary/foreign keys, row counts |
| **SQL execution** | `execute_query` tool — read-only SELECTs with safe error handling |
| **Charts** | Interactive Plotly **bar / line / pie / scatter** charts rendered inline |
| **Diagrams** | Mermaid **ER diagrams, flowcharts, graphs and mindmaps** rendered inline |
| **Explanations** | `explain_data` tool + conversational insights with real numbers |
| **SQL transparency** | The generated SQL is shown in a card with **Copy** and **Run** buttons |
| **Multi-database** | Registry in `backend/config.py` — add SQLite files and the agent can talk to them (selector in the UI) |
| **History & favorites** | Questions + SQL saved server-side; star favorites; click to re-ask |
| **Pinned dashboard** | Pin any chart to a dashboard panel that survives reloads |
| **Graceful fallbacks** | Query retry logic, friendly error events, unknown-tool handling |

## 🚀 Quick start

**Windows** — double-click `run.bat` (or right-click → Run).

**macOS / Linux** — open Terminal in the project folder and run `./run.sh`.

The launcher does everything for you: creates the virtual environment,
installs dependencies and starts the server. On the very first run it will
ask for your Gemini API key (free at https://aistudio.google.com/apikey),
then run it once more and you're done.

Manual setup (equivalent):

```bash
cd backend
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# create .env with your key
copy .env.example .env      # then edit GEMINI_API_KEY=...

uvicorn app:app --reload --port 8000
```

Open http://localhost:8000 and try:

1. *"Top 5 products by revenue, show a bar chart"*
2. *"Now show the revenue trend over time"*
3. *"Draw me the ER diagram for this database"*
4. *"Create a flowchart showing how orders flow through our system"*

## 🏗️ Architecture

```
frontend/            pure HTML/CSS/JS chat app (no build step)
├── index.html       layout + CDN libs (marked, Plotly, Mermaid)
├── style.css        dark ChatGPT-like theme
└── app.js           SSE client, artifact renderers, history, dashboard

backend/             FastAPI + Gemini agent
├── app.py           HTTP layer: /api/chat (SSE), schema, query, history
├── agent.py         streaming agent loop (function calling, SSE events)
├── tool_registry.py the 5 agent tools + explicit JSON function schemas
├── database_tools.py  get_schema / execute_query / generate_chart
├── diagram_tools.py   generate_diagram (Mermaid, keyword normalization)
├── explanation_tools.py statistical summaries
├── config.py        env config + multi-database registry
├── history_store.py JSON-file-backed query history & favorites
└── tests/           21 pytest unit tests

database/             sample SQLite e-commerce dataset
```

**Agent flow**

```
user message ─▶ Gemini (streaming) ─▶ function call ─▶ tool executes
      ▲                                                    │
      └────────── result fed back to model ◀───────────────┘
```

Events streamed over SSE: `delta` (text), `sql` (transparency), `tool` /
`tool_result` (incl. `chart`, `diagram`, `columns`+`rows`), `done`, `error`.

## 🧰 Agent tools

| Tool | Purpose | Arguments | Output |
|---|---|---|---|
| `get_schema` | Discover tables/columns/keys | `database` | JSON schema |
| `execute_query` | Run read-only SQL | `sql`, `database` | rows |
| `generate_chart` | Plotly bar/line/pie/scatter | `data_json`, `chart_type`, `x_column`, `y_column`, `title` | figure JSON |
| `generate_flowchart` | Mermaid ER/flow/graph/mindmap | `diagram_type`, `title`, `content` | mermaid code |
| `explain_data` | Stats: counts, min/max/avg, top values | `data_json` | summary JSON |

## 🧪 Tests

```bash
cd backend
venv\Scripts\python.exe -m pytest tests -q
```

## 🔑 Environment (`.env.example`)

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

## 📡 API summary

- `POST /api/chat` `{messages, database}` → SSE stream
- `GET /api/databases` · `GET /api/schema?database=`
- `POST /api/query` `{sql, database}`
- `GET|POST /api/history` · `PATCH /api/history/{id}?favorite=` · `DELETE /api/history/{id}`

## 💡 Extending

Add a database in `backend/config.py`:

```python
DATABASES = {
    "grocery": {...},
    "my_new_db": {
        "path": r"C:\path\to\file.db",
        "description": "What this database contains",
    },
}
```