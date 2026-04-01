# eventstream

Opinionated Python logging with dual output:

- plain logs on disk
- colored logs on stdout
- a small API built on top of the standard `logging` module

## Features

- Linux-kernel-inspired level colors for console output
- separate stdout and file formatters
- simple `get_logger()` entrypoint
- optional directory creation for file logging
- handler reuse to avoid duplicate output
- a configuration object that leaves room for future expansion

## Install

```bash
pip install -e .
```

## Quick start

```python
from eventstream import get_logger

logger = get_logger("demo", log_file="logs/demo.log")

logger.debug("debug message")
logger.info("service started")
logger.warning("disk usage high")
logger.error("request failed")
logger.critical("system halted")
```

## Development scripts

The `tests/` directory contains direct-run scripts you can execute manually:

```bash
python tests/test_stdout_colors.py
python tests/test_file_logging.py
python tests/test_reconfigure.py
```
