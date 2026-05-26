from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List

from sqlalchemy import inspect


@dataclass(frozen=True)
class SchemaInfo:
    tables: Dict[str, List[str]]


@lru_cache(maxsize=8)
def load_schema_info(engine) -> SchemaInfo:
    inspector = inspect(engine)
    tables: Dict[str, List[str]] = {}
    for table_name in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns(table_name)]
        tables[table_name] = columns
    return SchemaInfo(tables=tables)


def format_schema_for_prompt(schema: SchemaInfo) -> str:
    lines: List[str] = []
    for table_name in sorted(schema.tables.keys()):
        cols = ", ".join(schema.tables[table_name])
        lines.append(f"- {table_name}({cols})")
    return "\n".join(lines)

