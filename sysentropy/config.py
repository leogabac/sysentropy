"""Configuration primitives for sysentropy."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping
import logging


DEFAULT_COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[30;41m",
}


@dataclass(slots=True)
class LoggerConfig:
    """Configuration for a logger instance and its handlers."""

    level: int = logging.INFO
    log_file: str | Path | None = None
    console_format: str = "%(asctime)s %(levelname_fixed)s : %(message)s"
    file_format: str = "%(asctime)s %(levelname_fixed)s : %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    level_width: int = 8
    use_colors: bool = True
    propagate: bool = False
    create_directories: bool = True
    stream_handler_name: str = "sysentropy.stdout"
    file_handler_name: str = "sysentropy.file"
    colors: Mapping[str, str] = field(default_factory=lambda: dict(DEFAULT_COLORS))
