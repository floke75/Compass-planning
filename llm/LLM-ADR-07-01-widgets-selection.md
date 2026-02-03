---
id: ADR-07-01-LLM
type: adr
area: 07-widget-libraries
title: Widget Component Library Selection (LLM View)
status: proposed
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the widget rendering library decision
tags: [widgets, components, thesys, shadcn, decision, llm, view]
related:
  - ADR-07-01
  - RF-07-01
  - ADR-02-01
  - DD-19-01
links:
  - rel: related
    target_id: "RF-07-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "DD-19-01"
view: llm
source_id: ADR-07-01
source_updated: 2026-02-03
staleness: fresh
---

# Widget Component Library Selection (LLM View)

## LLM Summary
This ADR proposes a hybrid widget rendering approach: Thesys C1 as the primary generative UI layer combined with custom shadcn/ui plus dnd-kit components for specialized planning widgets. The decision aligns with Mastra + AI SDK orchestration and supports dynamic, schema-driven widgets with streaming and custom extensions. It targets full coverage of the Compass widget taxonomy while minimizing orchestration glue code. Alternatives considered include CopilotKit, a pure shadcn/ui JSON registry, and SurveyJS; each was rejected due to higher integration cost, missing native Mastra alignment, or licensing and styling constraints. The trade-off is reliance on a young vendor and a C1 DSL in exchange for faster delivery and a simpler integration surface. Consequences include building a limited set of custom widgets (roughly eight) and managing a vendor dependency for the core rendering layer.

## Canonical Statements
- Compass SHOULD use Thesys C1 as the primary widget rendering layer.
- Custom widgets MUST be built with shadcn/ui and dnd-kit where C1 lacks coverage.
- Widget rendering MUST support streaming and schema-driven specs.

## Scope and Non-Goals
- In scope: Widget component library selection.
- Out of scope: Widget schema definition and orchestration logic.

## Dependencies and Interfaces
- Research evidence: `RF-07-01`.
- Orchestration context: `ADR-02-01`.
- Widget schema: `DD-19-01`.

## Evidence and Freshness
- Source updated 2026-01-26; staleness marked fresh.
- Evidence grounded in `RF-07-01` library evaluation.

## Open Questions
- Final stakeholder approval and C1 integration prototype outcomes.

## Change Log
- 2026-02-03: LLM view created from `ADR-07-01` with no semantic changes.

## Decision
- Use Thesys C1 plus custom shadcn/ui components for widget rendering.

## Drivers
- Native Mastra alignment and streaming UI support.
- Faster delivery than building a full custom registry.
- Extensibility for specialized planning widgets.

## Alternatives and Disposition
- CopilotKit: Rejected due to missing Mastra integration and higher complexity.
- Pure shadcn/ui: Rejected due to greater build effort and missing streaming.
- SurveyJS: Rejected due to styling constraints and licensing costs.

## Consequences
- Positive: Faster implementation and strong generative UI alignment.
- Negative: Vendor dependency and custom widget build effort.
