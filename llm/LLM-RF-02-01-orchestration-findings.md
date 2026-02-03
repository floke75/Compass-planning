---
id: RF-02-01-LLM
type: rf
area: 02-llm-orchestration
title: LLM Orchestration Framework Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of orchestration framework research findings
tags: [orchestration, llm, mastra, vercel-ai-sdk, research, llm, view]
related:
  - RF-02-01
  - ADR-02-01
  - DD-18-01
  - DD-19-01
view: llm
source_id: RF-02-01
source_updated: 2026-01-25
staleness: fresh
---

# LLM Orchestration Framework Research Findings (LLM View)

## LLM Summary
This research evaluates orchestration frameworks for Compass and recommends a two-layer approach: Mastra for workflow orchestration and Vercel AI SDK v6 for structured outputs and provider abstraction. The key insight is that Compass needs durable, branching, multi-session workflows, which Mastra provides via state machines and suspend/resume, while AI SDK v6 provides reliable schema-constrained JSON for widget generation. Alternatives like AI SDK plus XState require more custom build time, and LangGraph.js is not recommended due to TypeScript issues and Zod-to-JSONSchema incompatibilities that impact strict output modes. Instructor excels at extraction but lacks orchestration. The trade-off is adopting a young framework with proprietary workflow DSL in exchange for a 2-3 week integration versus 6-10 weeks of custom orchestration. These findings inform ADR-02-01 and downstream widget and questioning-arc work.

## Canonical Statements
- Mastra + AI SDK v6 is the recommended orchestration stack.
- Structured output reliability is critical for widget generation.
- Multi-session persistence and branching are required capabilities.
- LangGraph.js is not recommended for Compass in its current TS state.

## Scope and Non-Goals
- In scope: Orchestration framework evaluation for Compass.
- Out of scope: Widget rendering or backend selection.

## Dependencies and Interfaces
- Decision output: `ADR-02-01`.
- Planning workflow: `DD-18-01`.
- Widget schema: `DD-19-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Evidence based on vendor docs and community reports; no benchmarks.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-02-01` with no semantic changes.

## Findings
- Mastra provides native state machines and suspend/resume for the questioning arc.
- AI SDK v6 offers the strongest structured output and provider abstraction in TS.
- LangGraph.js has schema conversion issues affecting strict JSON modes.

## Limitations
- Mastra is young and long-term stability is unverified.
- No hands-on performance benchmarking performed.
- Some TypeScript assessments rely on community reports.

## Recommendation
- Recommend Mastra + AI SDK v6 for Compass orchestration.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
