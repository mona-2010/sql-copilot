from __future__ import annotations

from src.database.schema import SchemaInfo
from src.database.validator import ensure_limit, is_safe_query, validate_sql


def test_is_safe_query_blocks_destructive() -> None:
    assert not is_safe_query("DROP TABLE users;")
    assert not is_safe_query("DELETE FROM users;")
    assert not is_safe_query("UPDATE users SET a=1;")
    assert not is_safe_query("INSERT INTO users(a) VALUES(1);")


def test_is_safe_query_allows_select_with() -> None:
    assert is_safe_query("SELECT 1;")
    assert is_safe_query("WITH t AS (SELECT 1) SELECT * FROM t;")


def test_ensure_limit_adds_limit_when_missing() -> None:
    out = ensure_limit("SELECT * FROM customers", max_rows=100)
    assert "LIMIT 100" in out.upper()


def test_validate_sql_checks_table_exists() -> None:
    schema = SchemaInfo(tables={"customers": ["customer_id"]})
    ok = validate_sql(query="SELECT * FROM customers", schema=schema, max_rows=100)
    assert ok.ok
    bad = validate_sql(query="SELECT * FROM missing_table", schema=schema, max_rows=100)
    assert not bad.ok

