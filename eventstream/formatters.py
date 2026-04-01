"""Formatter implementations used by eventstream."""

from __future__ import annotations

from typing import Mapping
import copy
import logging


class EventStreamFormatter(logging.Formatter):
    """Render a fixed-width level label for aligned output."""

    def __init__(
        self,
        fmt: str,
        datefmt: str | None = None,
        level_width: int = 8,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self._level_width = level_width

    def format(self, record: logging.LogRecord) -> str:
        rendered = copy.copy(record)
        rendered.levelname_fixed = self._render_level_label(record)
        return super().format(rendered)

    def _render_level_label(self, record: logging.LogRecord) -> str:
        return record.levelname.ljust(self._level_width)


class KernelColorFormatter(EventStreamFormatter):
    """Color only the rendered level name for console output."""

    RESET = "\033[0m"

    def __init__(
        self,
        fmt: str,
        datefmt: str | None = None,
        level_width: int = 8,
        colors: Mapping[str, str] | None = None,
        use_colors: bool = True,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, level_width=level_width)
        self._colors = dict(colors or {})
        self._use_colors = use_colors

    def _render_level_label(self, record: logging.LogRecord) -> str:
        label = super()._render_level_label(record)
        if not self._use_colors:
            return label
        color = self._colors.get(record.levelname)
        if not color:
            return label
        return f"{color}{label}{self.RESET}"
