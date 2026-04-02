"""Direct-run script to inspect exception logging behavior."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger, log_exceptions


logger = get_logger("sysentropy.exception-demo", level=logging.ERROR)


@log_exceptions(logger=logger)
def decorated_failure() -> None:
    # The decorator path should log the traceback before this escapes.
    raise RuntimeError("decorated failure")


def main() -> None:
    try:
        decorated_failure()
    except RuntimeError:
        print("decorator re-raised as expected")

    try:
        # The context-manager path uses the same underlying implementation.
        with log_exceptions(logger=logger, message="context failure"):
            raise ValueError("context-managed failure")
    except ValueError:
        print("context manager re-raised as expected")


if __name__ == "__main__":
    main()
