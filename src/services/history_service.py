from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class HistoryItem:
    timestamp_utc: str
    question: str
    sql: str
    row_count: int
    seconds: float


class HistoryService:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _init(self) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                question TEXT NOT NULL,
                sql TEXT NOT NULL,
                row_count INTEGER NOT NULL,
                seconds REAL NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()

    def add(self, *, question: str, sql: str, row_count: int, seconds: float) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            "INSERT INTO query_history(timestamp_utc, question, sql, row_count, seconds) VALUES(?,?,?,?,?)",
            (
                datetime.now(timezone.utc).isoformat(),
                question,
                sql,
                int(row_count),
                float(seconds),
            ),
        )
        conn.commit()
        conn.close()

    def list_recent(self, *, limit: int = 50) -> List[HistoryItem]:
        conn = sqlite3.connect(self._db_path)
        cur = conn.execute(
            """
            SELECT timestamp_utc, question, sql, row_count, seconds
            FROM query_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),),
        )
        rows = cur.fetchall()
        conn.close()
        return [
            HistoryItem(
                timestamp_utc=r[0],
                question=r[1],
                sql=r[2],
                row_count=int(r[3]),
                seconds=float(r[4]),
            )
            for r in rows
        ]

