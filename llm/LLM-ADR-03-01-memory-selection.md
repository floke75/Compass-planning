---
id: ADR-03-01-LLM
type: adr
area: 03-memory-retrieval
title: Memory and Retrieval Architecture Selection (LLM View)
status: proposed
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the memory and retrieval architecture decision
tags: [memory, retrieval, convex, rag, decision, llm, view]
related:
  - ADR-03-01
  - RF-03-01
  - ADR-01-01
  - ADR-02-01
links:
  - rel: related
    target_id: "RF-03-01"
  - rel: related
    target_id: "ADR-01-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: responds_to
    target_id: "RF-03-01"
view: llm
source_id: ADR-03-01
source_updated: 2026-02-03
staleness: fresh
---

# Memory and Retrieval Architecture Selection (LLM View)

## LLM Summary
This ADR proposes a Convex-primary memory architecture using @convex-dev/rag for all three memory layers: session, project, and ecosystem. The approach uses namespace isolation, temporal fields, and a Convex event log to enable semantic retrieval and basic time-based queries without external services. The decision is driven by integration simplicity, a single source of truth, lower cost ($10-30/month vs $100-400/month for external services), and sufficient capability for Phase 1-2 requirements. External services such as Zep Graphiti, Supermemory, or Mem0 are reserved as Phase 3 enrichment if bi-temporal queries, MCP integration, or stronger isolation become necessary. The trade-off is custom implementation for advanced temporal queries and reliance on convention-based namespace isolation. Consequences include faster delivery, fewer moving parts, and possible future migration work if external services are added.

## Canonical Statements
- Memory MUST be implemented within Convex using @convex-dev/rag for Phase 1-2.
- The system MUST support session, project, and ecosystem memory layers.
- External memory services MAY be added only with documented justification.
- Namespace isolation MUST prevent cross-layer leakage.

## Scope and Non-Goals
- In scope: Memory and retrieval architecture for Compass.
- Out of scope: Widget rendering, orchestration framework selection, or frontend hosting.

## Dependencies and Interfaces
- Research evidence: `RF-03-01`.
- Backend foundation: `ADR-01-01`.
- Orchestration context: `ADR-02-01`.

## Evidence and Freshness
- Source updated 2026-01-26; staleness marked fresh.
- Evidence grounded in `RF-03-01` with pricing and capability analysis.

## Open Questions
- Whether Phase 3 bi-temporal requirements justify Zep Graphiti remains open.

## Change Log
- 2026-02-03: LLM view created from `ADR-03-01` with no semantic changes.

## Decision
- Use Convex-only memory with @convex-dev/rag for all memory layers.

## Drivers
- Integration simplicity and single source of truth.
- Lower cost and fewer moving parts for a small team.
- Adequate semantic and temporal filtering for Phase 1-2.

## Alternatives and Disposition
- Zep Graphiti: Deferred to Phase 3 for bi-temporal needs.
- Supermemory: Deferred unless MCP integration becomes critical.
- Mem0: Rejected due to cost and overlapping capabilities.

## Consequences
- Positive: Faster delivery, lower cost, simpler operations.
- Negative: Custom temporal logic and potential future migration work.
