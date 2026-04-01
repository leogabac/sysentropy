# eventstream

Opinionated Python logging for the recurring problem of:
"I just need a decent logger, why am I formatting timestamps by hand again?"

`eventstream` is a small Python library that writes plain logs to disk, colored logs to stdout, and gives you a reusable timestamp helper so you can stop retyping `strftime` formats you were never going to remember anyway.

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

## Features

- Linux-kernel-inspired level colors for console output
- separate stdout and file formatters
- simple `get_logger()` entrypoint
- optional directory creation for file logging
- handler reuse to avoid duplicate output
- a configuration object that leaves room for future expansion
- a `timestamp()` helper that returns `YYYYMMDD_HHMMSS`

## Install

```bash
pip install -e .
```

## Quick start

```python
from eventstream import get_logger, timestamp

logger = get_logger("demo", log_file=f"logs/demo-{timestamp()}.log")

logger.debug("debug message")
logger.info("service started")
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
from eventstream import timestamp

filename = f"run-{timestamp()}.log"
```

It returns values like:

```text
20260401_223735
```
