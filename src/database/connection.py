from __future__ import annotations

from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase


def create_sqlalchemy_engine(database_url: str):
    if database_url.startswith("sqlite:///"):
        path = database_url[len("sqlite:///") :]
        if path.startswith("file:"):
            return create_engine(database_url)
        return create_engine(f"sqlite:///file:{path}?mode=ro&uri=true")
    return create_engine(database_url)


def get_sql_database(database_url: str) -> SQLDatabase:
    return SQLDatabase.from_uri(database_url)

