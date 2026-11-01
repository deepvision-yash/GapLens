# Contributing to GapLens

Thanks for helping improve GapLens. This guide describes the current repository and a small, reviewable contribution workflow.

## Before changing code

1. Read [`docs/architecture/architecture.md`](docs/architecture/architecture.md) and the relevant API or product documentation.
2. Check the existing implementation before relying on the research blueprint: some blueprint choices describe future direction rather than shipped code.
3. Keep provider credentials, `.env` files, local databases, and user research data out of commits.

## Local development

Follow [`docs/development/setup.md`](docs/development/setup.md) to create a Python environment, install backend dependencies, configure providers, and run the app. The frontend is static HTML served by FastAPI; no Node build is required.

## Changes

- Keep API contracts in sync with Pydantic schemas and the browser client.
- Keep expensive/provider-specific work behind service boundaries and handle unavailable providers clearly.
- Preserve source provenance when changing claim, gap, or conflict analysis.
- Update the docs when changing setup, routes, environment variables, persistence, or user-visible workflow.
- Use focused commits and explain the behavior change, relevant limitations, and manual checks in the pull request.

## Validation

There is a `backend/tests` directory and pytest dependencies are pinned. Before adding or relying on test commands, inspect the current test configuration and available test modules; do not assume the test suite covers the application. For a manual smoke check, start Uvicorn from `backend/`, open `/`, inspect `/health`, and walk through a research session with provider credentials configured.

## Pull request checklist

- [ ] The change matches the current product flow and API contracts.
- [ ] Documentation and `.env.example` are updated when applicable.
- [ ] No secret, generated database, or unrelated artifact is included.
- [ ] Validation performed and its result is stated accurately.
- [ ] Known limitations and migrations are called out.
