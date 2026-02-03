---
id: ADR-02-01-LLM
type: adr
area: 02-llm-orchestration
title: LLM Orchestration Framework Selection (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the orchestration framework decision
tags: [orchestration, llm, mastra, vercel-ai-sdk, decision, llm, view]
related:
  - ADR-02-01
  - RF-02-01
  - ADR-01-01
  - ADR-09-01
  - DD-18-01
links:
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "RF-09-01"
  - rel: related
    target_id: "ADR-09-01"
  - rel: related
    target_id: "ADR-01-01"
  - rel: related
    target_id: "DD-13-01"
view: llm
source_id: ADR-02-01
source_updated: 2026-02-03
staleness: fresh
---

# LLM Orchestration Framework Selection (LLM View)

## LLM Summary
This ADR proposes Mastra combined with Vercel AI SDK v6 as the orchestration architecture for Compass planning workflows. Mastra provides state-machine workflows with suspend and resume, thread persistence, and branching primitives that map directly to the questioning arc, while AI SDK v6 provides structured output and provider abstraction for widget generation. The decision is driven by integration speed (2-3 weeks vs 6-10 weeks for custom orchestration), native TypeScript support, and alignment with the Convex backend. Alternatives considered include AI SDK plus XState, LangGraph.js, and deferring the decision. The key trade-off is adopting a young framework with a proprietary DSL in exchange for faster delivery and built-in workflow primitives. Consequences include a dependency on Mastra stability, the need to implement custom branch visualization and merge logic, and a defined fallback to AI SDK plus XState if Mastra proves limiting.

## Canonical Statements
- Compass SHOULD use Mastra with Vercel AI SDK v6 for orchestration.
- The orchestration layer MUST support structured outputs, persistence, and branching.
- Provider abstraction MUST support tiered model routing.
- A fallback to AI SDK + XState MUST remain viable if Mastra constrains workflows.

## Scope and Non-Goals
- In scope: Orchestration framework selection for planning workflows.
- Out of scope: Widget component rendering and frontend hosting.

## Dependencies and Interfaces
- Research evidence: `RF-02-01`.
- Backend foundation: `ADR-01-01`.
- Model routing: `ADR-09-01`.
- Planning workflow definition: `DD-18-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Evidence grounded in `RF-02-01` vendor and community research.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Change Log
- 2026-02-03: LLM view created from `ADR-02-01` with no semantic changes.

## Decision
- Use Mastra with Vercel AI SDK v6 for Compass orchestration.

## Drivers
- Workflow primitives map to the questioning arc.
- Thread persistence integrates with Convex.
- Lower engineering cost and faster delivery.

## Alternatives and Disposition
- AI SDK + XState: Fallback if Mastra is too constraining.
- LangGraph.js: Rejected due to TypeScript and schema conversion issues.
- Defer decision: Rejected due to downstream blocking.

## Consequences
- Positive: Faster build, native structured output, provider abstraction.
- Negative: Young framework risk and custom merge visualization work.
