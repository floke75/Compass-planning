---
id: RF-10-01-LLM
type: rf
area: 10-dev-tooling
title: Development Tooling Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of development tooling research findings
tags: [dev-tooling, testing, linting, ci, vitest, biome, research, llm, view]
related:
  - RF-10-01
  - ADR-10-01
  - ADR-01-01
  - ADR-08-01
view: llm
source_id: RF-10-01
source_updated: 2026-01-28
staleness: fresh
---

# Development Tooling Research Findings (LLM View)

## LLM Summary
This research evaluates development tooling for Compass and recommends Vitest with convex-test for testing, Biome for linting and formatting, GitHub Actions for validation-only CI, and Vercel-managed deployment. The selection prioritizes LLM maintainability, minimal configuration, and fast feedback for a small team working in TypeScript with Convex and Vercel. Biome is chosen over ESLint plus Prettier to reduce configuration overhead, and Playwright E2E testing is deferred to avoid maintenance complexity until a real need emerges. The trade-off is adopting newer tools with smaller ecosystems in exchange for simpler setup and faster iteration. Costs are zero beyond existing platform subscriptions. The stack favors predictable defaults and clear diagnostics for AI-assisted development. It also optimizes for patterns LLMs are most likely to generate correctly. These findings support ADR-10-01 and guide the development workflow.

## Canonical Statements
- Vitest plus convex-test is the recommended testing stack.
- Biome should be the single linting and formatting tool.
- CI should validate only; deployments are handled by Vercel.
- TypeScript strict mode should be enabled.

## Scope and Non-Goals
- In scope: Testing, linting/formatting, and CI/CD tooling evaluation.
- Out of scope: Product architecture or runtime operations.

## Dependencies and Interfaces
- Backend and hosting context: `ADR-01-01`, `ADR-08-01`.
- Decision output: `ADR-10-01`.

## Evidence and Freshness
- Source updated 2026-01-28; staleness marked fresh.
- Tooling preferences are somewhat subjective; ecosystem evolves quickly.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-10-01` with no semantic changes.

## Findings
- Vitest and convex-test align with Convex patterns and LLM familiarity.
- Biome reduces configuration complexity relative to ESLint plus Prettier.
- Vercel-managed deployment minimizes CI/CD overhead.

## Limitations
- Some tooling choices are subjective and ecosystem-dependent.
- convex-test is relatively new with less training data coverage.

## Recommendation
- Recommend Vitest + convex-test, Biome, GitHub Actions validation, and Vercel deployment.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
