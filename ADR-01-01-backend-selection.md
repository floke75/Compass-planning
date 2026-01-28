---
id: ADR-01-01
type: adr
area: 01-backend
title: Backend Platform Selection
status: accepted
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Selects Convex as the backend platform for Compass and the broader EFN tool ecosystem based on TypeScript-native development, built-in LLM agent infrastructure, automatic real-time collaboration, and transactional safety for AI-generated code
tags: [backend, database, convex, llm, typescript, real-time, decision]
related:
  - RF-01-01
  - DD-14-01
  - DD-12-01
  - DD-13-01
decision_date: 2026-01-25
deciders: [efn-builders]
supersedes: null
---

# Backend Platform Selection

## Status

**Accepted** — Decision finalized based on RF-01-01 research findings and stakeholder review.

---

## Context

Compass is an LLM-orchestrated planning, research, and documentation system that requires a backend platform to support its core architecture layers:

**Layer 2 (Authoritative State)**: Projects, decisions, branches, workflow runs, permissions, and versioning must persist across sessions spanning days or weeks.

**Layer 3 (Artifact Store)**: Canonical documents and handoff bundles require structured storage with full history tracking.

**Layer 4 (Memory & Retrieval)**: Semantic and literal search with temporal awareness supports planning workflows.

**Layer 5 (Pristine Context)**: Verified sources and citations with timestamps require reliable storage and retrieval.

**Layer 6 (Integration & Events)**: Webhooks, queues, and schedulers synchronize with external systems.

The Compass System Definition (§1.7) establishes several guiding principles with backend implications: "Artifacts are truth; chat is a mutation vector," "State is externalized," "Multi-agent safety and human merge gates," and "Auditability and reversibility."

The backend platform must also serve EFN's broader tool ecosystem (DD-14-01), including broadcast-critical tools requiring highest reliability, production pipelines for video analytics and captions, publishing pipelines, and analytics systems. This demands expandability and modularity.

**Team context**: EFN's builders are non-traditional developers who rely on LLM coding agents as their primary development method. The team has no notable SQL familiarity. LLM maintainability—how well AI assistants can generate correct code for the platform—is a critical selection criterion.

**Budget constraints** (System Definition §4.1): $600–$2,000/year initial; $3,000–$5,000 at proven value. All evaluated platforms fall well within these targets.

---

## Options Considered

### Option 1: Convex

Convex is a backend-as-a-service providing a document-relational database, serverless functions, file storage, and real-time sync in a unified TypeScript environment. Queries and mutations are pure TypeScript functions running on managed infrastructure.

**Pros:**

Convex's TypeScript-native approach eliminates context-switching between TypeScript and SQL. When Claude or Cursor generates database code, it's pure TypeScript with full type checking. The schema definition flows through queries to frontend components with zero configuration—a critical advantage for LLM-assisted development.

The @convex-dev/agent component provides exactly what Compass requires: persistent threads for chat history across sessions, tool-based database access with argument validation, streaming via WebSocket, and human-in-the-loop support for merge gates. Building equivalent functionality on other platforms would require significant custom development.

Serializable transactions (the strictest ACID isolation level) with automatic rollback mean AI-generated mutations either complete fully or fail safely. No partial writes, no corrupted state. Convex describes this as making it "nearly impossible for AI to write code that could corrupt your data."

Automatic reactivity provides real-time collaboration without WebSocket configuration or cache invalidation logic. When any user modifies data, all connected clients see updates immediately. This directly supports broadcast workflow integrations where multiple operators may view the same project simultaneously.

The official MCP server includes "agent mode" limiting permissions for remote coding agents, and the built-in @convex-dev/rag component supports hybrid search combining text and vector results. Cost at Phase 3 scale is approximately $25-75/month.

**Cons:**

The proprietary document-relational model and TypeScript query DSL create vendor dependency. No SQL export or pg_dump equivalent exists. Migration would require rewriting queries and translating schema. There is no self-hosting option.

The ecosystem is smaller than PostgreSQL's. Fewer tutorials, examples, and community resources exist compared to SQL-based platforms.

Learning CQRS patterns (queries/mutations separation) differs from traditional database interaction. Aggregate queries (COUNT, SUM) require workarounds.

---

### Option 2: Supabase

Supabase wraps PostgreSQL with auto-generated REST/GraphQL APIs, authentication, file storage, edge functions, and real-time subscriptions. It's the closest open-source equivalent to Firebase with standard PostgreSQL underneath.

**Pros:**

Standard PostgreSQL provides maximum vendor independence. Data exports via pg_dump, the entire platform is open-source (Apache 2.0), and self-hosting is available. Migration to any PostgreSQL provider requires minimal changes.

The mature ecosystem includes 96K+ GitHub stars, extensive tutorials, and documentation. PostgreSQL skills transfer across the tool portfolio.

Row-level security (RLS) provides fine-grained access control at the row level. The security model is well-understood and battle-tested for multi-tenant applications.

Built-in authentication supports 18+ OAuth providers with SAML 2.0 SSO on the Pro plan. Real-time subscriptions handle collaborative features.

**Cons:**

The official MCP server is explicitly restricted to development only—documentation warns "Don't connect to production" and "Don't give to your customers." Production LLM database access requires building custom infrastructure with Edge Functions and RLS policies.

No built-in agent component exists. Implementing persistent threads, tool-based database access, streaming, and human-in-the-loop support requires significant custom development that Convex provides out of the box.

Type generation requires manual CLI commands and refresh cycles rather than automatic end-to-end flow. LLM-generated code must context-switch between TypeScript and SQL.

User feedback indicates RLS complexity can be error-prone for complex authorization requirements. Local development has been described as "a massive pain" for building "anything more robust than a toy app."

---

### Option 3: Neon

Neon is a serverless PostgreSQL database with copy-on-write branching, scale-to-zero capability, and compute-storage separation. Unlike Supabase and Convex, it's purely a database service—no auth, storage, or functions included.

**Pros:**

Database branching enables unique LLM safety workflows. Branches create in approximately one second regardless of database size using copy-on-write. LLM agents can operate with full freedom on sandbox branches; humans review diffs; approved changes merge to main. Neon reports that over 80% of their databases are now created by AI agents *(as_of: 2026-01-25)*.

The comprehensive MCP server and llms.txt documentation provide the highest LLM maintainability score among evaluated platforms. Standard PostgreSQL ensures maximum vendor independence.

Post-Databricks acquisition pricing is competitive, with storage costs reduced 80% from previous rates.

**Cons:**

Database-only service requires assembling multiple external services: compute platform (Vercel, Cloudflare Workers), authentication (Clerk, Auth0), file storage (S3, R2), and real-time (Ably, Pusher). Total cost and complexity increase substantially.

No built-in agent component, chat persistence, or real-time subscriptions. All must be implemented in the external compute layer.

PostgreSQL LISTEN/NOTIFY provides the only real-time mechanism—no WebSocket layer included. Real-time collaboration requires additional services.

---

### Option 4: Do Nothing (Continue Without Backend Decision)

Defer the backend decision to allow more evaluation time.

**Pros:**

No immediate implementation effort. Additional research could surface new options.

**Cons:**

Backend selection blocks multiple downstream research phases: RF-02-01 (LLM Orchestration), RF-03-01 (Memory & Retrieval), RF-08-01 (Hosting), Area 10 (Dev Tooling—research pending), and DD-17-01 (Integration Patterns). The research program cannot progress meaningfully without this foundational decision.

The evaluated platforms (Convex, Supabase, Neon) represent the leading options for LLM-assisted development. Waiting for hypothetical better options provides no concrete benefit.

---

## Decision

We will use **Convex** as the backend platform for Compass and the broader EFN tool ecosystem.

The decision is driven by three factors that align with EFN's specific context:

**Factor 1: LLM-Native Development**. The team has no notable SQL familiarity and relies on LLM coding agents as their primary development method. Convex's TypeScript-native approach eliminates the SQL context-switching that degrades AI code generation quality. The entire codebase—schema, queries, mutations, and frontend—can be pure TypeScript with end-to-end type safety.

**Factor 2: Built-In Agent Infrastructure**. Compass's core architecture requires persistent chat threads, tool-based database access with validation, streaming, and human-in-the-loop merge gates. Convex's @convex-dev/agent component provides this out of the box. Building equivalent infrastructure on Supabase or Neon would require weeks of custom development before Compass-specific work could begin.

**Factor 3: Automatic Real-Time for Broadcast Workflows**. EFN's tool ecosystem includes broadcast-critical applications where multiple operators view the same data simultaneously. Convex's automatic reactivity makes real-time collaboration native behavior rather than a feature requiring additional configuration. This directly supports the broadcast workflow integrations that are valuable across EFN's tool portfolio.

The vendor lock-in concern has been evaluated and accepted. The team prioritizes development velocity and LLM compatibility over SQL portability. The proprietary model is mitigated through abstraction layers, portable artifact formats (JSON, Markdown), periodic data exports, and documented migration strategies.

---

## Consequences

### Positive

The @convex-dev/agent component accelerates Compass development by providing pre-built infrastructure for the LLM-orchestrated planning workflows described in the System Definition. Persistent threads, tool-based database interaction, and human-in-the-loop support are available immediately rather than requiring custom implementation.

TypeScript-native development improves LLM coding assistant effectiveness. AI-generated database code receives full type checking, and the transactional model ensures mutations either complete fully or roll back entirely—preventing partial writes or corrupted state from AI errors.

Automatic real-time sync reduces implementation complexity for collaborative features. Multiple users viewing the same project will see updates immediately without WebSocket configuration, cache invalidation logic, or manual subscription management.

A single service for database, functions, storage, and real-time simplifies operations. Fewer moving parts to configure, deploy, and debug compared to assembling multiple services.

The built-in RAG component (@convex-dev/rag) provides a foundation for Compass's memory layer without requiring external vector database services.

### Negative

The proprietary query model creates vendor dependency. If Convex as a company fails or significantly changes direction, migration would require rewriting database interaction code. This is accepted as a calculated trade-off given the productivity advantages.

The CQRS pattern (queries/mutations separation) requires learning new patterns that differ from traditional database interaction. Team members will need to understand reactive subscriptions, optimistic updates, and the distinction between queries (read), mutations (write), and actions (side effects).

Aggregate queries (COUNT, SUM, GROUP BY) require workarounds in Convex's model. For analytics-heavy features, this may require creative solutions or hybrid approaches.

The ecosystem is smaller than PostgreSQL's. When encountering edge cases, fewer community resources, Stack Overflow answers, and tutorials are available compared to SQL-based platforms.

### Neutral

Database operations will be abstracted behind interfaces that could theoretically be reimplemented for other backends. While this mitigation exists, the practical likelihood of migration is low given the deep integration with Convex-specific features.

Artifacts will be stored in portable formats (JSON for structured data, Markdown for documents) within Convex's document-relational model. This preserves content portability even if the storage layer changes.

Periodic JSON exports will be established as a routine practice, providing a data backup that is independent of Convex's infrastructure.

---

## Implementation Notes

### Initial Setup

Create a Convex project and configure the development environment. Define the initial schema for core Compass entities: artifacts, threads, decisions, branches, workflow runs, and citations.

Implement basic CRUD operations using Convex's query/mutation patterns. Integrate @convex-dev/agent for LLM-orchestrated planning sessions with persistent thread storage.

Test real-time sync with multiple concurrent users to verify collaborative editing behavior meets expectations.

### Vendor Independence Mitigation

Abstract database operations behind TypeScript interfaces that define the contract for data access. While these interfaces will be implemented using Convex-specific code, the abstraction provides documentation of what any replacement would need to support.

Store artifacts in portable formats: YAML frontmatter for metadata, Markdown for content, JSON for structured data. Avoid Convex-specific data representations in artifact content.

Establish weekly or daily JSON exports of critical data as a routine backup procedure. Document the export format and restoration process.

Maintain a migration strategy document that identifies Convex-specific patterns and their PostgreSQL equivalents, updated as the codebase evolves.

### EFN Ecosystem Expansion

As additional EFN tools are built on Convex, establish shared patterns for common operations: authentication flows, audit logging, real-time subscriptions, and file storage.

Create reusable Convex components that can be shared across the tool portfolio, promoting consistency and reducing duplication.

Document the integration patterns that enable different tools to share data or communicate through Convex's infrastructure.

---

## Related Documents

**Research foundation**: RF-01-01 provides the comprehensive research findings that informed this decision, including detailed platform evaluations, comparative analysis, and community sentiment.

**Informs downstream research**: This decision enables RF-02-01 (LLM Orchestration), RF-03-01 (Memory & Retrieval), RF-08-01 (Hosting), Area 10 (Dev Tooling—research pending), and DD-17-01 (Integration Patterns) to proceed with Convex as the backend assumption.

**Ecosystem context**: DD-14-01 (EFN Tooling Ecosystem Requirements) defines the tool archetypes and reliability tiers that Convex must support as the platform expands beyond Compass.

**Artifact storage**: DD-13-01 (Artifact Taxonomy) defines the document structures that will be stored in Convex's document-relational model.

---

*End of Backend Platform Selection (ADR-01-01)*
