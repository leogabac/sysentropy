"""Public package interface for eventstream."""

from .config import LoggerConfig
from .core import configure_logger, get_logger
from .formatters import KernelColorFormatter
from .utils import timestamp

__all__ = [
    "KernelColorFormatter",
    "LoggerConfig",
    "configure_logger",
    "get_logger",
    "timestamp",
]
