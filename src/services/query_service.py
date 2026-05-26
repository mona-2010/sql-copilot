from __future__ import annotations

import time
from dataclasses import dataclass

import pandas as pd
from sqlalchemy import text


@dataclass(frozen=True)
class QueryExecutionResult:
    dataframe: pd.DataFrame
    seconds: float
    row_count: int


def preflight_sql(engine, sql: str) -> None:
    with engine.connect() as conn:
        conn.execute(text(f"EXPLAIN QUERY PLAN {sql.rstrip(';')}"))


def execute_sql(engine, sql: str) -> QueryExecutionResult:
    started = time.perf_counter()
    df = pd.read_sql_query(sql, engine)
    elapsed = time.perf_counter() - started
    return QueryExecutionResult(dataframe=df, seconds=elapsed, row_count=len(df.index))

