# API reference

The API is served by FastAPI. Use `/docs` for the generated OpenAPI schema, validation constraints, and precise payload models. All session routes are under `/api/research`.

## Health

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Returns app status/version and configured provider readiness flags. This checks key presence, not remote provider connectivity. |

## Session and scope

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/research` | List up to 50 most recently updated sessions. |
| `POST` | `/api/research` | Create session. `goal` must be 10–2000 characters. Optional URL sources are persisted; file uploads are a separate endpoint. |
| `POST` | `/api/research/{session_id}/understand` | Interpret the goal and generate dimensions; transitions `created` to `scope_review`. |
| `GET` | `/api/research/{session_id}/scope` | Read interpreted goal, dimensions, and state. |
| `PATCH` | `/api/research/{session_id}/scope` | Replace dimensions during `scope_review` (1–`MAX_DIMENSIONS`). |

Creation accepts URL inputs with `kind: "url"`. The API schema also defines a `file` input shape, but creation rejects file sources; upload after the session exists.

## Sources and pipeline

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/research/{session_id}/sources/upload` | Multipart upload of one or more PDF, DOCX, or TXT files (10 MB/file); only before research starts. |
| `POST` | `/api/research/{session_id}/start` | Start the pipeline after scope review. |
| `POST` | `/api/research/{session_id}/resume-checklist` | Resume the saved verification workflow (see `/docs` for current request behavior). |
| `GET` | `/api/research/{session_id}/events` | Server-Sent Events progress stream. |
| `GET` | `/api/research/{session_id}/status` | Read session state and current progress information. |

## Results

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/research/{session_id}/results` | Combined goal, dimensions, sources, claims, gaps, conflicts, checklist and status. |
| `GET` | `/api/research/{session_id}/sources` | Sources for a session. |
| `GET` | `/api/research/{session_id}/claims` | Extracted claims. |
| `GET` | `/api/research/{session_id}/gaps` | Identified coverage gaps and next steps. |
| `GET` | `/api/research/{session_id}/conflicts` | Conflicting claim pairs and resolution hints. |
| `GET` | `/api/research/{session_id}/checklist` | Verification tasks. |
| `PATCH` | `/api/research/{session_id}/checklist/{task_id}` | Set a task's `completed` state. |

## Typical interaction

```text
POST   /api/research
POST   /api/research/{id}/sources/upload   (optional)
POST   /api/research/{id}/understand
PATCH  /api/research/{id}/scope           (optional scope edits)
POST   /api/research/{id}/start
GET    /api/research/{id}/events           (follow progress)
GET    /api/research/{id}/results
PATCH  /api/research/{id}/checklist/{task_id} (as tasks are verified)
```

## Error behavior

FastAPI returns standard JSON errors with a `detail` field. Common cases include `400` for malformed UUIDs on upload, `404` for missing sessions/tasks, `409` for invalid lifecycle transitions, `413` for oversized files, `415` for unsupported file extensions, `422` for invalid payloads/content/limits, and `502` when scope generation cannot complete through the configured LLM. Provider errors during background pipeline execution are reflected in session status/error where possible.

## Important contract notes

- The session ID is an identifier, not an access token. There is currently no authentication or per-session authorization.
- SSE progress is held in process memory. It may not be available after a restart or when requests reach a different worker.
- URL and document source content can be persisted and may be returned in previews; handle results as potentially sensitive.
- Inspect the live OpenAPI output for exact schemas; this document is a navigational summary and should be updated with route changes.
