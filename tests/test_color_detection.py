"""Direct-run script to inspect automatic color enablement."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import io
import logging
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sysentropy import get_logger


class FakeStdout(io.StringIO):
    """Tiny stream stub so the script can force TTY and non-TTY cases."""

    def __init__(self, *, is_tty: bool) -> None:
        super().__init__()
        self._is_tty = is_tty

    def isatty(self) -> bool:
        return self._is_tty


@contextmanager
def patched_stdout(stream: FakeStdout):
    original = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = original


def run_case(name: str, *, is_tty: bool, no_color: bool) -> str:
    stream = FakeStdout(is_tty=is_tty)
    original_no_color = os.environ.get("NO_COLOR")

    if no_color:
        os.environ["NO_COLOR"] = "1"
    elif original_no_color is not None:
        del os.environ["NO_COLOR"]

    try:
        with patched_stdout(stream):
            # Unique logger names avoid handler reuse between cases.
            logger = get_logger(f"sysentropy.color-demo.{name}", level=logging.INFO)
            logger.info("color check")
        return stream.getvalue()
    finally:
        if original_no_color is None:
            os.environ.pop("NO_COLOR", None)
        else:
            os.environ["NO_COLOR"] = original_no_color


def main() -> None:
    tty_output = run_case("tty", is_tty=True, no_color=False)
    no_tty_output = run_case("notty", is_tty=False, no_color=False)
    no_color_output = run_case("no-color", is_tty=True, no_color=True)

    print("TTY contains ANSI:", "\033[" in tty_output)
    print("Non-TTY contains ANSI:", "\033[" in no_tty_output)
    print("NO_COLOR contains ANSI:", "\033[" in no_color_output)


if __name__ == "__main__":
    main()
