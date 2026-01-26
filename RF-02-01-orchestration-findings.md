---
id: RF-02-01
type: rf
area: 02-llm-orchestration
title: LLM Orchestration Framework Research Findings
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Evaluates LLM orchestration frameworks for Compass, recommending Mastra + Vercel AI SDK for stateful planning workflows with structured output generation
tags: [orchestration, llm, framework, mastra, vercel-ai-sdk, langchain, typescript]
related:
  - DD-13-01
  - DD-14-01
  - RF-01-09
  - ADR-09-01
confidence: high
methodology: "Web research with official vendor documentation, GitHub repositories, community discussions, and third-party comparison reports"
limitations:
  - "Mastra is a young framework (2025), long-term stability unverified"
  - "No hands-on performance benchmarking conducted"
  - "LangGraph TypeScript issues based on community reports, not direct testing"
  - "Instructor TypeScript version activity may have changed since research"
responds_to: null
implications_for: [ADR-02-01, ADR-07-01, DD-18-01, DD-19-01]
---

# LLM Orchestration Framework Research Findings

## Executive Summary

**Recommendation**: Implement a two-layer architecture combining **Mastra** for workflow orchestration and **Vercel AI SDK v6** for structured output generation and provider abstraction.

**Confidence**: High — Both frameworks have strong backing (Vercel for AI SDK, YC/Gradient/Vercel for Mastra), excellent TypeScript support, and directly address Compass requirements.

**Key insight**: Compass's multi-day planning workflows with branching exploration require more than a simple LLM abstraction layer. Mastra provides native workflow graphs with suspend/resume capabilities, while AI SDK v6 handles the structured output generation that widget systems depend on.

**Key trade-off**: Mastra introduces framework commitment (proprietary DSL for workflows), but the alternative—building custom orchestration on AI SDK alone—requires 6-10 weeks of additional engineering versus 2-3 weeks for Mastra integration.

**Critical exclusion**: LangGraph.js is not recommended despite powerful checkpointing features. TypeScript quality issues and Zod-to-JSONSchema conversion problems directly impact widget generation reliability.

---

## Part 1: Context and Scope

### 1.1 Research Question

What orchestration framework best supports Compass's requirements for schema-constrained output generation, multi-session conversation management, provider abstraction, and stateful planning workflows?

### 1.2 Compass-Specific Requirements

The evaluation focused on five capabilities derived from the Compass System Definition.

**Structured Output Generation** (§2.2 Structured Input): Compass generates schema-constrained widget specifications dynamically. The orchestration layer must reliably produce JSON matching Zod schemas with tool calling fallback.

**Session Persistence** (§2.1 Planning Workflow): Planning workflows span days or weeks with pause/resume capability. State must survive server restarts and enable rollback to previous decision points.

**Provider Abstraction** (§3.1 LLM-Driven Conversation): Compass uses a tiered model strategy with Claude Opus 4.5 for planning and Claude Haiku 4.5 for orchestration, with Gemini and GPT-5.2 as fallbacks. Switching providers must be straightforward.

**Branching Exploration** (§2.6 Branching): Users explore alternative approaches before committing. The system must support parallel investigation paths with eventual merge.

**TypeScript-First Development**: Compass is built with TypeScript. The orchestration layer must provide strong typing, good IDE support, and maintainability for LLM coding agents.

### 1.3 Candidates Evaluated

The research evaluated five approaches representing different points on the abstraction spectrum:

| Candidate | Category | GitHub Stars | Last Major Release |
|-----------|----------|--------------|-------------------|
| Vercel AI SDK v6 | Provider abstraction + structured output | 21.2k | Dec 24, 2025 |
| Mastra | Full orchestration framework | 18k | Oct 2025 (seed) |
| LangGraph.js | Graph-based orchestration | 11.4k (monorepo) | Continuous |
| Instructor | Structured output extraction | 1.2k (TS) | ~Jan 2025 |
| Direct API | Custom orchestration | N/A | N/A |

---

## Part 2: Capability Assessment

### 2.1 Structured Output Generation

Structured output is critical for widget generation. All major providers now support schema-constrained JSON output, but framework support varies significantly.

**Vercel AI SDK v6** provides the strongest structured output capabilities. The December 2025 release introduced `Output.object()`, `Output.array()`, and `Output.choice()` methods that work with Zod schemas directly. Schema adherence is guaranteed via provider-native modes: Claude's constrained sampling (beta), OpenAI's strict JSON mode, and Gemini's schema enforcement.

```typescript
const { output } = await generateText({
  model: anthropic("claude-opus-4.5"),
  output: Output.object({
    schema: z.object({
      widgetType: z.enum(['choice', 'slider', 'tradeoff_table']),
      config: z.record(z.any()),
    }),
  }),
  prompt: 'Generate a planning widget...',
});
```

**Mastra** inherits AI SDK's structured output capabilities since it's built on top of the AI SDK. No additional abstraction or translation required.

**LangGraph.js** has documented issues with Zod-to-JSONSchema conversion. The `zod-to-json-schema` library produces `$ref` references that break OpenAI's strict mode, and optional field handling varies across providers. GitHub issue #6479 in the LangChain.js repository documents the problem and remains open.

**Instructor** provides excellent structured output with a unique advantage: automatic retry with validation error feedback. When schema validation fails, Instructor feeds the Zod error back to the LLM for self-correction. However, it offers no orchestration capabilities beyond extraction.

**Confidence**: High — AI SDK v6 structured output verified against official documentation and release notes.

### 2.2 Session Persistence and Multi-Turn Management

Planning workflows spanning days require durable state management. This is where frameworks diverge most significantly.

**Mastra** provides comprehensive persistence through its thread-based memory system. Threads persist conversation history with configurable storage backends (PostgreSQL, LibSQL, Upstash Redis, MongoDB, DynamoDB). Working memory uses Zod schemas with merge semantics—object fields deep-merge while arrays replace entirely. The `suspend()` function within workflow steps enables natural pause points.

```typescript
const planningWorkflow = createWorkflow({
  id: "compass-planning",
  stateSchema: z.object({ 
    stage: z.enum(["OPEN", "FOLLOW", "SHARPEN", "BOUNDARY", "GROUND"]),
    approaches: z.array(z.object({ name: z.string(), explored: z.boolean() }))
  })
})
  .then(openStep)
  .branch([
    [ctx => ctx.explore, exploreStep],
    [ctx => ctx.refine, refineStep]
  ])
  .commit();
```

**Vercel AI SDK** provides persistence hooks (`onFinish`, `onToolCall`) but requires building the actual storage layer. The `UIMessage` format provides a serialization pattern, but developers must implement the database layer, session management, and resume logic.

**LangGraph.js** offers sophisticated checkpointing with time travel capabilities. `PostgresSaver` and `DynamoDBSaver` provide production-grade persistence. The checkpoint/thread model separates conversation identity from state snapshots, enabling rollback without losing thread context. However, integrating with TypeScript codebases introduces friction due to quality issues.

**Instructor** provides no persistence capabilities. It's designed for single extraction calls.

**Confidence**: High — Mastra persistence verified against official documentation and architecture diagrams.

### 2.3 Provider Abstraction

All evaluated options except Instructor (which requires `llm-polyglot` for Claude) provide solid provider abstraction.

**Vercel AI SDK** supports 53+ providers through a unified interface. Provider-specific features like Claude's extended thinking and OpenAI's reasoning effort are accessible via `providerOptions` without breaking the abstraction:

```typescript
providerOptions: {
  anthropic: { thinking: { budgetTokens: 10000 }, effort: 'high' }
}
```

**Mastra** inherits AI SDK's provider abstraction directly. No additional configuration required for multi-provider support.

**LangGraph.js** provides good provider abstraction through LangChain's chat model interface. However, advanced provider-specific features may require workarounds.

**Critical gap**: None of the frameworks provide built-in automatic failover. If Claude API fails, the application must implement retry logic and provider switching. This is a common limitation across the ecosystem.

**Confidence**: High — Provider switching verified against AI SDK documentation and Mastra architecture.

### 2.4 Branching and Rollback

Compass requires exploring alternative approaches before committing. This capability varies significantly across options.

**LangGraph.js** provides the most sophisticated branching through its checkpointing system. Any checkpoint can be forked to explore alternatives, and results can be compared before committing. Time travel enables rollback to any previous state.

**Mastra** offers `.parallel()` for simultaneous exploration and `.branch()` for conditional paths, but explicit branch visualization and management require custom implementation. Mastra doesn't provide built-in UI for branch trees—applications must track branch metadata in working memory.

**Vercel AI SDK** provides no native branching. Developers must build custom tree structures with snapshot storage.

**Recommendation**: For Compass's branching requirement, implement a custom metadata layer on Mastra that tracks branch relationships in working memory. The pattern involves creating separate thread IDs per branch and maintaining a tree structure in application state.

**Confidence**: Moderate — Branching patterns inferred from framework capabilities; no direct implementation experience.

---

## Part 3: LLM Maintainability Assessment

The maintainability rubric evaluates how effectively AI coding assistants can help maintain and extend Compass. Both AI SDK and Mastra score above the 7/14 threshold required for consideration.

### 3.1 Scoring Methodology

Each criterion scores 0-2: 0 indicates absent or unusable, 1 indicates present but limited, and 2 indicates excellent and well-documented.

### 3.2 Framework Scores

| Criterion | AI SDK v6 | Mastra | LangGraph.js | Instructor |
|-----------|-----------|--------|--------------|------------|
| Documentation quality | 2 | 2 | 1 | 1.5 |
| TypeScript-first design | 2 | 2 | 1 | 2 |
| Common patterns vs DSL | 2 | 1.5 | 1 | 2 |
| LLM-specific support | 2 | 2 | 2 | 1.5 |
| Error message quality | 1 | 1.5 | 1 | 1.5 |
| Community knowledge | 2 | 1.5 | 2 | 1 |
| Single-page quickstart | 2 | 2 | 1 | 1.5 |
| **Total** | **13/14** | **12.5/14** | **9/14** | **11/14** |

### 3.3 Score Rationale

**Vercel AI SDK (13/14)**: Comprehensive documentation at ai-sdk.dev, native TypeScript design with full type inference, standard JavaScript patterns without proprietary DSL, `llms.txt` file for AI-assisted development, and active community with 20M+ monthly npm downloads.

**Mastra (12.5/14)**: Strong documentation with dedicated MCP docs server (`@mastra/mcp-docs-server`), TypeScript-first architecture. Loses half point on DSL—workflow definitions use `.then()`, `.branch()`, `.parallel()` methods that require learning Mastra conventions.

**LangGraph.js (9/14)**: Fails TypeScript quality criterion due to documented ESM/CJS conflicts, type inconsistencies, and Python-first development that leaves JavaScript documentation lagging. Multiple community reports cite debugging difficulties with compiled code.

**Instructor (11/14)**: Solid TypeScript support and simple API, but limited scope reduces usefulness. TypeScript version shows lower activity compared to Python version.

**Confidence**: High — Scores derived from documentation review, GitHub metrics, and community feedback.

---

## Part 4: Engineering Cost Analysis

### 4.1 Framework Integration (Mastra)

Estimated integration time is **2-3 weeks** with 1-2 developers.

| Task | Duration | Notes |
|------|----------|-------|
| Project setup and configuration | 2-3 days | Mastra CLI, database setup |
| Agent definitions | 3-4 days | Planning, orchestration, widget agents |
| Workflow implementation | 4-5 days | State machine, branching logic |
| Persistence integration | 2-3 days | PostgreSQL adapter configuration |
| Testing and refinement | 3-4 days | End-to-end workflow testing |

### 4.2 Custom Orchestration (AI SDK + XState)

Estimated build time is **6-10 weeks** with 1-2 senior developers.

| Component | Duration | Notes |
|-----------|----------|-------|
| Provider abstraction layer | 2-3 weeks | Or use AI SDK directly |
| State machine (XState v5) | 2-3 weeks | Planning workflow states |
| Persistence layer | 1-2 weeks | Session/branch storage |
| Streaming abstraction | 0.5-1 week | Cross-provider normalization |
| Branching/rollback logic | 1-2 weeks | Custom tree structure |
| Testing | 2-3 weeks | Comprehensive coverage |

### 4.3 Ongoing Maintenance

Both approaches require similar maintenance effort:

| Activity | Frequency | Duration |
|----------|-----------|----------|
| Provider API updates | Monthly | 2-4 hours |
| New model integration | Quarterly | 1-2 days |
| Framework upgrades | Quarterly | 4-8 hours |
| Bug fixes and patches | Weekly | 2-4 hours |

**Confidence**: Moderate — Estimates based on similar projects and framework documentation; actual duration depends on team experience.

---

## Part 5: Framework Comparison Matrix

### 5.1 Capability Summary

| Capability | AI SDK v6 | Mastra | LangGraph.js | Instructor | Direct API |
|------------|-----------|--------|--------------|------------|------------|
| Structured output (Zod) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Multi-turn management | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Provider abstraction | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Streaming | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| State machine | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Suspend/resume | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Branching/rollback | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Persistence | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |

### 5.2 Compass Fit Assessment

| Requirement | Best Fit | Runner-Up | Notes |
|-------------|----------|-----------|-------|
| Widget generation | AI SDK / Mastra | Instructor | Zod schema native support |
| Planning workflow | Mastra | LangGraph | Native state machines |
| Multi-day sessions | Mastra | LangGraph | Thread-based persistence |
| Provider switching | AI SDK / Mastra | LangGraph | One-line switching |
| Branching exploration | LangGraph | Mastra | Time travel vs parallel |
| TypeScript quality | AI SDK | Mastra | LangGraph fails criterion |

---

## Part 6: Recommended Architecture

### 6.1 Primary Recommendation: Mastra + AI SDK

The recommended architecture layers Mastra's workflow orchestration on AI SDK's structured output capabilities:

```
┌─────────────────────────────────────────────────────────┐
│                   Compass Application                    │
├─────────────────────────────────────────────────────────┤
│                  Mastra Agent Layer                      │
│          (Planning / Orchestration / Widget agents)      │
├─────────────────────────────────────────────────────────┤
│                Mastra Workflow Engine                    │
│          (suspend/resume, branching, state machine)      │
├─────────────────────────────────────────────────────────┤
│     Mastra Memory Layer          │  Working Memory       │
│     (PostgreSQL threads)         │  (Zod schemas)        │
├─────────────────────────────────────────────────────────┤
│                  Vercel AI SDK v6                        │
│     (generateText, Output.object, streaming)             │
├─────────────────────────────────────────────────────────┤
│   @ai-sdk/anthropic    │   @ai-sdk/openai    │   etc.   │
└─────────────────────────────────────────────────────────┘
```

**Why this combination works**: Mastra is built on top of the AI SDK, making integration seamless. The AI SDK handles low-level provider communication and structured output, while Mastra manages workflow state and persistence. There's no abstraction mismatch or translation layer required.

### 6.2 Tiered Model Implementation

Following ADR-09-01 recommendations, the architecture implements model routing through provider options:

```typescript
// Planning agent - Claude Opus 4.5 with extended thinking
const planningAgent = createAgent({
  model: anthropic("claude-opus-4.5"),
  providerOptions: {
    anthropic: {
      thinking: { type: "enabled", budgetTokens: 12000 },
    }
  }
});

// Orchestration agent - Claude Haiku 4.5 (no thinking overhead)
const orchestrationAgent = createAgent({
  model: anthropic("claude-haiku-4.5"),
});
```

### 6.3 Branch Exploration Pattern

Mastra doesn't provide built-in branch visualization, but the pattern can be implemented through working memory:

```typescript
const branchingWorkflow = createWorkflow({
  stateSchema: z.object({
    branches: z.array(z.object({
      id: z.string(),
      parentId: z.string().nullable(),
      status: z.enum(['active', 'merged', 'abandoned']),
      threadId: z.string(),
    })),
    activeBranch: z.string(),
  })
})
  .then(createBranchStep)
  .parallel([exploreApproachA, exploreApproachB])
  .then(mergeBranchesStep);
```

Merging involves copying relevant context from the branch thread to the primary thread and updating branch metadata.

### 6.4 Fallback Strategy

If Mastra's workflow DSL proves too constraining, the alternative is **AI SDK v6 + XState v5**. XState provides mature state machine capabilities with TypeScript support and persistence options. The combination requires more custom code but offers maximum flexibility:

| Component | Tool | Notes |
|-----------|------|-------|
| Provider abstraction | Vercel AI SDK v6 | Native |
| Structured output | Vercel AI SDK v6 | Output.object() |
| State machine | XState v5 | Actor model |
| Persistence | Custom + Supabase | Per ADR-01-01 |
| Branching | Custom | Tree structure |

---

## Part 7: Implications for Related Areas

### 7.1 Area 07 (Widget Libraries)

Widget schemas should use Zod's `.describe()` annotations extensively to improve LLM output quality:

```typescript
const widgetSchema = z.object({
  type: z.enum(['choice', 'slider']).describe('The widget interaction type'),
  question: z.string().describe('The question to present to the user'),
  options: z.array(z.string()).describe('Available choices, 2-6 items'),
});
```

Streaming partial objects via `partialOutputStream` enables progressive widget rendering.

### 7.2 Area 18 (Questioning Arc)

Mastra's `suspend()` function maps directly to the questioning arc's need for human-in-the-loop pauses. Workflow steps can suspend at natural pause points (end of OPEN phase, awaiting user input in SHARPEN phase) with automatic state preservation.

### 7.3 Area 19 (Widget Schema)

Zod schemas serve as the single source of truth for widget types. Both AI SDK and Mastra convert Zod to JSON Schema automatically. Testing with OpenAI's strict mode should occur early to catch edge cases. Define schemas with explicit `additionalProperties: false` for strict mode compatibility.

**Known limitation**: Discriminated unions (`z.discriminatedUnion`) have unreliable behavior across providers. Use explicit type fields or separate schemas for different widget types.

---

## Part 8: Limitations and Open Questions

### 8.1 Research Limitations

**Framework maturity**: Mastra is a young framework (seed funding October 2025). Long-term stability is unverified, though $13M funding from YC, Gradient Ventures, and Vercel's Guillermo Rauch suggests sustained development commitment.

**No benchmarking**: This research did not conduct hands-on performance testing. Latency, throughput, and memory usage under load remain unverified.

**Community reports**: LangGraph TypeScript issues are based on GitHub issues and community discussions, not direct testing. Issues may have been resolved in recent releases.

**Provider beta features**: Claude's structured outputs remain in public beta. API changes could require orchestration layer updates.

### 8.2 Open Questions

**Branch merge complexity**: How should conflicting branch decisions be reconciled? The recommended pattern (copy context to primary thread) may lose important context from abandoned branches.

**State machine complexity**: Will Compass's planning workflow require more complex state transitions than Mastra's DSL supports? Early prototyping should verify.

**Checkpoint storage costs**: For multi-week planning sessions, how much storage will checkpoint history consume? Consider retention policies early.

---

## Sources

All sources assessed per STD-20-01 evidence standards.

### Tier 1: Official Documentation

1. **[T1/S1]** Vercel. "AI SDK v6 Announcement". Published 2025-12-24. Retrieved 2026-01-25. https://vercel.com/blog/ai-sdk-6
   Note: Official release announcement with feature details.

2. **[T1/S1]** Vercel. "AI SDK Core: Generating Structured Data". Retrieved 2026-01-25. https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
   Note: Official documentation for Output.object() and related methods.

3. **[T1/S1]** Mastra. "Documentation". Retrieved 2026-01-25. https://mastra.ai/docs
   Note: Official framework documentation.

4. **[T1/S1]** Mastra. "Workflows and State Machines". Retrieved 2026-01-25. https://mastra.ai/docs/workflows
   Note: Official workflow documentation.

5. **[T1/S1]** Anthropic. "Structured Outputs (Beta)". Retrieved 2026-01-25. https://platform.claude.com/docs/en/build-with-claude/structured-outputs
   Note: Official Claude API documentation, beta status verified.

6. **[T1/S1]** LangChain. "LangGraph.js Overview". Retrieved 2026-01-25. https://docs.langchain.com/oss/javascript/langgraph/overview
   Note: Official LangGraph documentation.

### Tier 2: Credible Developer Sources

7. **[T2/S2]** VendorTruth. "Report: Mastra vs Vercel AI SDK vs LangGraph". Retrieved 2026-01-25. https://www.vendortruth.org/article/report-mastra-vs-vercel-ai-sdk-vs-langgraph
   Note: Independent comparison report.

8. **[T2/S2]** Mastra. "Seed Round Announcement". Published 2025-10. Retrieved 2026-01-25. https://mastra.ai/blog/seed-round
   Note: $13M funding from YC, Gradient Ventures, Vercel.

9. **[T2/S2]** GitHub. "Zod union with generateObject discussion". Retrieved 2026-01-25. https://github.com/vercel/ai/discussions/5089
   Note: Community discussion on schema limitations.

10. **[T2/S2]** GitHub. "LangChain.js Zod-to-JSONSchema issues". Retrieved 2026-01-25. https://github.com/langchain-ai/langchainjs/issues/6479
    Note: Open issue documenting strict mode compatibility problems.

### Tier 3: General Technology Sources

11. **[T3/S2]** FASHN. "Choosing the Best AI Agent Framework in 2025". Retrieved 2026-01-25. https://fashn.ai/blog/choosing-the-best-ai-agent-framework-in-2025
    Note: Industry perspective on framework selection.

---

## Appendix A: Glossary

**Checkpoint**: A snapshot of workflow state that enables rollback and time travel in LangGraph.

**DSL (Domain-Specific Language)**: Custom syntax for expressing framework concepts. Mastra's `.then()`, `.branch()`, `.parallel()` methods constitute a DSL.

**Extended thinking**: Claude's capability to reason through complex problems before generating responses. Configured via `providerOptions.anthropic.thinking`.

**JSON Schema**: Standard format for describing JSON structure. LLM providers use JSON Schema for structured output validation.

**MCP (Model Context Protocol)**: Standard for connecting LLMs to data sources. Both AI SDK and Mastra support MCP servers.

**Strict mode**: OpenAI's schema enforcement mode that guarantees output matches the provided JSON Schema exactly.

**Thread**: Mastra's abstraction for conversation history, enabling multi-session persistence.

**Working memory**: Mastra's Zod-validated state that persists across workflow steps with merge semantics.

**Zod**: TypeScript-first schema validation library. Provides runtime validation and static type inference.

---

## Appendix B: Related Documents

- **RF-01-09**: LLM Provider Research Findings (tiered model strategy)
- **ADR-09-01**: LLM Provider Selection (Claude Opus/Haiku 4.5 decision)
- **ADR-01-01**: Backend Platform Selection (PostgreSQL via Supabase)
- **DD-13-01**: Artifact Taxonomy (document formatting standards)
- **DD-14-01**: EFN Ecosystem Definitions (integration requirements)
- **Compass System Definition**: Authoritative system specification (§2.1, §2.2, §2.6, §3.1)

---

*End of LLM Orchestration Framework Research Findings (RF-02-01)*
