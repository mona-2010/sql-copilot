from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import streamlit as st


def render_sidebar(*, db_url: str, model: str, tables: List[str], history_count: int) -> None:
    st.sidebar.header("SQL Copilot")
    st.sidebar.caption("Local NL→SQL using Ollama + LangChain")
    st.sidebar.divider()
    st.sidebar.write("**Database**")
    st.sidebar.code(db_url, language="text")
    st.sidebar.write("**Model**")
    st.sidebar.code(model, language="text")
    st.sidebar.write("**Tables**")
    st.sidebar.write(", ".join(tables) if tables else "(none)")
    st.sidebar.write("**History**")
    st.sidebar.write(f"{history_count} saved queries")


def render_sql(sql: str) -> None:
    st.subheader("Generated SQL")
    st.code(sql, language="sql")


def render_results(df: pd.DataFrame, *, seconds: float) -> None:
    st.subheader("Result")
    st.caption(f"{len(df.index)} row(s) • {seconds:.3f}s")
    st.dataframe(df, use_container_width=True, hide_index=True)

