---
id: ADR-09-01
type: adr
area: 09-llm-provider
title: LLM Provider Selection
status: proposed
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Selects Claude Opus 4.5 as the primary LLM for planning tasks (frontier reasoning) with Claude Haiku 4.5 for orchestration (reliable instruction following), backed by Gemini 3 Pro/2.5 Flash and GPT-5.2/Mini as fallbacks
tags: [llm, provider, decision, anthropic, openai, google]
related:
  - RF-01-09
decision_date: null
deciders: []
supersedes: null
---

# LLM Provider Selection

## Status

**Proposed** — Awaiting stakeholder review and approval.

---

## Context

Compass is an LLM-orchestrated planning, research, and documentation system that requires reliable, capable, and cost-effective LLM API access. The system will use LLMs for:

- **Planning conversations**: Multi-turn dialogues through OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND stages
- **Research synthesis**: Analyzing sources and generating findings
- **Document generation**: Creating specifications, ADRs, and handoff bundles
- **Orchestration**: Routing requests, classification, and administrative tasks

Per the Compass System Definition §1.7, the system must be "LLM-agnostic by design: No hard dependency on a single model vendor or orchestration framework."

**Budget constraints** (System Definition §4.1):
- Phase 1: <$200/month for LLM APIs
- Phase 3: <$800/month for LLM APIs

**Token volume estimates**:
- Phase 1: ~3.68M input + ~1.52M output tokens/month
- Phase 3: ~14.72M input + ~6.08M output tokens/month

---

## Options Considered

### Option 1: Single Provider (Claude Only)

Use Anthropic Claude for all tasks, selecting model tier based on complexity.

| Model | Use Case | Phase 3 Cost (if 100%) |
|-------|----------|------------------------|
| Sonnet 4.5 | Default | $135.36/month |
| Opus 4.5 | Complex reasoning | $225.60/month |
| Haiku 4.5 | Fast tasks | $45.12/month |

**Pros:**
- Simplest implementation—single API, single billing
- Claude excels at planning and agentic tasks
- Consistent behavior across all interactions

**Cons:**
- Single point of failure for all LLM operations
- No cost optimization for simple tasks ($3/$15 is expensive for routing)
- Violates "LLM-agnostic" principle

### Option 2: Single Provider (OpenAI Only)

Use OpenAI GPT-5 series for all tasks.

| Model | Use Case | Phase 3 Cost (if 100%) |
|-------|----------|------------------------|
| GPT-5.2 | Default | $110.88/month |
| GPT-5 Mini | Fast tasks | $15.84/month |
| GPT-5 Nano | Routing | $3.17/month |

**Pros:**
- Widest model variety within single provider
- Structured outputs GA (not beta)
- Aggressive pricing on budget models

**Cons:**
- Single point of failure
- GPT-5.2 structured output less refined than Claude for planning
- Missing computer use capability

### Option 3: Single Provider (Google Only)

Use Google Gemini series for all tasks.

| Model | Use Case | Phase 3 Cost (if 100%) |
|-------|----------|------------------------|
| Gemini 3 Pro | Complex | $102.40/month |
| Gemini 2.5 Flash | Default | $19.62/month |
| Gemini 2.0 Flash | Routing | $3.90/month |

**Pros:**
- Lowest overall cost
- 1M+ token context windows
- Free tier available for experimentation

**Cons:**
- Gemini 3 still in Preview (not GA)
- Gemini 2.0 Flash deprecating March 2026
- Single point of failure

### Option 4: Hybrid Strategy with Tiered Routing (Recommended)

Use different providers and model tiers optimized for different task types:

| Task Type | Primary Model | Fallback Model |
|-----------|---------------|----------------|
| Planning & research | Claude Opus 4.5 | Gemini 3 Pro / GPT-5.2 |
| Orchestration & tool use | Claude Haiku 4.5 | Gemini 2.5 Flash / GPT-5 Mini |
| Document generation | Claude Haiku 4.5 | Gemini 2.5 Flash |

**Pros:**
- Optimal capability for each task type (frontier for planning, reliable for orchestration)
- Redundancy across providers (no single point of failure)
- Aligns with "LLM-agnostic" principle
- ~52% cost savings vs all-Opus approach while maintaining planning quality

**Cons:**
- More complex implementation (abstraction layer required)
- Multiple billing relationships
- Must carefully route tasks to appropriate models

**Critical note**: This option explicitly **excludes Gemini 2.0 Flash** despite its low cost ($0.10/$0.40). Its weak instruction following makes it unsuitable for orchestration tasks that involve tool calling.

### Option 5: API Aggregator (OpenRouter)

Use OpenRouter as single API endpoint with automatic model routing.

**Pros:**
- Single API, multiple providers
- Built-in fallback and load balancing
- Simplified billing

**Cons:**
- Additional vendor dependency
- Markup on API costs (~10-20%)
- Less control over routing logic
- Potential latency overhead

---

## Decision

We will implement **Option 4: Hybrid Strategy with Tiered Routing**, with an emphasis on **frontier models for planning** and **reliable mid-tier models for orchestration**.

**Primary provider**: Anthropic Claude
- **Claude Opus 4.5** for all planning and research tasks (requires frontier reasoning to generate well-rounded choices)
- **Claude Haiku 4.5** for orchestration, tool calling, and document generation (reliable instruction following)

**Secondary provider**: Google Gemini
- **Gemini 3 Pro** for planning fallback (frontier reasoning, 1M context)
- **Gemini 2.5 Flash** for orchestration fallback (stable, reliable instruction following)
- **Gemini 2.0 Flash excluded** — weak instruction following and deprecating March 2026

**Tertiary provider**: OpenAI GPT-5.2
- **GPT-5.2** as planning fallback (comparable frontier reasoning)
- **GPT-5 Mini** as orchestration fallback (reliable tool use)

---

## Rationale

### Why Frontier Models for Planning?

Planning tasks in Compass are fundamentally different from instruction-following tasks:

1. **Generating choices, not following orders**: The planning workflow requires the model to generate sensible, well-rounded options for users during OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND stages. This requires anticipating user needs and trade-offs—not just following explicit instructions.

2. **Nuanced judgment**: Deciding what questions to ask, what trade-offs to surface, and how to synthesize research into actionable recommendations requires frontier-level reasoning.

3. **Cost is not the constraint**: At ~$79/month (Phase 3) for planning with Opus 4.5, we're using only ~10% of our budget ceiling. Quality of planning outputs directly impacts user value.

### Why Mid-Tier Models for Orchestration?

Orchestration tasks (routing, tool calling, classification) don't require deep reasoning but **do require reliable instruction following**:

1. **Tool use demands compliance**: Unreliable instruction following leads to malformed tool calls, incorrect routing, and cascading failures.

2. **Cheap ≠ Reliable**: Models like Gemini 2.0 Flash and GPT-5 Nano are cheap but have notably weaker instruction compliance. The cost savings (~$15/month) aren't worth the reliability risk.

3. **Haiku 4.5 hits the sweet spot**: At $1/$5 per million tokens, Haiku provides reliable instruction following at 5× lower cost than Sonnet.

### Why Exclude Gemini 2.0 Flash?

Despite attractive pricing ($0.10/$0.40 per MTok), Gemini 2.0 Flash is **not suitable** for Compass:

1. **Deprecation**: Scheduled end-of-life March 31, 2026—within our Phase 1 timeline
2. **Weak instruction following**: Notably worse than Gemini 2.5 Flash on tool calling and structured output compliance
3. **Risk/reward imbalance**: Saves ~$10-15/month vs Gemini 2.5 Flash, but introduces reliability concerns

### Cost Projection

| Scenario | Phase 1 | Phase 3 |
|----------|---------|---------|
| All Claude Opus 4.5 | $56.40 | $225.60 |
| **Hybrid (recommended)** | **$27.07** | **$108.27** |
| Budget ceiling | $200.00 | $800.00 |
| **Headroom** | **86%** | **87%** |

---

## Consequences

### Positive

- **Significant cost savings**: 56% reduction vs single-provider approach
- **Redundancy**: No single point of failure for LLM operations
- **Flexibility**: Can adjust routing percentages as usage patterns emerge
- **Future-proof**: Abstraction layer enables easy provider changes

### Negative

- **Implementation complexity**: Requires abstraction layer (Area 02)
- **Testing overhead**: Must test behavior across multiple providers
- **Billing complexity**: Three vendor relationships to manage
- **Potential inconsistency**: Responses may vary between providers during failover

### Neutral

- **Monitoring requirements**: Need observability across all providers
- **Documentation needs**: Must document provider-specific behaviors
- **Vendor relationship management**: Standard enterprise consideration

---

## Reversibility

**Easy** — This decision is easily reversible with proper abstraction:

1. The abstraction layer (Area 02) isolates provider-specific code
2. Routing configuration can shift 100% to any single provider
3. No data lock-in with any provider
4. Migration requires only configuration changes, not code rewrites

---

## Notes for Area 02 (LLM Orchestration)

The orchestration layer must support:

1. **Provider abstraction**: Uniform interface across Claude, OpenAI, Gemini
2. **Model router**: Task classification → model selection based on task type:
   - Planning tasks → Frontier models (Opus 4.5, Gemini 3 Pro, GPT-5.2)
   - Orchestration tasks → Mid-tier with reliable instruction following (Haiku 4.5, Gemini 2.5 Flash, GPT-5 Mini)
3. **Fallback chain**: Primary → Secondary → Tertiary with automatic failover
4. **Cost tracking**: Per-request cost estimation and budget enforcement
5. **Rate limit handling**: Queue management and exponential backoff

**Critical design consideration**: The orchestration layer itself uses LLMs for routing and tool calling. These orchestration tasks require models with **reliable instruction following**, not just cheap inference. The model router must use Haiku 4.5 / Gemini 2.5 Flash / GPT-5 Mini—not GPT-5 Nano or Gemini 2.0 Flash.

**Why this matters**: If the orchestration layer uses a model with weak instruction following, tool calls may be malformed, routing decisions may be inconsistent, and the entire system becomes unreliable. The ~$15/month savings from using cheaper models is not worth this risk.

Recommended approach: Lightweight custom abstraction or Vercel AI SDK rather than heavy frameworks (LangChain, LlamaIndex), per Compass principle of "common stacks, strong docs, simple patterns."

---

## Related Documents

- **RF-01-09**: LLM Provider Research Findings (companion research)
- **Compass System Definition**: §1.7 (LLM-agnostic), §4.1 (Budget)
- **ADR-02-01**: LLM Orchestration Selection (pending, informed by this decision)

---

*End of LLM Provider Selection (ADR-09-01)*
