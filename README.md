# sysentropy

Opinionated Python logging for the recurring problem of:
"I just need a decent logger, why am I formatting timestamps by hand again?"

`sysentropy` is a small Python library that writes plain logs to disk, colored logs to stdout, and gives you reusable timestamp, timing, and exception helpers so you can stop rebuilding the same logging glue in every project.

## How This Repo Happened

This repo exists because writing the same logging setup in every project gets old fast.

One day it is:
- "I'll just do a tiny logger wrapper."
- then "I want colors."
- then "I want a logfile too."
- then "why is this handler duplicated?"
- then "what was that timestamp format again?"

At that point the only rational response was obviously to make a library about it.

So this is the result: a lightweight package extracted from that exact cycle of mild annoyance, repeated enough times to become a design requirement. Very noble. Very serious. Entirely unnecessary until it suddenly isn't.

## What It Does

- plain logs on disk
- colored logs on stdout
- a small API built on top of the standard `logging` module
- a reusable timestamp helper for logfile names and other boring-but-common cases
- a timing decorator for quick execution-time logging
- lightweight helpers for timed blocks and exception logging

## Features

- Linux-kernel-inspired level colors for console output
- separate stdout and file formatters
- simple `get_logger()` entrypoint
- optional directory creation for file logging
- handler reuse to avoid duplicate output
- a configuration object that leaves room for future expansion
- a `timestamp()` helper that returns `YYYYMMDD_HHMMSS`
- a `timing()` decorator that logs function runtime
- a `time_block()` context manager for inline timing
- a `log_exceptions()` helper that logs tracebacks before re-raising
- automatic color detection for TTY vs redirected output

## Install

```bash
pip install sysentropy
```

## Quick start

```python
from sysentropy import get_logger, log_exceptions, time_block, timestamp, timing

logger = get_logger("demo", log_file=f"logs/demo-{timestamp()}.log")


@timing(logger=logger)
@log_exceptions(logger=logger)
def do_work() -> None:
    with time_block("startup", logger=logger):
        logger.info("service started")

logger.debug("debug message")
do_work()
logger.warning("disk usage high")
logger.error("request failed")
logger.critical("system halted")
```

Default output style:

```text
2026-04-01 22:00:00 INFO     : service started
2026-04-01 22:00:00 WARNING  : disk usage high
2026-04-01 22:00:00 ERROR    : request failed
```

## Timestamp Helper

If you only need the timestamp format, import it directly:

```python
from sysentropy import timestamp

filename = f"run-{timestamp()}.log"
```

It returns values like:

```text
20260401_223735
```

## Timing Helper

Use `timing()` as a decorator when you want a quick runtime measurement in your logs:

```python
from sysentropy import get_logger, timing

logger = get_logger("demo")


@timing(logger=logger, label="expensive task")
def expensive_task() -> None:
    ...
```

It logs lines like:

```text
2026-04-02 09:15:00 INFO     : expensive task completed in 0.012384s
```

## Timed Blocks

Use `time_block()` when you only want to time one section of a function:

```python
from sysentropy import get_logger, time_block

logger = get_logger("demo")

with time_block("database warmup", logger=logger):
    ...
```

## Exception Logging

Use `log_exceptions()` to log tracebacks before the exception keeps propagating:

```python
from sysentropy import get_logger, log_exceptions

logger = get_logger("demo")


@log_exceptions(logger=logger)
def run_job() -> None:
    raise RuntimeError("boom")
```
