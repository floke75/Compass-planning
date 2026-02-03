---
id: ADR-01-01-LLM
type: adr
area: 01-backend
title: Backend Platform Selection (LLM View)
status: accepted
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the backend platform selection decision
tags: [backend, database, convex, decision, llm, view]
related:
  - ADR-01-01
  - RF-01-01
  - DD-14-01
  - DD-12-01
  - DD-13-01
links:
  - rel: related
    target_id: "RF-01-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
view: llm
source_id: ADR-01-01
source_updated: 2026-02-03
staleness: fresh
---

# Backend Platform Selection (LLM View)

## LLM Summary
This ADR selects Convex as the backend platform for Compass and the broader EFN tool ecosystem. The decision prioritizes LLM-native development for a non-traditional team, built-in agent infrastructure for persistent threads and tool-based database access, and automatic real-time sync for collaborative workflows. Convex's TypeScript-first model removes SQL context switching, and serializable transactions reduce risk from AI-generated mutations. Alternatives included Supabase (PostgreSQL portability but dev-only MCP and more custom work), Neon (database-only, strong branching but requires many external services), and deferring the decision (blocks downstream research). The trade-off accepted is vendor lock-in and a smaller ecosystem in exchange for velocity, reliability, and LLM maintainability. Consequences include reduced integration complexity, faster delivery for core planning workflows, and the need to learn CQRS patterns and manage potential future migration risk.

## Canonical Statements
- Compass MUST use Convex as the backend platform.
- The backend MUST support LLM-native development and agent tooling.
- Real-time collaboration SHOULD be native rather than custom-built.
- Vendor lock-in is an accepted trade-off for velocity and maintainability.

## Scope and Non-Goals
- In scope: Backend platform selection for Compass and EFN tools.
- Out of scope: Frontend hosting, orchestration framework, or PM tooling.

## Dependencies and Interfaces
- Research evidence: `RF-01-01`.
- Ecosystem requirements: `DD-14-01`.
- Repository and artifact standards: `DD-12-01`, `DD-13-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Evidence grounded in `RF-01-01` with pricing and vendor feature verification.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `ADR-01-01` with no semantic changes.

## Decision
- Use Convex as the backend platform for Compass and EFN tools.

## Drivers
- LLM-native TypeScript development for a non-SQL team.
- Built-in agent infrastructure for persistent threads and tool access.
- Automatic real-time sync for multi-user workflows.

## Alternatives and Disposition
- Supabase: Rejected due to dev-only MCP and higher custom build effort.
- Neon: Rejected due to database-only scope and external service complexity.
- Defer decision: Rejected because it blocks downstream research and delivery.

## Consequences
- Positive: Faster delivery, safer AI mutations, integrated agent tooling.
- Negative: Vendor lock-in, smaller ecosystem, CQRS learning curve.
