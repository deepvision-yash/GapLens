# Development setup

## Prerequisites

- Python 3.10 or newer.
- pip and a virtual environment.
- Provider credentials for full AI research. Supported LLM integrations are Gemini and Groq; web search supports Jina or Tavily. Jina Reader can fetch submitted URLs under its unauthenticated limits.

The UI is served from `frontend/html/` by the backend. Node.js and `frontend/node_modules` are not needed to run the app.

## Install and run

From the repository root in PowerShell:

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add provider keys to `backend/.env`, then run:

```powershell
uvicorn app.main:app --reload --port 8000
```

Visit `http://127.0.0.1:8000/`, `http://127.0.0.1:8000/docs`, and `http://127.0.0.1:8000/health`.

Run from `backend/`: the default SQLite URL is relative (`./gaplens.db`) and the settings file is `.env` in the working directory. Launching Uvicorn from the repository root can therefore load different config/database paths than intended.

## Provider configuration

The canonical variable list and defaults are in [`../../backend/.env.example`](../../backend/.env.example). Keep actual credentials in ignored `backend/.env` only. `LLM_PROVIDER` selects Gemini or Groq; available configuration may provide fallback behavior in the external service. `SEARCH_PROVIDER` selects Jina or Tavily. `/health` reports key presence, not that credentials are valid or quota is available.

To exercise user-supplied URLs without search, create a session with URLs. Search-backed research needs the selected search integration configured. Local interface and persisted session browsing can run without provider calls, but scope generation and analysis require a usable LLM.

## Data files

Startup creates tables in the database configured by `DATABASE_URL`; by default this is `backend/gaplens.db`. This file is local state and should not be committed or copied into issue reports. To use another location, set `DATABASE_URL` to an async SQLAlchemy URL.

## Useful checks

- Confirm `/health` returns HTTP 200 and the expected provider readiness flags.
- Confirm `/docs` contains routes from the `/api/research` router.
- Create a research session, generate/edit scope, and verify status transitions before debugging a full provider-backed run.
- For uploads, use text-based PDF, DOCX, or UTF-8 TXT under 10 MB. Scanned PDF images are not OCR processed.

The repository has pytest dependencies and a `backend/tests` directory, but no maintained test suite or test command is documented here. Verify the current test files/config before treating tests as a reliable gate.
