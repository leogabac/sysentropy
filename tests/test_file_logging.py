"""Direct-run script to verify disk output stays uncolored."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger


def main() -> None:
    # This script demonstrates dual-output behavior:
    # colored lines on stdout, plain text lines written to a log file on disk.
    log_path = Path("tests/output/file-demo.log")
    logger = get_logger(
        "sysentropy.file-demo",
        log_file=log_path,
        level=logging.DEBUG,
    )

    logger.debug("plain file debug")
    logger.info("plain file info")
    logger.warning("plain file warning")
    logger.error("plain file error")
    logger.critical("plain file critical")

    # Expected result: the file exists and contains readable log lines without ANSI escapes.
    print(f"Wrote log file to: {log_path}")
    print("Open it and confirm there are no ANSI color escape codes.")


if __name__ == "__main__":
    main()
