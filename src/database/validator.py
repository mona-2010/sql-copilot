from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Set

from src.database.schema import SchemaInfo


_UNSAFE_KEYWORDS = re.compile(
    r"\b(DELETE|DROP|UPDATE|ALTER|TRUNCATE|INSERT|REPLACE|VACUUM|ATTACH|DETACH|PRAGMA\s+writable_schema)\b",
    re.IGNORECASE,
)
_SAFE_START = re.compile(r"^\s*(SELECT|WITH|SHOW|DESCRIBE|PRAGMA|EXPLAIN)\b", re.IGNORECASE)
_MULTI_STMT = re.compile(r";\s*\S")
_LIMIT = re.compile(r"\blimit\b", re.IGNORECASE)
_FROM_JOIN = re.compile(r"\b(from|join)\s+([`\"\\[]?)([a-zA-Z_][\w]*)\2", re.IGNORECASE)


@dataclass(frozen=True)
class SqlValidationResult:
    ok: bool
    reason: str | None = None
    sql: str | None = None


def is_safe_query(query: str) -> bool:
    if not query or not query.strip():
        return False
    if _UNSAFE_KEYWORDS.search(query):
        return False
    if not _SAFE_START.search(query):
        return False
    if _MULTI_STMT.search(query.strip().rstrip(";")):
        return False
    return True


def ensure_limit(query: str, *, max_rows: int) -> str:
    stripped = query.strip().rstrip(";").strip()
    if _LIMIT.search(stripped):
        return stripped + ";"
    return f"{stripped}\nLIMIT {int(max_rows)};"


def extract_referenced_tables(query: str) -> Set[str]:
    return {m.group(3) for m in _FROM_JOIN.finditer(query)}


def validate_tables_exist(query: str, schema: SchemaInfo) -> SqlValidationResult:
    referenced = extract_referenced_tables(query)
    if not referenced:
        return SqlValidationResult(ok=True, sql=query)

    existing = set(schema.tables.keys())
    missing = sorted(t for t in referenced if t not in existing)
    if missing:
        return SqlValidationResult(ok=False, reason=f"Unknown table(s): {', '.join(missing)}")
    return SqlValidationResult(ok=True, sql=query)


def validate_sql(
    *,
    query: str,
    schema: SchemaInfo,
    max_rows: int,
) -> SqlValidationResult:
    if not is_safe_query(query):
        return SqlValidationResult(ok=False, reason="Unsafe query detected (read-only SELECT/WITH only).")
    limited = ensure_limit(query, max_rows=max_rows)
    table_check = validate_tables_exist(limited, schema)
    if not table_check.ok:
        return table_check
    return SqlValidationResult(ok=True, sql=limited)

