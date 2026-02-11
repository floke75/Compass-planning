---
id: RF-03-02
type: rf
area: 03-memory-retrieval
title: Advanced Memory and Context Engineering Research Findings
status: draft
created: 2026-02-06
updated: 2026-02-06
author: compass-research
summary: Evaluates advanced memory systems and context engineering methodologies for Compass Phase 3, covering bi-temporal knowledge graphs (Graphiti/GraphZep), MCP-native memory, context assembly patterns, and dynamic branching state management, with recommendation for a layered enrichment architecture preserving the Convex-primary baseline
tags: [memory, mcp, context-engineering, 2026-research, graphiti, temporal, knowledge-graph]
related:
  - RF-03-01
  - ADR-03-01
  - ADR-01-01
  - ADR-02-01
  - DD-11-01
  - DD-18-01
  - DD-20-01
  - SYS-00
confidence: medium-high
methodology: "Web research with arXiv papers, GitHub repositories, official vendor documentation, framework documentation, developer blogs, and integration pattern analysis. Conducted February 2026."
limitations:
  - "Graphiti is Python-native; TypeScript port (GraphZep) is community-maintained with unverified production readiness"
  - "Supermemory MCP is undergoing v1 deprecation and monorepo migration as of January 2026"
  - "Context engineering is an emerging discipline; best practices are rapidly evolving"
  - "No hands-on implementation testing performed; findings are research-grade"
  - "Pricing and feature sets subject to change"
responds_to: ADR-03-01
implications_for: [ADR-03-01, ADR-02-01, DD-11-01, DD-18-01]
---

# Advanced Memory and Context Engineering Research Findings

## Executive Summary

**Primary Recommendation**: Adopt a **layered enrichment architecture** that preserves the Convex-primary baseline (ADR-03-01) while introducing three targeted enhancements: (1) a Convex-native event sourcing layer for bi-temporal queries, (2) Graphiti via MCP server as a sidecar for graph-based contextual retrieval, and (3) a structured Context Pack assembly pipeline using the Write-Select-Compress-Isolate (WSCI) pattern from established context engineering literature.

**Strategic Recommendation**: These findings **support a formal revision of ADR-03-01** to elevate the Phase 3 enrichment pathway from "optional" to "planned," with Graphiti (accessed via its MCP server) replacing Zep Cloud as the recommended external enrichment service. The revision should also formalize the Context Pack assembly pattern as a first-class architectural concern.

**Confidence**: Medium-High — The Graphiti framework has peer-reviewed validation (arXiv:2501.13956), sustained adoption (25,000+ weekly PyPI downloads, 22,500+ GitHub stars as of February 2026, up from 14K in July 2025), and a v1.0 MCP server release (November 2025) with hundreds of thousands of weekly users. However, its Python-native core introduces a TypeScript integration gap that requires either the community GraphZep port or MCP-mediated access. Context engineering patterns are well-documented by Anthropic, LangChain, Google ADK, and LlamaIndex but remain an emerging discipline without standardized tooling. Mastra's memory system has matured significantly since RF-03-01, now offering four distinct memory types (Message History, Working Memory, Semantic Recall, Observational Memory) that natively address ~60-70% of Compass context engineering requirements.

**Key Insight**: The critical evolution for Compass is not adding another memory database — it is transitioning from "retrieval" to "context assembly." The 2025-2026 industry consensus, crystallized by Andrej Karpathy and formalized by Anthropic's engineering team, is that context engineering is the successor to prompt engineering. For Compass, this means the memory system must not merely store and retrieve chunks; it must *assemble* coherent Context Packs (DD-11-01) through a deterministic pipeline of selection, compression, and isolation that respects branch boundaries (DD-18-01) and the Truth Hierarchy (SYS-00).

**Trade-offs accepted**:

- Graphiti via MCP introduces a Python sidecar process (Neo4j or FalkorDB dependency), adding operational complexity
- GraphZep (TypeScript port) is community-maintained by aexy-io with limited production verification
- Context Pack assembly patterns require custom implementation; no turnkey solution exists for the Compass-specific schema
- Bi-temporal event sourcing within Convex demands custom schema design, increasing initial development effort

---

## Part 1: Bi-Temporal and Temporal Memory

### 1.1 The Compass Requirement

ADR-03-01 deferred bi-temporal queries ("what was the state as of date X?") to Phase 2/3, noting this as the primary gap in the Convex-only baseline. The Questioning Arc (DD-18-01) creates a rich temporal dimension: decisions progress through EXPLORING → CHOSEN/REJECTED/BLOCKED/DEFERRED, branches fork and merge, and the Archivist must reconstruct state at arbitrary historical points for audit (SYS-00 Truth Hierarchy: Audit Truth).

The system requires two temporal dimensions:

- **Event Time (T)**: When a fact or decision actually occurred or became valid in the planning domain
- **Ingestion Time (T′)**: When the system recorded this information

This distinction is essential for retroactive corrections (a user realizes a constraint was different than recorded) and for audit trails that distinguish between "what we knew then" and "what we know now."

### 1.2 Graphiti's Bi-Temporal Model

Graphiti, the open-source knowledge graph engine underlying Zep, implements a rigorous bi-temporal model validated in the peer-reviewed paper "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" (arXiv:2501.13956, January 2025). Every edge in the Graphiti knowledge graph carries four timestamps [1]:

- `t_valid`: When the fact became true in the real world
- `t_invalid`: When the fact ceased to be true
- `t'_created`: When the system first recorded this fact
- `t'_expired`: When the system invalidated this record

This model enables the precise "as-of" queries Compass needs: "Reconstruct the state of decisions for Project X as they existed on January 15" requires filtering on `t'_created <= Jan 15 AND (t'_expired IS NULL OR t'_expired > Jan 15)`, giving the knowledge state at that ingestion point.

**Benchmark results**: Zep (powered by Graphiti) achieves 94.8% accuracy on the Deep Memory Retrieval benchmark versus MemGPT's 93.4%, and demonstrates up to 18.5% accuracy improvement on LongMemEval temporal reasoning tasks with 90% lower response latency [1].

### 1.3 Convex-Native Event Sourcing Alternative

For the Convex-primary path, bi-temporal queries can be implemented through event sourcing schema patterns within Convex itself, as outlined in ADR-03-01's Phase 2 code sketch. The approach stores immutable `decisionEvents` with both `occurredAt` (event time) and `recordedAt` (ingestion time) fields, then reconstructs state by replaying events up to the target timestamp.

**Advantages**: No external dependencies, full TypeScript native, serializable transactions, real-time reactivity.

**Limitations**: Requires custom projection logic for each entity type; no pre-built graph traversal for relationship queries; replay performance degrades linearly with event volume without snapshot optimization.

**Recommendation**: Implement Convex event sourcing for the core decision timeline (the primary audit requirement) and reserve Graphiti for cross-entity relationship queries that demand graph traversal (e.g., "which decisions were affected when Constraint X changed?").

### 1.4 Evidence Assessment

| Source | Grade | Notes |
|--------|-------|-------|
| arXiv:2501.13956 (Zep paper) | [T1/S1] | Peer-reviewed, benchmarked, reproducible |
| Graphiti GitHub (getzep/graphiti) | [T1/S1] | 22K+ stars (from 14K in July 2025), 25K weekly downloads, 79+ contributors, MCP Server v1.0 |
| Neo4j blog on Graphiti | [T2/S2] | Vendor-endorsed technical analysis |
| Bi-temporal event sourcing literature | [T3/S2] | Well-established pattern, multiple production reports |
| Convex event sourcing sketch (ADR-03-01) | [T4/S3] | Untested internal design; plausible but unvalidated |

---

## Part 2: Graph-Based Contextual Retrieval

### 2.1 Graphiti Deep Dive

Graphiti (github.com/getzep/graphiti) is the strongest candidate for graph-based contextual retrieval. It is designed for exactly the Compass use case: dynamically building knowledge graphs from ongoing conversations while maintaining temporal relationships.

**Architecture**: Graphiti uses a multi-subgraph hierarchy:

- **Episodic Subgraph**: Records raw data episodes (conversations, JSON imports) as immutable records
- **Semantic Subgraph**: Extracted entities, relationships, and facts with temporal validity
- **Community Subgraph**: Thematic clusters of related entities for high-level reasoning

**Search**: Graphiti implements hybrid retrieval combining cosine semantic similarity, BM25 keyword search, and breadth-first graph traversal — critically, without LLM calls during retrieval, achieving P95 latency of 300ms [5].

**Database backends**: Neo4j (default), FalkorDB (496x faster at P99 latency, 6x memory efficiency), Amazon Neptune, and Kuzu. For Compass, FalkorDB is attractive due to its Docker simplicity and performance characteristics.

**MCP Server**: Graphiti includes a native MCP server implementation in its `mcp_server/` directory, enabling any MCP-aware client to interact with the knowledge graph via the Model Context Protocol. This directly satisfies ADR-04-01's MCP-native mandate.

**LLM Support**: Anthropic Claude is supported for inference alongside OpenAI and Groq, aligning with ADR-09-01's tiered LLM strategy.

### 2.2 GraphZep: The TypeScript Port

A community TypeScript reimplementation called **GraphZep** (github.com/aexy-io/graphzep) directly addresses the Compass stack requirement for TypeScript-native solutions (ADR-01-01):

- Full TypeScript implementation with Zod validation
- 100% API compatibility with Graphiti Python on base level
- Neo4j and FalkorDB driver support
- Multi-modal memory types: episodic, semantic, and procedural
- Bi-temporal data model with event occurrence tracking
- Built-in MCP server in the `mcp_server/` directory
- LLM integration: OpenAI, Anthropic, Google Gemini, and Groq

**Caution**: GraphZep is maintained by aexy-io, a smaller organization. The repository has limited stars and contributors compared to the official Graphiti Python repository. It warrants careful evaluation against slop detection criteria (Section 5).

### 2.3 OpenMemory (Mem0 / CaviraOSS)

**OpenMemory** (github.com/CaviraOSS/OpenMemory) is an emerging alternative that ships a native MCP server and supports temporal fact storage with `valid_from` fields. It offers:

- Native MCP server for any MCP-aware client
- Migration tooling to import from Mem0, Zep, and Supermemory
- Integrations with LangChain, CrewAI, AutoGen
- Connectors for GitHub, Notion, Google Drive
- Temporal fact API with subject-predicate-object triples

However, OpenMemory is newer and has less production validation than Graphiti. It is worth monitoring but is not recommended as the primary enrichment layer at this time.

### 2.4 Comparison Matrix

| Criterion | Graphiti (Python) | GraphZep (TypeScript) | OpenMemory |
|-----------|-------------------|-----------------------|------------|
| **TypeScript Native** | ❌ Python | ✅ Full TypeScript | ✅ Python + TS client |
| **Bi-Temporal Model** | ✅ Four timestamps | ✅ Event occurrence tracking | ⚠️ Basic `valid_from` |
| **MCP Server** | ✅ Native | ✅ Native | ✅ Native |
| **Graph Database** | ✅ Neo4j/FalkorDB/Neptune/Kuzu | ✅ Neo4j/FalkorDB | ⚠️ Not graph-native |
| **Benchmark Validation** | ✅ arXiv paper, DMR + LongMemEval | ❌ None published | ❌ None published |
| **Production Adoption** | ✅ 25K weekly downloads | ⚠️ Limited | ⚠️ Limited |
| **Compass Stack Fit** | Medium (MCP bridge) | High (native TS) | Medium (MCP bridge) |
| **Risk Level** | Low | Medium-High | Medium |

---

## Part 3: MCP-Native Memory Systems

### 3.1 The MCP Memory Landscape (February 2026)

The Model Context Protocol has matured into the standard interface for AI-tool integrations. ADR-04-01 mandates MCP as the primary integration pattern. Several memory systems now expose MCP servers natively:

**Tier 1 — Production-Grade MCP Memory**:

1. **Anthropic Reference Memory Server** (`@modelcontextprotocol/server-memory`): Official reference implementation using a knowledge-graph-style JSONL store. Lightweight, well-documented, but lacks temporal awareness and semantic search.

2. **Graphiti MCP Server** (v1.0, November 2025): Ships with the Graphiti repository. Provides full access to temporal knowledge graph capabilities via MCP tools. Deployable via Docker with Neo4j or FalkorDB. Reports hundreds of thousands of weekly users across Claude Desktop, Cursor, and other MCP clients. Backed by contributions from AWS, Microsoft, FalkorDB, and Neo4j.

**Tier 2 — Emerging MCP Memory**:

3. **Supermemory MCP** (supermemoryai/supermemory-mcp): Universal memory system for cross-LLM portability. TypeScript-based. Currently undergoing v1 deprecation and monorepo migration. The hosted version requires no login; self-hosting uses an API key. Approximately 1,600 GitHub stars.

4. **OpenMemory MCP**: Native MCP server with temporal facts, migration tooling, and broad integration support.

5. **MCP Memory Service** (doobidoo/mcp-memory-service): SQLite-vec backed memory with optional ML capabilities. Supports 13+ AI tools. Uses lightweight ONNX embeddings by default.

### 3.2 Supermemory Assessment

Supermemory was identified as a primary alternative in ADR-03-01. Current status (February 2026):

- The original MCP v1 is being deprecated in favor of a monorepo at `supermemoryai/supermemory/tree/main/apps/mcp`
- Hosted version available at `app.supermemory.ai` with no login required
- Self-hosting via `console.supermemory.ai` API key
- MIT licensed, TypeScript-native
- Approximately 1,600 stars on the MCP repository

**Concern**: The active deprecation/migration suggests architectural instability. While the TypeScript-native implementation aligns with Compass requirements, the lack of bi-temporal capabilities and the migration uncertainty make it a weaker candidate than Graphiti for the enrichment layer.

**Revised Assessment**: Supermemory is better suited as a cross-tool memory portability layer (enabling Compass memories to be accessible in Claude Desktop, Cursor, etc.) than as the primary context retrieval engine. It could complement Graphiti rather than replace it.

### 3.3 MCP Integration Architecture for Compass

The recommended architecture uses MCP as the integration protocol between Compass and external memory services, preserving the Convex-primary baseline:

```
┌──────────────────────────────────────────────┐
│            Compass (Mastra + Convex)          │
│                                               │
│  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Session Mem  │  │ Context Pack Assembler  │ │
│  │ (Convex RAG) │  │ (WSCI Pipeline)         │ │
│  └─────────────┘  └──────────┬──────────────┘ │
│  ┌─────────────┐             │                │
│  │ Project Mem  │             │                │
│  │ (Convex RAG) │      ┌─────▼─────┐          │
│  └─────────────┘      │ MCP Client │          │
│  ┌─────────────┐      └─────┬─────┘          │
│  │ Event Log   │            │                 │
│  │ (Convex ES) │      ┌─────▼─────┐          │
│  └─────────────┘      │ MCP Server│          │
│                        └─────┬─────┘          │
└──────────────────────────────┼────────────────┘
                               │
                  ┌────────────▼────────────┐
                  │ Graphiti MCP Server     │
                  │ (Docker: FalkorDB +     │
                  │  Graphiti Python)        │
                  └─────────────────────────┘
```

This architecture:

- Keeps Convex as the source of truth for all three memory layers
- Uses MCP as the protocol for enrichment queries to Graphiti
- Preserves namespace isolation (Convex prefixes remain authoritative)
- Supports graceful degradation (if Graphiti is unavailable, Convex RAG still works)
- Satisfies ADR-04-01's MCP mandate

---

## Part 4: Long-Context Window Management and Context Pack Assembly

### 4.1 Context Engineering: The Paradigm Shift

The 2025-2026 research landscape has crystallized around a fundamental insight: **context engineering is the successor to prompt engineering**. This was formalized by:

- **Andrej Karpathy**: "Context engineering is the delicate art and science of filling the context window with just the right information for the next step" [7]
- **Anthropic's Engineering Team**: "Context, therefore, must be treated as a finite resource with diminishing marginal returns... LLMs have an 'attention budget' that they draw on when parsing large volumes of context" [8]
- **Google ADK Team**: "Separate storage from presentation... Context is built through named, ordered processors, not ad-hoc string concatenation" [9]
- **ACE Framework (arXiv:2510.04618)**: Agentic Context Engineering treats contexts as "evolving playbooks that accumulate, refine, and organize strategies through a modular process of generation, reflection, and curation" [10]

### 4.2 The WSCI Pattern for Compass

The industry has converged on four core context management strategies, identified by LangChain and echoed by LlamaIndex, Anthropic, and Google. We map these to Compass concepts:

**Write**: Persist context to external storage

- Compass mapping: Decisions, artifacts, and evidence are written to Convex tables and the Obsidian vault. The Archivist (DD-18-01) maintains the dependency graph as external state.

**Select**: Retrieve relevant context via search, tools, or structured lookup

- Compass mapping: The Context Pack (DD-11-01 Section 3.7) requires selecting relevant decisions, evidence, and source materials. This maps to multi-stage retrieval: recent (session) → relevant (project) → patterns (ecosystem).

**Compress**: Reduce context volume through summarization, trimming, or pruning

- Compass mapping: For long planning sessions spanning weeks, conversation history must be compressed. The MemAgent approach (Yu et al., 2025) of reinforcement-learned memory slot management is applicable: keep structured decisions intact while compressing exploratory dialogue.

**Isolate**: Split context across sub-agents or tool-specific windows

- Compass mapping: Research branches (DD-18-01) naturally isolate context. Each branch gets its own context window allocation. The Archivist operates with isolated context focused on dependency analysis.

### 4.3 Context Pack Assembly Pipeline

For Compass, the Context Pack (DD-11-01) is the concrete instantiation of context engineering. The assembly pipeline should be deterministic and auditable:

```
Stage 1: COLLECT
  ├── Query Convex for decisions matching project namespace
  ├── Query Convex for active constraints and requirements  
  ├── Query Graphiti (via MCP) for entity relationships
  └── Retrieve evidence citations from the pristine context layer

Stage 2: RANK
  ├── Recency weighting (recent decisions rank higher)
  ├── Dependency weighting (decisions with unresolved deps rank higher)
  ├── Relevance weighting (semantic similarity to current query)
  └── Branch-awareness (filter to current branch context)

Stage 3: COMPRESS
  ├── Full text for CHOSEN/BLOCKED decisions
  ├── Summary-only for REJECTED/DEFERRED decisions
  ├── Snippet-only for ecosystem patterns
  └── Metadata-only for expired evidence (with freshness warning)

Stage 4: FORMAT
  ├── Assemble into JSON-serializable Context Pack schema
  ├── Include token budget metadata
  ├── Tag with provenance for audit trail
  └── Validate against STD-11-01 minimum requirements
```

### 4.4 Context Rot and Degradation Mitigation

Anthropic's engineering team identifies **context rot** as a key failure mode: as token count increases, recall accuracy decreases due to the n² attention scaling problem. For Compass planning sessions that span weeks:

- **Conversation compaction**: After each session, compress dialogue into structured decision summaries. Google ADK's compaction model (summarize older events over a sliding window) maps to Mastra's thread-based memory.
- **Context isolation via branches**: Research branches receive their own context windows, preventing the main arc's context from bloating during investigation phases.
- **Priority ordering**: Place the most critical context (active constraints, BLOCKED decisions) at the beginning and end of the context window, exploiting the known recency and primacy biases in LLM attention.

### 4.5 Model Strategy Alignment

Per ADR-09-01's tiered strategy (Claude Opus 4.5 / Gemini 3 Pro), the context assembly pipeline must be model-aware:

- **Claude (200K context)**: Supports larger Context Packs but benefits from structured formatting (XML tags, clear section delimiters)
- **Gemini (1M+ context)**: Can accommodate fuller project history but still benefits from compression to reduce latency and cost
- **Cost optimization**: Compress aggressively for routine queries; expand for complex cross-project analysis

---

## Part 5: Dynamic Branching State

### 5.1 The Compass Branching Requirement

DD-18-01 defines two branch types that require distinct memory isolation:

- **Research Branches**: Linear investigation ("I don't know X") → Findings document
- **Exploration Branches**: Git-like fork ("A or B — let's see which") → Design comparison

Both require that branch state is isolated, serializable to JSON, and mergeable via human-approved merge gates. The memory system must track which decisions, artifacts, and evidence belong to which branch without cross-contamination.

### 5.2 Convex-Native Branch Isolation

The recommended approach for branch isolation leverages Convex's namespace prefixing (ADR-03-01) extended with branch identifiers:

```
Namespace pattern: {layer}:{project}:{branch}:{entity}

Examples:
  session:proj-001:main:current-question
  project:proj-001:main:decisions
  project:proj-001:branch-research-api:findings
  project:proj-001:branch-explore-arch-a:decisions
  project:proj-001:branch-explore-arch-b:decisions
```

**Merge operation**: When a branch merges via merge gate, the Archivist:

1. Compares decision sets between branch and main using the dependency graph
2. Detects CONFLICTS_WITH relationships
3. Surfaces conflicts for human resolution
4. Copies approved decisions from branch namespace to main namespace
5. Archives the branch namespace (retained for audit, not deleted)

### 5.3 Graphiti's Role in Branch Context

Graphiti's episodic subgraph naturally supports branching. Each branch creates its own episodes, and entity relationships can be tagged with branch provenance. When merging:

- New entities discovered during research are promoted to the main graph
- Conflicting facts (same entity, different values) surface temporal conflicts
- The bi-temporal model preserves the branch's "knowledge state" for historical audit

### 5.4 Mastra's Suspend/Resume for Branch State

Mastra's `suspend()` function (ADR-02-01) maps to branch state checkpointing. When a research branch is initiated:

1. The main arc's state is serialized via `suspend()`
2. A new workflow thread is created with the branch namespace
3. Research proceeds with isolated memory context
4. On merge gate approval, findings are integrated into the main arc's state
5. The main arc resumes from the suspension point with enriched context

Mastra's thread-based memory with `resourceId` and `threadId` scoping provides the foundation, but Compass-specific branch semantics require a custom orchestration layer on top.

---

## Part 6: Slop Detection and Evidence Quality

### 6.1 Slop Detection Results

Per DD-20-01 and the RF-21-01 "Claude-Flow" exclusion benchmark, all candidates were assessed for artificial engagement signals:

| Candidate | Stars | Weekly Downloads | Contributors | Slop Signals | Assessment |
|-----------|-------|------------------|--------------|--------------|------------|
| **Graphiti** | 22,500+ | 25,000+ | 79+ | None detected; 60% growth in 6 months validates organic adoption | ✅ Legitimate |
| **GraphZep** | ~50 | N/A (npm) | ~3 | Low star count, small team | ⚠️ Monitor |
| **Supermemory MCP** | ~1,600 | N/A | ~10 | Active deprecation/migration | ⚠️ Instability |
| **OpenMemory** | ~2,000 | N/A | ~15 | Young project, rapid claims | ⚠️ Monitor |
| **MCP Memory Service** | ~1,200 | N/A | ~5 | Reasonable for scope | ✅ Legitimate |

**GraphZep Flag**: The aexy-io/graphzep repository claims "100% API compatibility" with Graphiti Python — a strong claim for a community port of a complex system. This warrants validation testing before production adoption.

### 6.2 Source Quality Summary

All sources used in this research are graded per DD-20-01:

| # | Source | Grade | Notes |
|---|--------|-------|-------|
| [1] | Rasmussen et al. "Zep: A Temporal Knowledge Graph Architecture" arXiv:2501.13956 | [T1/S1] I1 | Peer-reviewed, benchmarked, January 2025 |
| [2] | Graphiti GitHub Repository (getzep/graphiti) | [T1/S1] I1 | Official source, actively maintained |
| [3] | GraphZep GitHub (aexy-io/graphzep) | [T4/S3] I3 | Community port, limited validation |
| [4] | Supermemory GitHub (supermemoryai/supermemory-mcp) | [T1/S2] I2 | Official, but undergoing migration |
| [5] | Neo4j Blog: "Graphiti: Knowledge Graph Memory" | [T2/S1] I2 | Vendor-endorsed, technically sound |
| [6] | FalkorDB Blog: "Graphiti + FalkorDB Integration" | [T2/S2] I2 | Vendor-endorsed, benchmark claims |
| [7] | LangChain Blog: "Context Engineering for Agents" | [T2/S1] I2 | Industry reference, well-cited |
| [8] | Anthropic: "Effective Context Engineering for AI Agents" | [T1/S1] I1 | Authoritative, from LLM vendor |
| [9] | Google Developers Blog: "Architecting Context-Aware Multi-Agent Framework" | [T1/S1] I2 | Authoritative, ADK team |
| [10] | Zhang et al. "ACE: Agentic Context Engineering" arXiv:2510.04618 | [T1/S1] I2 | Peer-reviewed, January 2026 revision |
| [11] | LlamaIndex Blog: "Context Engineering Guide" | [T2/S1] I2 | Industry reference, framework vendor |
| [12] | Mastra Documentation: Agent Memory | [T1/S1] I1 | Official framework docs |
| [13] | MCP Memory Benchmark (aimultiple.com) | [T3/S2] I3 | Independent benchmark, limited methodology detail |
| [14] | OpenMemory GitHub (CaviraOSS/OpenMemory) | [T4/S3] I3 | New project, unvalidated claims |

---

## Part 7: Weighted Selection Matrix

Evaluating candidates against the selection criteria mandated in the research directive:

| Criterion | Weight | Graphiti (MCP) | GraphZep (TS) | Supermemory | OpenMemory | Convex ES |
|-----------|--------|---------------|---------------|-------------|------------|-----------|
| **TypeScript Integration** | Critical | Medium (MCP bridge) | High (native) | High (native) | Medium | High (native) |
| **Context Density** | Critical | High (graph + temporal) | High (graph + temporal) | Medium (flat) | Medium | Medium (custom) |
| **MCP Native** | High | ✅ Native server | ✅ Native server | ✅ Native | ✅ Native | ❌ Custom |
| **Code Transparency** | High | ✅ Apache-2.0 | ✅ Open source | ✅ MIT | ✅ Open source | ✅ In-house |
| **Reliability Tier 2** | High | High (300ms P95) | Unvalidated | Medium | Unvalidated | High (Convex guarantees) |
| **Bi-Temporal** | High | ✅ Full 4-timestamp | ✅ Ported | ❌ None | ⚠️ Basic | ⚠️ Custom |
| **Production Validation** | Medium | ✅ arXiv + benchmarks | ❌ None | ⚠️ Migration flux | ❌ None | ⚠️ Pattern only |
| **Compass Fit Score** | — | **8.5/10** | **7/10** | **5/10** | **5.5/10** | **7.5/10** |

---

## Part 8: Strategic Recommendation

### 8.1 Recommended Architecture: Layered Enrichment

**Phase 2A (Immediate)**: Implement Convex-native event sourcing for the decision timeline. This satisfies the core bi-temporal requirement (audit trail, point-in-time reconstruction) without external dependencies. Build the Context Pack assembly pipeline as a deterministic WSCI pipeline within Mastra workflows.

**Phase 2B (Near-term)**: Deploy Graphiti via its Docker-based MCP server (FalkorDB backend) as an enrichment sidecar. Convex remains the source of truth; Graphiti provides supplementary graph-based retrieval for entity relationship queries. Access is exclusively via MCP, maintaining clean separation.

**Phase 3 (Conditional)**: Evaluate GraphZep for direct TypeScript integration if the MCP bridge introduces unacceptable latency. Monitor Supermemory and OpenMemory for cross-tool memory portability features.

### 8.2 ADR-03-01 Revision Triggers

This research recommends triggering an ADR-03-01 revision when:

1. ✅ Phase 2 planning begins — **NOW** (bi-temporal requirements confirmed as necessary)
2. ✅ MCP becomes primary integration pattern — **CONFIRMED** (ADR-04-01, Graphiti MCP server exists)
3. The Context Pack assembly pipeline is designed and requires external enrichment data
4. Cross-project queries emerge as a significant retrieval pattern

### 8.3 Budget Impact

| Component | Phase 2A | Phase 2B | Phase 3 |
|-----------|----------|----------|---------|
| Convex event sourcing | $0 (included) | $0 (included) | $0 (included) |
| Convex @convex-dev/rag | $10-30/month | $10-30/month | $25-75/month |
| Graphiti MCP (Docker) | $0 | $20-50/month (VPS) | $20-50/month |
| FalkorDB | $0 | $0 (Docker) | $0-30/month (cloud) |
| LLM calls for Graphiti | $0 | $15-40/month | $30-60/month |
| **Total Memory Cost** | **$10-30/month** | **$45-120/month** | **$75-215/month** |

All projections remain within the budget parameters defined in SYS-00 (Phase 1: <$200/month; Phase 3: <$800/month).

### 8.4 Implementation Priority

| Priority | Action | Dependency | Effort |
|----------|--------|------------|--------|
| P0 | Design Convex event sourcing schema for decisions | ADR-03-01 revision | 2-3 days |
| P0 | Define Context Pack assembly pipeline (WSCI) | DD-11-01 schema | 1-2 days |
| P1 | Implement Convex event log table and replay logic | P0 schema | 3-5 days |
| P1 | Build Context Pack assembler in Mastra workflow | P0 pipeline | 3-5 days |
| P2 | Deploy Graphiti MCP server (Docker + FalkorDB) | Infrastructure | 1-2 days |
| P2 | Build MCP client integration in Mastra | ADR-04-01 patterns | 2-3 days |
| P3 | Evaluate GraphZep for direct TS integration | P2 results | 2-3 days |
| P3 | Branch isolation namespace extension | DD-18-01 implementation | 2-3 days |

---

## Sources

1. **[T1/S1]** Rasmussen, P. et al. "Zep: A Temporal Knowledge Graph Architecture for Agent Memory."
   Published January 2025. Retrieved 2026-02-06. https://arxiv.org/abs/2501.13956

2. **[T1/S1]** Zep AI. "Graphiti: Build Real-Time Knowledge Graphs for AI Agents." GitHub Repository.
   Updated January 2026. Retrieved 2026-02-06. https://github.com/getzep/graphiti

3. **[T4/S3]** aexy-io. "GraphZep: A temporal knowledge graph memory system for AI agents in TypeScript."
   GitHub Repository. Retrieved 2026-02-06. https://github.com/aexy-io/graphzep

4. **[T1/S2]** Supermemory AI. "Supermemory MCP." GitHub Organization.
   Updated January 2026. Retrieved 2026-02-06. https://github.com/supermemoryai

5. **[T2/S1]** Neo4j. "Graphiti: Knowledge Graph Memory for an Agentic World."
   Published August 2025. Retrieved 2026-02-06. https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/

6. **[T2/S2]** FalkorDB. "Graphiti integrates FalkorDB for sub-millisecond multi-agent knowledge graphs."
   Published July 2025. Retrieved 2026-02-06. https://www.falkordb.com/blog/graphiti-falkordb-multi-agent-performance/

7. **[T2/S1]** LangChain (Lance Martin). "Context Engineering for Agents."
   Published June 2025. Retrieved 2026-02-06. https://blog.langchain.com/context-engineering-for-agents/

8. **[T1/S1]** Anthropic. "Effective context engineering for AI agents."
   Published 2025. Retrieved 2026-02-06. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

9. **[T1/S1]** Google Developers Blog. "Architecting efficient context-aware multi-agent framework for production."
   Published December 2025. Retrieved 2026-02-06. https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/

10. **[T1/S1]** Zhang, Q. et al. "ACE: Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models."
    Published October 2025, revised January 2026. Retrieved 2026-02-06. https://arxiv.org/abs/2510.04618

11. **[T2/S1]** LlamaIndex. "Context Engineering Guide: Techniques for AI Agents."
    Published 2025. Retrieved 2026-02-06. https://www.llamaindex.ai/blog/context-engineering-what-it-is-and-techniques-to-consider

12. **[T1/S1]** Mastra. "Agent Memory | Agents | Mastra Docs."
    Retrieved 2026-02-06. https://mastra.ai/docs/agents/agent-memory

13. **[T3/S2]** AI Multiple Research. "AI Apps with MCP Memory Benchmark & Tutorial in 2026."
    Published 2026. Retrieved 2026-02-06. https://research.aimultiple.com/memory-mcp/

14. **[T4/S3]** CaviraOSS. "OpenMemory: Local persistent memory store for LLM applications."
    GitHub Repository. Retrieved 2026-02-06. https://github.com/CaviraOSS/OpenMemory

15. **[T1/S1]** Zep AI. "Graphiti MCP Server." PyPI.
    Updated January 2026. Retrieved 2026-02-06. https://pypi.org/project/graphiti-core/

16. **[T2/S2]** Zep Blog. "Graphiti: FalkorDB support and 14K GitHub Stars."
    Published July 2025. Retrieved 2026-02-06. https://blog.getzep.com/graphiti-knowledge-graphs-falkordb-support/

---

*End of Advanced Memory and Context Engineering Research Findings (RF-03-02)*
