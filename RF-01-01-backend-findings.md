---
id: RF-01-01
type: rf
area: 01-backend
title: Backend Platform Research Findings
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Evaluates Convex, Supabase, and Neon as backend platforms for Compass with emphasis on LLM interactions, documentation handling, and expandability to serve as the foundational backend for EFN's full application infrastructure
tags: [backend, database, convex, supabase, neon, llm, mcp, vibe-coding, baas]
related:
  - DD-14-01
  - DD-12-01
  - DD-13-01
  - ADR-01-01
confidence: high
methodology: "Web research with official vendor documentation, community sentiment analysis from HN/Reddit/GitHub, real-world founder experiences, pricing verification, and LLM tooling capability assessment"
limitations:
  - "Pricing subject to change; verified January 25, 2026"
  - "No hands-on implementation testing performed"
  - "Convex structured outputs and Neon Auth are in beta"
  - "User sentiment reflects current community; may shift as platforms evolve"
responds_to: null
implications_for: [ADR-01-01]
---

# Backend Platform Research Findings

## Executive Summary

**Primary Recommendation**: **Convex** for Compass and the broader EFN application infrastructure.

**Confidence**: High — Convex provides the most cohesive experience for LLM-orchestrated development with built-in agent infrastructure, automatic real-time sync, and TypeScript-native data modeling that eliminates the SQL context-switching problem for AI coding assistants.

**Key insight**: For an LLM-orchestrated planning and documentation system built by a small non-traditional team, the question isn't "which database is most powerful?" but "which platform minimizes the gap between what an LLM generates and what runs correctly in production?" Convex's document-relational model with end-to-end TypeScript type safety makes it nearly impossible for AI-generated code to corrupt data—a critical safety property when LLM agents are primary developers.

**Trade-offs accepted**:

- Proprietary query model (no SQL portability) in exchange for transactional safety and AI-friendliness
- Smaller ecosystem than PostgreSQL in exchange for more integrated developer experience
- Learning CQRS patterns (queries/mutations separation) in exchange for automatic reactivity

**Alternatives assessment**:

- **Supabase**: Best choice if PostgreSQL compatibility, mature ecosystem, and RLS-based security model are priorities. MCP server is development-only—production LLM database access requires custom implementation. Recommended if the team has PostgreSQL experience or needs specific extensions.
- **Neon**: Best choice if database branching for safe AI experimentation and PostgreSQL compatibility are essential. Database-only service requires external compute, auth, and storage. Recommended as a complementary service for isolated AI sandbox workflows.

**Budget assessment**: All options well within targets. Convex ~$25/month at Phase 3 scale, Supabase ~$25/month base, Neon ~$5-25/month depending on usage. All far below the $800/month ceiling.

---

## Part 1: Research Context and Requirements

### 1.1 Compass-Specific Requirements

Based on the Compass System Definition, the backend platform must support:

**Core architecture layers** (System Definition §5.1):

| Layer | Backend Requirements |
|-------|---------------------|
| Layer 2: Authoritative State | Projects, decisions, branches, workflow runs, permissions, versioning |
| Layer 3: Artifact Store | Canonical docs and handoff bundles with history (git-friendly) |
| Layer 4: Memory & Retrieval | Semantic and literal search, temporal awareness |
| Layer 5: Pristine Context | Verified sources, citations, timestamps |
| Layer 6: Integration & Events | Webhooks, queues, schedulers |

**Guiding principles with backend implications**:

- **Artifacts are truth; chat is a mutation vector** → Need structured document storage with versioning
- **State is externalized** → Must reconstruct context from stored state, not conversation history
- **Auditability and reversibility** → Every change attributable, branch/compare/merge/rollback capabilities
- **LLM-agnostic by design** → No hard coupling to specific LLM provider
- **Memory that actually remembers** → Cross-session, temporally-aware project memory

**Operational constraints** (System Definition §4):

- Budget: $600–$2,000/year initial; $3,000–$5,000 proven value
- Team: Non-traditional developers using LLM coding agents
- Security: Robust auth, audit logs, encryption (but not enterprise SSO initially)
- Vendor independence: Data export capability, standard formats preferred

### 1.2 EFN Ecosystem Expansion Considerations

Compass is the foundational layer, but the backend will eventually serve EFN's broader tool ecosystem (DD-14-01):

- Broadcast-critical tools (highest reliability)
- Production pipelines (video analytics, captions)
- Publishing pipelines (article companions, website CMS)
- Analytics and intelligence (viewer data, competitive research)
- Internal utilities (file conversion, automation)

The backend must be **expandable and modular** enough to serve this diverse portfolio while maintaining consistency.

### 1.3 Evaluation Criteria Prioritization

Based on Compass requirements and stakeholder input:

| Criterion | Priority | Rationale |
|-----------|----------|-----------|
| **LLM maintainability** | Critical | Non-traditional team relies on AI coding assistants |
| **LLM agent integration** | Critical | Core system is LLM-orchestrated; agents need safe database access |
| **Chat/thread persistence** | Critical | Planning workflows span days/weeks (§2.1) |
| **Documentation handling** | Critical | Artifacts are the source of truth |
| **Real-time collaboration** | High | Multiple users viewing same project (§3.4) |
| **Expandability/modularity** | High | Must grow to serve full EFN ecosystem |
| **Vendor independence** | High | Explicit requirement (§4.5) |
| **Cost efficiency** | Medium | Budget generous but prefer efficient use |
| **Search capabilities** | Medium | Separate memory layer planned; backend search supplementary |
| **Enterprise auth** | Low | Not required initially; sensitive data kept separate |

---

## Part 2: Platform Evaluations

### 2.1 Convex

**What it is**: Convex is a backend-as-a-service providing a document-relational database, serverless functions, file storage, and real-time sync—all in a unified TypeScript environment. Unlike traditional databases, queries and mutations are pure TypeScript functions that run on Convex's managed infrastructure.

**Architecture philosophy**: Convex uses a document-relational model combining JSON-like nested objects with relational tables. All queries are reactive by default—when underlying data changes, subscribed clients update automatically without cache invalidation or manual WebSocket management. Transactions use serializable isolation (the strictest ACID level) with optimistic concurrency control.

#### Pricing (January 2026)

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Free | $0 | 0.5GB storage, 1M function calls/mo | Development and small projects |
| Starter | Pay-as-you-go | Usage-based | No base fee |
| Professional | $25/dev/month | 25M function calls, 50GB storage | Per-seat model |

**Cost estimate for Compass**:

- Phase 1 (2-3 users): Free tier likely sufficient; if exceeded, ~$25-50/month
- Phase 3 (10-20 users): ~$25-75/month depending on function call volume

#### LLM Maintainability: Exceptional

Convex has made AI-first development a core strategy, achieving what they describe as making it "nearly impossible for AI to write code that could corrupt your data."

| Criterion | Assessment | Evidence |
|-----------|------------|----------|
| MCP Server | ✅ Official | CLI-integrated: `npx convex@latest mcp start` |
| llms.txt | ✅ Full + lite | Comprehensive documentation for AI consumption |
| Cursor Rules | ✅ Pre-built | Continuously updated via automated evaluations |
| TypeScript Types | ✅ End-to-end | Schema → queries → frontend with zero config |
| LLM Error Prevention | ✅ Excellent | Automatic reactivity removes cache bugs; transactions prevent partial writes |

**Why this matters for Compass**: The TypeScript-native approach means LLMs don't need to context-switch between TypeScript and SQL. When Claude or Cursor generates database code, it's pure TypeScript that gets full type checking. The transactional guarantees mean AI-generated mutations either complete fully or roll back entirely—no partial writes or corrupted state.

Convex maintains a public **LLM Leaderboard** testing which models write the best Convex code, demonstrating their commitment to AI-assisted development. Their **Chef AI builder** produces working full-stack apps from natural language descriptions.

**MCP Server capabilities**:

- List tables and their schemas
- Paginate and query data
- Fetch function specifications
- Manage environment variables
- `runOneoffQuery`: Execute sandboxed, read-only JavaScript queries

The MCP includes an "agent mode" that limits permissions for remote coding agents like Cursor or Codex, providing development-time safety.

#### LLM Agent Integration for Production

Convex provides the **@convex-dev/agent** component—the most structured approach to production LLM database interaction among evaluated platforms.

**How it works**: LLMs interact with your database exclusively through developer-defined tools with explicit argument validation. The LLM cannot execute arbitrary database operations—only the specific, validated tools you provide.

```typescript
const documentAgent = new Agent(components.agent, {
  name: "Documentation Agent",
  chat: openai.chat("gpt-4o-mini"),
  tools: {
    searchDocs: tool({
      description: "Search documentation",
      args: { query: v.string() },
      handler: async (ctx, args) => ctx.runQuery(api.docs.search, args)
    }),
    createArtifact: tool({
      description: "Create a new artifact",
      args: { 
        type: v.union(v.literal("spec"), v.literal("adr"), v.literal("rf")),
        title: v.string(),
        content: v.string()
      },
      handler: async (ctx, args) => ctx.runMutation(api.artifacts.create, args)
    })
  }
});
```

**Built-in features for Compass use cases**:

- Persistent thread/message storage (chat history across sessions)
- Streaming via WebSocket deltas
- Human-in-the-loop support (merge gates for proposals)
- Usage tracking per-provider/per-model/per-user
- RAG integration via @convex-dev/rag

This directly supports Compass's requirement for "multi-agent safety and human merge gates" where "sub-agents produce proposals, not canonical truth."

#### Chat and Thread Persistence

Convex's agent component provides native chat persistence:

- **Threads**: Persistent conversation containers that survive across sessions
- **Messages**: Stored with full context, tool calls, and responses
- **Streaming**: Real-time updates via WebSocket without manual implementation
- **History retrieval**: Query past conversations with full context

For Compass's planning workflows that "may span multiple sessions over time" (System Definition §3.2), this is directly relevant.

#### Real-time Collaboration

Convex's automatic reactivity makes real-time collaboration trivial:

- Queries are subscriptions by default
- When any user modifies data, all connected clients see updates immediately
- No manual WebSocket management, no cache invalidation logic
- Sub-50ms latency at 5,000 concurrent connections (documented benchmarks)

**For Compass**: Multiple users viewing the same project (§3.4) works automatically. Real-time synchronization for simultaneous edits is native behavior, not an add-on feature.

#### Documentation and Artifact Storage

Convex's document-relational model maps well to Compass's artifact structure:

```typescript
// Schema definition example
defineSchema({
  artifacts: defineTable({
    id: v.string(), // SPEC-auth-001
    type: v.union(v.literal("spec"), v.literal("adr"), v.literal("rf"), ...),
    status: v.union(v.literal("draft"), v.literal("review"), v.literal("active"), ...),
    title: v.string(),
    content: v.string(),
    frontmatter: v.object({...}),
    created: v.number(),
    updated: v.number(),
    author: v.string(),
    version: v.number()
  })
    .index("by_type", ["type"])
    .index("by_status", ["status"])
    .index("by_updated", ["updated"]),
  
  decisions: defineTable({
    artifactId: v.id("artifacts"),
    status: v.union(v.literal("proposed"), v.literal("accepted"), v.literal("rejected")),
    options: v.array(v.object({...})),
    rationale: v.optional(v.string())
  })
})
```

Versioning can be implemented via separate version tables or change tracking patterns. The transactional model ensures artifact updates are atomic—a spec update either fully completes (including all related records) or fully rolls back.

#### Search and Retrieval

**Vector search**: Built-in with `ctx.vectorSearch()`, supporting configurable dimensions and index types. No external service required.

**Hybrid search**: The @convex-dev/rag component provides:

- Automatic embedding generation
- Namespaced search
- Chunk context retrieval
- Importance weighting
- `hybridRank()` combining text and vector results with configurable weights

**Full-text search**: Available but less mature than PostgreSQL FTS.

**For Compass**: Since a separate memory layer is planned, backend search is supplementary. Convex's built-in capabilities provide a solid foundation without requiring external services like Pinecone or Elasticsearch.

#### Expandability and Modularity

Convex supports multi-app architectures and shared data patterns:

- **Convex Components**: Reusable, installable modules (rate limiting, agents, RAG)
- **HTTP endpoints**: Expose functions as REST APIs for non-Convex clients
- **Cron jobs**: Scheduled function execution (documentation reconciliation loops)
- **File storage**: Built-in with CDN, or integrate R2 via component

**For EFN ecosystem**: Different tools can share the same Convex deployment with table-level access control, or use separate deployments with shared patterns. The TypeScript-native model means consistent developer experience across the tool portfolio.

#### Vendor Independence Concerns

**This is Convex's primary weakness**. The document-relational model and TypeScript query DSL are proprietary:

- No SQL export or pg_dump equivalent
- Migration requires rewriting queries
- Data can be exported as JSON, but schema translation needed
- No self-hosting option (cloud-only)

Convex has published "How Hard Is It to Migrate Away from Convex?" acknowledging the concern. Their position: "code modifications required to move away from Convex could be manageable" but not trivial.

**Mitigation strategies**:

1. Abstract database operations behind interfaces that could be reimplemented
2. Use JSON/Markdown for artifact storage (portable formats)
3. Maintain periodic JSON exports of critical data
4. Accept the trade-off given other advantages

#### Founder and Community Sentiment

**Positive signals**:

- "What made Convex different was how little backend glue I needed to write. Realtime sync just worked. TypeScript felt native. It felt like hiring a backend team on day one." — Matt Luo, LanguageHopper.com
- Multiple startups report growing from small deployments to 70+ tables serving web, mobile, and REST APIs
- Strong enthusiasm for AI-assisted development workflows

**Concerns raised**:

- Learning CQRS patterns (mutation/query separation) differs from traditional backends
- No aggregate queries (COUNT, SUM) without workarounds
- Smaller ecosystem than PostgreSQL (fewer examples, tutorials)

---

### 2.2 Supabase

**What it is**: Supabase wraps PostgreSQL with auto-generated REST/GraphQL APIs, authentication, file storage, edge functions, and real-time subscriptions. It's the closest equivalent to Firebase in the open-source world, with the advantage of standard PostgreSQL underneath.

**Architecture philosophy**: "Postgres as a platform." Supabase adds layers on top of standard PostgreSQL while keeping the database accessible via standard tools. Everything ultimately maps to PostgreSQL tables, triggers, and functions.

#### Pricing (January 2026)

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Free | $0 | 500MB DB, 50K MAUs, 2 projects | Auto-pauses after 7 days inactivity |
| Pro | $25/month | 8GB DB, 100K MAUs, includes $10 compute | Per-project |
| Team | $599/month | SOC2, HIPAA, priority support | Enterprise compliance |

**Cost estimate for Compass**:

- Phase 1: ~$25/month (Pro plan for stability)
- Phase 3: ~$25-75/month (compute scaling if needed)

**Hidden costs to watch**:

- Each staging environment counts as separate project
- Email sending limits (3/hour on free) can block auth flows unexpectedly
- Compute costs not obvious on pricing page

#### LLM Maintainability: Strong

| Criterion | Assessment | Evidence |
|-----------|------------|----------|
| MCP Server | ✅ Official | 20+ tools for schema design, migrations, SQL |
| llms.txt | ✅ Present | Available at supabase.com/llms.txt |
| Cursor Rules | ✅ Available | Pre-built integration guides |
| TypeScript Types | ⚠️ Generated | Via CLI command, requires manual refresh |
| LLM Error Prevention | ⚠️ Moderate | SQL requires more careful AI generation |

Supabase has invested heavily in AI developer experience with a "Supabase for Vibe Coders" landing page and explicit marketing to AI-assisted development workflows.

**MCP Server capabilities**:

- Project creation and management
- Table design and migration generation
- SQL execution
- TypeScript type generation
- Storage and auth configuration

**Critical limitation**: Official documentation explicitly warns:

> "Don't connect to production" and "Don't give to your customers."

The MCP server operates under developer permissions—it's strictly for development, testing, and schema design. Production LLM database access requires custom implementation.

#### LLM Agent Integration for Production

Unlike Convex, Supabase has no official "agent component." Production LLM database access requires building your own architecture:

```typescript
// Typical pattern for Supabase + LLM
export async function documentAgent(userQuery: string) {
  // 1. Your app calls Edge Function
  // 2. Edge Function invokes LLM
  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-5-20250514",
    messages: [{ role: "user", content: userQuery }],
    tools: [/* your defined tools */]
  });
  
  // 3. Validate and execute against database
  if (response.tool_calls) {
    for (const call of response.tool_calls) {
      // Validate call against allowed operations
      // Execute with scoped permissions (read-only role, RLS)
      const result = await supabase
        .from(call.table)
        .select(call.columns)
        .match(call.filters);
    }
  }
}
```

**Security model**: Row-level security (RLS) policies scope what data any request can access. Create dedicated database roles with minimal permissions for LLM access. Never expose service keys (which bypass RLS) to LLM operations.

**For Compass**: This requires more custom development than Convex but offers fine-grained control. The PostgreSQL security model is well-understood and battle-tested.

#### Chat and Thread Persistence

No built-in solution—implement with standard tables:

```sql
CREATE TABLE threads (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid REFERENCES projects(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id uuid REFERENCES threads(id),
  role text NOT NULL, -- 'user', 'assistant', 'system'
  content text NOT NULL,
  tool_calls jsonb,
  created_at timestamptz DEFAULT now()
);
```

This is straightforward but requires manual implementation of streaming, tool call tracking, and context management that Convex provides out of the box.

#### Real-time Collaboration

Supabase Realtime provides three mechanisms:

1. **Postgres Changes**: Listen to INSERT/UPDATE/DELETE via PostgreSQL logical replication
2. **Broadcast**: Low-latency ephemeral messages (cursor tracking, typing indicators)
3. **Presence**: CRDT-backed state for tracking online users

**Limitations**:

- "Postgres Changes doesn't scale as well as Broadcast" (official docs)
- Connection limits: 200 (Free), 500 (Pro)
- Messages capped: 2M/mo (Free), 5M/mo (Pro)

**For Compass**: Works for multiple users viewing the same project, but requires more configuration than Convex's automatic reactivity.

#### Documentation and Artifact Storage

PostgreSQL handles structured documents well:

```sql
CREATE TABLE artifacts (
  id text PRIMARY KEY, -- SPEC-auth-001
  type artifact_type NOT NULL,
  status lifecycle_status NOT NULL DEFAULT 'draft',
  title text NOT NULL,
  content text NOT NULL,
  frontmatter jsonb NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  author text NOT NULL,
  version integer DEFAULT 1
);

-- History tracking via trigger or separate table
CREATE TABLE artifact_versions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  artifact_id text REFERENCES artifacts(id),
  version integer NOT NULL,
  content text NOT NULL,
  changed_at timestamptz DEFAULT now(),
  changed_by text NOT NULL
);
```

PostgreSQL's JSONB support handles flexible frontmatter schemas well. Full-text search on content is excellent via tsvector.

#### Search and Retrieval

**Full-text search**: PostgreSQL's tsvector/tsquery is production-grade:

```sql
-- Add search index
ALTER TABLE artifacts ADD COLUMN search_vector tsvector 
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', title), 'A') ||
    setweight(to_tsvector('english', content), 'B')
  ) STORED;

CREATE INDEX artifacts_search_idx ON artifacts USING gin(search_vector);
```

**Vector search**: pgvector extension with HNSW and IVFFlat indexes:

```sql
CREATE EXTENSION vector;
ALTER TABLE artifacts ADD COLUMN embedding vector(1536);
CREATE INDEX ON artifacts USING hnsw (embedding vector_cosine_ops);
```

**Hybrid search**: Combine tsvector and pgvector results via Reciprocal Rank Fusion (documented pattern).

**For Compass**: PostgreSQL's search capabilities are mature and powerful. If search is eventually brought into the backend (rather than separate memory layer), Supabase is well-positioned.

#### Expandability and Modularity

Supabase's PostgreSQL foundation provides maximum flexibility:

- **Schemas**: Isolate different apps/domains within same database
- **Extensions**: 50+ available (PostGIS, pg_cron, pg_net, etc.)
- **Edge Functions**: Deno-based serverless for custom logic
- **Database branches**: Available via Supabase Branching (for preview environments)

**For EFN ecosystem**: Different tools can share database with schema-level isolation, or use separate projects with consistent patterns. PostgreSQL skills transfer across the portfolio.

#### Vendor Independence

**This is Supabase's primary strength**:

- Standard PostgreSQL with pg_dump export
- Entirely open-source (Apache 2.0)
- Self-hosting available via Docker Compose
- Supabase-specific elements (Auth tables, helper functions) are documented and portable

Migration to any PostgreSQL provider (Neon, RDS, self-hosted) requires minimal changes beyond recreating Supabase-specific functions.

#### Founder and Community Sentiment

**Positive signals**:

- Massive community (96K+ GitHub stars)
- "We trained a junior developer with zero backend experience—she was shipping authenticated CRUD features within 3 hours." — Agency case study
- Strong tutorial ecosystem and documentation

**Concerns raised**:

- "Even though it looks like a great product initially, it has a lot of errors and bugs when you are trying to actually build something more robust than a toy app. Local development is a massive pain." — HN user
- "On an architectural level, it is terrifying to have your database exposed to the public internet just hidden behind RLS policies." — HN user (note: this is a deliberate architectural choice, not a bug)
- RLS complexity can be error-prone for complex authorization requirements

---

### 2.3 Neon

**What it is**: Neon is a serverless PostgreSQL database with copy-on-write branching, scale-to-zero capability, and compute-storage separation. Unlike Supabase and Convex, it's purely a database service—no auth, storage, or functions included.

**Architecture philosophy**: "Serverless Postgres with branching." Neon separates compute from storage, enabling instant database branching, independent scaling, and zero-cost periods when idle. This architectural foundation enables unique workflows, particularly for AI-assisted development.

#### Pricing (January 2026, post-Databricks acquisition)

| Component | Rate | Notes |
|-----------|------|-------|
| Compute | $0.106–$0.222/CU-hour | 15–25% reduction from pre-acquisition |
| Storage | $0.35/GB-month | 80% reduction from $1.75 |
| Free tier | 100 CU-hours, 0.5GB | Doubled Oct 2025 |
| Launch plan | $19/month base | Small teams |
| Scale plan | $700/month | SOC2, HIPAA, 99.95% SLA |

**Cost estimate for Compass** (database only):

- Phase 1: ~$5-25/month
- Phase 3: ~$25-50/month

**Critical note**: These estimates are for database only. Add ~$20-40/month for external auth service (Clerk/Auth0) and compute platform (Vercel/Cloudflare Workers). Total comparable to Supabase/Convex.

#### LLM Maintainability: Highest Score

Neon has the most comprehensive LLM development tooling of any evaluated platform:

| Criterion | Assessment | Evidence |
|-----------|------------|----------|
| MCP Server | ✅ Official | Comprehensive tool set with 20+ operations |
| llms.txt | ✅ Comprehensive | With AI Starter Kit and rules files |
| GitHub Copilot | ✅ Direct integration | Agents with Neon integration |
| Claude Code | ✅ Plugin available | Database operations via natural language |
| TypeScript Types | ✅ Auto-generated | Via Neon CLI |
| Standard Patterns | ✅ Pure PostgreSQL | No proprietary query language |

Neon reports that **over 80% of their databases are now created by AI agents**—a remarkable indicator of the platform's fit for agentic workflows.

**MCP Server capabilities** (@neondatabase/mcp-server-neon):

- Project and branch management
- SQL execution with transactions
- Schema comparison between branches
- Migration workflow tools
- Query optimization analysis
- Read-only mode available

#### LLM Agent Integration: Unique Branching Approach

Neon's differentiator for LLM production use is **database branching for sandboxing**:

```typescript
// 1. Create isolated sandbox (~1 second, regardless of database size)
const sandbox = await neon.createBranch({
  projectId: 'docs-system',
  branchName: 'llm-experiment-' + Date.now(),
  parentBranchId: 'main'
});

// 2. LLM operates with full freedom on sandbox
await neon.runSql(sandbox.id, 'ALTER TABLE docs ADD COLUMN ai_summary TEXT');
await neon.runSql(sandbox.id, 'UPDATE docs SET ai_summary = ...');

// 3. Review changes before committing
const diff = await neon.compareSchema(sandbox.id, 'main');

// 4. Either commit to production OR discard completely
if (approved) {
  await neon.runSql('main', migrationSQL);
}
await neon.deleteBranch(sandbox.id);
```

**Why this matters for Compass**: The "multi-agent safety and human merge gates" principle (System Definition §1.7) can be implemented at the database level. Agents propose changes on branches; humans review diffs; approved changes merge to main.

**Cost is minimal** because branches use copy-on-write—you only pay for changed data. Branches scale to zero when idle.

**Limitations**:

- Still requires external compute layer to run the LLM orchestration logic
- No built-in agent component (build your own)
- MCP documentation recommends "Never connect MCP agents to production databases"—use branching instead

#### Chat and Thread Persistence

No built-in solution—implement with standard PostgreSQL tables (same pattern as Supabase). Since Neon is database-only, you'll implement this in your compute layer (Vercel, Cloudflare Workers, etc.).

#### Real-time Collaboration

PostgreSQL LISTEN/NOTIFY only—no built-in WebSocket layer. Requires:

- External service (Ably, Pusher) for WebSocket connections
- Application-level pub/sub implementation
- Or use Supabase Realtime separately

**For Compass**: Real-time collaboration requires additional services. This is the main gap versus Convex and Supabase.

#### Documentation and Artifact Storage

Standard PostgreSQL—same patterns as Supabase. Neon supports PostgreSQL 14-18 with 80+ extensions including pgvector, pg_search (ParadeDB), and PostGIS.

#### Search and Retrieval

**Full-text search**: Standard PostgreSQL FTS plus pg_search extension (ParadeDB) for BM25 ranking.

**Vector search**: pgvector with HNSW indexing, same as Supabase.

**Hybrid search**: Combine FTS and vector results in single queries.

**Unique capability**: Per-branch search indexes. Each branch can have different search configurations, useful for A/B testing retrieval strategies.

#### Expandability and Modularity

Neon is purely a database—expandability depends on your compute layer:

- **Vercel**: Seamless integration, serverless functions
- **Cloudflare Workers**: Edge compute, low latency
- **Any PostgreSQL client**: Standard drivers work

**For EFN ecosystem**: Neon pairs well with existing infrastructure. If EFN already uses Vercel or Cloudflare, Neon integrates cleanly. The branching model supports isolated environments per tool.

#### Vendor Independence

**Very strong**:

- Standard PostgreSQL with pg_dump export
- Open-source backend released late 2024
- Migration to any PostgreSQL provider is straightforward
- No proprietary query language

#### Founder and Community Sentiment

**Positive signals**:

- "A perfect match for agentic workflows" — Multiple developer testimonials
- Strong integration with Drizzle ORM (10% discount for Drizzle users)
- Databricks acquisition provides enterprise backing
- "80% of databases created by AI agents" indicates strong AI-first positioning

**Concerns raised**:

- Cold starts of 500ms-1s (mitigated by connection pooling and always-on options)
- Storage pricing compounds with PITR retention
- No database logs on free tier
- Database-only requires assembling multiple services

---

## Part 3: Comparative Analysis

### 3.1 Compass Requirements Fit

| Requirement | Convex | Supabase | Neon |
|-------------|--------|----------|------|
| **LLM maintainability** | ✅ Excellent (TypeScript-native) | ✅ Good (SQL + tooling) | ✅ Excellent (best MCP) |
| **LLM agent integration** | ✅ Built-in (@convex-dev/agent) | ⚠️ Build your own | ⚠️ Build your own (+ branching) |
| **Chat persistence** | ✅ Native threads/messages | ⚠️ Implement with tables | ⚠️ Implement with tables |
| **Real-time collaboration** | ✅ Automatic reactivity | ✅ Realtime subscriptions | ❌ Requires external service |
| **Artifact storage** | ✅ Document-relational | ✅ PostgreSQL + JSONB | ✅ PostgreSQL + JSONB |
| **Versioning/audit** | ✅ Transactional | ✅ Triggers/history tables | ✅ Triggers/history tables + branching |
| **Search capabilities** | ✅ Built-in vector + hybrid | ✅ pgvector + FTS | ✅ pgvector + FTS + pg_search |
| **Expandability** | ✅ Components, HTTP APIs | ✅ Extensions, Edge Functions | ⚠️ Database-only (pair with compute) |
| **Vendor independence** | ❌ Proprietary model | ✅ Standard PostgreSQL | ✅ Standard PostgreSQL |

### 3.2 Full-Service Comparison

| Capability | Convex | Supabase | Neon |
|------------|--------|----------|------|
| Database | ✅ Document-relational | ✅ PostgreSQL | ✅ PostgreSQL |
| Real-time | ✅ Automatic | ✅ Subscription-based | ❌ LISTEN/NOTIFY only |
| Authentication | ⚠️ Beta + integrations | ✅ Built-in (18+ OAuth) | ⚠️ Beta + integrations |
| File Storage | ✅ Built-in + R2 component | ✅ S3-compatible, CDN | ❌ External only |
| Serverless Functions | ✅ Queries/Mutations/Actions | ✅ Deno Edge Functions | ❌ External only |
| Vector Search | ✅ Built-in | ✅ pgvector | ✅ pgvector |
| Hosting | ❌ External | ❌ External | ❌ External |

### 3.3 AI-Native Features Comparison

| Feature | Convex | Supabase | Neon |
|---------|--------|----------|------|
| MCP Server | ✅ Official + agent mode | ✅ Official (dev only) | ✅ Official |
| llms.txt | ✅ Full + lite versions | ✅ Present | ✅ Comprehensive |
| Agent Component | ✅ @convex-dev/agent | ❌ Build your own | ❌ Build your own |
| RAG Component | ✅ @convex-dev/rag | ❌ Build with pgvector | ❌ Build with pgvector |
| LLM Sandboxing | ⚠️ Via tool constraints | ⚠️ Via RLS policies | ✅ Database branching |
| Production LLM Access | ✅ Tool-based guardrails | ⚠️ Custom + RLS | ⚠️ Custom + branching |

### 3.4 Cost Comparison at Compass Scale

| Platform | Phase 1 | Phase 3 | Notes |
|----------|---------|---------|-------|
| Convex | $0-50/mo | $25-75/mo | All-in-one |
| Supabase | ~$25/mo | ~$25-75/mo | All-in-one |
| Neon | ~$25-65/mo | ~$45-90/mo | Add auth ($20) + compute ($20) |

All options well within budget constraints ($800/month Phase 3 ceiling).

### 3.5 Vendor Lock-in Spectrum

```
Highest Lock-in                                           Lowest Lock-in
       |                                                          |
       v                                                          v
    Convex ─────────────────────────────────────── Supabase ─── Neon
    (Proprietary                                    (PostgreSQL   (Pure
     query model,                                    with extras,  PostgreSQL,
     no self-host)                                   open-source)  open-source)
```

---

## Part 4: Recommendation

### 4.1 Primary Recommendation: Convex

**For Compass and initial EFN tool development, Convex is recommended** based on:

1. **Lowest implementation complexity for LLM-orchestrated systems**: The @convex-dev/agent component provides exactly what Compass needs—persistent threads, tool-based database access, streaming, human-in-the-loop support. Building equivalent functionality on Supabase or Neon requires significant custom development.

2. **Transactional safety for AI-generated code**: Serializable transactions with automatic rollback mean AI-generated mutations either complete fully or fail safely. No partial writes, no corrupted state.

3. **Automatic real-time for collaborative features**: Multiple users viewing the same project "just works" without WebSocket configuration or cache invalidation.

4. **TypeScript-native eliminates SQL context-switching**: LLMs generate better code when they don't need to switch between TypeScript and SQL. The entire Compass codebase can be pure TypeScript.

5. **Built-in RAG and vector search**: Memory layer integration doesn't require external services.

6. **Simpler operational model**: Single service for database, functions, storage, real-time. Fewer moving parts to configure and debug.

**Confidence level**: High (85%)

**Accepted trade-offs**:

- Proprietary model creates vendor dependency
- Smaller ecosystem than PostgreSQL
- Learning curve for CQRS patterns

### 4.2 Mitigation for Vendor Lock-in

Given Convex's proprietary nature and Compass's "vendor independence" requirement (System Definition §4.5):

1. **Abstract database operations** behind interfaces that could be reimplemented for PostgreSQL
2. **Store artifacts in portable formats** (JSON, Markdown) within the document-relational model
3. **Maintain periodic data exports** in JSON format
4. **Document migration strategy** as part of system architecture
5. **Accept calculated risk** given significant productivity advantages

### 4.3 Alternative Recommendations

**Choose Supabase if**:

- PostgreSQL compatibility is non-negotiable
- Team has existing PostgreSQL expertise
- RLS-based security model is preferred
- Maximum vendor independence is required
- Willing to build custom LLM agent infrastructure

**Choose Neon if**:

- Database branching for AI sandboxing is critical
- Existing compute infrastructure (Vercel, Cloudflare) is in place
- Pure database service with maximum flexibility is preferred
- AI-driven schema management is a primary use case

### 4.4 Hybrid Architecture Consideration

A viable alternative: **Convex as primary with Neon for AI sandboxing**

- Convex handles core Compass functionality (artifacts, threads, real-time)
- Neon branches serve as isolated sandboxes for experimental AI operations
- Best of both: Convex's developer experience + Neon's branching safety

This adds complexity but may be valuable if LLM sandboxing proves critical during development.

---

## Part 5: Open Questions for Stakeholders

1. **Vendor lock-in tolerance**: Is the productivity gain from Convex worth the proprietary dependency? The mitigation strategies reduce but don't eliminate lock-in risk.

2. **PostgreSQL ecosystem value**: Are there specific PostgreSQL extensions or tools EFN expects to need that would require PostgreSQL compatibility?

3. **Team learning curve**: Is the CQRS pattern (queries/mutations separation) acceptable, or would SQL familiarity be more valuable?

4. **Branching workflow value**: Would Neon's database branching for AI sandboxing justify the additional complexity of a hybrid architecture?

5. **Real-time requirements**: How critical is automatic real-time sync versus subscription-based updates? This affects the Convex vs Supabase trade-off.

---

## Part 6: Next Steps

**If proceeding with Convex**:

1. Create Convex project and configure development environment
2. Define initial schema for artifacts, threads, and workflow runs
3. Implement basic CRUD operations with @convex-dev/agent integration
4. Test real-time sync with multiple users
5. Evaluate vector search for memory layer integration
6. Establish data export procedures for vendor independence verification

**If proceeding with Supabase**:

1. Provision Pro plan instance ($25/month)
2. Configure Row Level Security policies for multi-user access
3. Set up TypeScript type generation in development workflow
4. Build custom LLM agent infrastructure with Edge Functions
5. Enable pgvector extension for semantic search
6. Implement real-time subscriptions for collaborative features

**If additional evaluation needed**:

1. Prototype the same feature (collaborative document editing with LLM-assisted updates) on Convex and Supabase
2. Measure development velocity with each platform's AI tooling
3. Evaluate agent component complexity (Convex built-in vs Supabase custom)

---

## Appendix A: Detailed Pricing Breakdown

### Convex Pricing Details

| Resource | Free | Professional |
|----------|------|--------------|
| Database storage | 0.5GB | 50GB included, then $0.25/GB |
| File storage | 0.5GB | 50GB included |
| Function calls | 1M/mo | 25M included, then $2/M |
| WebSocket connections | Included | Included |
| Bandwidth | 1GB | 50GB included |

### Supabase Pricing Details

| Resource | Free | Pro ($25/mo) |
|----------|------|--------------|
| Database size | 500MB | 8GB |
| Storage | 1GB | 100GB |
| Bandwidth | 2GB | 250GB |
| Edge Function invocations | 500K | 2M |
| Realtime messages | 2M | 5M |
| MAUs | 50K | 100K |

### Neon Pricing Details

| Resource | Free | Launch ($19/mo) |
|----------|------|-----------------|
| Compute | 100 CU-hours | 300 CU-hours |
| Storage | 0.5GB | 10GB |
| Branches | Unlimited | Unlimited |
| PITR | 6 hours | 7 days |
| Projects | 1 | 10 |

---

## Appendix B: Glossary

**CQRS (Command Query Responsibility Segregation)**: Pattern separating read operations (queries) from write operations (mutations). Convex enforces this at the API level.

**Copy-on-write**: Storage technique where branching doesn't duplicate data until changes are made. Used by Neon for instant branching.

**MCP (Model Context Protocol)**: Standard for LLM tools to interact with external services. All three platforms offer MCP servers.

**pgvector**: PostgreSQL extension for vector similarity search, used by both Supabase and Neon.

**RLS (Row Level Security)**: PostgreSQL feature for fine-grained access control at the row level. Central to Supabase's security model.

**Serializable isolation**: Strictest ACID transaction isolation level, ensuring transactions behave as if executed sequentially. Convex uses this by default.

---

## Appendix C: Sources

1. **[T1/S1]** Convex. "Documentation and AI Integration." Retrieved 2026-01-25. https://docs.convex.dev
   Note: Official documentation covering agent component, TypeScript patterns, and AI tooling.

2. **[T1/S1]** Supabase. "Documentation and MCP Server." Retrieved 2026-01-25. https://supabase.com/docs
   Note: Official documentation including MCP server limitations and RLS patterns.

3. **[T1/S1]** Neon. "Documentation and Branching Guide." Retrieved 2026-01-25. https://neon.tech/docs
   Note: Official documentation covering branching workflows and AI integration.

4. **[T2/S2]** Hacker News. Various discussion threads on backend platforms. Retrieved 2026-01-25.
   Note: Community sentiment and founder experiences compiled from multiple threads.

5. **[T2/S2]** GitHub. Platform repositories and issue discussions. Retrieved 2026-01-25.
   Note: Technical details and community feedback from official repositories.

6. **[T3/S2]** Stack by Convex. Founder testimonials and case studies. Retrieved 2026-01-25.
   Note: Real-world implementation experiences from Convex users.

---

## Appendix D: Related Documents

- **Compass System Definition**: Authoritative system specification (requirements source)
- **DD-14-01**: EFN Tooling Ecosystem Requirements (expansion context)
- **DD-12-01**: Repository Structure (artifact storage patterns)
- **DD-13-01**: Artifact Taxonomy (document structure requirements)
- **ADR-01-01**: Backend Selection (pending decision document)

---

*End of Backend Platform Research Findings (RF-01-01)*
