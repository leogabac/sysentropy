"""Direct-run script to inspect timed block output."""

from __future__ import annotations

from pathlib import Path
import logging
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger, time_block


def main() -> None:
    # This script shows block timing without requiring a separate helper function.
    logger = get_logger("sysentropy.time-block-demo", level=logging.INFO)

    with time_block("sleep block", logger=logger):
        time.sleep(0.01)

    # This fallback path should still print even if no logger was configured.
    with time_block("fallback block"):
        time.sleep(0.01)


if __name__ == "__main__":
    main()
