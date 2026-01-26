---
id: RF-03-01
type: rf
area: 03-memory-retrieval
title: Memory and Retrieval Architecture Research Findings
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Evaluates memory and retrieval solutions for Compass with recommendation for Convex-primary architecture using @convex-dev/rag for three-layer memory model, supplemented by optional external services for complex temporal queries
tags: [memory, retrieval, vector-search, temporal, convex, rag, llm]
related:
  - RF-01-01
  - ADR-01-01
  - DD-13-01
  - DD-14-01
confidence: high
methodology: "Web research with official vendor documentation, pricing verification, GitHub repositories, developer testimonials, and integration pattern analysis"
limitations:
  - "Pricing subject to change; verified January 25, 2026"
  - "No hands-on implementation testing performed"
  - "Zep Graphiti self-hosted costs estimated based on infrastructure requirements"
  - "Convex @convex-dev/rag v0.5.4 capabilities may expand in future releases"
responds_to: null
implications_for: [ADR-03-01, A02, A04]
---

# Memory and Retrieval Architecture Research Findings

## Executive Summary

**Primary Recommendation**: **Convex-primary architecture** using the built-in @convex-dev/rag component with namespace isolation for all three memory layers (session, project, ecosystem). External memory services are optional enrichment for complex temporal queries only.

**Confidence**: High — Convex's built-in capabilities satisfy Compass requirements for semantic search, namespace isolation, and basic temporal filtering. The cost differential between Convex-only ($0-25/month) and external services ($100-400/month) is significant, and the integration complexity of external services adds operational burden without proportional benefit for Phase 1-2 requirements.

**Key insight**: The critical question for Compass memory architecture is not "which external memory service is best?" but rather "does Convex's built-in @convex-dev/rag component satisfy requirements, and if not, what specific gaps require external services?" Analysis shows that Convex handles semantic search, namespace isolation, and basic temporal filtering adequately. The primary gap is sophisticated bi-temporal queries ("what was the state as of date X?"), which can be addressed through schema design (event sourcing) rather than external services.

**Trade-offs accepted**:

- Convex-only approach requires custom implementation for point-in-time temporal queries
- Namespace isolation via string prefixes is less elegant than dedicated tenant separation
- No pre-built "infinite context" solution—requires MemGPT-style hierarchical summarization pattern

**Alternatives assessment**:

- **Zep Graphiti**: Best choice if bi-temporal knowledge graphs and entity relationship tracking become critical requirements. Justified only for Phase 3 if planning workflows develop complex cross-project dependency patterns. Cost: $40-70/month self-hosted or $150-300/month managed.
- **Supermemory**: Best choice if MCP (Model Context Protocol) integration and sub-400ms latency are priorities. Simpler integration path than Zep but weaker temporal capabilities. Cost: $19/month Pro, $99/month Scale.
- **Mem0**: Best choice if session-level memory isolation and change history tracking are critical. Good for conversational context but limited temporal query support. Cost: $249/month Pro.

**Budget assessment**: All options within targets. Phase 1 (<$100/month): Convex-only at $0-25/month. Phase 3 (<$400/month): Convex + optional Zep Graphiti at $70-150/month or Supermemory Scale at $99/month.

---

## Part 1: Research Context and Requirements

### 1.1 Memory Requirements from System Definition

The Compass System Definition (§3.2) specifies three memory layers with distinct characteristics:

| Layer | Scope | Persistence | Key Requirements |
|-------|-------|-------------|------------------|
| **Session Memory** | Current conversation | Ephemeral (hours) | What is being discussed now; fast retrieval |
| **Project Memory** | Single project | Long-lived (months/years) | Decisions, constraints, artifacts, history; cross-session |
| **Ecosystem Memory** | Cross-project | Permanent | Patterns, standards, prior solutions; "have we solved this before?" |

**Core memory entities** (System Definition §3.2):

- Project: Canonical container
- Artifact: Versioned document (spec, ADR, research finding, etc.)
- Decision: Typed record with status, rationale, options, dependencies
- Branch: Alternate planning universe
- Workflow run: Trace of arc progression
- Citation/evidence: Reference to source with timestamp
- Profile: User/team preferences
- Adapter: Import/export mappings

**Temporal awareness requirements**:

The System Definition emphasizes memory that "supports semantic and temporal retrieval" including queries like "what changed since Monday?" This implies:

1. **Recency-weighted retrieval**: Recent decisions should rank higher than historical ones
2. **Point-in-time queries**: "What was decided as of date X?"
3. **Change tracking**: "What changed between date A and date B?"
4. **Supersession awareness**: Decisions marked as superseded should be retrievable for historical context but not returned as current truth

### 1.2 Prior Research Context

ADR-01-01 selected **Convex** as the backend platform. Key implications for memory architecture:

- Convex provides **built-in vector search** via `ctx.vectorSearch()` supporting up to 4096 dimensions
- The **@convex-dev/rag component** (v0.5.4) provides namespace isolation, hybrid search, and automatic embedding generation
- Convex's **document-relational model** allows storing embeddings alongside structured metadata
- **Real-time reactivity** means memory updates propagate automatically to all connected sessions
- **No PostgreSQL/pgvector** — the research pivot is toward Convex-native solutions

### 1.3 Evaluation Criteria

| Criterion | Priority | Rationale |
|-----------|----------|-----------|
| **Convex integration quality** | Critical | Backend is Convex; memory must integrate cleanly |
| **Three-layer isolation** | Critical | Session, project, ecosystem memory must not leak |
| **Temporal query support** | High | Planning decisions need point-in-time retrieval |
| **Graceful degradation** | High | Memory unavailability shouldn't crash Compass |
| **Cost efficiency** | Medium | Budget generous but efficiency preferred |
| **Operational simplicity** | Medium | Non-technical team; managed services preferred |
| **Infinite context handling** | Medium | Planning conversations can span weeks |

---

## Part 2: Convex Built-in Capabilities

### 2.1 @convex-dev/rag Component Analysis

The @convex-dev/rag component (v0.5.4, January 2026) provides a comprehensive RAG toolkit designed specifically for Convex applications.

**Core capabilities**:

| Feature | Capability | Compass Fit |
|---------|------------|-------------|
| **Namespace isolation** | String-based namespace prefix for document separation | ✅ Maps to session/project/ecosystem |
| **Hybrid search** | Combined vector + text search via `hybridRank()` | ✅ Semantic + keyword retrieval |
| **Custom filtering** | Up to 16 filter fields per query | ✅ Temporal, status, type filters |
| **Embedding generation** | Automatic via configurable embedding model | ✅ Reduces integration complexity |
| **Chunk context** | Retrieves surrounding chunks for context | ✅ Important for document retrieval |
| **Importance weighting** | Configurable relevance scoring | ✅ Recency boosting possible |

**Architecture pattern**:

```typescript
// Convex schema for memory with namespace isolation
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Session memory - ephemeral, auto-expires
  sessionMemory: defineTable({
    sessionId: v.string(),
    namespace: v.string(), // "session:{sessionId}"
    content: v.string(),
    embedding: v.array(v.float64()),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    createdAt: v.number(),
    expiresAt: v.number(), // TTL for cleanup
  })
    .index("by_session", ["sessionId"])
    .index("by_namespace", ["namespace"])
    .vectorIndex("by_embedding", {
      vectorField: "embedding",
      dimensions: 1536,
      filterFields: ["namespace", "sessionId"],
    }),

  // Project memory - long-lived, versioned
  projectMemory: defineTable({
    projectId: v.string(),
    namespace: v.string(), // "project:{projectId}"
    artifactId: v.optional(v.string()),
    content: v.string(),
    embedding: v.array(v.float64()),
    memoryType: v.union(
      v.literal("decision"),
      v.literal("constraint"),
      v.literal("requirement"),
      v.literal("context")
    ),
    validFrom: v.number(), // Temporal: when this became true
    validUntil: v.optional(v.number()), // Temporal: when superseded (null = current)
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_project", ["projectId"])
    .index("by_namespace", ["namespace"])
    .index("by_type", ["projectId", "memoryType"])
    .index("by_valid_range", ["projectId", "validFrom", "validUntil"])
    .vectorIndex("by_embedding", {
      vectorField: "embedding",
      dimensions: 1536,
      filterFields: ["namespace", "projectId", "memoryType"],
    }),

  // Ecosystem memory - cross-project patterns
  ecosystemPatterns: defineTable({
    namespace: v.literal("ecosystem"),
    patternType: v.union(
      v.literal("convention"),
      v.literal("prior_solution"),
      v.literal("anti_pattern"),
      v.literal("standard")
    ),
    content: v.string(),
    embedding: v.array(v.float64()),
    sourceProjects: v.array(v.string()), // Which projects established this
    usageCount: v.number(), // How often referenced
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_type", ["patternType"])
    .vectorIndex("by_embedding", {
      vectorField: "embedding",
      dimensions: 1536,
      filterFields: ["namespace", "patternType"],
    }),
});
```

### 2.2 Native Vector Search Limitations

Convex's native `ctx.vectorSearch()` has specific constraints:

| Constraint | Limit | Impact on Compass |
|------------|-------|-------------------|
| **Max dimensions** | 4096 | ✅ Sufficient (OpenAI ada-002 uses 1536) |
| **Max results per query** | 256 | ✅ Adequate for retrieval |
| **Filter fields** | 16 per index | ✅ Sufficient for temporal + type filters |
| **Vector indexes per table** | Multiple allowed | ✅ Can have separate indexes for different query patterns |

**What Convex cannot do natively**:

1. **Bi-temporal queries**: "What was the project state as of January 15?" requires application-level event sourcing
2. **Graph traversal**: Entity relationships (decisions → artifacts → requirements) need explicit joins
3. **Cross-namespace search**: Searching across session + project + ecosystem requires multiple queries
4. **Automatic summarization**: No built-in hierarchical memory compression for infinite context

### 2.3 Temporal Query Implementation in Convex

Convex supports basic temporal filtering but not true bi-temporal queries out of the box.

**What works natively**:

```typescript
// Query: "Recent decisions in this project"
const recentDecisions = await ctx.db
  .query("projectMemory")
  .withIndex("by_project", (q) => q.eq("projectId", projectId))
  .filter((q) => q.gte(q.field("createdAt"), oneWeekAgo))
  .order("desc")
  .take(10);

// Query: "Current (not superseded) decisions"
const currentDecisions = await ctx.db
  .query("projectMemory")
  .withIndex("by_project", (q) => q.eq("projectId", projectId))
  .filter((q) => q.eq(q.field("validUntil"), null))
  .collect();
```

**What requires custom implementation**:

```typescript
// Query: "What was decided as of January 15, 2026?"
// Requires: validFrom <= targetDate AND (validUntil > targetDate OR validUntil IS NULL)
async function getDecisionsAsOf(ctx: QueryCtx, projectId: string, asOfDate: number) {
  const allDecisions = await ctx.db
    .query("projectMemory")
    .withIndex("by_project", (q) => q.eq("projectId", projectId))
    .filter((q) => q.lte(q.field("validFrom"), asOfDate))
    .collect();
  
  // Application-level filter for validUntil
  return allDecisions.filter(d => 
    d.validUntil === null || d.validUntil > asOfDate
  );
}
```

**Event sourcing pattern for full temporal support**:

```typescript
// Decision events table for complete history
decisionEvents: defineTable({
  projectId: v.string(),
  eventType: v.union(
    v.literal("decision_created"),
    v.literal("decision_modified"),
    v.literal("decision_superseded"),
    v.literal("decision_reverted")
  ),
  decisionId: v.string(),
  content: v.string(), // Full decision content at this point
  previousContent: v.optional(v.string()),
  changedBy: v.string(),
  changedAt: v.number(),
  validFrom: v.number(), // When this version became effective
  supersededBy: v.optional(v.string()), // Link to superseding decision
})
  .index("by_project_time", ["projectId", "changedAt"])
  .index("by_decision", ["decisionId", "changedAt"])
```

This pattern enables:
- "What changed since Monday?" → Query events where `changedAt > mondayTimestamp`
- "State as of date X" → Replay events up to date X
- "History of decision Y" → All events for `decisionId = Y`

---

## Part 3: External Memory Service Evaluation

### 3.1 Supermemory

**What it is**: Supermemory is a managed memory API service providing persistent memory storage with MCP (Model Context Protocol) integration. It focuses on simple integration for AI applications needing conversation memory.

**Pricing (January 2026)**:

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Free | $0 | 100 memories, 50 searches/day | Development only |
| Pro | $19/month | 10,000 memories, unlimited searches | Production use |
| Scale | $99/month | 100,000 memories, priority support | High-volume applications |
| Enterprise | Custom | Custom limits, SLA | Large organizations |

**Capabilities assessment**:

| Capability | Support | Notes |
|------------|---------|-------|
| **MCP integration** | ✅ Excellent | Native MCP server for Claude, Cursor |
| **Namespace isolation** | ✅ Yes | User-level and container-level isolation |
| **Semantic search** | ✅ Yes | Vector search with configurable similarity |
| **Temporal queries** | ⚠️ Limited | Recency bias but no point-in-time queries |
| **Hybrid search** | ⚠️ Basic | Less sophisticated than Convex hybrid ranking |
| **Latency** | ✅ Sub-400ms | Advertised P95 latency |

**Integration with Convex**:

Supermemory would function as a **separate memory layer** alongside Convex:

```typescript
// Convex action calling Supermemory API
import { action } from "./_generated/server";
import { v } from "convex/values";

export const searchMemory = action({
  args: { query: v.string(), namespace: v.string() },
  handler: async (ctx, { query, namespace }) => {
    const response = await fetch("https://api.supermemory.ai/v1/search", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.SUPERMEMORY_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        filter: { namespace },
        limit: 10,
      }),
    });
    return response.json();
  },
});
```

**Why Supermemory might be valuable**:

1. **MCP integration**: If Compass uses Claude's MCP for tool calling, Supermemory provides native memory tools
2. **Rapid setup**: No schema design or embedding pipeline needed
3. **Sub-400ms latency**: Important for real-time planning conversations

**Why Supermemory might not be needed**:

1. **Duplicate storage**: Memories stored in both Convex and Supermemory
2. **Sync complexity**: Keeping two systems consistent adds operational burden
3. **Limited temporal support**: Convex event sourcing provides better temporal queries
4. **Cost**: $19-99/month for capabilities Convex provides natively

### 3.2 Zep Graphiti

**What it is**: Zep Graphiti is a bi-temporal knowledge graph for AI agent memory. It stores facts with both "valid time" (when the fact was true in the real world) and "transaction time" (when it was recorded in the system), enabling sophisticated temporal reasoning.

**Deployment options**:

| Option | Cost Estimate | Complexity |
|--------|---------------|------------|
| **Self-hosted (Docker)** | $40-70/month (infrastructure) | Medium |
| **Zep Cloud** | $150-300/month (estimated) | Low |
| **Self-hosted (Kubernetes)** | $100-200/month (infrastructure) | High |

**Capabilities assessment**:

| Capability | Support | Notes |
|------------|---------|-------|
| **Bi-temporal queries** | ✅ Excellent | Core differentiator; "state as of date X" native |
| **Entity relationships** | ✅ Excellent | Graph structure for decision → artifact → requirement |
| **Namespace isolation** | ✅ Yes | User and project-level separation |
| **Semantic search** | ✅ Yes | Vector search with graph context |
| **Fact extraction** | ✅ Yes | LLM-driven entity and relationship extraction |
| **Contradiction detection** | ✅ Yes | Identifies conflicting facts |

**Bi-temporal query example**:

```python
# Zep Graphiti: "What did we know about authentication as of January 15?"
from zep_cloud.client import AsyncZep

client = AsyncZep(api_key="...")

# Query with temporal bounds
results = await client.graph.search(
    user_id="project-compass",
    query="authentication requirements",
    valid_at=datetime(2026, 1, 15),  # State as of this date
    limit=10
)
```

**Integration with Convex**:

Zep Graphiti would serve as a **temporal reasoning layer** with Convex as the source of truth:

```typescript
// Convex → Zep sync pattern
export const syncDecisionToZep = action({
  args: { decisionId: v.string() },
  handler: async (ctx, { decisionId }) => {
    const decision = await ctx.runQuery(api.decisions.get, { id: decisionId });
    
    // Extract entities and relationships
    const facts = extractFacts(decision);
    
    // Send to Zep with bi-temporal timestamps
    await zepClient.graph.add({
      user_id: decision.projectId,
      messages: facts.map(fact => ({
        content: fact.content,
        valid_from: decision.validFrom,
        metadata: { source: "decision", decisionId }
      }))
    });
  },
});
```

**Why Zep Graphiti might be valuable**:

1. **True bi-temporal queries**: Only evaluated solution with native "state as of date X" support
2. **Entity relationships**: Graph structure matches Compass's interconnected decisions/artifacts/requirements
3. **Contradiction detection**: Useful for identifying conflicting decisions across planning sessions
4. **Sophisticated temporal reasoning**: "What changed about authentication between January and March?"

**Why Zep Graphiti might not be needed**:

1. **Complexity**: Graph database adds significant operational burden
2. **Cost**: $40-300/month depending on deployment model
3. **Overkill for Phase 1**: Simple temporal queries achievable with Convex event sourcing
4. **Sync complexity**: Two-system architecture increases failure modes

### 3.3 Mem0

**What it is**: Mem0 is a memory layer for AI applications focusing on user and session-level memory persistence with automatic importance scoring and memory consolidation.

**Pricing (January 2026)**:

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Free | $0 | 1,000 memories, 100 searches/day | Development only |
| Pro | $249/month | 100,000 memories, unlimited searches | Production use |
| Enterprise | Custom | Custom limits, dedicated infrastructure | Large organizations |

**Capabilities assessment**:

| Capability | Support | Notes |
|------------|---------|-------|
| **Session isolation** | ✅ Excellent | Core strength; clean session boundaries |
| **User memory** | ✅ Yes | Long-term user preferences and context |
| **Semantic search** | ✅ Yes | Vector search with importance weighting |
| **Memory consolidation** | ✅ Yes | Automatic summarization and deduplication |
| **History tracking** | ✅ Yes | `get_all` API with change history |
| **Temporal queries** | ⚠️ Limited | History available but no point-in-time |

**Why Mem0 might be valuable**:

1. **Session management**: Clean session boundaries for planning conversations
2. **Automatic consolidation**: Reduces memory bloat over long conversations
3. **Change history**: `get_all` returns memory evolution

**Why Mem0 might not be needed**:

1. **High cost**: $249/month is expensive for capabilities Convex approximates
2. **Session focus**: Less suited for project-level and ecosystem-level memory
3. **Limited temporal queries**: No bi-temporal support
4. **Overlap with Convex**: Session memory achievable with Convex + TTL cleanup

### 3.4 Custom Vector Stores (Qdrant, Pinecone, Weaviate)

**When separate vector database is justified**:

| Scenario | Recommendation |
|----------|----------------|
| Convex vector search insufficient | ❌ Convex handles Compass scale |
| Need advanced temporal filtering | ⚠️ Qdrant datetime filters helpful |
| Multi-tenant isolation critical | ❌ Convex namespace isolation adequate |
| Sub-10ms latency required | ⚠️ Dedicated vector DB may help |
| Cost optimization at massive scale | ❌ Compass scale doesn't justify |

**Qdrant** (most relevant for temporal use case):

| Feature | Support |
|---------|---------|
| **Datetime filtering** | ✅ Native datetime type with range queries |
| **Payload filtering** | ✅ Rich filtering on metadata |
| **Hybrid search** | ✅ Vector + keyword via sparse vectors |
| **Cost** | Free tier: 1GB, 1M vectors; Cloud: $25+/month |

**Temporal query in Qdrant**:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, DatetimeRange

client = QdrantClient(url="...")

# Query: Decisions created before January 15, 2026
results = client.search(
    collection_name="project_memory",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="valid_from",
                range=DatetimeRange(lte="2026-01-15T00:00:00Z")
            ),
            FieldCondition(
                key="project_id",
                match={"value": "compass"}
            )
        ]
    ),
    limit=10
)
```

**Recommendation**: Qdrant as optional Phase 2 addition if Convex temporal filtering proves inadequate. Free tier sufficient for evaluation.

---

## Part 4: Temporal Query Architecture

### 4.1 Temporal Query Patterns

Compass requires three categories of temporal queries:

**Category 1: Recency-weighted retrieval** (supported by Convex natively)

"What are the recent decisions about authentication?"
- Implementation: Sort by `createdAt` descending, apply recency decay to relevance scores
- Convex support: ✅ Native via `order("desc")` and importance weighting in @convex-dev/rag

**Category 2: Point-in-time queries** (requires custom implementation)

"What was decided about authentication as of January 15?"
- Implementation: Filter where `validFrom <= targetDate AND (validUntil > targetDate OR validUntil IS NULL)`
- Convex support: ⚠️ Requires application-level filtering or event sourcing

**Category 3: Change tracking** (requires event sourcing)

"What changed about authentication between January 1 and January 15?"
- Implementation: Query decision events in date range, group by entity
- Convex support: ⚠️ Requires explicit event log table

### 4.2 Uni-Temporal vs Bi-Temporal

**Uni-temporal** (recommended for Phase 1-2):

Tracks one time dimension: "valid time" (when the fact was true in the real world).

```typescript
// Uni-temporal schema
projectMemory: defineTable({
  // ... other fields
  validFrom: v.number(),  // When this decision became effective
  validUntil: v.optional(v.number()),  // When superseded (null = current)
})
```

Enables:
- "Current decisions" → `validUntil IS NULL`
- "Decisions as of date X" → `validFrom <= X AND (validUntil > X OR validUntil IS NULL)`
- "Decision history" → All versions of a decision ID

Does not enable:
- "What did we know about X as of date Y?" (transaction time)
- "When was decision X recorded?" (distinct from when it became effective)

**Bi-temporal** (recommended for Phase 3 if needed):

Tracks two time dimensions: "valid time" and "transaction time" (when recorded in system).

```typescript
// Bi-temporal schema
projectMemory: defineTable({
  // ... other fields
  validFrom: v.number(),      // When this became true in real world
  validUntil: v.optional(v.number()),  // When superseded in real world
  recordedAt: v.number(),     // When recorded in system
  supersededAt: v.optional(v.number()),  // When this record was superseded
})
```

Enables:
- "What did we know as of system date X?" → Filter by `recordedAt <= X AND (supersededAt > X OR supersededAt IS NULL)`
- "When did we learn about decision Y?" → Query by `decisionId`, sort by `recordedAt`
- Audit trail of knowledge evolution

**Recommendation**: Start with uni-temporal; bi-temporal only justified for audit/compliance requirements.

### 4.3 Event Sourcing Pattern

For complete temporal reconstruction, implement event sourcing:

```typescript
// Event types for decision lifecycle
type DecisionEvent = 
  | { type: "created"; content: string; validFrom: number }
  | { type: "modified"; content: string; previousContent: string; validFrom: number }
  | { type: "superseded"; supersededBy: string; validUntil: number }
  | { type: "reverted"; revertedFrom: string; validFrom: number };

// Event log table
decisionEvents: defineTable({
  decisionId: v.string(),
  projectId: v.string(),
  eventType: v.string(),
  eventData: v.any(), // JSON blob with event details
  occurredAt: v.number(), // When the event happened
  recordedAt: v.number(), // When we recorded it (usually same, but not always)
  actor: v.string(), // Who/what caused the event
})
  .index("by_decision", ["decisionId", "occurredAt"])
  .index("by_project", ["projectId", "occurredAt"])
```

**Temporal query implementation**:

```typescript
// Reconstruct project state as of a specific date
async function getProjectStateAsOf(
  ctx: QueryCtx, 
  projectId: string, 
  asOfDate: number
): Promise<Map<string, DecisionState>> {
  // Get all events up to the target date
  const events = await ctx.db
    .query("decisionEvents")
    .withIndex("by_project", q => q.eq("projectId", projectId))
    .filter(q => q.lte(q.field("occurredAt"), asOfDate))
    .order("asc")
    .collect();
  
  // Replay events to build state
  const state = new Map<string, DecisionState>();
  for (const event of events) {
    applyEvent(state, event);
  }
  
  return state;
}

function applyEvent(state: Map<string, DecisionState>, event: DecisionEvent) {
  switch (event.eventType) {
    case "created":
      state.set(event.decisionId, {
        content: event.eventData.content,
        validFrom: event.eventData.validFrom,
        validUntil: null,
      });
      break;
    case "superseded":
      const existing = state.get(event.decisionId);
      if (existing) {
        existing.validUntil = event.eventData.validUntil;
      }
      break;
    // ... handle other event types
  }
}
```

---

## Part 5: Infinite Context Architecture

### 5.1 The Infinite Context Problem

Compass planning conversations can span weeks, generating context that exceeds LLM context windows. The System Definition (§3.2) requires "cross-session, temporally-aware project memory."

**Challenge**: A typical planning workflow might generate:
- 50+ conversation turns per session
- 10+ sessions per project
- 500+ artifacts, decisions, and research findings

This easily exceeds 200K token context limits even with efficient encoding.

### 5.2 Hierarchical Memory Architecture (MemGPT Pattern)

The solution is hierarchical memory with automatic summarization, inspired by MemGPT/Letta architecture:

**Layer 1: Working Memory (In-Context)**
- Current conversation turns (last 10-20 messages)
- Active decision being discussed
- Immediate constraints and requirements
- Size: ~10K tokens

**Layer 2: Session Memory (Fast Retrieval)**
- Full current session history
- Session-specific context and goals
- Retrieval: Semantic search + recency weighting
- Size: ~50K tokens (summarized if larger)

**Layer 3: Project Memory (Indexed Retrieval)**
- All decisions, artifacts, constraints for project
- Cross-session context
- Retrieval: Semantic search with temporal filtering
- Size: Unlimited (only relevant portions retrieved)

**Layer 4: Ecosystem Memory (Pattern Matching)**
- Cross-project conventions and standards
- Prior solutions to similar problems
- Anti-patterns and lessons learned
- Retrieval: Semantic search for pattern matching

**Implementation in Convex**:

```typescript
// Hierarchical memory retrieval
export const getContextForPlanning = query({
  args: { 
    projectId: v.string(), 
    sessionId: v.string(),
    currentQuery: v.string(),
  },
  handler: async (ctx, { projectId, sessionId, currentQuery }) => {
    const embedding = await generateEmbedding(currentQuery);
    
    // Layer 1: Working memory (passed in context, not stored)
    
    // Layer 2: Session memory (recent, high relevance threshold)
    const sessionMemories = await ctx.db
      .query("sessionMemory")
      .withIndex("by_session", q => q.eq("sessionId", sessionId))
      .order("desc")
      .take(20);
    
    // Layer 3: Project memory (semantic search)
    const projectMemories = await ctx.vectorSearch("projectMemory", "by_embedding", {
      vector: embedding,
      limit: 15,
      filter: q => q.eq("projectId", projectId),
    });
    
    // Layer 4: Ecosystem patterns (semantic search)
    const ecosystemPatterns = await ctx.vectorSearch("ecosystemPatterns", "by_embedding", {
      vector: embedding,
      limit: 5,
    });
    
    // Assemble context with priority ordering
    return {
      session: summarizeIfNeeded(sessionMemories, 5000),
      project: formatRetrievedMemories(projectMemories, 8000),
      ecosystem: formatPatterns(ecosystemPatterns, 2000),
    };
  },
});

// Automatic session summarization when exceeding threshold
async function summarizeIfNeeded(
  memories: SessionMemory[], 
  maxTokens: number
): Promise<string> {
  const totalTokens = estimateTokens(memories);
  
  if (totalTokens <= maxTokens) {
    return formatMemories(memories);
  }
  
  // Summarize older memories, keep recent verbatim
  const recent = memories.slice(0, 10);
  const older = memories.slice(10);
  
  const summary = await generateSummary(older);
  return formatWithSummary(recent, summary);
}
```

### 5.3 Memory Consolidation Strategy

Periodic consolidation prevents memory bloat:

```typescript
// Scheduled job for memory maintenance
export const consolidateProjectMemory = internalAction({
  handler: async (ctx) => {
    const projects = await ctx.runQuery(internal.projects.listActive);
    
    for (const project of projects) {
      // 1. Merge duplicate/similar memories
      await mergeSimilarMemories(ctx, project.id);
      
      // 2. Summarize old session memories
      await summarizeOldSessions(ctx, project.id, 30); // 30 days
      
      // 3. Promote patterns to ecosystem memory
      await promoteCommonPatterns(ctx, project.id);
      
      // 4. Archive superseded decisions
      await archiveSuperseded(ctx, project.id, 90); // 90 days
    }
  },
});

// Run daily
export const scheduleConsolidation = cronJobs.daily(
  "consolidate memory",
  { hour: 3, minute: 0 }, // 3 AM
  internal.memory.consolidateProjectMemory
);
```

---

## Part 6: Graceful Degradation

### 6.1 Failure Modes

Memory system failures should not crash Compass. The System Definition (§3.8) requires the system to "degrade gracefully when external services are unavailable."

**Failure scenarios**:

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Vector search unavailable | No semantic retrieval | Fall back to keyword search |
| External memory service down | No enriched context | Use Convex-only memory |
| Embedding API unavailable | No new embeddings | Use cached embeddings, queue for later |
| High latency | Poor user experience | Timeout and return partial results |

### 6.2 Circuit Breaker Pattern

```typescript
// Circuit breaker for external memory services
class MemoryCircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: "closed" | "open" | "half-open" = "closed";
  
  private readonly failureThreshold = 5;
  private readonly recoveryTimeout = 60000; // 1 minute
  
  async call<T>(fn: () => Promise<T>, fallback: () => T): Promise<T> {
    if (this.state === "open") {
      if (Date.now() - this.lastFailure > this.recoveryTimeout) {
        this.state = "half-open";
      } else {
        return fallback();
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      return fallback();
    }
  }
  
  private onSuccess() {
    this.failures = 0;
    this.state = "closed";
  }
  
  private onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.failureThreshold) {
      this.state = "open";
    }
  }
}

// Usage in memory retrieval
const memoryCircuitBreaker = new MemoryCircuitBreaker();

export const getEnrichedContext = action({
  args: { query: v.string(), projectId: v.string() },
  handler: async (ctx, { query, projectId }) => {
    // Always get Convex memory (local, reliable)
    const convexMemory = await ctx.runQuery(api.memory.search, { query, projectId });
    
    // Attempt external enrichment with circuit breaker
    const externalMemory = await memoryCircuitBreaker.call(
      () => fetchExternalMemory(query, projectId),
      () => null // Fallback: no external memory
    );
    
    return {
      primary: convexMemory,
      enriched: externalMemory,
    };
  },
});
```

### 6.3 Cache Strategy

```typescript
// Memory cache with TTL
const memoryCache = new Map<string, { data: any; expiresAt: number }>();

function getCached<T>(key: string): T | null {
  const cached = memoryCache.get(key);
  if (cached && cached.expiresAt > Date.now()) {
    return cached.data as T;
  }
  memoryCache.delete(key);
  return null;
}

function setCache<T>(key: string, data: T, ttlMs: number): void {
  memoryCache.set(key, { data, expiresAt: Date.now() + ttlMs });
}

// Cache TTLs by memory type
const CACHE_TTL = {
  sessionMemory: 5 * 60 * 1000,      // 5 minutes
  activeDecisions: 5 * 60 * 1000,    // 5 minutes
  projectConventions: 15 * 60 * 1000, // 15 minutes
  ecosystemPatterns: 60 * 60 * 1000,  // 1 hour
  historicalContext: 60 * 60 * 1000,  // 1 hour
};
```

### 6.4 Fallback Hierarchy

When memory retrieval fails, degrade in stages:

1. **Primary**: Convex vector search + external enrichment
2. **Level 1 fallback**: Convex vector search only (skip external)
3. **Level 2 fallback**: Convex keyword search (skip vector)
4. **Level 3 fallback**: Cached results (may be stale)
5. **Level 4 fallback**: Embedded defaults (system prompts only)

```typescript
export const getMemoryWithFallback = action({
  args: { query: v.string(), projectId: v.string() },
  handler: async (ctx, { query, projectId }) => {
    // Try primary
    try {
      return await getPrimaryMemory(ctx, query, projectId);
    } catch (e) {
      console.warn("Primary memory failed, trying fallback 1");
    }
    
    // Try Convex-only
    try {
      return await getConvexOnlyMemory(ctx, query, projectId);
    } catch (e) {
      console.warn("Convex vector failed, trying fallback 2");
    }
    
    // Try keyword search
    try {
      return await getKeywordMemory(ctx, query, projectId);
    } catch (e) {
      console.warn("Keyword search failed, trying fallback 3");
    }
    
    // Try cache
    const cached = getCached(`memory:${projectId}:${hashQuery(query)}`);
    if (cached) {
      return { ...cached, stale: true };
    }
    
    // Return embedded defaults
    return {
      primary: [],
      enriched: null,
      fallback: true,
      message: "Memory system unavailable; proceeding with limited context",
    };
  },
});
```

---

## Part 7: Cost Analysis

### 7.1 Convex-Only Costs

Convex pricing is bundled with backend costs (already budgeted in ADR-01-01):

| Component | Phase 1 | Phase 3 | Notes |
|-----------|---------|---------|-------|
| Vector storage | Included | Included | Part of document storage |
| Vector search queries | Included | Included | Part of function calls |
| Embedding generation | $0-10/month | $20-50/month | OpenAI ada-002 API calls |
| **Total memory cost** | **$0-10/month** | **$20-50/month** | |

### 7.2 External Service Costs

| Service | Phase 1 | Phase 3 | Value Add |
|---------|---------|---------|-----------|
| **Supermemory Pro** | $19/month | $19-99/month | MCP integration, managed service |
| **Zep Graphiti (self-hosted)** | $40-70/month | $70-150/month | Bi-temporal graphs |
| **Zep Cloud** | $150/month | $150-300/month | Managed bi-temporal |
| **Mem0 Pro** | $249/month | $249/month | Session memory, consolidation |
| **Qdrant Cloud** | $0-25/month | $25-50/month | Temporal filtering, hybrid search |

### 7.3 Recommended Budget Allocation

**Phase 1 (<$100/month budget)**:

| Component | Allocation | Recommendation |
|-----------|------------|----------------|
| Convex memory | $0-10 | Built-in @convex-dev/rag |
| Embeddings (OpenAI) | $10-20 | ada-002 for all embeddings |
| External service | $0 | Not needed |
| **Total** | **$10-30/month** | |

**Phase 3 (<$400/month budget)**:

| Component | Allocation | Recommendation |
|-----------|------------|----------------|
| Convex memory | $20-50 | Built-in @convex-dev/rag |
| Embeddings (OpenAI) | $30-50 | ada-002 for all embeddings |
| External service (optional) | $0-100 | Zep Graphiti if bi-temporal needed |
| **Total** | **$50-200/month** | |

---

## Part 8: Recommendations

### 8.1 Primary Recommendation: Convex-Only Architecture

For Phase 1-2, implement memory entirely within Convex using @convex-dev/rag:

**Architecture**:

1. **Session memory**: Convex table with TTL-based cleanup, namespace isolation via `session:{id}` prefix
2. **Project memory**: Convex table with uni-temporal fields (`validFrom`, `validUntil`), namespace isolation via `project:{id}` prefix
3. **Ecosystem memory**: Convex table for cross-project patterns, `ecosystem` namespace
4. **Event log**: Convex table for decision events, enabling temporal reconstruction
5. **Hierarchical retrieval**: Multi-stage query combining recent (session) → relevant (project) → pattern (ecosystem)

**Why Convex-only**:

- Convex @convex-dev/rag provides namespace isolation, hybrid search, and filtering
- Event sourcing pattern enables temporal queries without external services
- Single system reduces operational complexity
- Cost: $10-30/month vs $100-400/month for external services
- Integration: No sync complexity, single source of truth

### 8.2 Alternative: Convex + Zep Graphiti (Phase 3)

If bi-temporal knowledge graphs become critical (complex cross-project dependencies, audit requirements):

**When to upgrade**:

- Planning workflows require "what did we know as of date X?" queries
- Entity relationships (decision → artifact → requirement → implementation) need graph traversal
- Contradiction detection across projects becomes important
- Budget allows $70-150/month additional infrastructure

**Integration pattern**:

- Convex remains source of truth for all data
- Zep Graphiti provides temporal reasoning layer
- Async sync from Convex to Zep via scheduled actions
- Query routing: Simple queries → Convex, temporal reasoning → Zep

### 8.3 Alternative: Convex + Supermemory (Phase 2-3)

If MCP integration and managed memory service are priorities:

**When to choose**:

- Compass heavily uses Claude's MCP for tool calling
- Sub-400ms memory latency critical for real-time planning
- Team prefers managed service over custom temporal implementation
- Budget allows $19-99/month additional service

**Integration pattern**:

- Convex stores canonical data
- Supermemory provides fast retrieval layer for active conversations
- Sync on write from Convex to Supermemory
- Fallback to Convex if Supermemory unavailable

### 8.4 Implementation Roadmap

**Phase 1 (Weeks 1-4)**:

1. Implement three-layer namespace schema in Convex
2. Set up @convex-dev/rag with hybrid search
3. Implement basic temporal filtering (`validFrom`, `validUntil`)
4. Build hierarchical retrieval function
5. Implement session TTL cleanup

**Phase 2 (Weeks 5-8)**:

1. Add event sourcing for decision history
2. Implement temporal reconstruction queries
3. Build memory consolidation jobs
4. Add graceful degradation with circuit breakers
5. Evaluate Qdrant for temporal filtering enhancement

**Phase 3 (Weeks 9-12)**:

1. Monitor temporal query patterns
2. If bi-temporal needed: Integrate Zep Graphiti
3. If MCP needed: Integrate Supermemory
4. Optimize retrieval latency
5. Scale embedding pipeline

---

## Part 9: Open Questions for Stakeholders

1. **Temporal query priority**: How critical is "state as of date X" functionality in Phase 1? If essential, Zep Graphiti investment may be justified earlier.

2. **MCP integration plans**: Will Compass use Claude's MCP for tool calling? If yes, Supermemory's native MCP support becomes more valuable.

3. **Audit requirements**: Are there regulatory or compliance requirements for tracking when decisions were recorded (transaction time)? This would justify bi-temporal architecture.

4. **Cross-project patterns**: How important is ecosystem memory in Phase 1? Could be deferred to Phase 2 if project memory is sufficient initially.

5. **Latency tolerance**: What memory retrieval latency is acceptable during planning conversations? Sub-100ms requires optimization; sub-1s is achievable with Convex-only.

---

## Appendix A: Glossary

**Bi-temporal**: Database pattern tracking both "valid time" (when fact was true) and "transaction time" (when recorded in system).

**Circuit breaker**: Pattern that stops calling a failing service temporarily to prevent cascade failures.

**Ecosystem memory**: Cross-project patterns, conventions, and prior solutions.

**Event sourcing**: Pattern where state is derived from a sequence of events rather than stored directly.

**Hierarchical memory**: Memory organized in layers with different persistence and retrieval characteristics.

**Namespace isolation**: Separating memory by prefix (e.g., `project:123`) to prevent cross-contamination.

**Point-in-time query**: Query asking "what was the state as of date X?"

**Project memory**: Decisions, constraints, and context for a specific project across sessions.

**Session memory**: Ephemeral memory for the current conversation.

**Temporal query**: Query involving time-based filtering or reconstruction.

**Uni-temporal**: Database pattern tracking only "valid time" (when fact was true).

**Working memory**: The portion of context actively loaded into an LLM's context window.

---

## Appendix B: Sources

1. **[T1/S1]** Convex. "@convex-dev/rag Documentation." Retrieved 2026-01-25. https://www.convex.dev/components/rag

2. **[T1/S1]** Convex. "Vector Search Documentation." Retrieved 2026-01-25. https://docs.convex.dev/search/vector-search

3. **[T1/S1]** Supermemory. "Developer Documentation." Retrieved 2026-01-25. https://supermemory.ai/developers

4. **[T1/S1]** Zep. "Graphiti Documentation." Retrieved 2026-01-25. https://help.getzep.com/graphiti

5. **[T1/S1]** Mem0. "Documentation." Retrieved 2026-01-25. https://docs.mem0.ai

6. **[T2/S2]** DataCamp. "Mem0 Tutorial: Persistent Memory Layer for AI Applications." Retrieved 2026-01-25. https://www.datacamp.com/tutorial/mem0-tutorial

7. **[T2/S2]** Qdrant. "Filtering Documentation." Retrieved 2026-01-25. https://qdrant.tech/documentation/concepts/filtering/

8. **[T3/S2]** LangChain. "MemGPT Integration Guide." Retrieved 2026-01-25. https://python.langchain.com/docs/integrations/memory/

9. **[T2/S2]** Pinecone. "Implement Multitenancy." Retrieved 2026-01-25. https://docs.pinecone.io/guides/index-data/implement-multitenancy

---

## Appendix C: Related Documents

- **RF-01-01**: Backend Platform Research Findings (Convex selection context)
- **ADR-01-01**: Backend Platform Selection (Convex as backend)
- **DD-13-01**: Artifact Taxonomy (memory entity definitions)
- **Compass System Definition**: §3.2 Memory requirements, §3.8 Reliability requirements
- **ADR-03-01**: Memory Architecture Selection (pending decision document)

---

*End of Memory and Retrieval Architecture Research Findings (RF-03-01)*
