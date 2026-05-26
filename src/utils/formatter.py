from __future__ import annotations

import re


_WS = re.compile(r"[ \t]+")


def normalize_sql(sql: str) -> str:
    """
    Lightweight SQL normalization for display/logging (not a formatter).
    """
    sql = sql.strip()
    sql = _WS.sub(" ", sql)
    return sql

