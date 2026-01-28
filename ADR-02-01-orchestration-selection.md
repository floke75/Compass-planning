---
id: ADR-02-01
type: adr
area: 02-llm-orchestration
title: LLM Orchestration Framework Selection
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Selects Mastra + Vercel AI SDK v6 as the LLM orchestration architecture for Compass planning workflows
tags: [orchestration, llm, framework, mastra, vercel-ai-sdk, architecture, decision]
related:
  - RF-02-01
  - RF-09-01
  - ADR-09-01
  - ADR-01-01
  - DD-13-01
decision_date: 2026-01-25
deciders: [compass-research]
supersedes: null
---

# LLM Orchestration Framework Selection

## Status

Draft — Awaiting stakeholder review.

## Context

Compass requires an LLM orchestration layer to manage planning workflows that span multiple sessions over days or weeks. The system must generate schema-constrained widget specifications, maintain conversation state across server restarts, support branching exploration of alternatives, and abstract across multiple LLM providers (Claude Opus/Haiku 4.5, Gemini 3 Pro, GPT-5.2).

Research findings in RF-02-01 evaluated five approaches: Vercel AI SDK v6, Mastra, LangGraph.js, Instructor, and direct API implementation. The evaluation criteria included structured output reliability, session persistence, provider abstraction, TypeScript quality, and engineering cost.

## Options Considered

### Option 1: Mastra + Vercel AI SDK v6

Mastra provides workflow orchestration with native state machines, suspend/resume capabilities, and thread-based persistence. Built on top of the AI SDK, it inherits the SDK's structured output and provider abstraction without requiring a separate integration layer.

**Pros:**

Directly models Compass's planning workflow with `.then()`, `.branch()`, and `.parallel()` primitives. Thread-based memory with Zod schema validation provides structured state management. Suspend/resume maps to the questioning arc's human-in-the-loop requirements. Mastra's persistence adapters integrate with the Convex backend selected in ADR-01-01. Integration time estimated at 2-3 weeks versus 6-10 weeks for custom alternatives.

**Cons:**

Young framework (seed funding October 2025) with unverified long-term stability. Proprietary DSL requires learning Mastra-specific patterns. Branch visualization and merge logic require custom implementation. $13M funding provides some confidence but doesn't guarantee continued development.

### Option 2: Vercel AI SDK v6 + XState v5

The AI SDK provides structured output and provider abstraction, while XState v5 handles state machine logic. This approach requires building the persistence layer and workflow orchestration manually.

**Pros:**

AI SDK has the highest maintainability score (13/14) and is backed by Vercel. XState is a mature, well-documented state machine library with TypeScript support. Maximum flexibility in implementation choices. No dependency on a young framework.

**Cons:**

Requires 6-10 weeks of custom development for session persistence, workflow management, and branching logic. Ongoing maintenance burden for custom orchestration code. XState integration with LLM workflows requires additional abstraction.

### Option 3: LangGraph.js

LangGraph provides graph-based orchestration with sophisticated checkpointing and time travel capabilities. The checkpointing system directly supports Compass's branching exploration requirement.

**Pros:**

Most powerful branching and rollback capabilities. Checkpointing with time travel enables exploration without losing context. Large community and ecosystem.

**Cons:**

TypeScript quality issues documented in GitHub (ESM/CJS conflicts, type inconsistencies). Zod-to-JSONSchema conversion breaks OpenAI strict mode for widget generation. Python-first development leaves JavaScript documentation lagging. Maintainability score (9/14) falls below threshold for simple codebases.

### Option 4: Do Nothing

Continue without a framework selection, deferring the decision until implementation begins.

**Pros:**

No implementation effort. Retains flexibility to choose based on changing requirements.

**Cons:**

Blocks dependent research areas (RF-07-01/ADR-07-01 Widget Libraries, DD-18-01 Questioning Arc, DD-19-01 Widget Schema) that need to know orchestration patterns. Delays Compass development timeline. Risk of making hasty decisions during implementation.

## Decision

We will use **Mastra + Vercel AI SDK v6** as the LLM orchestration architecture because Mastra directly addresses Compass's workflow requirements while minimizing engineering effort.

The key factors in this decision are that Mastra's workflow primitives map naturally to Compass's planning state machine (OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND), suspend/resume enables the questioning arc's human-in-the-loop design, thread-based persistence integrates with the Convex backend from ADR-01-01, and integration time (2-3 weeks) is 60-70% less than custom alternatives.

If Mastra's DSL proves too constraining during implementation, the fallback strategy is to use AI SDK v6 + XState v5, accepting the additional development time.

## Consequences

### Positive

The primary workflow orchestration requirement is addressed with minimal custom code. Provider abstraction via AI SDK enables the tiered model strategy from ADR-09-01 (Opus 4.5 for planning, Haiku 4.5 for orchestration). Zod schema validation provides type safety across the orchestration layer. Thread-based memory enables multi-week planning sessions with proper state isolation. The architecture supports Areas 07, 18, and 19 with clear integration patterns.

### Negative

Dependency on a young framework introduces long-term stability risk. Mastra's DSL requires the team to learn framework-specific patterns. Branch visualization and merge logic require custom implementation on top of Mastra's primitives. Framework updates may require orchestration code changes.

### Neutral

Both Mastra and the fallback (AI SDK + XState) provide viable paths. The decision optimizes for time-to-implementation while accepting framework commitment risk. Monitoring Mastra's development activity and community adoption should continue.

## Implementation Notes

### Model Routing Configuration

Following ADR-09-01, configure agents for tiered model usage:

```typescript
// Planning agent with extended thinking
const planningAgent = createAgent({
  model: anthropic("claude-opus-4.5"),
  providerOptions: {
    anthropic: { thinking: { type: "enabled", budgetTokens: 12000 } }
  }
});

// Orchestration agent without thinking overhead
const orchestrationAgent = createAgent({
  model: anthropic("claude-haiku-4.5"),
});
```

### Persistence Configuration

Configure Mastra memory to integrate with the Convex backend selected in ADR-01-01. Mastra's thread-based persistence can be configured to use Convex for workflow state storage:

```typescript
const mastra = new Mastra({
  memory: new ConvexAdapter({
    client: convexClient,
  }),
});
```

### Branching Pattern

Implement branch tracking in working memory:

```typescript
const branchSchema = z.object({
  branches: z.array(z.object({
    id: z.string(),
    parentId: z.string().nullable(),
    status: z.enum(['active', 'merged', 'abandoned']),
    threadId: z.string(),
  })),
  activeBranch: z.string(),
});
```

## Risk Mitigation

**Framework abandonment**: Monitor Mastra GitHub activity monthly. If development stalls or community declines, begin migration to AI SDK + XState fallback.

**DSL limitations**: Prototype the full planning workflow early in development. If Mastra's primitives cannot express required transitions, switch to fallback before significant investment.

**Provider beta features**: Claude structured outputs remain in beta. Implement fallback to tool-based extraction if beta behavior changes.

## Related Documents

- **RF-02-01**: LLM Orchestration Framework Research Findings (detailed evaluation)
- **RF-09-01**: LLM Provider Research Findings (model selection)
- **ADR-09-01**: LLM Provider Selection (tiered model strategy)
- **ADR-01-01**: Backend Platform Selection (Convex)
- **DD-13-01**: Artifact Taxonomy (document standards)
- **Compass System Definition**: Authoritative system specification (§2.1, §2.2, §2.6, §3.1)

---

*End of LLM Orchestration Framework Selection (ADR-02-01)*
