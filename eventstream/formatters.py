"""Formatter implementations used by eventstream."""

from __future__ import annotations

from typing import Mapping
import copy
import logging


class KernelColorFormatter(logging.Formatter):
    """Color only the rendered level name for console output."""

    RESET = "\033[0m"

    def __init__(
        self,
        fmt: str,
        datefmt: str | None = None,
        colors: Mapping[str, str] | None = None,
        use_colors: bool = True,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self._colors = dict(colors or {})
        self._use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        if not self._use_colors:
            return super().format(record)

        color = self._colors.get(record.levelname)
        if not color:
            return super().format(record)

        rendered = copy.copy(record)
        rendered.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(rendered)
