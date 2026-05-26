from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.core.prompts import PROMPT_TEMPLATE


_FENCE_RE = re.compile(r"^\s*```(?:sql)?\s*|\s*```\s*$", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class SqlGenerationResult:
    sql: str


def _clean_llm_sql(text: str) -> str:
    cleaned = _FENCE_RE.sub("", text).strip()
    cleaned = cleaned.strip().strip(";").strip()
    return cleaned + ";"


def clean_llm_sql(text: str) -> str:
    return _clean_llm_sql(text)


def generate_sql(*, llm, schema: str, question: str) -> SqlGenerationResult:
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    raw = chain.invoke({"schema": schema, "question": question})
    return SqlGenerationResult(sql=_clean_llm_sql(raw))

