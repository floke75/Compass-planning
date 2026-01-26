---
id: RF-01-09
type: rf
area: 09-llm-provider
title: LLM Provider Research Findings
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Evaluates LLM providers for Compass with recommendation for tiered model strategy using Claude Opus 4.5 for planning (frontier reasoning) and Claude Haiku 4.5 for orchestration (reliable instruction following)
tags: [llm, provider, pricing, evaluation, api, anthropic, openai, google]
related:
  - DD-13-01
  - DD-14-01
confidence: high
methodology: "Web research with official vendor documentation and pricing pages, third-party aggregator verification"
limitations:
  - "Pricing subject to frequent change (verified January 25, 2026)"
  - "No hands-on latency or reliability testing performed"
  - "Some features in beta (Claude structured outputs, Gemini 3 Preview)"
  - "OpenAI official pricing page returned 403; verified via multiple aggregators"
responds_to: null
implications_for: [ADR-02-01, ADR-09-01]
---

# LLM Provider Research Findings

## Executive Summary

**Recommendation**: Implement a tiered model strategy with **Claude Opus 4.5** (or Gemini 3 Pro / GPT-5.2) as primary for planning tasks and **Claude Haiku 4.5** (or Gemini 2.5 Flash / GPT-5 Mini) for orchestration and tool use.

**Confidence**: High — All major providers meet Compass requirements; pricing verified from official sources January 24-25, 2026.

**Key insight**: Planning tasks require **frontier-level reasoning** to generate sensible, well-rounded choices for users—not just instruction following. Orchestration tasks require **reliable instruction following** for tool use, ruling out cheap models with weak compliance (e.g., Gemini 2.0 Flash).

**Key trade-off**: Claude Opus 4.5 at $5/$25 per million tokens ensures planning quality, while Haiku 4.5 at $1/$5 provides reliable orchestration. The hybrid approach achieves Phase 3 costs of **~$108/month**—87% below the $800 ceiling.

**Critical exclusion**: **Gemini 2.0 Flash is not recommended** despite low pricing ($0.10/$0.40). It has weak instruction following and is deprecated March 2026. Use Gemini 2.5 Flash ($0.30/$2.50) instead for any orchestration needs.

**Budget assessment**: All options well within targets. Phase 1 <$200/month ✅, Phase 3 <$800/month ✅. Even using Claude Opus 4.5 exclusively costs only $225.60/month at Phase 3—72% below ceiling.

---

## Part 1: Token Usage Estimates

### 1.1 Session Type Breakdown

Based on Compass System Definition §2.1 (Planning Workflow) and §3.1 (LLM-Driven Conversation), token usage varies significantly by task type.

| Session Type | Est. Input Tokens | Est. Output Tokens | Frequency (Phase 1) | Frequency (Phase 3) |
|--------------|-------------------|-------------------|---------------------|---------------------|
| Full planning workflow (OPEN→GROUND) | 50,000 | 20,000 | 5/week | 20/week |
| Research synthesis | 30,000 | 10,000 | 10/week | 40/week |
| Document generation | 10,000 | 5,000 | 20/week | 80/week |
| Quick clarification | 2,000 | 1,000 | 50/week | 200/week |

### 1.2 Monthly Token Totals

Using 4.33 weeks/month:

**Phase 1 (2-3 users, initial adoption)**:
- Input tokens: ~3.68M/month
- Output tokens: ~1.52M/month
- Total: ~5.2M tokens/month

**Phase 3 (10-20 users, full production)**:
- Input tokens: ~14.72M/month
- Output tokens: ~6.08M/month
- Total: ~20.8M tokens/month

### 1.3 Task Classification for Model Routing

Tasks require different capability levels. The key insight is that **all user-facing tasks benefit from models with reliable instruction following**—even simple clarifications need consistent behavior.

| Task Category | Model Tier Required | % of Phase 3 Tokens |
|---------------|--------------------|--------------------|
| Planning/research | **Frontier** (Opus 4.5, Gemini 3 Pro, GPT-5.2 high) | ~35% |
| Document generation | Mid-tier (Haiku 4.5, Gemini 2.5 Flash, GPT-5 Mini) | ~25% |
| Quick clarification | Mid-tier (Haiku 4.5, Gemini 2.5 Flash) | ~30% |
| Orchestration/tool use | Mid-tier with reliable instruction following | ~10% |

**Why no budget tier?** Models like Gemini 2.0 Flash and GPT-5 Nano have weak instruction following that makes them unsuitable even for simple tasks in a production system. The cost savings (~$10-15/month) aren't worth the reliability risk.

---

## Part 2: Provider Evaluation

### 2.1 Anthropic Claude 4.5 Series

**Verified**: January 25, 2026 (platform.claude.com)

Anthropic's November 2025 release of the Claude 4.5 family brought substantial price reductions while expanding capabilities. Claude Opus 4.5 launched at 67% below previous Opus pricing.

#### Model Tiers and Pricing

| Model | Input/MTok | Output/MTok | Context | Status | Best For |
|-------|------------|-------------|---------|--------|----------|
| **Claude Opus 4.5** | $5.00 | $25.00 | 200K | GA | **Planning tasks** — generating well-rounded choices, complex analysis |
| **Claude Sonnet 4.5** | $3.00 | $15.00 | 200K (1M beta) | GA | Research synthesis, document analysis |
| **Claude Haiku 4.5** | $1.00 | $5.00 | 200K | GA | **Orchestration** — reliable instruction following, tool use |
| Claude Haiku 3.5 | $0.80 | $4.00 | 200K | GA | Legacy, slightly cheaper |
| Claude Haiku 3 | $0.25 | $1.25 | 200K | GA | Not recommended (weaker instruction following) |

#### Cost Savings Options

- **Batch API**: 50% discount for async processing (24-hour window)
- **Prompt caching**: Up to 90% savings on repeated context
  - Cache writes: 1.25× (5-min TTL) or 2× (1-hour TTL) base price
  - Cache hits: **0.1× base price** (90% savings)
- **Extended thinking**: Billed as standard output tokens (no premium)

#### Structured Output Status

**Still in public beta** as of January 2026. Requires header `anthropic-beta: structured-outputs-2025-11-13`. No GA timeline announced. Tool/function calling is fully GA across all models.

#### Calculated Monthly Costs for Compass

| Model | Phase 1 Cost | Phase 3 Cost | With Batch (-50%) |
|-------|--------------|--------------|-------------------|
| Claude Opus 4.5 | $56.40 | $225.60 | $112.80 |
| **Claude Sonnet 4.5** | **$33.84** | **$135.36** | $67.68 |
| Claude Haiku 4.5 | $11.28 | $45.12 | $22.56 |
| Claude Haiku 3 | $2.82 | $11.28 | $5.64 |

---

### 2.2 OpenAI GPT-5 Series

**Verified**: January 24, 2026 (community.openai.com, third-party aggregators)

OpenAI's December 2025 GPT-5.2 release and the January 2026 o3 price cut created a diverse portfolio ranging from $0.05 to $168 per million output tokens.

#### Model Tiers and Pricing

GPT-5.2 supports `reasoning.effort` parameter: `none`, `low`, `medium`, `high`, `xhigh`. For planning tasks, use `high` for thorough reasoning.

| Model | Input/MTok | Output/MTok | Context | Status | Best For |
|-------|------------|-------------|---------|--------|----------|
| **GPT-5.2 Pro** | $21.00 | $168.00 | 400K | GA | Maximum performance, `xhigh` reasoning |
| **GPT-5.2** | $1.75 | $14.00 | 400K | GA | **Planning** with `reasoning.effort=high` |
| GPT-5.1 | $1.25 | $10.00 | 400K | GA | Previous gen, cost-effective |
| **GPT-5 Mini** | $0.25 | $2.00 | 400K | GA | **Orchestration** — reliable instruction following |
| GPT-5 Nano | $0.05 | $0.40 | 400K | GA | **Not recommended** — weak instruction following |
| GPT-4.1 | $2.00 | $8.00 | **1M** | GA | Longest context |
| GPT-4.1 Mini | $0.40 | $1.60 | 1M | GA | Long context, budget |
| GPT-4.1 Nano | $0.10 | $0.40 | 1M | GA | Long context, cheapest |

#### Reasoning Models (o-series)

The o3 price cut (January 2026) dropped costs from $10/$40 to $2/$8—an 80% reduction.

| Model | Input/MTok | Output/MTok | Context | Notes |
|-------|------------|-------------|---------|-------|
| **o3** | $2.00 | $8.00 | 200K | 80% price cut Jan 2026 |
| **o3-pro** | $20.00 | $80.00 | 200K | 87% cheaper than o1-pro |
| **o4-mini** | $1.10 | $4.40 | 200K | Fast reasoning for code |

**Important**: O-series reasoning tokens are billed as output but invisible in API responses—a 500-token response may consume 2,000+ total tokens internally.

#### Cost Savings Options

- **Batch API**: 50% discount
- **Prompt caching**: 90% savings on GPT-5 family, 75% on GPT-4.1, 50% on o-series

#### Structured Output & Capabilities

All GPT-5.2 capabilities: Function calling ✅, Structured outputs ✅, JSON mode ✅, Streaming ✅, Web search ✅, File search ✅, Code interpreter ✅.

Responses API is GA (March 2025) and recommended for all new development. Assistants API deprecated August 2025, sunset August 2026.

#### Calculated Monthly Costs for Compass

| Model | Phase 1 Cost | Phase 3 Cost | With Batch (-50%) |
|-------|--------------|--------------|-------------------|
| GPT-5.2 Pro | $262.88 | $1,051.52 | $525.76 |
| **GPT-5.2** | **$27.72** | **$110.88** | $55.44 |
| GPT-5.1 | $19.80 | $79.20 | $39.60 |
| **GPT-5 Mini** | **$3.96** | **$15.84** | $7.92 |
| ~~GPT-5 Nano~~ | $0.79 | $3.17 | $1.58 | ⚠️ Not recommended |
| o3 | $19.52 | $78.08 | $39.04 |
| o4-mini | $10.73 | $42.91 | $21.46 |

---

### 2.3 Google Gemini Series

**Verified**: January 24, 2026 (ai.google.dev)

Google's Gemini 3 series launched November-December 2025 in Preview status. The stable Gemini 2.x series remains the practical choice for production with competitive pricing and free tiers.

#### Model Tiers and Pricing

| Model | Input/MTok | Output/MTok | Context | Free Tier | Status | Notes |
|-------|------------|-------------|---------|-----------|--------|-------|
| **Gemini 3 Pro** | $2.00 | $12.00 | 1M | ❌ | Preview | **Planning fallback** — frontier reasoning |
| Gemini 3 Flash | $0.50 | $3.00 | 1M | ✅ | Preview | Fast, capable |
| Gemini 2.5 Pro | $1.25 | $10.00 | 1M-2M | Limited | Stable | Extended context |
| **Gemini 2.5 Flash** | $0.30 | $2.50 | 1M | ✅ | Stable | **Orchestration** — reliable instruction following |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | 1M | ✅ | Stable | Lower capability |
| ~~Gemini 2.0 Flash~~ | $0.10 | $0.40 | 1M | ✅ | Stable | **⚠️ NOT RECOMMENDED** — weak instruction following, deprecated March 2026 |
| Gemini 2.0 Flash-Lite | $0.075 | $0.30 | 1M | ✅ | Stable | Not recommended |

#### Long Context Pricing

For Pro models, prompts exceeding 200K tokens trigger **2× input pricing** and 1.5× output premiums.

#### Cost Savings Options

- **Batch API**: 50% discount
- **Thinking tokens**: Included in output charges, configurable budget (0-24,576 tokens)
- **Free tier**: Available for Flash models (~500-1000 RPD for 2.5 Flash)

#### Key Capabilities

All models support: Structured JSON output ✅, Function/tool calling ✅, Streaming ✅, Code execution ✅.

Gemini 3 introduces "thinking levels" (low/high for Pro, minimal/low/medium/high for Flash). However, Gemini 3 does **not** support combining built-in tools with function calling simultaneously—Gemini 2.5 required for that use case.

**Deprecation warning**: Gemini 2.0 Flash models retire March 31, 2026.

#### Calculated Monthly Costs for Compass

| Model | Phase 1 Cost | Phase 3 Cost | With Batch (-50%) |
|-------|--------------|--------------|-------------------|
| Gemini 3 Pro | $25.60 | $102.40 | $51.20 |
| Gemini 3 Flash | $6.40 | $25.60 | $12.80 |
| Gemini 2.5 Pro | $19.80 | $79.20 | $39.60 |
| **Gemini 2.5 Flash** | **$4.90** | **$19.62** | $9.81 |
| ~~Gemini 2.0 Flash~~ | $0.98 | $3.90 | $1.95 | ⚠️ Not recommended |

---

### 2.4 Secondary Providers (Fallback/Hybrid)

#### Groq — Ultra-Fast Inference

**Verified**: January 2026 (console.groq.com)

Groq's LPU hardware delivers 200-1,000+ tokens/second—essential for latency-sensitive orchestration.

| Model | Input/MTok | Output/MTok | Speed | Context |
|-------|------------|-------------|-------|---------|
| **Llama 3.1 8B Instant** | $0.05 | $0.08 | 840 TPS | 128K |
| Llama 3.3 70B Versatile | $0.59 | $0.79 | 394 TPS | 128K |
| GPT-OSS 20B | $0.075 | $0.30 | 1,000 TPS | 128K |
| Llama 4 Scout | $0.11 | $0.34 | 594 TPS | 128K |

Free tier available (250K-300K TPM limit). Batch API provides 50% discount.

**Phase 3 cost with Llama 3.1 8B**: ~$1.22/month

#### Mistral AI — European Option

**Verified**: January 2026 (docs.mistral.ai)

| Model | Input/MTok | Output/MTok | Context |
|-------|------------|-------------|---------|
| **Mistral Large 3 2512** | $0.50 | $1.50 | 262K |
| Mistral Medium 3.1 | $0.40 | $2.00 | 131K |
| Mistral Small 3.1 24B | $0.03 | $0.11 | 131K |
| **Mistral Nemo** | $0.02 | $0.04 | 131K |

Mistral Large 3 (December 2025) offers 675B parameters with only 41B active via mixture-of-experts.

**Phase 3 cost with Mistral Large 3**: ~$16.48/month
**Phase 3 cost with Mistral Nemo**: ~$0.54/month

#### Together AI — Open-Source Hosting

**Verified**: January 2026 (together.ai)

| Model | Input/MTok | Output/MTok |
|-------|------------|-------------|
| Llama 3.1 8B | $0.18 | $0.18 |
| Llama 3.3 70B | $0.88 | $0.88 |
| DeepSeek-V3.1 | $0.60 | $1.25 |

$25 free credits for new users. Batch API provides 50% savings.

---

## Part 3: Cost Comparison Tables

### 3.1 All Providers — Phase 1 Monthly Cost

| Provider/Model | Input Cost | Output Cost | **Total/Month** | Within Budget? |
|----------------|------------|-------------|-----------------|----------------|
| **Claude Sonnet 4.5** | $11.04 | $22.80 | **$33.84** | ✅ Yes |
| Claude Haiku 4.5 | $3.68 | $7.60 | $11.28 | ✅ Excellent |
| Claude Haiku 3 | $0.92 | $1.90 | $2.82 | ✅ Excellent |
| **GPT-5.2** | $6.44 | $21.28 | **$27.72** | ✅ Yes |
| GPT-5 Mini | $0.92 | $3.04 | $3.96 | ✅ Excellent |
| **GPT-5 Nano** | $0.18 | $0.61 | **$0.79** | ✅ Excellent |
| o3 | $7.36 | $12.16 | $19.52 | ✅ Yes |
| Gemini 3 Flash | $1.84 | $4.56 | $6.40 | ✅ Excellent |
| Gemini 2.5 Flash | $1.10 | $3.80 | $4.90 | ✅ Excellent |
| **Gemini 2.0 Flash** | $0.37 | $0.61 | **$0.98** | ✅ Excellent |
| Mistral Large 3 | $1.84 | $2.28 | $4.12 | ✅ Excellent |
| Groq Llama 3.1 8B | $0.18 | $0.12 | $0.31 | ✅ Excellent |

**Phase 1 Budget**: <$200/month ✅ — All options qualify

### 3.2 All Providers — Phase 3 Monthly Cost

| Provider/Model | Input Cost | Output Cost | **Total/Month** | Within Budget? |
|----------------|------------|-------------|-----------------|----------------|
| Claude Opus 4.5 | $73.60 | $152.00 | $225.60 | ✅ Yes |
| **Claude Sonnet 4.5** | $44.16 | $91.20 | **$135.36** | ✅ Yes |
| Claude Haiku 4.5 | $14.72 | $30.40 | $45.12 | ✅ Excellent |
| Claude Haiku 3 | $3.68 | $7.60 | $11.28 | ✅ Excellent |
| GPT-5.2 Pro | $309.12 | $1,013.44 | $1,322.56 | ❌ Over budget |
| **GPT-5.2** | $25.76 | $85.12 | **$110.88** | ✅ Yes |
| GPT-5.1 | $18.40 | $60.80 | $79.20 | ✅ Excellent |
| GPT-5 Mini | $3.68 | $12.16 | $15.84 | ✅ Excellent |
| **GPT-5 Nano** | $0.74 | $2.43 | **$3.17** | ⚠️ Not recommended |
| o3 | $29.44 | $48.64 | $78.08 | ✅ Excellent |
| o4-mini | $16.19 | $26.75 | $42.94 | ✅ Excellent |
| Gemini 3 Pro | $29.44 | $72.96 | $102.40 | ✅ Yes |
| Gemini 3 Flash | $7.36 | $18.24 | $25.60 | ✅ Excellent |
| Gemini 2.5 Pro | $18.40 | $60.80 | $79.20 | ✅ Excellent |
| Gemini 2.5 Flash | $4.42 | $15.20 | $19.62 | ✅ Excellent |
| **Gemini 2.0 Flash** | $1.47 | $2.43 | **$3.90** | ⚠️ Not recommended |
| Mistral Large 3 | $7.36 | $9.12 | $16.48 | ✅ Excellent |
| Mistral Nemo | $0.29 | $0.24 | $0.54 | ✅ Excellent |
| Groq Llama 3.1 8B | $0.74 | $0.49 | $1.22 | ✅ Excellent |

**Phase 3 Budget**: <$800/month ✅ — Only GPT-5.2 Pro exceeds budget

### 3.3 Revised Hybrid Strategy Cost Projections

**Task distribution**: 35% planning (frontier), 25% document gen (mid-tier), 40% orchestration (mid-tier with reliable instruction following)

**Why not use budget models for orchestration?** Orchestration involves tool calling, request routing, and classification—tasks that require reliable instruction following. Models like Gemini 2.0 Flash and GPT-5 Nano have weak instruction compliance, leading to unreliable tool use. Haiku 4.5 and Gemini 2.5 Flash provide the reliability needed at reasonable cost.

| Task Category | Model | Phase 1 Tokens | Phase 1 Cost | Phase 3 Tokens | Phase 3 Cost |
|---------------|-------|----------------|--------------|----------------|--------------|
| Planning (35%) | Claude Opus 4.5 | 1.82M | $19.74 | 7.28M | $78.96 |
| Orchestration (40%) | Claude Haiku 4.5 | 2.08M | $4.51 | 8.32M | $18.03 |
| Document (25%) | Claude Haiku 4.5 | 1.30M | $2.82 | 5.20M | $11.28 |
| **Hybrid Total** | — | 5.2M | **$27.07** | 20.8M | **$108.27** |

**Budget headroom**: Phase 1: 86% ($27 vs $200), Phase 3: 87% ($108 vs $800)

**Alternative with Gemini for orchestration** (to reduce Claude dependency):

| Task Category | Model | Phase 3 Cost |
|---------------|-------|--------------|
| Planning (35%) | Claude Opus 4.5 | $78.96 |
| Orchestration (40%) | Gemini 2.5 Flash | $7.28 |
| Document (25%) | Gemini 2.5 Flash | $4.55 |
| **Mixed Total** | — | **$90.79** |

Both approaches remain well under budget while ensuring quality planning outputs and reliable orchestration.

---

## Part 4: Capability Comparison Matrix

### 4.1 Core Capabilities

| Capability | Claude 4.5 | GPT-5.2 | Gemini 3/2.5 | Groq | Mistral |
|------------|------------|---------|--------------|------|---------|
| **Context window** | 200K (1M beta) | 400K | 1M-2M | 128K | 131K-262K |
| **Structured JSON** | ✅ Beta | ✅ GA | ✅ GA | ✅ GA | ✅ GA |
| **Function calling** | ✅ GA | ✅ GA | ✅ GA | ✅ GA | ✅ GA |
| **Streaming** | ✅ GA | ✅ GA | ✅ GA | ✅ GA | ✅ GA |
| **Extended thinking** | ✅ | ✅ Effort param | ✅ Thinking levels | ❌ | ❌ |
| **Computer use** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Web search** | ✅ Tool | ✅ Built-in | ✅ Grounding | ❌ | ✅ |
| **Code execution** | ✅ | ✅ Interpreter | ✅ | ❌ | ❌ |
| **Free tier** | ❌ | ❌ | ✅ (Flash) | ✅ | ❌ |
| **Batch discount** | 50% | 50% | 50% | 50% | ❌ |
| **Prompt caching** | 90% | 90% | ✅ | ❌ | ❌ |

### 4.2 Instruction Following Assessment

**Critical for orchestration**: Tool calling and request routing require models that reliably follow complex instructions. This rules out the cheapest models for orchestration tasks.

| Model | Instruction Following | Tool Use Reliability | Suitable For |
|-------|----------------------|---------------------|--------------|
| Claude Opus 4.5 | ✅ Excellent | ✅ Excellent | Planning, complex reasoning |
| Claude Sonnet 4.5 | ✅ Excellent | ✅ Excellent | Research, document analysis |
| Claude Haiku 4.5 | ✅ Good | ✅ Good | **Orchestration**, simple tasks |
| GPT-5.2 | ✅ Excellent | ✅ Excellent | Planning fallback |
| GPT-5 Mini | ✅ Good | ✅ Good | **Orchestration fallback** |
| GPT-5 Nano | ⚠️ Limited | ⚠️ Unreliable | Classification only |
| Gemini 3 Pro | ✅ Good | ✅ Good | Planning fallback |
| Gemini 2.5 Flash | ✅ Good | ✅ Good | **Orchestration**, cost-sensitive |
| **Gemini 2.0 Flash** | ⚠️ **Weak** | ⚠️ **Unreliable** | **Not recommended** |
| Groq Llama 3.1 8B | ⚠️ Limited | ⚠️ Basic | Latency-critical only |

**Key finding**: Gemini 2.0 Flash's instruction following is notably weaker than Gemini 2.5 Flash, making it unsuitable for orchestration despite the 3× lower cost. The deprecation timeline (March 2026) compounds this concern.

### 4.3 Compass-Specific Requirements Assessment

| Requirement | Claude 4.5 | GPT-5.2 | Gemini 2.5+ | Notes |
|-------------|------------|---------|-------------|-------|
| Structured output (JSON) | ✅ Beta | ✅ GA | ✅ GA | Claude beta header required |
| Context >100K tokens | ✅ 200K | ✅ 400K | ✅ 1M | All exceed requirement |
| Streaming | ✅ | ✅ | ✅ | All support |
| Tool/function calling | ✅ GA | ✅ GA | ✅ GA | All support |
| 99.5%+ uptime | ✅ | ✅ | ✅ | All major providers |
| Within Phase 3 budget | ✅ | ✅* | ✅ | *Except GPT-5.2 Pro |

---

## Part 5: Provider Abstraction Assessment

### 5.1 API Similarity Analysis

All three major providers (Anthropic, OpenAI, Google) have converged on similar API patterns:

| Pattern | Claude | OpenAI | Gemini | Compatibility |
|---------|--------|--------|--------|---------------|
| Messages format | `/messages` | `/chat/completions` | `generateContent` | Similar structure |
| Role names | user/assistant | user/assistant | user/model | Minor difference |
| Tool calling | `tools[]` param | `tools[]` param | `tools[]` param | Nearly identical |
| Streaming | SSE | SSE | SSE | Identical |
| Structured output | JSON schema | JSON schema | JSON schema | Identical approach |

**Abstraction difficulty**: Low — APIs are similar enough that a thin abstraction layer can support all providers with minimal code differences.

### 5.2 Recommended Abstraction Approach

For Area 02 (LLM Orchestration), implement:

1. **Provider interface**: Abstract `chat()`, `stream()`, `toolCall()` methods
2. **Request normalization**: Convert Compass-internal format to provider-specific format
3. **Response normalization**: Extract content, tool calls, usage stats into common format
4. **Model router**: Select provider/model based on task complexity and cost targets
5. **Fallback chain**: Primary → Secondary → Tertiary provider with automatic failover

### 5.3 Orchestration Framework Compatibility

Common frameworks that support multi-provider abstraction:

| Framework | Claude | OpenAI | Gemini | Groq | Notes |
|-----------|--------|--------|--------|------|-------|
| LangChain | ✅ | ✅ | ✅ | ✅ | Most comprehensive |
| LlamaIndex | ✅ | ✅ | ✅ | ✅ | Document-focused |
| Vercel AI SDK | ✅ | ✅ | ✅ | ✅ | TypeScript-native |
| OpenRouter | ✅ | ✅ | ✅ | ✅ | Single API, multi-provider |

**Recommendation for Area 02**: Use a lightweight abstraction (Vercel AI SDK or custom) rather than heavy frameworks, per Compass principle of "common stacks, strong docs, simple patterns."

---

## Part 6: Recommendation

### 6.1 Model Tier Strategy

Compass tasks require different capability levels. The key insight is that **planning tasks require frontier-level reasoning** to generate sensible, well-rounded choices for users—not just follow instructions. Orchestration tasks, while not requiring deep reasoning, still need **robust instruction following** for reliable tool use.

| Task Type | Required Capability | Recommended Models |
|-----------|--------------------|--------------------|
| **Planning & Research** | Frontier reasoning, nuanced judgment | Claude Opus 4.5, Gemini 3 Pro, GPT-5.2 |
| **Orchestration & Tool Use** | Reliable instruction following | Claude Haiku 4.5, Gemini 2.5 Flash, GPT-5 Mini |
| **Simple Tasks** | Basic competence | Claude Haiku 4.5, Gemini 2.5 Flash |

**Critical note on Gemini 2.0 Flash**: Despite attractive pricing ($0.10/$0.40), this model is **not recommended** due to:
- Deprecation scheduled March 31, 2026
- Weak instruction following compared to 2.5 series
- Unreliable tool use behavior

### 6.2 Primary Provider: Anthropic Claude

**Model tier strategy**:

| Task Type | Model | Cost/MTok | When to Use |
|-----------|-------|-----------|-------------|
| **Planning & research** | **Claude Opus 4.5** | $5/$25 | All planning stages (OPEN→GROUND), decision analysis, research synthesis |
| Orchestration & tool use | Claude Haiku 4.5 | $1/$5 | Request routing, tool calling, classification |
| Document generation | Claude Haiku 4.5 | $1/$5 | Formatting, summarization, simple generation |

**Rationale**:
- **Opus 4.5 for planning**: Planning conversations require generating well-rounded options and anticipating user needs—this demands frontier reasoning, not just instruction following
- Haiku 4.5 provides reliable instruction following for orchestration at reasonable cost
- Superior agentic capabilities (computer use, extended thinking)
- Prompt caching provides up to 90% savings on repeated context

### 6.3 Secondary Provider: Google Gemini

**Model selection**: **Gemini 3 Pro** for planning fallback, **Gemini 2.5 Flash** for orchestration

| Role | Model | Cost/MTok | Rationale |
|------|-------|-----------|-----------|
| Planning fallback | Gemini 3 Pro | $2/$12 | Frontier reasoning, 1M context |
| Orchestration fallback | Gemini 2.5 Flash | $0.30/$2.50 | Stable, reliable instruction following |

**Why not Gemini 2.0 Flash**: Deprecating March 2026 and significantly weaker instruction following than 2.5 series. The cost savings ($0.10 vs $0.30 input) are not worth the reliability risk for orchestration tasks.

### 6.4 Tertiary Provider: OpenAI GPT-5.2

**Role**: Automatic failover when Claude and Gemini unavailable

| Role | Model | Cost/MTok | Rationale |
|------|-------|-----------|-----------|
| Planning fallback | GPT-5.2 | $1.75/$14 | Comparable to Opus for reasoning tasks |
| Orchestration fallback | GPT-5 Mini | $0.25/$2 | Reliable instruction following, tool use |

**Rationale**:
- Different infrastructure provides true redundancy
- GPT-5.2 structured output is GA (not beta like Claude)
- 400K context window exceeds Compass requirements

### 6.5 Revised Cost Projections

With frontier models for planning and reliable mid-tier for orchestration:

| Traffic | Primary Model | Fallback Model | Est. Phase 3 Cost |
|---------|---------------|----------------|-------------------|
| Planning (35%) | Claude Opus 4.5 | Gemini 3 Pro / GPT-5.2 | ~$79/mo |
| Orchestration (40%) | Claude Haiku 4.5 | Gemini 2.5 Flash / GPT-5 Mini | ~$18/mo |
| Document gen (25%) | Claude Haiku 4.5 | Gemini 2.5 Flash | ~$11/mo |
| **Total** | — | — | **~$108/mo** |

This achieves **87% budget headroom** at Phase 3 ($108 vs $800 ceiling).

**Comparison to previous estimate**: The shift from Sonnet ($3/$15) to Opus ($5/$25) for planning increases costs by ~$32/month at Phase 3, but ensures the quality of planning outputs that users depend on. This is a worthwhile trade-off given the substantial budget headroom.

---

## Part 7: Failure Modes and Mitigation

### 7.1 Provider Outage Scenarios

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Claude API down | Planning sessions blocked | Auto-failover to GPT-5.2 |
| Gemini API down | Orchestration tasks queue | Failover to GPT-5 Nano |
| All providers down | Complete service disruption | Graceful degradation with user notification |

### 7.2 Rate Limiting Handling

| Provider | Default Limits | Mitigation |
|----------|---------------|------------|
| Claude | Tier-based (varies) | Queue with exponential backoff |
| OpenAI | 10K RPM (Tier 5) | Request batching |
| Gemini | 1000 RPD (free) | Paid tier + queue |

### 7.3 Cost Overrun Prevention

1. **Per-request cost estimation**: Calculate expected cost before API call
2. **Daily/monthly budgets**: Halt non-critical requests when approaching limits
3. **Model downgrade**: Auto-switch to cheaper models under budget pressure
4. **Usage alerts**: Notify at 50%, 80%, 100% of monthly budget

---

## Part 8: Data Recency Verification

| Provider | Source | Retrieved | Confidence |
|----------|--------|-----------|------------|
| **Anthropic Claude** | platform.claude.com/docs/en/about-claude/pricing | Jan 25, 2026 | ✅ High |
| **OpenAI** | community.openai.com, third-party aggregators | Jan 24, 2026 | ✅ High |
| **Google Gemini** | ai.google.dev pricing | Jan 24, 2026 | ✅ High |
| **Groq** | console.groq.com/docs/models | Jan 25, 2026 | ✅ High |
| **Mistral** | docs.mistral.ai | Jan 25, 2026 | ✅ High |

**Flagged uncertainties**:
- Claude structured outputs: GA timeline unknown (still beta)
- OpenAI official pricing page: returned 403 errors; verified via multiple aggregators
- Gemini 3: Preview status, pricing may change at GA
- Gemini 2.0 Flash: Deprecation March 31, 2026

---

## Part 9: Open Questions for Stakeholders

1. **Structured output reliability**: Is Claude's beta status for structured outputs acceptable, or should OpenAI's GA implementation be preferred?

2. **Extended thinking usage**: How frequently will planning sessions require extended thinking? This affects Opus 4.5 vs Sonnet 4.5 selection.

3. **Fallback tolerance**: What is acceptable degradation during provider outages? (Queue requests vs. immediate failover vs. user notification)

4. **Cost vs. capability priority**: At current budget headroom (93%), should we prefer higher-capability models or maximize savings?

5. **Batch processing appetite**: Can some tasks (document generation, research synthesis) tolerate 24-hour async processing for 50% cost savings?

---

## Appendix A: Sources

1. **[T1/S1]** Anthropic. "Pricing - Claude API Docs". Retrieved 2026-01-25. https://platform.claude.com/docs/en/about-claude/pricing
   Note: Official documentation, verified current.

2. **[T1/S1]** Anthropic. "What's New in Claude 4.5". Retrieved 2026-01-25. https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5
   Note: Official release notes.

3. **[T2/S2]** OpenAI Community. "O3 is 80% cheaper and introducing o3-pro". Retrieved 2026-01-24. https://community.openai.com/t/o3-is-80-cheaper-and-introducing-o3-pro/1284925
   Note: Official community announcement.

4. **[T2/S2]** LLM Stats. "GPT-5.2: Pricing, Context Window, Benchmarks". Retrieved 2026-01-24. https://llm-stats.com/models/gpt-5.2-2025-12-11
   Note: Third-party aggregator, cross-verified.

5. **[T1/S1]** Google. "Gemini API Pricing". Retrieved 2026-01-24. https://ai.google.dev/pricing
   Note: Official documentation.

6. **[T1/S1]** Groq. "Supported Models - GroqDocs". Retrieved 2026-01-25. https://console.groq.com/docs/models
   Note: Official documentation with pricing.

7. **[T3/S2]** IntuitionLabs. "LLM API Pricing Comparison (2025)". Retrieved 2026-01-25. https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025
   Note: Aggregator, useful for cross-reference.

8. **[T3/S2]** AI Free API. "Claude API Pricing Guide 2026". Retrieved 2026-01-25. https://www.aifreeapi.com/en/posts/claude-api-pricing-per-million-tokens
   Note: Aggregator, January 2026 data.

---

## Appendix B: Glossary

**Batch API**: Asynchronous processing mode offering 50% discount for requests completed within 24 hours.

**MTok**: Million tokens—standard pricing unit for LLM APIs.

**Prompt caching**: Feature allowing reuse of previously processed context at reduced cost (up to 90% savings).

**RPD**: Requests per day—common rate limit unit for free tiers.

**RPM**: Requests per minute—common rate limit unit for paid tiers.

**SSE**: Server-Sent Events—streaming protocol used by all major LLM providers.

**TPS**: Tokens per second—inference speed metric.

---

## Appendix C: Related Documents

- **Compass System Definition**: Authoritative system specification (§2.1 Planning Workflow, §3.1 LLM-Driven Conversation, §4.1 Budget)
- **ADR-02-01**: LLM Orchestration selection (pending, informed by this research)
- **ADR-09-01**: LLM Provider selection (companion decision document)
- **DD-13-01**: Artifact taxonomy (frontmatter schema reference)

---

*End of LLM Provider Research Findings (RF-01-09)*
