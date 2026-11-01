# Security and data handling

GapLens stores research queries, extracted source text, claims, and verification state. Treat the database and API responses as potentially sensitive, even when a source was publicly reachable.

## Current security posture

- Email/password registration and sign-in are available. Passwords are stored as PBKDF2 hashes and authentication uses an expiring signed HTTP-only cookie.
- Research sessions are assigned to their creating account. Every `/api/research` request requires authentication, and session-specific routes check ownership.
- Sessions created before account ownership was added remain unassigned and are not exposed in any account's session list.
- Configure a unique `AUTH_SECRET_KEY` outside development. The development fallback is not suitable for deployment.
- CORS is configurable, but CORS is not access control. The default origins are development localhost origins.
- `/health` reports provider names and whether keys are configured; it does not return the keys.
- Uploaded document contents and retrieved page contents are persisted in SQLite.
- URL ingestion and server-side content fetching require protections against unsafe destinations and internal network access before operating with untrusted users. Review the current provider fetch flow and add an explicit SSRF policy for production.

The account flow is an MVP. Before a public deployment, add rate limits, account recovery, a reviewed CSRF strategy, and operational controls. Do not treat this as a complete identity platform.

## Secrets

- Keep provider credentials in `backend/.env` for local development; `.env` is ignored by Git.
- Use deployment secret injection for hosted environments.
- Rotate any key accidentally committed, pasted into logs, or shared outside its intended scope.
- Avoid logging request bodies, provider headers, complete source contents, or secret-bearing exceptions.

## Research data

Stored data includes the research goal, derived scope, URL and upload metadata, full extracted source text, model-derived claims, and checklist completion. Define a retention period and deletion mechanism before supporting real accounts. Restrict database backups, encrypt them at rest, and avoid attaching the database to bug reports.

Uploaded documents are read in memory with a 10 MB per-file limit. PDF extraction uses embedded text and does not OCR scanned pages. File extension checks are not a complete malware/content validation strategy; harden file handling if accepting untrusted public uploads.

## Model and source trust

Retrieved pages and files are untrusted input. Prompt injection, stale pages, extraction errors, and model hallucinations can affect generated claims and recommendations. Preserve source links/excerpts, label uncertainty, and have a human verify high-impact conclusions against the original source.

## Deployment checklist

- [ ] Add rate limits, account recovery, and complete production identity controls.
- [ ] Review CSRF protections, proxy headers, and cookie policy for the deployment topology.
- [ ] Restrict origins and apply proxy/API rate limits.
- [ ] Add URL destination validation and SSRF protections.
- [ ] Use managed secrets, TLS, encrypted backups, and documented retention/deletion.
- [ ] Set upload limits and validate file content, not just filename extension.
- [ ] Sanitize logs and expose only appropriate operational detail.
- [ ] Review provider data-processing terms for the data being submitted.
