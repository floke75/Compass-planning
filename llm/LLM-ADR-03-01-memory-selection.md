---
id: ADR-03-01-LLM
type: adr
area: 03-memory-retrieval
title: Memory and Retrieval Architecture Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the memory and retrieval architecture decision
tags: [memory, retrieval, convex, rag, decision, llm, view]
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
This ADR proposes a Convex-primary memory architecture using @convex-dev/rag for all three memory layers: session, project, and ecosystem. The approach uses namespace isolation, temporal fields, and a Convex event log to enable semantic retrieval and basic time-based queries without external services. The decision is driven by integration simplicity, a single source of truth, lower cost ($10-30/month vs $100-400/month for external services), and sufficient capability for initial planning workflow requirements. External services such as Zep Graphiti, Supermemory, or Mem0 may be added if advanced temporal queries become necessary, specifically if bi-temporal queries, MCP integration, or stronger isolation become necessary. The trade-off is custom implementation for advanced temporal queries and reliance on convention-based namespace isolation. Consequences include faster delivery, fewer moving parts, and possible future migration work if external services are added.

## Canonical Statements
- Memory MUST be implemented within Convex using @convex-dev/rag for initial implementation.
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

## Core Invariants
- Memory must live within Convex for initial implementation.
- Namespace isolation prevents cross-layer data leakage.
- External services require documented justification.

## Open Questions
- Whether advanced temporal query requirements justify Zep Graphiti remains open.

## Decision
- Use Convex-only memory with @convex-dev/rag for all memory layers.

## Drivers
- Integration simplicity and single source of truth.
- Lower cost and fewer moving parts for a small team.
- Adequate semantic and temporal filtering for initial planning workflow requirements.

## Alternatives and Disposition
- Zep Graphiti: May be added if advanced temporal queries become necessary.
- Supermemory: Deferred unless MCP integration becomes critical.
- Mem0: Rejected due to cost and overlapping capabilities.

## Consequences
- Positive: Faster delivery, lower cost, simpler operations.
- Negative: Custom temporal logic and potential future migration work.
