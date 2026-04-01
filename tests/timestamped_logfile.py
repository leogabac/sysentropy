"""Example script for creating a timestamped logfile path."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eventstream import get_logger, timestamp


def main() -> None:
    # This example highlights the timestamp helper.
    # Expected result: each run writes to a new logfile with the project's
    # standard YYYYMMDD_HHMMSS timestamp format in the filename.
    log_path = Path(__file__).resolve().parent / "output" / f"example-{timestamp()}.log"

    logger = get_logger(
        "eventstream.example.timestamped",
        log_file=log_path,
        level=logging.INFO,
    )
    logger.info("timestamped logfile created")

    print(f"Created logfile: {log_path}")


if __name__ == "__main__":
    main()
