"""Direct-run script to exercise handler reuse and reconfiguration."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eventstream import LoggerConfig, get_logger


def main() -> None:
    # This script highlights two behaviors:
    # 1. a logger can be reconfigured to write to a different file
    # 2. repeated setup should not duplicate stdout handlers
    output_dir = Path(__file__).resolve().parent / "output"
    first_path = output_dir / "reconfigure-first.log"
    second_path = output_dir / "reconfigure-second.log"

    logger = get_logger(
        "eventstream.reconfigure-demo",
        log_file=first_path,
        level=logging.INFO,
    )
    logger.info("first file target")

    config = LoggerConfig(
        level=logging.DEBUG,
        log_file=second_path,
        console_format="%(asctime)s %(name)s %(levelname_fixed)s : %(message)s",
        file_format="%(asctime)s %(name)s %(levelname_fixed)s : %(message)s",
    )
    logger = get_logger(
        "eventstream.reconfigure-demo",
        level=logging.DEBUG,
        config=config,
    )

    # Expected result: later messages land in the second file, and each stdout
    # message appears once even if this logger name is configured again.
    logger.debug("second file target after reconfigure")
    logger.info("same logger should not duplicate handlers")

    print(f"First log file:  {first_path}")
    print(f"Second log file: {second_path}")
    print("Re-run this script a few times and verify stdout lines do not duplicate.")


if __name__ == "__main__":
    main()
