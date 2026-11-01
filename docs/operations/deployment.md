# Deployment and operations

## Current deployment shape

GapLens is currently one FastAPI process that serves both the API and static HTML frontend. The default database is SQLite and pipeline progress is process-local. No container orchestration or production deployment workflow is configured in this repository.

These defaults suit local development and controlled demos. Before a public or multi-user deployment, complete the prerequisites below.

## Deployment prerequisites

1. **Access control:** the MVP has email/password auth and session ownership checks. Add rate limits, account recovery, and production identity controls before public deployment.
2. **Database durability:** configure persistent storage or a managed database. Confirm the selected SQLAlchemy async driver, backup/restore process, and migration path. `create_all` is not a schema migration strategy.
3. **Background work:** move long-running research runs to a durable worker/queue. Store progress in shared infrastructure instead of process memory before using multiple workers or replicas.
4. **Secrets:** inject provider keys through the hosting platform's secret store. Do not put them in source, container layers, build args, or logs.
5. **Runtime settings:** set `DEBUG=false`, set an explicit `ENVIRONMENT`, and configure exact allowed origins if a separate frontend is introduced.
6. **Resource limits:** set request and upload limits at the proxy and application layers; monitor provider costs and enforce per-user quotas when accounts exist.
7. **Data lifecycle:** decide retention, user deletion, backup encryption, and incident response for stored research content.

## Environment and startup

The backend reads settings from environment variables and `.env`. See [`../../backend/.env.example`](../../backend/.env.example). Local startup should run from `backend/` because both `.env` discovery and the default relative SQLite file depend on the process working directory.

The application initializes database tables at startup and closes provider HTTP clients at shutdown. Expose `/health` to the platform for basic process health. Its provider readiness fields check for configured keys only; they do not call upstream services.

## Operational checks

- Track status distribution (`completed`, `partial`, `failed`) and pipeline duration.
- Track provider timeouts, throttling, malformed model responses, and search/extraction failures without logging secrets or full sensitive documents.
- Monitor database size and backup success; source text is stored in full.
- Test restoring a backup and deploying schema changes before production upgrades.
- Validate SSE behavior through the actual proxy; disable buffering/timeouts as needed and keep the single-worker constraint in mind until progress is shared.

## Rollback and recovery

Before a release that changes models or stored schema, snapshot the database and preserve the previous app version. Since there are no checked-in migrations, do not assume an app rollback can undo schema changes safely. Define a forward migration and recovery plan before introducing schema changes to durable data.
