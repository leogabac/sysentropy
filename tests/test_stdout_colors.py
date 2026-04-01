"""Direct-run script to inspect colored stdout logging."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger


def main() -> None:
    # This script highlights the console color palette for each log level.
    # Expected result: stdout shows one line per level with colored level names.
    logger = get_logger("sysentropy.stdout-demo", level=logging.DEBUG)

    logger.debug("debug output should be cyan")
    logger.info("info output should be green")
    logger.warning("warning output should be yellow")
    logger.error("error output should be red")
    logger.critical("critical output should have a red background")


if __name__ == "__main__":
    main()
