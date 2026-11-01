# GapLens HTML frontend

The six original Stitch screens are the frontend. FastAPI serves the pages, browser script, and API from the same origin.

## Run locally

From `backend/`:

```powershell
uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/` for the landing page, then create an account or sign in. No Node.js frontend server is used.

## Pages

| Screen | URL |
| --- | --- |
| Research Home | `/research/new` |
| Research Scope | `/research/{session_id}/scope` |
| Research in Progress | `/research/{session_id}/progress` |
| Research Intelligence | `/research/{session_id}/intelligence` |
| Evidence Explorer | `/research/{session_id}/evidence` |
| Verification Workspace | `/research/{session_id}/verification` |

The session ID is preserved through navigation. `frontend/html/app.js` uses same-origin `/api/research` requests, so no frontend API URL or CORS setup is needed. PDF, DOCX, and TXT files up to 10 MB each can be uploaded; scanned PDFs require OCR and are rejected when they contain no extractable text. URLs are fetched with Jina Reader.

Configure rotated provider keys only in the ignored `backend/.env` file. `/health` reports which provider integrations are ready without exposing credentials. Real web search requires a Jina Search key when `SEARCH_PROVIDER=jina`; Jina Reader can fetch user-submitted URLs without that key at lower limits.

Set `GEMINI_API_KEY` and/or `GROQ_API_KEY` there for model analysis, plus `JINA_API_KEY` for search and chunk embeddings. `LLM_PROVIDER` selects the primary model; the other configured LLM is used as fallback when Gemini is primary. Copy the variable names from `backend/.env.example`; never paste provider secrets into source files or commit `.env`.

SQLite is initialized automatically at `backend/gaplens.db` on startup and persists sessions, source text, claims, and checklist state across restarts. This is sufficient for local MVP/demo use. A hosted deployment needs a persistent disk or a managed PostgreSQL database; ephemeral server storage will lose SQLite data. Install backend dependencies from `backend/requirements.txt` before starting Uvicorn.
