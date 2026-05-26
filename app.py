from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.chains.sql_chain import generate_sql
from src.core.config import load_settings, project_root
from src.database.connection import create_sqlalchemy_engine
from src.database.schema import format_schema_for_prompt, load_schema_info
from src.database.validator import validate_sql
from src.services.history_service import HistoryService
from src.services.llm_service import build_llm
from src.services.query_service import execute_sql, preflight_sql
from src.ui.components import render_results, render_sidebar, render_sql


def _ensure_sample_db_exists(db_path: Path) -> None:
    if db_path.exists():
        return
    from database.init_db import init_db

    init_db(db_path)


def main() -> None:
    settings = load_settings()
    st.set_page_config(page_title="SQL Copilot", layout="wide")

    root = project_root()
    db_path = root / "database" / "sales.db"
    _ensure_sample_db_exists(db_path)

    engine = create_sqlalchemy_engine(settings.database_url)
    schema_info = load_schema_info(engine)
    schema_text = format_schema_for_prompt(schema_info)

    history = HistoryService(root / "database" / "history.db")
    recent = history.list_recent(limit=50)

    llm = build_llm(model=settings.ollama_model, temperature=0.0)

    render_sidebar(
        db_url=settings.database_url,
        model=settings.ollama_model,
        tables=sorted(schema_info.tables.keys()),
        history_count=len(recent),
    )

    st.title("SQL Copilot")
    st.caption("Ask questions in plain English. The assistant generates safe, read-only SQL.")

    with st.expander("Schema (used by the model)", expanded=False):
        st.code(schema_text, language="text")

    question = st.chat_input("Ask a question about the database…")
    if not question:
        return

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating SQL with Ollama…"):
            gen = generate_sql(llm=llm, schema=schema_text, question=question)

        validation = validate_sql(query=gen.sql, schema=schema_info, max_rows=settings.max_rows)
        if not validation.ok or not validation.sql:
            st.error(validation.reason or "Query validation failed.")
            render_sql(gen.sql)
            return

        safe_sql = validation.sql
        render_sql(safe_sql)

        try:
            preflight_sql(engine, safe_sql)
        except Exception as exc:  # noqa: BLE001
            st.error(f"SQL preflight failed: {exc}")
            return

        with st.spinner("Executing query…"):
            result = execute_sql(engine, safe_sql)

        history.add(
            question=question,
            sql=safe_sql,
            row_count=result.row_count,
            seconds=result.seconds,
        )

        render_results(result.dataframe, seconds=result.seconds)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download CSV",
                data=result.dataframe.to_csv(index=False).encode("utf-8"),
                file_name="result.csv",
                mime="text/csv",
            )
        with col2:
            st.download_button(
                "Download JSON",
                data=result.dataframe.to_json(orient="records").encode("utf-8"),
                file_name="result.json",
                mime="application/json",
            )


if __name__ == "__main__":
    main()

