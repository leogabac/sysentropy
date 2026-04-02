"""Direct-run script to inspect timing decorator output."""

from __future__ import annotations

from pathlib import Path
import logging
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger, timing


logger = get_logger("sysentropy.timing-demo", level=logging.INFO)


@timing(logger=logger, label="short task")
def short_task() -> None:
    time.sleep(0.01)


@timing(label="default logger task")
def default_logger_task() -> None:
    time.sleep(0.01)


def main() -> None:
    # Expected result: stdout includes a logger-backed line and a plain fallback line.
    short_task()
    default_logger_task()


if __name__ == "__main__":
    main()
