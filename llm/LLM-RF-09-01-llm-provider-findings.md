---
id: RF-09-01-LLM
type: rf
area: 09-llm-provider
title: LLM Provider Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of LLM provider research findings
tags: [llm, provider, anthropic, openai, google, research, llm, view]
related:
  - RF-09-01
  - ADR-09-01
  - ADR-02-01
view: llm
source_id: RF-09-01
source_updated: 2026-01-25
staleness: fresh
---

# LLM Provider Research Findings (LLM View)

## LLM Summary
This research evaluates LLM providers and recommends a tiered model strategy: Claude Opus 4.5 for planning and research, Claude Haiku 4.5 for orchestration and routine generation, with Gemini 3 Pro/2.5 Flash and GPT-5.2/Mini as fallbacks. The key insight is that planning requires frontier reasoning, while orchestration demands reliable instruction following. Cheap models like Gemini 2.0 Flash are explicitly excluded due to weak compliance and impending deprecation. Pricing analysis shows the tiered approach stays well below budget ceilings, even at Phase 3 scale, while maintaining quality for critical tasks. The strategy emphasizes redundancy without sacrificing planning quality. Trade-offs include increased routing complexity and multi-provider management in exchange for redundancy and cost control. These findings inform ADR-09-01 and the orchestration routing strategy.

## Canonical Statements
- A tiered, multi-provider strategy best fits Compass requirements.
- Planning tasks require frontier-level models.
- Orchestration tasks require reliable instruction following.
- Budget models with weak compliance are not acceptable.

## Scope and Non-Goals
- In scope: LLM provider and model tier evaluation.
- Out of scope: Orchestration framework implementation details.

## Dependencies and Interfaces
- Decision output: `ADR-09-01`.
- Orchestration context: `ADR-02-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Pricing verified January 24-25, 2026; subject to change.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-09-01` with no semantic changes.

## Findings
- Claude Opus 4.5 and Haiku 4.5 provide the best planning and orchestration pairing.
- Gemini and GPT-5 models serve as cost-effective fallbacks.
- Budget models with poor instruction following are risky for production use.

## Limitations
- Pricing changes frequently; some data verified via aggregators.
- No hands-on latency or reliability testing performed.
- Some features remain in beta or preview.

## Recommendation
- Recommend tiered Claude-first strategy with Gemini and GPT-5 fallbacks.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
