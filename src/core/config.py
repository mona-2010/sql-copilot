from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

import os


@dataclass(frozen=True)
class Settings:
    ollama_model: str
    database_url: str
    max_rows: int
    debug: bool


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        ollama_model=os.getenv("OLLAMA_MODEL", "codellama"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///database/sales.db"),
        max_rows=int(os.getenv("MAX_ROWS", "100")),
        debug=os.getenv("DEBUG", "False").lower() in {"1", "true", "yes", "y"},
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

