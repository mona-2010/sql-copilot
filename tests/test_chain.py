from __future__ import annotations

from src.chains.sql_chain import clean_llm_sql


def test_clean_llm_sql_strips_fences_and_adds_semicolon() -> None:
    text = "```sql\nSELECT 1\n```"
    assert clean_llm_sql(text) == "SELECT 1;"

