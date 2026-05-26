---
name: project-setup
description: "Set up a production-ready AI SQL Assistant project with Ollama, LangChain, Streamlit, and SQLite. The assistant should convert natural language questions into SQL queries, execute them safely, and display results. The project should be modular, scalable, and secure against destructive SQL operations."
user-invocable: true
---

# AI SQL Assistant — Full Project Context

## Project Overview

Build a production-ready AI SQL Assistant web application that allows users to query SQL databases using natural language.

Example:

* User Input: "Which product generated the highest revenue last month?"
* AI Output:

  * Generated SQL query
  * Executed result
  * Human-readable explanation

The application should:

* Run locally using Ollama
* Use LangChain for orchestration
* Support SQLite initially
* Use Streamlit for frontend UI
* Be modular and scalable
* Be safe against destructive SQL operations

---

# Core Tech Stack

## Frontend

* Streamlit

## Backend / AI

* Python 3.11+
* LangChain
* LangChain Community
* LangChain Experimental
* LangChain Ollama

## LLM

* Ollama
* codellama OR llama3

## Database

* SQLite (initial version)

## Future-ready architecture

Design code so PostgreSQL/MySQL support can be added later.

---

# Main Features

## 1. Natural Language to SQL

Users should type plain English questions.

Example:

* "Show top 5 customers by revenue"
* "Which employee had highest sales this quarter?"

The AI should:

1. Understand schema
2. Generate SQL
3. Validate SQL
4. Execute query
5. Return results

---

## 2. SQL Query Display

Always show:

* Generated SQL
* Execution result
* Execution time

---

## 3. Database Schema Awareness

The assistant must:

* Read database schema dynamically
* Understand:

  * tables
  * columns
  * foreign keys
  * relationships

Use:

```python
SQLDatabase.from_uri()
```

---

## 4. SQL Safety Layer

VERY IMPORTANT.

The app MUST block:

* DELETE
* DROP
* UPDATE
* ALTER
* TRUNCATE
* INSERT

Only allow:

* SELECT
* WITH
* SHOW
* DESCRIBE

Implement:

```python
def is_safe_query(query: str) -> bool:
```

Use regex validation before execution.

---

## 5. Query Validation

Before executing:

* Check hallucinated columns
* Check hallucinated tables
* Prevent invalid joins
* Limit large queries

Add:

```sql
LIMIT 100
```

automatically if missing.

---

## 6. Query History

Store:

* User question
* Generated SQL
* Result
* Timestamp

Persist locally using SQLite or JSON.

---

## 7. Download Results

Allow exporting:

* CSV
* JSON

---

## 8. Chat UI

Create conversational UI:

* Chat history
* Assistant responses
* SQL preview
* Query result tables

---

# Recommended Project Structure

```txt
ai-sql-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── database/
│   ├── sales.db
│   └── init_db.py
│
├── src/
│   ├── chains/
│   │   └── sql_chain.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── prompts.py
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── validator.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── query_service.py
│   │   └── history_service.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── formatter.py
│   │   └── helpers.py
│   │
│   └── ui/
│       └── components.py
│
└── tests/
    ├── test_validator.py
    ├── test_queries.py
    └── test_chain.py
```

---

# UI Requirements

## Streamlit Layout

### Sidebar

* Database info
* Connected tables
* LLM status
* Ollama model selector
* Query history

### Main Area

* Chat interface
* User question input
* SQL generation preview
* Query execution result
* Download buttons

---

# LLM Setup

Use Ollama locally.

Supported models:

* codellama
* llama3
* mistral

Default:

```python
model="codellama"
temperature=0
```

Reason:
SQL generation should be deterministic.

---

# Prompt Engineering

Create a dedicated prompt template.

Prompt Rules:

* Use ONLY available schema
* NEVER invent columns
* Return ONLY SQL
* Use proper joins
* Use LIMIT 100 if unspecified
* Prefer readable SQL formatting

Example:

```python
PROMPT_TEMPLATE = """
You are a senior SQL engineer.

Given the schema below, generate a correct SQL query.

RULES:
- Use ONLY tables and columns from schema
- Never hallucinate columns
- Never generate destructive queries
- Return ONLY SQL
- Add LIMIT 100 if no limit exists

Schema:
{schema}

Question:
{question}
"""
```

---

# LangChain Architecture

Use:

```python
SQLDatabase
SQLDatabaseChain
ChatOllama
PromptTemplate
StrOutputParser
```

Prefer LCEL-based architecture over legacy chains.

---

# Result Processing

After SQL execution:

* Format rows into dataframe
* Display clean table
* Show:

  * row count
  * execution time
  * generated SQL

---

# Error Handling

Handle:

* Invalid SQL
* Missing tables
* Ollama not running
* Database connection failure
* Empty responses
* Timeout issues

Show user-friendly errors.

---

# Logging

Add structured logging.

Log:

* prompts
* generated SQL
* execution errors
* latency

---

# Security Requirements

Critical:

* Never expose raw DB credentials
* Use environment variables
* Read-only DB access
* SQL sanitization layer

---

# Environment Variables

```env
OLLAMA_MODEL=codellama
DATABASE_URL=sqlite:///database/sales.db
MAX_ROWS=100
DEBUG=True
```

---

# README Requirements

Generate professional README with:

* project overview
* screenshots section
* setup guide
* Ollama installation
* model download
* Streamlit run instructions
* architecture diagram
* future roadmap

---

# Setup Commands

```bash
pip install -r requirements.txt
```

Run Ollama:

```bash
ollama serve
```

Pull model:

```bash
ollama pull codellama
```

Run app:

```bash
streamlit run app.py
```

---

# requirements.txt

```txt
streamlit
langchain
langchain-community
langchain-experimental
langchain-ollama
sqlalchemy
pandas
python-dotenv
tabulate
```

---

# Advanced Features (Optional)

## Add later

* PostgreSQL support
* MySQL support
* Multi-database support
* Authentication
* User sessions
* Query caching
* Charts and visualizations
* SQL explanation mode
* AI-generated insights
* Voice input
* Dark mode
* Docker deployment

---

# Important Engineering Constraints

## Code Quality

* Type hints everywhere
* Modular architecture
* Reusable services
* Clean separation of concerns

## Performance

* Cache schema
* Avoid repeated DB introspection
* Stream responses if possible

## UX

* Fast responses
* Clear loading states
* Clean modern UI

---

# GitHub Requirements

Initialize git repository.

Commit structure:

1. Initial setup
2. Database layer
3. LangChain integration
4. Streamlit UI
5. Security layer
6. Documentation

Push complete project to GitHub.

---

# Expected Deliverables

The generated project must include:

* Fully working source code
* README
* requirements.txt
* sample SQLite database
* sample queries
* modular architecture
* production-ready structure
* error handling
* SQL safety layer
* GitHub-ready repository

---

# Inspiration / Reference Architecture

This project is inspired by:

* LangChain SQL assistants
* Local Ollama AI workflows
* Text-to-SQL applications
* AI data analyst tools

Reference concepts:

* Schema contextualization
* SQL generation
* Query execution
* Result interpretation

---

# Success Criteria

The final app should:

* Run locally
* Work without OpenAI API
* Convert natural language to SQL accurately
* Prevent unsafe queries
* Show results clearly
* Be easy to extend
* Be deployable later

Build this as a clean, scalable, production-quality AI engineering project.
