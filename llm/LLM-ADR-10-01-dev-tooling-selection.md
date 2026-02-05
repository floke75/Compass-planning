---
id: ADR-10-01-LLM
type: adr
area: 10-dev-tooling
title: Development Tooling Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the development tooling stack decision
tags: [dev-tooling, testing, linting, ci, decision, llm, view]
links:
  - rel: related
    target_id: "RF-10-01"
  - rel: related
    target_id: "ADR-01-01"
  - rel: related
    target_id: "ADR-08-01"
view: llm
source_id: ADR-10-01
source_updated: 2026-02-03
staleness: fresh
---

# Development Tooling Selection (LLM View)

## LLM Summary
This ADR proposes a development tooling stack optimized for LLM maintainability and the Convex plus Vercel platform: Vitest with convex-test for testing, Biome for linting and formatting, GitHub Actions for validation-only CI, and Vercel-managed deployment. The decision emphasizes minimal configuration, fast feedback, and clear error messages for AI-assisted development. Alternatives included Jest with custom mocks, ESLint plus Prettier, and full CI-driven deployments, which were rejected due to higher maintenance burden and configuration complexity. Playwright E2E testing is deferred until post-MVP to avoid overhead. The trade-off is adopting newer tools like Biome and convex-test in exchange for simpler setup and faster runs. The stack prioritizes predictable defaults over deep customization. Consequences include a streamlined toolchain aligned with the stack and fewer moving parts for a small team.

## Canonical Statements
- Compass SHOULD use Vitest and convex-test for testing.
- Biome SHOULD be the single linting and formatting tool.
- CI MUST validate tests and linting; deployment remains Vercel-managed.
- TypeScript strict mode SHOULD be enabled by default.

## Scope and Non-Goals
- In scope: Testing, linting/formatting, and CI tooling selection.
- Out of scope: Product architecture and runtime operations.

## Dependencies and Interfaces
- Research evidence: `RF-10-01`.
- Backend and hosting context: `ADR-01-01`, `ADR-08-01`.

## Core Invariants
- Testing must use Vitest with convex-test.
- Biome is the single linting/formatting tool.
- CI validates only; deployment is Vercel-managed.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Decision
- Use Vitest + convex-test, Biome, GitHub Actions (validation), and Vercel-managed deployment.

## Drivers
- LLM maintainability and minimal configuration.
- Fast feedback and clear diagnostics.
- Alignment with Convex and Vercel stack.

## Alternatives and Disposition
- Jest + custom mocks: Rejected due to added maintenance.
- ESLint + Prettier: Rejected due to configuration complexity.
- Full CI deployment: Rejected in favor of Vercel integration.
- Playwright E2E: Deferred until core functionality is stable.

## Consequences
- Positive: Simpler toolchain and faster iteration.
- Negative: Reliance on newer tooling with smaller ecosystems.
