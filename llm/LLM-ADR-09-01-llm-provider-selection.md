---
id: ADR-09-01-LLM
type: adr
area: 09-llm-provider
title: LLM Provider Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the tiered LLM provider strategy decision
tags: [llm, provider, anthropic, google, openai, decision, llm, view]
links:
  - rel: related
    target_id: "RF-09-01"
  - rel: related
    target_id: "ADR-02-01"
view: llm
source_id: ADR-09-01
source_updated: 2026-02-03
staleness: fresh
---

# LLM Provider Selection (LLM View)

## LLM Summary
This ADR proposes a tiered, multi-provider strategy: Claude Opus 4.5 for planning and research, Claude Haiku 4.5 for orchestration and document generation, with Gemini 3 Pro/2.5 Flash and GPT-5.2/Mini as fallbacks. The decision aligns with the system requirement to be LLM-agnostic while balancing cost and capability. A hybrid routing model avoids single-provider failure risk and reduces cost versus running all tasks on frontier models. Alternatives considered include single-provider strategies (Anthropic-only, OpenAI-only, or Google-only) and using an API aggregator. The trade-off is increased integration complexity and multiple billing relationships in exchange for reliability, quality for complex planning, and cost optimization for lightweight tasks. The strategy keeps costs within initial and growth budget constraints while preserving redundancy. Consequences include the need for a routing layer and careful model assignment to task types.

## Canonical Statements
- Compass SHOULD use a tiered, multi-provider model strategy.
- Planning and research MUST use a frontier-capable model.
- Orchestration SHOULD use a fast, reliable model tier.
- The architecture MUST remain provider-agnostic with fallbacks.

## Scope and Non-Goals
- In scope: LLM provider and model tier selection.
- Out of scope: Orchestration framework implementation details.

## Dependencies and Interfaces
- Research evidence: `RF-09-01`.
- Orchestration context: `ADR-02-01`.

## Core Invariants
- Architecture must remain provider-agnostic with fallbacks.
- Planning tasks require frontier-capable models.
- Budget models with weak compliance are not acceptable.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Decision
- Use Claude Opus 4.5 for planning/research and Claude Haiku 4.5 for orchestration, with Gemini and GPT-5 as fallbacks.

## Drivers
- Maintain LLM-agnostic design and provider redundancy.
- Optimize cost for routine tasks while preserving planning quality.
- Align model capability to task criticality.

## Alternatives and Disposition
- Single-provider strategies: Rejected due to single point of failure and weaker alignment with task types.
- API aggregator: Considered but not selected due to control and reliability concerns.

## Consequences
- Positive: Better reliability and cost control with task-appropriate models.
- Negative: Added routing complexity and multi-provider management.
