import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "backend"))

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Configure it in Vercel environment variables."
    )

from app import app

handler = app
