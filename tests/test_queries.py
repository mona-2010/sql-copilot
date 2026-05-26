from __future__ import annotations

from pathlib import Path
import tempfile

from src.database.connection import create_sqlalchemy_engine
from src.database.schema import load_schema_info
from src.database.validator import validate_sql
from src.services.query_service import execute_sql, preflight_sql


def test_execute_safe_query_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        db_dir = root / "database"
        db_dir.mkdir(parents=True, exist_ok=True)
        db_path = db_dir / "sales.db"

        from database.init_db import init_db

        init_db(db_path)

        engine = create_sqlalchemy_engine(f"sqlite:///{db_path.as_posix()}")
        schema = load_schema_info(engine)
        validated = validate_sql(query="SELECT * FROM customers", schema=schema, max_rows=100)
        assert validated.ok and validated.sql

        preflight_sql(engine, validated.sql)
        result = execute_sql(engine, validated.sql)
        assert result.row_count >= 1

