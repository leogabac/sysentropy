"""General utility helpers for sysentropy."""

from __future__ import annotations

from contextlib import contextmanager
from contextlib import ContextDecorator
from datetime import datetime
from functools import wraps
import logging
import traceback
from time import perf_counter
from types import TracebackType
from typing import Any, Callable, Iterator, TypeVar, overload

F = TypeVar("F", bound=Callable[..., Any])


def timestamp() -> str:
    """Return the project's standard filesystem-friendly timestamp string."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


@overload
def timing(func: F, /) -> F:
    ...


@overload
def timing(
    func: None = None,
    /,
    *,
    label: str | None = None,
    logger: logging.Logger | None = None,
    level: int = logging.INFO,
) -> Callable[[F], F]:
    ...


def timing(
    func: F | None = None,
    /,
    *,
    label: str | None = None,
    logger: logging.Logger | None = None,
    level: int = logging.INFO,
) -> F | Callable[[F], F]:
    """Log how long a function call took.

    Can be used as ``@timing`` or ``@timing(label="...")``.
    """

    def decorator(target: F) -> F:
        @wraps(target)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            try:
                return target(*args, **kwargs)
            finally:
                elapsed = perf_counter() - start
                message = f"{label or target.__name__} completed in {elapsed:.6f}s"
                _emit_timing_message(logger, level, message)

        return wrapped  # type: ignore[return-value]

    if func is not None:
        return decorator(func)

    return decorator


@contextmanager
def time_block(
    label: str,
    *,
    logger: logging.Logger | None = None,
    level: int = logging.INFO,
) -> Iterator[None]:
    """Log how long a block of code took."""

    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        # Keep the message format aligned with ``timing()`` for predictable logs.
        _emit_log_message(logger, level, f"{label} completed in {elapsed:.6f}s")


@overload
def log_exceptions(func: F, /) -> F:
    ...


@overload
def log_exceptions(
    func: None = None,
    /,
    *,
    message: str | None = None,
    logger: logging.Logger | None = None,
    level: int = logging.ERROR,
) -> Callable[[F], F] | ContextDecorator:
    ...


def log_exceptions(
    func: F | None = None,
    /,
    *,
    message: str | None = None,
    logger: logging.Logger | None = None,
    level: int = logging.ERROR,
) -> F | Callable[[F], F] | ContextDecorator:
    """Log an exception with traceback, then re-raise it.

    Can be used as ``@log_exceptions`` or ``with log_exceptions(...):``.
    """

    if func is not None:
        wrapped_message = message or f"{func.__name__} raised an exception"
        return _LoggedExceptions(
            logger=logger,
            level=level,
            message=wrapped_message,
            infer_message_from_func=False,
        )(func)

    return _LoggedExceptions(
        logger=logger,
        level=level,
        message=message or "An exception was raised",
        infer_message_from_func=message is None,
    )


class _LoggedExceptions(ContextDecorator):
    """ContextDecorator lets one implementation power both APIs."""

    def __init__(
        self,
        *,
        logger: logging.Logger | None,
        level: int,
        message: str,
        infer_message_from_func: bool,
    ) -> None:
        self._logger = logger
        self._level = level
        self._message = message
        self._infer_message_from_func = infer_message_from_func

    def __enter__(self) -> "_LoggedExceptions":
        return self

    def __call__(self, func: F) -> F:
        if not self._infer_message_from_func:
            return super().__call__(func)

        # Decorator usage gets a more helpful default than the generic block message.
        return _LoggedExceptions(
            logger=self._logger,
            level=self._level,
            message=f"{func.__name__} raised an exception",
            infer_message_from_func=False,
        )(func)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None or exc is None or exc_tb is None:
            return False

        _emit_exception_message(
            logger=self._logger,
            level=self._level,
            message=self._message,
            exc_info=(exc_type, exc, exc_tb),
        )
        return False


def _emit_log_message(
    logger: logging.Logger | None,
    level: int,
    message: str,
) -> None:
    """Prefer logging, but still emit text when nothing is configured."""

    target = logger or logging.getLogger()
    if target.hasHandlers():
        target.log(level, message)
        return

    print(message)


def _emit_timing_message(
    logger: logging.Logger | None,
    level: int,
    message: str,
) -> None:
    _emit_log_message(logger, level, message)


def _emit_exception_message(
    logger: logging.Logger | None,
    level: int,
    message: str,
    exc_info: tuple[type[BaseException], BaseException, TracebackType],
) -> None:
    target = logger or logging.getLogger()
    if target.hasHandlers():
        target.log(level, message, exc_info=exc_info)
        return

    print(message)
    traceback.print_exception(*exc_info)
