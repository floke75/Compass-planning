---
id: ADR-03-01
type: adr
area: 03-memory-retrieval
title: Memory and Retrieval Architecture Selection
status: proposed
created: 2026-01-26
updated: 2026-01-26
author: compass-research
decision: Convex-primary architecture using @convex-dev/rag for three-layer memory (session, project, ecosystem) with optional Zep Graphiti or Supermemory enrichment in Phase 3
summary: Adopts unified Convex memory architecture over external memory services based on integration simplicity, cost efficiency, and adequate capability coverage for Compass requirements
tags: [memory, retrieval, vector-search, temporal, convex, rag, adr]
related:
  - RF-03-01
  - ADR-01-01
  - ADR-02-01
supersedes: null
superseded_by: null
responds_to: RF-03-01
---

# Memory and Retrieval Architecture Selection

## Decision Summary

**Selected**: Convex-primary architecture using @convex-dev/rag component (v0.5.4+) for all three memory layers defined in the System Definition.

**Alternatives evaluated**: Zep Graphiti, Supermemory, Mem0 as external memory services.

**Decision rationale**: Convex's built-in @convex-dev/rag provides namespace isolation, hybrid search, and temporal filtering sufficient for Compass Phase 1-2 requirements. The Convex-only approach eliminates integration complexity, maintains a single source of truth, and reduces costs from $100-400/month (external services) to $10-30/month (Convex-included).

---

## Context

The Compass System Definition (§3.2) specifies three memory layers with distinct persistence and retrieval characteristics:

| Layer | Scope | Persistence | Purpose |
|-------|-------|-------------|---------|
| **Session** | Current conversation | Hours | What is being discussed now |
| **Project** | Single project | Months/years | Decisions, constraints, artifacts |
| **Ecosystem** | Cross-project | Permanent | Patterns, standards, prior solutions |

ADR-01-01 selected Convex as the backend platform. This decision inherits that foundation and determines how memory and retrieval will be implemented within or alongside Convex.

**Critical requirements from System Definition:**

1. Semantic retrieval: "Find decisions similar to X"
2. Temporal retrieval: "What changed since Monday?"
3. Namespace isolation: Session memory must not leak into project memory
4. Graceful degradation: Memory unavailability must not crash Compass
5. Point-in-time queries: "What was the state as of date X?" (deferred to Phase 2)

---

## Decision

### Primary Architecture: Convex-Only with @convex-dev/rag

Implement memory entirely within Convex using the @convex-dev/rag component:

**Session Memory** — Convex table with TTL-based cleanup, `session:{id}` namespace prefix, auto-expiring after conversation end.

**Project Memory** — Convex table with uni-temporal fields (`validFrom`, `validUntil`), `project:{id}` namespace prefix, versioned decision records.

**Ecosystem Memory** — Convex table for cross-project patterns, `ecosystem` namespace, shared standards and conventions.

**Event Log** — Convex table for decision events, enabling temporal reconstruction via event sourcing pattern.

**Hierarchical Retrieval** — Multi-stage query combining recent (session) → relevant (project) → pattern (ecosystem) results with relevance and recency weighting.

### Phase 3 Option: External Service Enrichment

If specific requirements emerge, external memory services can supplement Convex:

| Trigger Condition | Service | Integration Pattern |
|-------------------|---------|---------------------|
| Bi-temporal queries required ("what did we know as of X?") | Zep Graphiti | Async sync via scheduled actions |
| MCP integration critical | Supermemory | Write-through cache layer |
| Session isolation requirements increase | Mem0 | Session-specific memory isolation |

Decision to add external services requires documented justification and ADR amendment.

---

## Rationale

### Why Convex-Primary (and not external services)?

**Integration simplicity** — Convex @convex-dev/rag integrates natively with the backend. External services require sync mechanisms, consistency management, and fallback handling.

**Single source of truth** — Memory lives where the data lives. No sync drift, no eventual consistency gaps between systems.

**Cost efficiency** — Convex-only costs $10-30/month (included in backend). External services add $100-400/month for capabilities that aren't critical in Phase 1-2.

**Adequate capability coverage** — Analysis in RF-03-01 shows Convex handles:
- ✅ Semantic search via vector indexing
- ✅ Namespace isolation via string prefixes
- ✅ Temporal filtering via `validFrom`/`validUntil` fields
- ✅ Hybrid search combining vector and keyword relevance
- ✅ Up to 16 filter fields per query

**Operational simplicity** — Non-technical team benefits from fewer moving parts. One system to monitor, one set of credentials, one failure mode.

### Why not Zep Graphiti?

Zep Graphiti excels at bi-temporal knowledge graphs and entity relationship tracking. However:

- Bi-temporal queries ("what did we know as of date X?") are not a Phase 1 requirement
- Knowledge graph traversal adds complexity without demonstrated need
- Self-hosted: $40-70/month infrastructure; managed: $150-300/month
- Integration requires custom sync logic and dual-system query routing

**Verdict**: Reserve for Phase 3 if cross-project dependency patterns or audit requirements emerge.

### Why not Supermemory?

Supermemory offers native MCP integration and sub-400ms latency. However:

- MCP integration value depends on Claude tool-calling patterns (uncertain in Phase 1)
- Latency requirements are sub-1s, achievable with Convex-only
- $19-99/month adds cost without filling a specific gap

**Verdict**: Consider in Phase 2-3 if MCP becomes a primary integration pattern.

### Why not Mem0?

Mem0 provides session-level memory isolation with change history. However:

- Convex namespace prefixes provide equivalent isolation
- $249/month Pro tier is expensive for capabilities Convex handles adequately
- Less mature enterprise features compared to alternatives

**Verdict**: Not recommended; Convex covers the use cases better.

---

## Consequences

### Positive

**Reduced complexity** — Single system for data and memory; no sync mechanisms or consistency management.

**Lower cost** — $10-30/month vs. $100-400/month with external services.

**Faster development** — No external integration work in Phase 1.

**Better reliability** — Fewer external dependencies; graceful degradation is simpler when there's one system.

**TypeScript consistency** — @convex-dev/rag uses same language and patterns as the rest of the stack.

### Negative

**Custom temporal implementation** — Point-in-time queries require event sourcing pattern rather than built-in bi-temporal support.

**Less sophisticated graph queries** — Entity relationship traversal requires manual implementation.

**Potential future migration** — If Phase 3 adds Zep Graphiti, requires data migration and dual-system architecture.

**Namespace isolation is convention-based** — String prefixes rely on correct implementation; no enforced tenant separation.

### Mitigations

| Risk | Mitigation |
|------|------------|
| Temporal queries become critical | Event sourcing pattern enables reconstruction; Zep integration path documented |
| MCP integration required | Supermemory has documented integration pattern; can add as cache layer |
| Namespace leakage | Unit tests verify namespace isolation; prefix generation centralized |
| Convex rate limits | Circuit breaker pattern with graceful degradation to cached results |

---

## Implementation Guidance

### Schema Pattern

Memory tables should follow this structure:

```typescript
// Namespace format
const namespaces = {
  session: (id: string) => `session:${id}`,
  project: (id: string) => `project:${id}`,
  ecosystem: () => "ecosystem",
};

// Required fields for all memory records
interface MemoryRecord {
  namespace: string;      // Isolation key
  content: string;        // Text for embedding
  embedding: number[];    // Vector (1536 dimensions for ada-002)
  createdAt: number;      // Timestamp
  validFrom: number;      // When this became true (temporal)
  validUntil?: number;    // When superseded (null = current)
}
```

### Retrieval Pattern

Hierarchical retrieval should query in order:

1. **Session** — Most recent conversation context (limit: 10 results)
2. **Project** — Relevant decisions and constraints (limit: 20 results)
3. **Ecosystem** — Cross-project patterns if project results insufficient (limit: 10 results)

Results combined using relevance scoring with recency boost for session memory.

### Temporal Query Pattern

For "what changed since Monday?" queries:

```typescript
// Filter by validFrom timestamp
const changes = await ctx.db
  .query("projectMemory")
  .filter((q) => q.and(
    q.eq(q.field("namespace"), `project:${projectId}`),
    q.gte(q.field("validFrom"), mondayTimestamp)
  ))
  .collect();
```

For "what was the state as of date X?" (Phase 2):

```typescript
// Event sourcing reconstruction
const eventsBeforeDate = await ctx.db
  .query("decisionEvents")
  .filter((q) => q.and(
    q.eq(q.field("namespace"), `project:${projectId}`),
    q.lte(q.field("occurredAt"), targetTimestamp)
  ))
  .order("asc")
  .collect();

// Replay events to reconstruct state
const stateAtDate = replayEvents(eventsBeforeDate);
```

### Graceful Degradation

Memory queries should implement circuit breaker pattern:

1. Attempt Convex query with 2-second timeout
2. On failure, return cached results from previous successful query
3. On repeated failures (3+), enter degraded mode with stale cache
4. Resume normal operation after 30-second recovery period
5. Log all degradation events for monitoring

---

## Budget Impact

| Component | Phase 1 | Phase 3 | Notes |
|-----------|---------|---------|-------|
| Convex @convex-dev/rag | $0-25/month | $25-75/month | Included in Convex pricing |
| Embeddings (ada-002) | $10-30/month | $30-50/month | ~1M tokens/month |
| External service (optional) | $0 | $0-150/month | Only if bi-temporal needed |
| **Total** | **$10-55/month** | **$55-275/month** | Well within budget |

**Budget assessment**: Phase 1 budget target is <$200/month total, Phase 3 is <$800/month. Memory costs represent 5-15% of budget, leaving substantial headroom.

---

## Related Decisions

| ADR | Relationship |
|-----|--------------|
| ADR-01-01 | Backend platform (Convex) — this decision inherits |
| ADR-02-01 | Orchestration (Mastra) — memory integrates with workflow state |
| ADR-09-01 | LLM provider (Claude) — embedding model compatible |

---

## Review Schedule

**Trigger conditions for ADR review:**

1. Phase 2 planning begins (evaluate temporal query needs)
2. MCP becomes primary integration pattern
3. Cross-project queries exceed 20% of retrieval volume
4. Convex @convex-dev/rag releases major version with breaking changes
5. External memory service pricing changes significantly

**Next scheduled review**: Phase 2 kickoff or 90 days, whichever comes first.

---

## Appendix: Candidate Comparison Matrix

| Criterion | Convex @convex-dev/rag | Zep Graphiti | Supermemory | Mem0 |
|-----------|------------------------|--------------|-------------|------|
| **Convex integration** | Native | Requires sync | Requires sync | Requires sync |
| **Namespace isolation** | String prefix | Entity-based | Collection-based | Session-based |
| **Temporal queries** | Uni-temporal | Bi-temporal | Basic | Basic |
| **Semantic search** | Hybrid (vector + text) | Graph + vector | Vector | Vector |
| **Cost (Phase 1)** | $10-30/month | $70-150/month | $19-99/month | $249/month |
| **Operational complexity** | Low | Medium-High | Low-Medium | Low-Medium |
| **Compass fit** | ✅ Excellent | Good (Phase 3) | Good (if MCP) | Adequate |

---

*End of Memory and Retrieval Architecture Selection (ADR-03-01)*
