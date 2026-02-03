---
id: RF-07-01-LLM
type: rf
area: 07-widget-libraries
title: Widget Component Library Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of widget component library research findings
tags: [widgets, components, generative-ui, thesys, shadcn, research, llm, view]
related:
  - RF-07-01
  - ADR-07-01
  - DD-19-01
  - STD-19-01
view: llm
source_id: RF-07-01
source_updated: 2026-01-26
staleness: fresh
---

# Widget Component Library Research Findings (LLM View)

## LLM Summary
This research evaluates widget component libraries and generative UI approaches for Compass and recommends a hybrid architecture: Thesys C1 for generative UI and standard interactions, plus shadcn/ui with dnd-kit for specialized planning widgets. The key insight is that generative UI reduces orchestration complexity by letting the LLM describe UI intent directly, while custom components are still required because no library covers more than half of the widget taxonomy. C1 offers native Mastra integration and streaming UI, which accelerates development compared to a fully custom JSON registry. Alternatives such as CopilotKit, pure shadcn/ui, and SurveyJS were rejected due to missing Mastra alignment, higher integration effort, or styling and licensing constraints. The trade-off is vendor dependency and recurring cost in exchange for faster delivery and a simpler LLM-to-UI pipeline. These findings support ADR-07-01 and widget schema work.

## Canonical Statements
- A hybrid C1 + custom shadcn/ui approach best fits the widget taxonomy.
- Generative UI reduces orchestration complexity for dynamic widgets.
- Custom widgets are required for ranked, comparative, and spatial interactions.

## Scope and Non-Goals
- In scope: Widget rendering library evaluation.
- Out of scope: Widget schema definition and orchestration design.

## Dependencies and Interfaces
- Decision output: `ADR-07-01`.
- Widget schema and standards: `DD-19-01`, `STD-19-01`.

## Evidence and Freshness
- Source updated 2026-01-26; staleness marked fresh.
- Vendor maturity and pricing may change; no performance benchmarks performed.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-07-01` with no semantic changes.

## Findings
- Thesys C1 provides native Mastra integration and streaming generative UI.
- shadcn/ui plus dnd-kit enables specialized widget coverage.
- No evaluated library covers the full Compass taxonomy natively.

## Limitations
- Thesys C1 is young; long-term stability unverified.
- No hands-on performance benchmarking performed.
- Custom component estimates are based on similar projects.

## Recommendation
- Recommend Thesys C1 with custom shadcn/ui extensions.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
