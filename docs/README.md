# GapLens documentation

This index separates the current implementation guide from product direction and older research materials.

## Start here

- [Project README](../README.md) — product summary, quick start, configuration, and limits.
- [Architecture](architecture/architecture.md) — runtime structure, data flow, persistence, and known architectural constraints.
- [API reference](api/README.md) — route inventory and workflow.
- [Development setup](development/setup.md) — local environment and debugging.
- [Deployment and operations](operations/deployment.md) — deployment prerequisites and operational checks.
- [Security and data handling](operations/security-and-data.md) — secrets, research data, and current access-control limitations.
- [Contributing](../CONTRIBUTING.md) — contribution workflow.

## Product and research

- [Product flow](product/App_flow.md) — UI workflow and how the screens map to backend stages.
- [Design notes](product/GapLens_Design.md) — product rationale and design direction.
- [`../GAPLENS_AI_DEEP_RESEARCH_AND_IMPLEMENTATION_BLUEPRINT.md`](../GAPLENS_AI_DEEP_RESEARCH_AND_IMPLEMENTATION_BLUEPRINT.md) and the Shinchan hackathon research documents are planning/reference artifacts. They may describe future or superseded choices; use code and the implementation docs above to determine current behavior.

## Documentation rule

When a change affects the shipped route, environment, persistence, or workflow, update the matching implementation document and this index if a document is added or moved. Label roadmap ideas as proposed rather than implemented.
