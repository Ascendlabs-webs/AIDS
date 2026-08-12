"""Vercel serverless entrypoint (ASGI).

Imports the FastAPI application from the backend package so the
@vercel/python runtime can serve it as a serverless function.
"""
import os
import sys
from fastapi import Request, JSONResponse

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "backend"))
    from app import app
    handler = app
except Exception as e:
    # Fallback app to show import error
    app = FastAPI()
    @app.get("/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        return JSONResponse(
            status_code=500,
            content={"detail": "Failed to initialize application: " + str(e)},
        )
    handler = app
