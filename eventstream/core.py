"""Core logger construction helpers for eventstream."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import logging
import sys

from .config import LoggerConfig
from .formatters import KernelColorFormatter


def configure_logger(logger: logging.Logger, config: LoggerConfig) -> logging.Logger:
    """Apply eventstream handler configuration to an existing logger."""

    logger.setLevel(config.level)

    stream_handler = _get_named_handler(logger, config.stream_handler_name)
    if stream_handler is None:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.set_name(config.stream_handler_name)
        logger.addHandler(stream_handler)

    stream_handler.setLevel(config.level)
    stream_handler.setFormatter(
        KernelColorFormatter(
            fmt=config.console_format,
            datefmt=config.date_format,
            colors=config.colors,
            use_colors=config.use_colors,
        )
    )

    file_handler = _get_named_handler(logger, config.file_handler_name)
    if config.log_file is not None:
        target = Path(config.log_file)
        if config.create_directories:
            target.parent.mkdir(parents=True, exist_ok=True)

        needs_replacement = False
        if isinstance(file_handler, logging.FileHandler):
            current = Path(file_handler.baseFilename)
            needs_replacement = current != target.resolve()
        elif file_handler is not None:
            needs_replacement = True

        if needs_replacement:
            logger.removeHandler(file_handler)
            file_handler.close()
            file_handler = None

        if file_handler is None:
            file_handler = logging.FileHandler(target, encoding="utf-8")
            file_handler.set_name(config.file_handler_name)
            logger.addHandler(file_handler)

        file_handler.setLevel(config.level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=config.file_format,
                datefmt=config.date_format,
            )
        )
    elif file_handler is not None:
        logger.removeHandler(file_handler)
        file_handler.close()

    logger.propagate = config.propagate
    return logger


def get_logger(
    name: str,
    log_file: str | Path | None = None,
    level: int | None = None,
    *,
    config: LoggerConfig | None = None,
) -> logging.Logger:
    """Create or reuse a named logger configured the eventstream way."""

    effective = replace(config) if config is not None else LoggerConfig()
    if level is not None:
        effective.level = level
    effective.log_file = log_file if log_file is not None else effective.log_file

    return configure_logger(logging.getLogger(name), effective)


def _get_named_handler(
    logger: logging.Logger,
    handler_name: str,
) -> logging.Handler | None:
    for handler in logger.handlers:
        if handler.get_name() == handler_name:
            return handler
    return None
