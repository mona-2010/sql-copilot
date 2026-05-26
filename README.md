# SQL Copilot (Local AI SQL Assistant)

SQL Copilot is a production-ready, local-first AI SQL Assistant that converts natural language questions into **safe, read-only SQL**, executes them against a SQLite database, and displays results in a clean Streamlit UI.

Tech: Streamlit • LangChain • Ollama • SQLite • Pandas

## Features

- Natural language → SQL generation with schema awareness
- SQL safety layer (blocks destructive statements)
- Automatic `LIMIT 100` (configurable)
- Query history persisted locally
- Download results as CSV/JSON

## Quickstart

### 1) Prereqs

- Python 3.11+
- Ollama installed and running

### 2) Install deps

```bash
pip install -r requirements.txt
```

### 3) Start Ollama + pull a model

```bash
ollama serve
ollama pull codellama
```

### 4) Initialize the sample database

```bash
python database/init_db.py
```

If you prefer creating the DB manually:

```bash
sqlite3 database/sales.db < database/seed.sql
```

### 5) Run the app

```bash
streamlit run app.py
```

## Environment Variables

Copy `.env.example` → `.env` and adjust as needed:

```env
OLLAMA_MODEL=codellama
DATABASE_URL=sqlite:///database/sales.db
MAX_ROWS=100
DEBUG=True
```

## Architecture

Key directories:

- `app.py`: Streamlit entrypoint
- `src/chains/`: NL→SQL generation chain
- `src/database/`: DB connection, schema loading, and SQL validation
- `src/services/`: LLM, query execution, and history persistence
- `src/ui/`: Streamlit UI components
- `database/`: sample SQLite DB + initializer

## Roadmap

- PostgreSQL/MySQL connectors
- Better column-level validation
- Authentication and user sessions
