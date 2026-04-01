"""General utility helpers for eventstream."""

from __future__ import annotations

from datetime import datetime


def timestamp() -> str:
    """Return the project's standard filesystem-friendly timestamp string."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")
