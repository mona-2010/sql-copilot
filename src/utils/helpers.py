from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator


@dataclass
class TimedBlockResult:
    seconds: float


@contextmanager
def timed_block() -> Iterator[TimedBlockResult]:
    started = time.perf_counter()
    result = TimedBlockResult(seconds=0.0)
    try:
        yield result
    finally:
        result.seconds = time.perf_counter() - started
