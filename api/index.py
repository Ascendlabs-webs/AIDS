"""Vercel serverless entrypoint (ASGI).

Imports the FastAPI application from the backend package so the
@vercel/python runtime can serve it as a serverless function.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "backend"))

from app import app  # noqa: E402
