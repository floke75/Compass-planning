---
id: RF-03-01-LLM
type: rf
area: 03-memory-retrieval
title: Memory and Retrieval Architecture Research Findings (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of memory and retrieval research findings
tags: [memory, retrieval, convex, rag, research, llm, view]
view: llm
source_id: RF-03-01
source_updated: 2026-01-25
staleness: fresh
---

# Memory and Retrieval Architecture Research Findings (LLM View)

## LLM Summary
This research evaluates memory and retrieval options for Compass and recommends a Convex-primary approach using @convex-dev/rag for session, project, and ecosystem memory layers. The analysis shows Convex can deliver semantic search, namespace isolation, and basic temporal filtering at low cost, while external services add complexity and cost for initial implementation needs. Zep Graphiti, Supermemory, and Mem0 are positioned as optional advanced capability stage enrichments if bi-temporal queries or MCP integration become critical. The key trade-off is implementing advanced temporal queries via schema patterns (event sourcing) rather than using a specialized external system. Costs favor Convex-only ($0-25/month) compared to $100-400/month with external services. These findings support ADR-03-01 and emphasize a single source of truth and operational simplicity for a small team and low overhead.

## Canonical Statements
- Convex-primary memory is recommended for initial implementation.
- External memory services are optional and conditional for advanced capability stage.
- Namespace isolation and temporal filtering are required capabilities.
- Cost and integration complexity are major selection drivers.

## Scope and Non-Goals
- In scope: Memory and retrieval services for Compass.
- Out of scope: Orchestration frameworks or widget rendering.

## Dependencies and Interfaces
- Decision output: `ADR-03-01`.
- Backend foundation: `ADR-01-01`.

## Open Questions
- Whether advanced capability stage requires bi-temporal services remains open.

## Findings
- Convex @convex-dev/rag covers semantic search and isolation needs.
- Bi-temporal queries are the main gap, addressable with event sourcing.
- External services are useful only if advanced temporal needs emerge.

## Evidence Quality
- Vendor documentation: T1/S1 (official sources)
- Pricing estimates: T2/S2 (verified January 2026)
- Self-hosted cost estimates: T3/S3 (estimates based on similar deployments)

## Limitations
- Pricing and vendor features may change.
- No hands-on implementation testing performed.
- Some costs are estimated for self-hosted options.

## Recommendation
- Recommend Convex-only memory for initial implementation with optional advanced capability stage enrichment.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
