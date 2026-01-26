---
id: IDX-00-MASTER
type: index
title: Compass Project Reference Index
status: active
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Master navigation index for LLM agents traversing Compass documentation
tags: [index, navigation, reference, retrieval]
related: []
---

# Compass Project Reference Index

## Purpose

This document provides structured navigation for LLM agents working with Compass documentation. Use it to locate specific concepts, understand document relationships, and find authoritative sources for requirements.

**Navigation strategy**: Start with the Document Registry to identify relevant documents, then use Section Maps for specific content, and Concept Index for term definitions.

---

## Document Registry

| ID | File | Type | Domain | One-Line Purpose |
|----|------|------|--------|------------------|
| â€” | `Compass___System_Definition.md` | Core Spec | System | **Authoritative system specification**â€”what Compass is, requirements, architecture |
| DD-12-01 | `DD-12-01-repository-definitions.md` | Definition | Structure | Repository layout, naming conventions, git workflow |
| DD-13-01 | `DD-13-01-artifacts-definitions.md` | Definition | Documentation | Artifact types, frontmatter schema, lifecycle states, templates |
| DD-14-01 | `DD-14-01-ecosystem-definitions.md` | Definition | EFN Tools | Tool archetypes, reliability tiers, integration patterns |
| STD-14-01 | `STD-14-01-ecosystem-standards.md` | Standard | EFN Tools | Compliance checklists per archetype |
| DD-15-01 | `DD-15-01-governance-definitions.md` | Definition | Governance | Roles, permissions, approval workflows, audit requirements |
| STD-15-01 | `STD-15-01-governance-standards.md` | Standard | Governance | Audit log schema, event types, compliance verification |
| DD-17-01 | `DD-17-01-integration-definitions.md` | Definition | Integration | Webhooks, retries, error handling, secret management patterns |
| STD-17-01 | `STD-17-01-integration-standards.md` | Standard | Integration | Secret rules, error logging, pre-deployment checklists |
| DD-20-01 | `DD-20-01-evidence-definitions.md` | Definition | Research | Evidence grading, source tiers, freshness rules |
| STD-20-01 | `STD-20-01-evidence-standards.md` | Standard | Research | Citation format specification, JSON schema, examples |
| RF-01-01 | `RF-01-01-backend-findings.md` | Research Finding | Backend | Backend evaluation: Convex, Supabase, Neon |
| ADR-01-01 | `ADR-01-01-backend-selection.md` | ADR | Backend | **Decision**: Convex selected as backend platform |
| RF-02-01 | `RF-02-01-orchestration-findings.md` | Research Finding | Orchestration | Orchestration evaluation: Mastra, Vercel AI SDK, LangGraph.js, Instructor |
| ADR-02-01 | `ADR-02-01-orchestration-selection.md` | ADR | Orchestration | **Decision**: Mastra + Vercel AI SDK v6 for planning workflows |
| RF-03-01 | `RF-03-01-memory-findings.md` | Research Finding | Memory | Memory/retrieval evaluation: Convex @convex-dev/rag, Zep, Supermemory, Mem0 |
| RF-08-01 | `RF-08-01-hosting-findings.md` | Research Finding | Hosting | Frontend hosting evaluation: Vercel, Cloudflare Pages, Netlify, Railway |
| ADR-08-01 | `ADR-08-01-hosting-selection.md` | ADR | Hosting | **Decision**: Vercel for frontend hosting |
| RF-09-01 | `RF-09-01-llm-provider-findings.md` | Research Finding | LLM | LLM provider evaluation: Claude 4.5, GPT-5.2, Gemini 3, Groq, Mistral |
| ADR-09-01 | `ADR-09-01-llm-provider-selection.md` | ADR | LLM | **Decision**: Tiered Claude strategy (Opus for planning, Haiku for orchestration) |

### Document Relationships

```
Compass System Definition (authoritative source)
    â”‚
    â”œâ”€â”€ DD-12-01 Repository Structure
    â”‚
    â”œâ”€â”€ DD-13-01 Artifact Taxonomy
    â”‚       â””â”€â”€ templates for all artifact types
    â”‚
    â”œâ”€â”€ DD-14-01 EFN Ecosystem â†â”€â”€companionâ”€â”€â†’ STD-14-01 Compliance Checklists
    â”‚
    â”œâ”€â”€ DD-20-01 Evidence Standards â†â”€â”€companionâ”€â”€â†’ STD-20-01 Citation Format
    â”‚
    â”œâ”€â”€ RF-01-01 Backend Platform Evaluation (Area 01)
    â”‚       â”œâ”€â”€ Evaluates: Convex, Supabase, Neon
    â”‚       â”œâ”€â”€ Recommends: Convex (TypeScript-native, @convex-dev/agent)
    â”‚       â””â”€â”€ ADR-01-01 Backend Selection â† formalizes decision
    â”‚
    â””â”€â”€ RF-09-01 LLM Provider Evaluation (Area 09)
            â”œâ”€â”€ Evaluates: Claude 4.5, GPT-5.2, Gemini 3, Groq, Mistral
            â”œâ”€â”€ Recommends: Tiered strategy (Opus + Haiku)
            â””â”€â”€ ADR-09-01 LLM Provider Selection â† formalizes decision
```

---

## Section Maps

### Compass System Definition

The authoritative specification. **Read first** before any research or planning.

| Part | Sections | Key Content |
|------|----------|-------------|
| **Part 1: Vision** | 1.1â€“1.8 | Core problem, what Compass is/isn't, ecosystem philosophy, core promises, guiding principles, critical junctions |
| **Part 2: Functional** | 2.1â€“2.7 | Planning workflow (OPENâ†’FOLLOWâ†’SHARPENâ†’BOUNDARYâ†’GROUND), widgets, research integration, documentation truth, decision records, branching, handoff bundles |
| **Part 3: Technical** | 3.1â€“3.8 | LLM conversation, memory layers, interface requirements, state management, versioning, integrations, performance, reliability |
| **Part 4: Constraints** | 4.1â€“4.6 | Budget ($600â€“$2000 initial), team capacity, security, privacy, vendor independence, timeline phases |
| **Part 5: Architecture** | 5.1â€“5.4 | Seven layers, mental diagram, open standards (MCP), reference patterns |
| **Appendix A** | Glossary | 30+ term definitions |

**Key references by topic:**

| Topic | Section | Key Point |
|-------|---------|-----------|
| What is Compass | 1.2 | LLM-orchestrated planning/research/documentation system |
| What Compass is NOT | 1.3 | Not code execution, deployment, PM replacement, or "chat that exports docs" |
| Spec permanence | 1.2 | "Specification is permanent; implementation is ephemeral" |
| Planning arc stages | 2.1 | OPEN (3â€“5 turns) â†’ FOLLOW (10â€“20) â†’ SHARPEN (5â€“8) â†’ BOUNDARY (4â€“6) â†’ GROUND (3â€“5) |
| Widget types | 2.2 | Choice, spectrum, comparative, spatial, generative, meta widgets |
| Widget guarantees | 2.2 | Every widget must have: escape hatch, help, research trigger |
| Research types | 2.3 | Technical, domain, contextual |
| Memory layers | 3.2 | Session, project (cross-session), ecosystem (cross-project) |
| Core entities | 3.2 | Project, Artifact, Decision, Branch, Workflow run, Citation, Profile, Adapter |
| Truth hierarchy | 3.2 | Intent truth â†’ Execution truth â†’ Audit truth |
- **Audit log schema** → STD-15-01 § Part 1 (JSON schema for governance audit events)
| Budget | 4.1 | $600â€“$2000/year initial; $3000â€“$5000 proven value |
| Architecture layers | 5.1 | Interaction â†’ Authoritative State â†’ Artifact Store â†’ Memory â†’ Evidence â†’ Integration â†’ Execution |

---

### DD-12-01: Repository Structure

| Part | Key Content |
|------|-------------|
| **Part 1: Topology** | Specialized documentation pattern (separate docs repo), spec-driven development |
| **Part 2: Folders** | Complete layout, folder-to-artifact mapping, llms.txt index, INDEX.md structure |
| **Part 3: Naming** | File naming rules (kebab-case), prefix conventions, ADR numbering, title conventions |
| **Part 4: References** | Within-repo (relative links), cross-repo (full URLs), canonical IDs |
| **Part 5: Git** | GitHub Flow, branch naming (`docs/{type}/{topic}`), decision branch workflow, PR requirements |
| **Part 6: Validation** | Automated checks, validation checklist, periodic maintenance |
| **Part 7: LLM Optimization** | Shallow nesting, self-contained sections, AGENTS.md file, chunking-aware writing |

**Quick lookup:**

| Need | Location |
|------|----------|
| Folder structure diagram | Part 2, Section 2.1 |
| File naming format | `{PREFIX}-{identifier}-{descriptive-title}.md` (Part 3.1) |
| Area codes (01â€“20) | Part 3.2 |
| Branch naming pattern | `docs/{type}/{topic}` (Part 5.2) |
| PR template | Part 5.4 |
| AGENTS.md content | Part 7.2 |

---

### DD-13-01: Artifact Taxonomy

| Part | Key Content |
|------|-------------|
| **Part 1: Type Catalog** | 8 artifact types: SPEC, ADR, RB, RF, DD, STD, HANDOFF, IDX |
| **Part 2: Frontmatter** | Universal fields (required), type-specific fields, validation rules |
| **Part 3: Lifecycle** | Four states: draft â†’ review â†’ active â†’ deprecated; transition rules |
| **Part 4: Definition of Done** | Per-type completeness checklists |
| **Part 5: Reconciliation** | Delta identification, classification (spec error, implementation error, gap, enhancement), update vs supersede |
| **Part 6: Templates** | Full templates for SPEC, ADR, RF, STD |

**Artifact type quick reference:**

| Prefix | Type | When to Create |
|--------|------|----------------|
| SPEC- | Specification | Before any new feature |
| ADR- | Architecture Decision Record | When choosing between options |
| RB- | Research Brief | When investigation needed |
| RF- | Research Finding | When research completes |
| DD- | Definition Document | When defining taxonomies/concepts |
| STD- | Standard | When practice must be enforced |
| HANDOFF- | Handoff Bundle | When work transfers to implementation |
| IDX- | Index | When organizing related artifacts |

**Lifecycle transitions:**

| From | To | Trigger |
|------|-----|---------|
| (new) | draft | Create document |
| draft | review | Submit for review |
| review | draft | Request changes |
| review | active | Approve (not self) |
| active | deprecated | Supersede or retire |
- **Structured output** → RF-02-01 § 2.1 (schema-constrained JSON generation from LLMs)

**Required frontmatter (all types):**
`id`, `type`, `title`, `status`, `created`, `updated`, `author`, `summary`, `tags`, `related`

---

### DD-14-01: EFN Ecosystem

| Part | Key Content |
|------|-------------|
| **Part 1: Archetypes** | 6 archetypes: Broadcast-Critical, Production Pipeline, Publishing Pipeline, Internal Utility, Analytics & Intelligence, Exploratory |
| **Part 2: Requirements Matrix** | Per-archetype: reliability, integration, privacy, UX, security |
| **Part 3: Shared Standards** | API design, authentication, logging, error handling, documentation, data formats, dependencies |
| **Part 4: Integration Map** | Core data domains, shared services, critical data flows |
| **Part 5: Assignment Guide** | Flowchart for archetype selection, upgrade paths |

**Archetype quick reference:**

| Archetype | Reliability | Failure Impact |
|-----------|-------------|----------------|
| Broadcast-Critical | Tier 1 (99.9%) | Visible to audience |
| Production Pipeline | Tier 2 (99%) | Blocks content creation |
| Publishing Pipeline | Tier 3 (95%) | Delays publication |
| Internal Utility | Tier 4 (90%) | Impacts efficiency |
| Analytics & Intelligence | Tier 4 (90%) | Degrades decisions |
| Exploratory | Tier 5 (best effort) | Expected/acceptable |

**Reliability tier meanings:**

| Tier | Availability | Recovery Time |
|------|--------------|---------------|
| Tier 1 | 99.9% (zero during broadcast) | < 30 seconds |
| Tier 2 | 99% | < 1 hour |
| Tier 3 | 95% | < 4 hours |
| Tier 4 | 90% | < 24 hours |
| Tier 5 | Best effort | Best effort |

**Privacy profiles:**
- **Public**: Outputs are published
- **Internal**: EFN only, standard handling
- **Sensitive**: Competitive/business intelligence, strict controls (Analytics archetype)

---

### STD-14-01: EFN Compliance Checklists

| Part | Key Content |
|------|-------------|
| **Part 1: Archetype Checklists** | Per-archetype compliance items: pre-development, architecture, development, operations, security |
| **Part 2: Shared Standards** | API, authentication, logging, observability, error handling, documentation, data formats, dependencies |
| **Part 3: Verification Points** | New tool review, pre-launch, periodic (quarterly), post-incident |
| **Part 4: Compliance Levels** | Level 1 (non-negotiable) â†’ Level 4 (desired within 90 days) |

**Use this document** for actionable checklists when planning/reviewing tools. DD-14-01 provides the rationale; this provides the checklist.

**Compliance levels:**

| Level | Timing | Examples |
|-------|--------|----------|
| Level 1 | Before any use | Auth, no SPOFs for broadcast, no data leaks for analytics |
| Level 2 | Before production | All archetype items, logging, README |
| Level 3 | Within 30 days | Full observability, runbook |
| Level 4 | Within 90 days | Polished docs, automated scanning |

---

### DD-20-01: Evidence Standards

| Part | Key Content |
|------|-------------|
| **Part 1: Evidence Grading** | Three dimensions: Source Reliability (S1â€“S4), Information Quality (I1â€“I4), Confidence (High/Medium/Low) |
| **Part 2: Source Classification** | Five-tier taxonomy: T1 Authoritative â†’ T5 Unverified |
| **Part 3: Citation Format** | Required fields, recommended fields, source types, in-document format |
| **Part 4: Freshness** | Staleness thresholds, freshness scoring, deprecation status |
| **Part 5: Evidence Storage** | JSON schema for evidence artifacts |
| **Part 6: Implementation Guidance** | For research authors, reviewers, implementation agents |

**Source tier quick reference:**

| Tier | Label | Examples |
|------|-------|----------|
| T1 | Authoritative | Official docs, release notes, peer-reviewed papers |
| T2 | Validated Community | High-vote Stack Overflow, MDN, maintainer-endorsed |
| T3 | Curated Secondary | Tutorials from reputable platforms, conference talks |
| T4 | General Community | Developer blogs, GitHub issues |
| T5 | Unverified | Anonymous posts, outdated answers, AI-generated |

**Reliability ratings:**

| Rating | Label | Definition |
|--------|-------|------------|
| S1 | Established | Official vendor, verified expertise |
| S2 | Credible | Editorial oversight, generally reliable |
| S3 | Uncertain | Unknown track record |
| S4 | Questionable | Anonymous, biased, or inaccurate |

**Information quality:**

| Rating | Label | Requirement |
|--------|-------|-------------|
| I1 | Verified | 2+ independent sources agree |
| I2 | Supported | Single reliable source, fits patterns |
| I3 | Plausible | Makes sense but poorly supported |
| I4 | Unverified | Speculative or contradicted |

**Freshness thresholds:**

| Content Type | Max Age |
|--------------|---------|
| Critical/compliance | 7 days |
| API documentation | Tied to version |
| Technical tutorials | Tied to software version |
| Technical blogs | 6â€“12 months |
| Stack Overflow | High skepticism always |

---

### STD-20-01: Citation Format Specification

| Part | Key Content |
|------|-------------|
| **Part 1: Format Spec** | Required fields, recommended fields, source_type enum, tier/reliability values |
| **Part 2: JSON Schema** | Citation object schema, full evidence artifact schema |
| **Part 3: In-Document Format** | Inline citations, source list format, tier prefix |
| **Part 4: Examples** | Correct citations for T1â€“T5 sources, version-specific citations |
| **Part 5: Common Errors** | 7 error patterns with corrections |
| **Part 6: Compliance Checklist** | Per-citation, document-level, freshness |

**Required citation fields:**
`id`, `source_url`, `title`, `source_type`, `retrieved_at`

**In-document format:**
```
N. **[T#/S#]** Author. "Title" Version. 
   Published DATE. Retrieved DATE. URL
```

**Source type enum:**
`api_docs`, `vendor_docs`, `announcement`, `article`, `book`, `paper`, `community`, `blog`, `webpage`

---

### RF-01-01: Backend Platform Evaluation

RF-01-01 evaluates backend platforms for Compass with emphasis on LLM maintainability, agent integration, and expandability to serve EFN's full tool ecosystem.

| Part | Key Content |
|------|-------------|
| **Part 1: Context** | Compass requirements mapped to backend needs, evaluation criteria prioritization |
| **Part 2: Platform Evaluations** | Detailed analysis of Convex, Supabase, Neon |
| **Part 3: Comparative Analysis** | Requirements fit matrix, AI-native features comparison, cost comparison |
| **Part 4: Recommendation** | Convex as primary with mitigation strategies for vendor lock-in |
| **Part 5: Open Questions** | Stakeholder decisions needed |

**Platform summary:**

| Platform | Type | Key Strength | Key Limitation |
|----------|------|--------------|----------------|
| **Convex** | Document-relational BaaS | TypeScript-native, @convex-dev/agent, automatic real-time | Proprietary model, no SQL export |
| **Supabase** | PostgreSQL BaaS | Standard PostgreSQL, RLS security, mature ecosystem | MCP server dev-only, custom agent build required |
| **Neon** | Serverless PostgreSQL | Database branching for LLM sandboxing, highest LLM maintainability | Database-only (no auth/storage/realtime) |

**Decision**: Convex selected (see ADR-01-01)

**Key factors for Convex selection:**
- TypeScript-native eliminates SQL context-switching for LLM-assisted development
- @convex-dev/agent provides built-in chat persistence, tool-based database access, human-in-the-loop
- Automatic real-time sync for collaborative features without WebSocket configuration
- Serializable transactions ensure AI-generated mutations either complete fully or roll back

**Accepted trade-offs:**
- Proprietary model creates vendor dependency (mitigated by abstraction layers, portable formats, periodic exports)
- Smaller ecosystem than PostgreSQL
- CQRS pattern learning curve

---

### ADR-01-01: Backend Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Compass architecture layers, team context (non-traditional developers using LLM agents), budget constraints |
| **Options** | Convex, Supabase, Neon, Do Nothing |
| **Decision** | **Convex** selected |
| **Rationale** | LLM-native development, built-in agent infrastructure, automatic real-time |
| **Consequences** | Positive (accelerated development, type safety), Negative (vendor lock-in, learning curve) |
| **Reversibility** | Moderateâ€”abstraction layers enable future migration if needed |

**Decision summary**: Convex is selected because the team has no SQL familiarity and relies on LLM coding agents. Convex's TypeScript-native approach and @convex-dev/agent component provide the lowest implementation complexity for an LLM-orchestrated system.

---

### RF-09-01: LLM Provider Evaluation

RF-09-01 evaluates LLM providers for Compass with detailed pricing analysis, capability comparison, and tiered model strategy recommendation.

| Part | Key Content |
|------|-------------|
| **Part 1: Token Estimates** | Session types, monthly volumes (Phase 1: ~5.2M, Phase 3: ~20.8M), task classification |
| **Part 2: Provider Evaluations** | Claude 4.5 series, OpenAI GPT-5 series, Google Gemini series, Groq, Mistral |
| **Part 3: Cost Comparison** | All providers at Phase 1 and Phase 3 scale, hybrid strategy projections |
| **Part 4: Capability Matrix** | Core capabilities, instruction following assessment, Compass requirements fit |
| **Part 5: Provider Abstraction** | API similarity analysis, recommended abstraction approach |
| **Part 6: Recommendation** | Tiered model strategy with fallback chain |

**Provider summary (January 2026 pricing):**

| Provider | Planning Model | Cost/MTok | Orchestration Model | Cost/MTok |
|----------|---------------|-----------|---------------------|-----------|
| **Anthropic** | Claude Opus 4.5 | $5/$25 | Claude Haiku 4.5 | $1/$5 |
| **OpenAI** | GPT-5.2 | $1.75/$14 | GPT-5 Mini | $0.25/$2 |
| **Google** | Gemini 3 Pro | $2/$12 | Gemini 2.5 Flash | $0.30/$2.50 |

**Key insight**: Planning tasks require **frontier-level reasoning** to generate well-rounded choicesâ€”not just instruction following. Orchestration tasks require **reliable instruction following** for tool use.

**Critical exclusion**: Gemini 2.0 Flash ($0.10/$0.40) is **not recommended** despite low costâ€”weak instruction following and deprecated March 2026.

**Cost projections (hybrid strategy):**

| Phase | Planning (35%) | Orchestration (65%) | Total |
|-------|----------------|---------------------|-------|
| Phase 1 | ~$19.74 | ~$7.33 | **~$27/month** |
| Phase 3 | ~$78.96 | ~$29.31 | **~$108/month** |

Budget headroom: 87% at Phase 3 ($108 vs $800 ceiling)

---

### ADR-09-01: LLM Provider Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Compass LLM requirements, budget constraints ($200/mo Phase 1, $800/mo Phase 3), task types |
| **Options** | Single provider (Claude/OpenAI/Google), Hybrid strategy, API aggregator |
| **Decision** | **Hybrid strategy with tiered routing** |
| **Primary** | Claude Opus 4.5 (planning), Claude Haiku 4.5 (orchestration) |
| **Fallbacks** | Gemini 3 Pro / GPT-5.2 (planning), Gemini 2.5 Flash / GPT-5 Mini (orchestration) |
| **Reversibility** | Easyâ€”abstraction layer isolates provider-specific code |

**Decision summary**: Implement tiered model strategy using Claude Opus 4.5 for planning tasks (frontier reasoning) and Claude Haiku 4.5 for orchestration (reliable instruction following). Gemini and OpenAI serve as fallbacks for redundancy.

**Why frontier models for planning**: Planning conversations require generating well-rounded options and anticipating user needsâ€”this demands frontier reasoning, not just instruction following.

**Why mid-tier for orchestration**: Orchestration tasks (routing, tool calling) need reliable instruction following but not deep reasoning. Haiku 4.5 at $1/$5 provides reliability at 5Ã— lower cost than Sonnet.

---

### DD-15-01: Governance, Roles, Permissions

| Part | Key Content |
|------|-------------|
| **Part 1: Role Catalog** | 5 roles: Owner, Planner, Contributor, Viewer, Agent |
| **Part 2: Permission Matrix** | What each role can do across projects, artifacts, branches, system config |
| **Part 3: Agent Permissions** | Sponsorship model, scoped access, audit attribution |
| **Part 4: Approval Workflows** | What requires approval, escalation paths, emergency bypass |
| **Part 5: Audit Requirements** | What gets logged, retention periods, reconstruction capability |
| **Part 6: Review Patterns** | Periodic reviews, access audits, governance health checks |

**Role quick reference:**

| Role | Who | Access Level | Typical Count |
|------|-----|--------------|---------------|
| Owner | System administrator | Everything | 1 |
| Planner | Primary users | Full planning access | 2â€"3 |
| Contributor | Domain experts | Propose but not approve | 0â€"5 |
| Viewer | Stakeholders | Read-only | 10â€"50 |
| Agent | LLM agents | Scoped by sponsor | N/A |

**Key principle:** Self-approval is permitted for Planners to avoid bottlenecks in small teams. Audit logs record who approved what for after-the-fact review.

---

### STD-15-01: Governance and Audit Standards

| Part | Key Content |
|------|-------------|
| **Part 1: Audit Log Schema** | Core schema fields, field specifications, required vs optional |
| **Part 2: Event Types** | Enumeration of all auditable events by category |
| **Part 3: Retention Rules** | How long to keep logs, archival strategy |
| **Part 4: Compliance Verification** | Checklists for role setup, permission verification, periodic review |

**Use this document** for implementing audit logging and verifying governance compliance. DD-15-01 provides the rationale; this provides the schema and checklists.

---

### DD-17-01: Integration Architecture Patterns

| Part | Key Content |
|------|-------------|
| **Part 1: Integration Types** | Four types: Implementation Platforms, PM tools, Research Sources, Authentication |
| **Part 2: Idempotency** | Standard idempotency key pattern, duplicate detection, exactly-once semantics |
| **Part 3: Retry Strategy** | Exponential backoff with jitter, max attempts, circuit breaker pattern |
| **Part 4: Error Handling** | Error classification (transient vs permanent), user-facing vs logged errors |
| **Part 5: Rate Limiting** | Client-side rate limiting, backpressure, queue-based smoothing |
| **Part 6: Secret Management** | Environment variables, rotation, access control, audit |

**Pattern quick reference:**

| Integration Type | Recommended Pattern | Rationale |
|-----------------|---------------------|-----------|
| PM tools (Linear, Notion) | Start with polling, add webhooks | Webhook support varies |
| LLM APIs | Direct action calls with retry | Synchronous request-response |
| Research APIs | Polling + aggressive caching | Usually request-response only |
| Implementation handoff | Push via scheduled action | One-way; receiver controls timing |

**Standard integration flow in Convex:**
```
User Action â†' Mutation (saves intent) â†' Scheduler â†' Action (calls external API)
```

---

### STD-17-01: Integration Standards

| Part | Key Content |
|------|-------------|
| **Part 1: Secret Management Rules** | Storage, transmission, logging, access control, rotation |
| **Part 2: Error Logging Rules** | What to log, sanitization requirements, structured format |
| **Part 3: Pre-Deployment Checklist** | Verification steps before deploying any integration |
| **Part 4: Quick Reference Card** | Common decisions and patterns |

**Use this document** for actionable checklists when building integrations. DD-17-01 provides the patterns and rationale; this provides the compliance rules.

---

### RF-02-01: LLM Orchestration Evaluation

RF-02-01 evaluates orchestration frameworks for Compass with emphasis on structured output generation, session persistence, and provider abstraction.

| Part | Key Content |
|------|-------------|
| **Part 1: Context** | Compass requirements mapped to orchestration needs, evaluation criteria |
| **Part 2: Capability Assessment** | Structured output, session persistence, provider abstraction, TypeScript quality |
| **Part 3: Vercel AI SDK v6** | Output.object(), Output.array(), provider abstraction, highest maintainability score |
| **Part 4: Mastra** | Workflow graphs, suspend/resume, thread-based memory, PostgreSQL persistence |
| **Part 5: LangGraph.js** | Powerful checkpointing, but TypeScript quality issues, Zod-to-JSONSchema problems |
| **Part 6: Instructor** | Structured extraction focus, limited workflow support |
| **Part 7: Recommendation** | Two-layer architecture: Mastra for workflows, AI SDK for structured output |

**Framework summary:**

| Framework | Category | Key Strength | Key Limitation |
|-----------|----------|--------------|----------------|
| **Mastra** | Workflow orchestration | Suspend/resume, thread-based memory | Young framework (2025) |
| **Vercel AI SDK v6** | Provider abstraction | Structured output, maintainability | Not full orchestration |
| LangGraph.js | Graph orchestration | Powerful checkpointing | TypeScript quality issues |
| Instructor | Structured extraction | Clean output validation | Limited workflow support |

**Decision**: Mastra + Vercel AI SDK v6 selected (see ADR-02-01)

---

### ADR-02-01: LLM Orchestration Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Compass workflow requirements, multi-session persistence, branching exploration |
| **Options** | Mastra + AI SDK, AI SDK + XState, LangGraph.js, Do Nothing |
| **Decision** | **Mastra + Vercel AI SDK v6** |
| **Rationale** | Mastra provides workflow graphs; AI SDK provides structured output and provider abstraction |
| **Consequences** | Positive (2â€"3 week integration vs 6â€"10 week custom), Negative (young framework risk) |

**Decision summary**: Implement two-layer architecture combining Mastra for workflow orchestration (suspend/resume, thread-based memory) and Vercel AI SDK v6 for structured output generation and provider abstraction. LangGraph.js excluded due to TypeScript quality issues affecting widget generation reliability.

---

### RF-03-01: Memory & Retrieval Evaluation

RF-03-01 evaluates memory and retrieval solutions for Compass with emphasis on Convex integration and the three-layer memory model.

| Part | Key Content |
|------|-------------|
| **Part 1: Requirements** | Three memory layers (session, project, ecosystem), temporal awareness, Convex integration |
| **Part 2: Convex @convex-dev/rag** | Built-in vector search, namespace isolation, hybrid search, $0â€"25/month |
| **Part 3: Zep Graphiti** | Bi-temporal knowledge graphs, entity relationships, $40â€"70/month self-hosted |
| **Part 4: Supermemory** | MCP integration, sub-400ms latency, $19â€"99/month |
| **Part 5: Mem0** | Session isolation, change history, $249/month |
| **Part 6: Recommendation** | Convex-primary architecture; external services optional for complex temporal queries |

**Solution summary:**

| Solution | Category | Key Strength | Cost | Status |
|----------|----------|--------------|------|--------|
| **Convex @convex-dev/rag** | Built-in | Native integration, namespace isolation | $0â€"25/month | **Recommended** |
| Zep Graphiti | External | Bi-temporal graphs, entity relationships | $40â€"70/month | Phase 3 option |
| Supermemory | External | MCP integration, sub-400ms latency | $19â€"99/month | Phase 3 option |
| Mem0 | External | Session isolation, change history | $249/month | Not recommended |

**Recommendation**: Convex-primary with @convex-dev/rag â€" Built-in capabilities satisfy requirements. External services (Zep, Supermemory) reserved for Phase 3 if bi-temporal or MCP requirements emerge. ADR pending.

---

### RF-08-01: Frontend Hosting Evaluation

RF-08-01 evaluates frontend hosting platforms for Compass with Convex as the backend.

| Part | Key Content |
|------|-------------|
| **Part 1: Context** | Convex handles backend; frontend hosting is commodity decision |
| **Part 2: Vercel** | Official Convex Marketplace integration, zero-config deployment, $20/user/month |
| **Part 3: Cloudflare Pages** | Largest CDN (300+ PoPs), flat $20/month, requires additional Convex config |
| **Part 4: Netlify** | Free preview deployments, credit-based pricing complexity |
| **Part 5: Railway** | Full-stack focus, unnecessary complexity for frontend-only |
| **Part 6: Recommendation** | Vercel for integration quality and deployment simplicity |

**Platform summary:**

| Platform | Key Strength | Key Limitation | Cost |
|----------|--------------|----------------|------|
| **Vercel** | Official Convex integration | Per-seat pricing | $20/user/month |
| Cloudflare Pages | Flat pricing, largest CDN | Additional config for Convex | $20/month flat |
| Netlify | Free preview deployments | Credit-based complexity | Variable |
| Railway | Full-stack support | Unnecessary for frontend-only | Variable |

**Decision**: Vercel selected (see ADR-08-01)

---

### ADR-08-01: Frontend Hosting Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Convex handles backend; need frontend hosting with good integration |
| **Options** | Vercel, Cloudflare Pages, Netlify, Railway |
| **Decision** | **Vercel** |
| **Rationale** | Official Convex Marketplace integration, zero-config deployment, documentation alignment |
| **Consequences** | Positive (seamless integration, preview deployments), Negative (per-seat pricing at scale) |

**Decision summary**: Vercel selected for official Convex integration and deployment simplicity. Cloudflare Pages recommended as Phase 3 alternative if cost optimization becomes priority ($20/month flat vs $100â€"200/month at scale).

---

## Concept Index

Quick lookup for key terms. Format: **Term** â†’ Document Â§ Section

### Aâ€“C

- **Acceptance criteria** â†’ System Definition Â§ 2.7 (handoff bundle contents)
- **ADR (Architecture Decision Record)** â†’ DD-13-01 Â§ 1.2
- **Agent component (@convex-dev/agent)** â†’ RF-01-01 Â§ 2.1; ADR-01-01 (built-in chat persistence, tool-based database access)
- **Agent (role)** → DD-15-01 § 1.2 (LLM agent acting on behalf of a user with scoped permissions)
- **Agent Pack** â†’ System Definition Â§ Appendix A
- **Archetype (tool)** â†’ DD-14-01 Â§ Part 1
- **Artifact** â†’ DD-13-01 Â§ Part 1; System Definition Â§ Appendix A
- **Artifact store** â†’ System Definition Â§ 5.1 (Layer 3)
- **Audit truth** â†’ System Definition Â§ 3.2
- **Audit log schema** → STD-15-01 § Part 1 (JSON schema for governance audit events)
- **Backend platform** â†’ RF-01-01; ADR-01-01 (Convex selected)
- **Batch API** â†’ RF-09-01 Â§ Part 2 (50% discount for async processing)
- **BMAD** â†’ System Definition Â§ 5.4, Appendix A
- **Boundaries (always/ask first/never)** â†’ DD-13-01 Â§ 4.1, 6.1 template
- **Branch** â†’ System Definition Â§ 2.6; DD-13-01 Â§ Appendix A
- **Broadcast-Critical** â†’ DD-14-01 Â§ 1.2; STD-14-01 Â§ 1.1
- **Budget** â†’ System Definition Â§ 4.1 ($600â€“$2000 initial)
- **Canonical ID** â†’ DD-12-01 Â§ 4.2
- **Citation** â†’ DD-20-01 Â§ Part 3; STD-20-01 Â§ Parts 1â€“4
- **Claude 4.5** â†’ RF-09-01 Â§ 2.1; ADR-09-01 (Opus for planning, Haiku for orchestration)
- **Compliance levels** â†’ STD-14-01 Â§ Part 4
- **Confidence levels** â†’ DD-20-01 Â§ 1.4
- **Convex** â†’ RF-01-01 Â§ 2.1; ADR-01-01 (selected backend: TypeScript-native, document-relational)
- **@convex-dev/rag** → RF-03-01 § Part 2 (Convex component for vector search and retrieval)
- **CQRS** â†’ RF-01-01 Â§ Appendix B (Command Query Responsibility Segregationâ€”queries/mutations separation)

### Dâ€“G

- **Database branching** â†’ RF-01-01 Â§ 2.3 (Neon: instant branching for LLM sandboxing)
- **Decision gate** â†’ System Definition Â§ Appendix A
- **Decision ledger** â†’ System Definition Â§ 2.5
- **Decision record** â†’ DD-13-01 Â§ 1.2 (ADR)
- **Definition Document (DD-)** â†’ DD-13-01 Â§ 1.2
- **Definition of Done** â†’ DD-13-01 Â§ Part 4
- **Delta (implementation)** â†’ DD-13-01 Â§ 5.1
- **Deprecated (status)** â†’ DD-13-01 Â§ 3.2
- **Document-relational model** â†’ RF-01-01 Â§ 2.1 (Convex: JSON-like nested objects with relational tables)
- **Ecosystem philosophy** â†’ System Definition Â§ 1.4
- **Error handling standard** â†’ DD-14-01 Â§ 3.4; STD-14-01 Â§ 2.5
- **Escape hatch** â†’ System Definition Â§ 2.2
- **Evidence artifact** â†’ DD-20-01 Â§ 5.1
- **Evidence grading** â†’ DD-20-01 Â§ Part 1
- **Execution truth** â†’ System Definition Â§ 3.2
- **Freshness** â†’ DD-20-01 Â§ Part 4
- **Frontier reasoning** â†’ RF-09-01 Â§ 6.1; ADR-09-01 (planning tasks require deep reasoning, not just instruction following)
- **Frontmatter** â†’ DD-13-01 Â§ Part 2
- **Gemini** â†’ RF-09-01 Â§ 2.3 (Google: Gemini 3 Pro for planning fallback, 2.5 Flash for orchestration)
- **GitHub Flow** â†’ DD-12-01 Â§ 5.1
- **GPT-5** â†’ RF-09-01 Â§ 2.2 (OpenAI: GPT-5.2 for planning fallback, GPT-5 Mini for orchestration)
- **GROUND (stage)** â†’ System Definition Â§ 2.1
- **GSD** â†’ System Definition Â§ 1.3, Appendix A

### Hâ€“M

- **Handoff bundle** â†’ System Definition Â§ 2.7; DD-13-01 Â§ 1.2
- **HANDOFF- prefix** â†’ DD-13-01 Â§ 1.2
- **Hybrid strategy (LLM)** â†’ RF-09-01 Â§ 6; ADR-09-01 (different models for different task types)
- **Idempotency** → DD-17-01 § Part 2 (processing same operation multiple times yields same result)
- **IDX- prefix** â†’ DD-13-01 Â§ 1.2
- **Index document** â†’ DD-13-01 Â§ 1.2; DD-12-01 Â§ 2.4
- **Information quality (I1â€“I4)** â†’ DD-20-01 Â§ 1.3
- **Instruction following** â†’ RF-09-01 Â§ 4.2 (critical for orchestration tasks; weak in Gemini 2.0 Flash, GPT-5 Nano)
- **Integration patterns** â†’ DD-14-01 Â§ 4.4
- **Integration patterns (detailed)** → DD-17-01 (webhooks, retries, error handling, secret management)
- **Intent truth** â†’ System Definition Â§ 3.2
- **Lifecycle states** â†’ DD-13-01 Â§ Part 3 (draft/review/active/deprecated)
- **llms.txt** â†’ DD-12-01 Â§ 2.3; RF-01-01 (LLM navigation index)
- **LLM maintainability** â†’ RF-01-01 (evaluation criterion: how well AI assistants generate correct code)
- **LLM provider** â†’ RF-09-01; ADR-09-01 (Claude primary, Gemini/OpenAI fallback)
- **Logging standard** â†’ DD-14-01 Â§ 3.3; STD-14-01 Â§ 2.3
- **MCP (Model Context Protocol)** â†’ System Definition Â§ 5.3; RF-01-01 (LLM tool integration standard)
- **Memory layers** â†’ System Definition Â§ 3.2 (session, project, ecosystem)
- **Merge gate** â†’ System Definition Â§ 2.3
- **Model router** â†’ RF-09-01 Â§ 5; ADR-09-01 (task classification â†’ model selection)
- **Mastra** → RF-02-01; ADR-02-01 (selected workflow orchestration framework with suspend/resume)

### Nâ€“R

- **Naming conventions** â†’ DD-12-01 Â§ Part 3
- **Neon** â†’ RF-01-01 Â§ 2.3 (serverless PostgreSQL, database branching, database-only service)
- **OPEN (stage)** â†’ System Definition Â§ 2.1
- **Owner (role)** → DD-15-01 § 1.2 (system administrator with full access)
- **Planner (role)** → DD-15-01 § 1.2 (primary user running full planning workflow)
- **pgvector** â†’ RF-01-01 Â§ 2.2, 2.3 (PostgreSQL vector search extension)
- **Planning arc** â†’ System Definition Â§ 2.1 (OPENâ†’FOLLOWâ†’SHARPENâ†’BOUNDARYâ†’GROUND)
- **Pristine context** â†’ System Definition Â§ 5.1 (Layer 5)
- **Privacy profiles** â†’ DD-14-01 Â§ 2.3
- **Production Pipeline** â†’ DD-14-01 Â§ 1.2; STD-14-01 Â§ 1.2
- **Prompt caching** â†’ RF-09-01 Â§ 2.1 (up to 90% savings on repeated context)
- **Questioning arc** â†’ System Definition Â§ 2.1
- **RB- (Research Brief)** â†’ DD-13-01 Â§ 1.2
- **Real-time collaboration** â†’ RF-01-01 Â§ 2.1 (Convex: automatic reactivity without WebSocket config)
- **Reconciliation** â†’ DD-13-01 Â§ Part 5
- **Reliability tier** â†’ DD-14-01 Â§ 2.1
- **Research Brief** â†’ DD-13-01 Â§ 1.2
- **Research Finding** â†’ DD-13-01 Â§ 1.2; DD-20-01 Â§ Part 6
- **RF- prefix** â†’ DD-13-01 Â§ 1.2
- **RLS (Row Level Security)** â†’ RF-01-01 Â§ 2.2 (Supabase: fine-grained access control)

### Sâ€“Z

- **Secret management** → DD-17-01 § Part 6; STD-17-01 § Part 1 (environment variables, rotation, access control)
- **Serializable isolation** â†’ RF-01-01 Â§ Appendix B (strictest ACID level; Convex defaultâ€”prevents partial writes)
- **SHARPEN (stage)** â†’ System Definition Â§ 2.1
- **Source reliability (S1â€“S4)** â†’ DD-20-01 Â§ 1.2
- **Source tier (T1â€“T5)** â†’ DD-20-01 Â§ 2.1
- **Spec permanence principle** â†’ System Definition Â§ 1.2
- **Sponsor (agent)** → DD-15-01 § Part 3 (human user responsible for agent actions)
- **SPEC- prefix** â†’ DD-13-01 Â§ 1.2
- **Specification** â†’ DD-13-01 Â§ 1.2
- **SSO (Single Sign-On)** â†’ RF-01-01 Â§ 2.2 (Supabase: SAML 2.0 on Pro plan)
- **Staleness** â†’ DD-20-01 Â§ 4.2
- **Standard (STD-)** â†’ DD-13-01 Â§ 1.2
- **STD- prefix** â†’ DD-13-01 Â§ 1.2
- **Supabase** â†’ RF-01-01 Â§ 2.2 (PostgreSQL BaaS, RLS security, alternative to Convex)
- **Supersede** â†’ DD-13-01 Â§ 5.3
- **Structured output** → RF-02-01 § 2.1 (schema-constrained JSON generation from LLMs)
- **Tiered model strategy** â†’ RF-09-01 Â§ 6; ADR-09-01 (frontier for planning, mid-tier for orchestration)
- **Timeline phases** â†’ System Definition Â§ 4.6 (Phases 1â€“5)
- **Token usage** â†’ RF-09-01 Â§ 1 (Phase 1: ~5.2M/mo, Phase 3: ~20.8M/mo)
- **Truth hierarchy** â†’ System Definition Â§ 3.2
- **TypeScript-native** â†’ RF-01-01 Â§ 2.1; ADR-01-01 (Convex: eliminates SQL context-switching)
- **Vendor independence** â†’ System Definition Â§ 4.5; RF-01-01 Â§ 3.5 (Convex accepted trade-off with mitigations)
- **Vendor lock-in** â†’ RF-01-01 Â§ 3.5 (Convex: proprietary model; mitigated by abstractions)
- **Vercel** → RF-08-01; ADR-08-01 (selected frontend hosting platform)
- **Vercel AI SDK v6** → RF-02-01; ADR-02-01 (selected LLM abstraction layer for structured output)
- **Widget taxonomy** â†’ System Definition Â§ 2.2
- **Workflow run** â†’ System Definition Â§ 3.2

---

## Cross-Reference Tables

### Where to Find Specific Guidance

| I need to... | Go to |
|--------------|-------|
| Understand what Compass is | System Definition Â§ 1.2â€“1.3 |
| Plan a new feature | System Definition Â§ 2.1â€“2.7 |
| Create a specification | DD-13-01 Â§ 6.1 (template) |
| Record an architecture decision | DD-13-01 Â§ 6.2 (ADR template) |
| Conduct research | DD-20-01, STD-20-01 |
| Write a research finding | DD-13-01 Â§ 6.3 (template), DD-20-01 Â§ Part 6 |
| Classify a new EFN tool | DD-14-01 Â§ Part 5 (flowchart) |
| Check compliance for a tool | STD-14-01 Â§ Part 1 (checklists) |
| Name a file | DD-12-01 Â§ Part 3 |
| Structure a repository | DD-12-01 Â§ Part 2 |
| Cite a source properly | STD-20-01 Â§ Parts 3â€“4 |
| Evaluate source quality | DD-20-01 Â§ Parts 1â€“2 |
| Understand lifecycle states | DD-13-01 Â§ Part 3 |
| Handle spec/implementation divergence | DD-13-01 Â§ Part 5 |
| Set up git workflow | DD-12-01 Â§ Part 5 |
| **Choose a backend platform** | RF-01-01, ADR-01-01 |
| **Choose an LLM provider** | RF-09-01, ADR-09-01 |
| **Understand model tier strategy** | RF-09-01 Â§ 6, ADR-09-01 |
| **Evaluate LLM costs** | RF-09-01 Â§ Part 3 |

### Document Pairs (Definition + Standard)

| Definition | Standard | Topic |
|------------|----------|-------|
| DD-14-01 | STD-14-01 | EFN tool requirements |
| DD-15-01 | STD-15-01 | Governance and audit |
| DD-17-01 | STD-17-01 | Integration patterns |
| DD-20-01 | STD-20-01 | Evidence/citations |

**Pattern**: DD documents explain *why* and *what*; STD documents provide *enforceable rules* and *checklists*.

### Research + Decision Pairs

| Research Finding | ADR | Topic | Decision |
|------------------|-----|-------|----------|
| RF-01-01 | ADR-01-01 | Backend Platform | Convex |
| RF-02-01 | ADR-02-01 | LLM Orchestration | Mastra + Vercel AI SDK v6 |
| RF-03-01 | *(pending)* | Memory & Retrieval | Convex-primary (recommended) |
| RF-08-01 | ADR-08-01 | Frontend Hosting | Vercel |
| RF-09-01 | ADR-09-01 | LLM Provider | Claude (tiered: Opus + Haiku) |

**Pattern**: RF documents provide research and analysis; ADR documents formalize the decision with rationale and consequences.

### Required Reading by Task

| Task | Must Read | Reference As Needed |
|------|-----------|---------------------|
| First-time orientation | System Definition (full) | â€” |
| Planning new feature | System Definition Â§ 2, DD-13-01 | DD-12-01 |
| Conducting research | DD-20-01, STD-20-01 | DD-13-01 Â§ 6.3 |
| Classifying EFN tool | DD-14-01 | STD-14-01 |
| Creating any artifact | DD-13-01 | DD-12-01 |
| Setting up repository | DD-12-01 | DD-13-01 |
| **Implementing backend** | RF-01-01, ADR-01-01 | System Definition Â§ 4 |
| **Implementing LLM layer** | RF-09-01, ADR-09-01 | System Definition Â§ 3 |
| **Implementing orchestration** | RF-02-01, ADR-02-01 | RF-09-01 |
| **Implementing memory** | RF-03-01 | ADR-01-01 |
| **Deploying frontend** | RF-08-01, ADR-08-01 | ADR-01-01 |
| **Building integrations** | DD-17-01, STD-17-01 | DD-14-01 |
| **Setting up governance** | DD-15-01, STD-15-01 | — |

---

## Quick Lookup Tables

### Artifact Prefixes â†’ Types

| Prefix | Artifact Type |
|--------|---------------|
| SPEC- | Specification |
| ADR- | Architecture Decision Record |
| RB- | Research Brief |
| RF- | Research Finding |
| DD- | Definition Document |
| STD- | Standard |
| HANDOFF- | Handoff Bundle |
| IDX- | Index |

### Area Codes

| Code | Domain |
|------|--------|
| 01 | Backend Platform |
| 02 | LLM Orchestration |
| 03 | Memory & Retrieval |
| 04 | Documentation Platform |
| 05 | PM Integration |
| 06 | Research Tools |
| 07 | Widget Libraries |
| 08 | Hosting |
| 09 | LLM Provider |
| 10 | Dev Tooling |
| 11 | Handoff Schema |
| 12 | Repository Structure |
| 13 | Artifact Taxonomy |
| 14 | EFN Ecosystem |
| 15 | Governance |
| 16 | Reliability Tiers |
| 17 | Integration Patterns |
| 18 | Questioning Arc |
| 19 | Widget Schema |
| 20 | Evidence Standards |

### Architecture Layers (System Definition Â§ 5.1)

| Layer | Name | Purpose |
|-------|------|---------|
| 1 | Interaction | Web/chat UI, widgets, questioning arc |
| 2 | Authoritative State | Projects, decisions, branches, permissions |
| 3 | Artifact Store | Canonical docs, handoff bundles (git-friendly) |
| 4 | Memory & Retrieval | Semantic/literal search, temporal awareness |
| 5 | Pristine Context | Verified sources, extracted ground truth |
| 6 | Integration & Event | Webhooks, queues, external sync |
| 7 | Execution Platforms | Downstream coding/execution tools |

### Planning Arc Stages

| Stage | Purpose | Typical Turns |
|-------|---------|---------------|
| OPEN | Extract fuzzy idea, motivations, outcomes | 3â€“5 |
| FOLLOW | Expand, discover requirements, gather signals | 10â€“20 |
| SHARPEN | Prioritize, force trade-offs, reveal priorities | 5â€“8 |
| BOUNDARY | Define out-of-scope, prevent scope creep | 4â€“6 |
| GROUND | Apply hard constraints (budget, security, timeline) | 3â€“5 |

### Backend Platform Decision (RF-01-01, ADR-01-01)

| Platform | Type | Key Strength | Key Limitation | Status |
|----------|------|--------------|----------------|--------|
| **Convex** | Document-relational BaaS | TypeScript-native, @convex-dev/agent | Proprietary model | **Selected** |
| Supabase | PostgreSQL BaaS | Standard SQL, RLS, mature ecosystem | Custom agent build required | Alternative |
| Neon | Serverless PostgreSQL | Database branching, highest LLM score | Database-only | Alternative |

### LLM Orchestration Decision (RF-02-01, ADR-02-01)

| Framework | Category | Key Strength | Key Limitation | Status |
|-----------|----------|--------------|----------------|--------|
| **Mastra** | Workflow orchestration | Suspend/resume, thread-based memory | Young framework (2025) | **Selected** |
| **Vercel AI SDK v6** | Provider abstraction | Structured output, maintainability | Not full orchestration | **Selected** |
| LangGraph.js | Graph orchestration | Powerful checkpointing | TypeScript quality issues | Excluded |
| Instructor | Structured extraction | Clean output validation | Limited workflow support | Alternative |

### Memory Architecture Decision (RF-03-01)

| Solution | Category | Key Strength | Cost | Status |
|----------|----------|--------------|------|--------|
| **Convex @convex-dev/rag** | Built-in | Native integration, namespace isolation | $0â€"25/month | **Recommended** |
| Zep Graphiti | External | Bi-temporal graphs, entity relationships | $40â€"70/month | Phase 3 option |
| Supermemory | External | MCP integration, sub-400ms latency | $19â€"99/month | Phase 3 option |
| Mem0 | External | Session isolation, change history | $249/month | Not recommended |

### Frontend Hosting Decision (RF-08-01, ADR-08-01)

| Platform | Key Strength | Key Limitation | Cost | Status |
|----------|--------------|----------------|------|--------|
| **Vercel** | Official Convex integration | Per-seat pricing | $20/user/month | **Selected** |
| Cloudflare Pages | Flat pricing, largest CDN | Additional config for Convex | $20/month flat | Phase 3 alternative |
| Netlify | Free preview deployments | Credit-based complexity | Variable | Alternative |
| Railway | Full-stack support | Unnecessary for frontend-only | Variable | Not recommended |

### LLM Provider Decision (RF-09-01, ADR-09-01)

**Primary provider: Anthropic Claude**

| Task Type | Model | Cost/MTok (in/out) | Rationale |
|-----------|-------|-------------------|-----------|
| Planning & research | Claude Opus 4.5 | $5/$25 | Frontier reasoning for generating choices |
| Orchestration & tool use | Claude Haiku 4.5 | $1/$5 | Reliable instruction following |

**Fallback providers:**

| Role | Gemini | OpenAI |
|------|--------|--------|
| Planning fallback | Gemini 3 Pro ($2/$12) | GPT-5.2 ($1.75/$14) |
| Orchestration fallback | Gemini 2.5 Flash ($0.30/$2.50) | GPT-5 Mini ($0.25/$2) |

**Cost projection:**

| Phase | Monthly Cost | Budget | Headroom |
|-------|--------------|--------|----------|
| Phase 1 | ~$27 | $200 | 86% |
| Phase 3 | ~$108 | $800 | 87% |

### Cost Projections Summary

| Component | Phase 1 | Phase 3 | Budget Target |
|-----------|---------|---------|---------------|
| LLM (tiered Claude) | ~$27/month | ~$108/month | $200 / $800 |
| Backend (Convex) | ~$25/month | ~$75/month | Included in total |
| Memory (Convex-primary) | $0–25/month | $0–25/month | Included in backend |
| Hosting (Vercel) | ~$40–60/month | ~$100–200/month | $50 / $150 |
| **Total** | **~$100–120/month** | **~$300–400/month** | $600–2000/year |

### Budget Reference

| Phase | LLM Budget | Backend Budget | Total Target |
|-------|------------|----------------|--------------|
| Phase 1 | <$200/month | ~$25/month | $600â€“$2000/year |
| Phase 3 | <$800/month | ~$75/month | $3000â€“$5000/year |

---

## Document Version Tracking

| Document | Status | Last Updated |
|----------|--------|--------------|
| System Definition | active (v2.0) | 2026-01-24 |
| DD-12-01 | draft | 2026-01-25 |
| DD-13-01 | draft | 2026-01-25 |
| DD-14-01 | draft | 2026-01-25 |
| STD-14-01 | draft | 2026-01-25 |
| DD-15-01 | draft | 2026-01-25 |
| STD-15-01 | draft | 2026-01-25 |
| DD-17-01 | draft | 2026-01-25 |
| STD-17-01 | draft | 2026-01-25 |
| DD-20-01 | draft | 2026-01-25 |
| STD-20-01 | draft | 2026-01-25 |
| RF-01-01 | draft | 2026-01-25 |
| **ADR-01-01** | **accepted** | 2026-01-25 |
| RF-02-01 | draft | 2026-01-25 |
| **ADR-02-01** | **draft** | 2026-01-25 |
| RF-03-01 | draft | 2026-01-25 |
| RF-08-01 | draft | 2026-01-25 |
| **ADR-08-01** | **proposed** | 2026-01-25 |
| RF-09-01 | draft | 2026-01-25 |
| **ADR-09-01** | **proposed** | 2026-01-25 |
| **This Index** | **1.3** | 2026-01-25 |

---

## Maintenance Notes

**When adding new documents:**
1. Add entry to Document Registry table
2. Create Section Map with part/section breakdown
3. Add key terms to Concept Index
4. Update Cross-Reference Tables
5. Update Document Version Tracking

**Index structure is designed for:**
- Fast concept lookup (Concept Index is alphabetical)
- Task-oriented navigation (Cross-Reference Tables)
- Document-by-document exploration (Section Maps)
- Quick reference during work (Quick Lookup Tables)

**Recent updates (v1.3):**
- Added RF-02-01 LLM Orchestration Findings (Mastra + Vercel AI SDK v6 recommended)
- Added ADR-02-01 Orchestration Selection
- Added RF-03-01 Memory & Retrieval Findings (Convex-primary recommended, ADR pending)
- Added RF-08-01 Frontend Hosting Findings (Vercel recommended)
- Added ADR-08-01 Hosting Selection
- Added DD-15-01 Governance Definitions
- Added STD-15-01 Governance Standards
- Added DD-17-01 Integration Patterns
- Added STD-17-01 Integration Standards
- Updated Document Relationships diagram with all RF→ADR pairs
- Added Section Maps for all new documents
- Added orchestration, memory, hosting, governance, and integration concepts to Concept Index
- Added Quick Lookup tables for orchestration, memory, and hosting decisions
- Added Cost Projections Summary table
- Updated Required Reading by Task for new implementation areas
- Corrected RF-01-09 filename references to RF-09-01

**Previous updates (v1.2):**
- Consolidated RF-01-01 to single document covering Convex, Supabase, Neon (removed alternatives document)
- Added ADR-01-01 Backend Selection (Convex selected)
- Added RF-09-01 LLM Provider Findings
- Added ADR-09-01 LLM Provider Selection (tiered Claude strategy)
- Updated Document Relationships diagram to show RFâ†’ADR pairs
- Added Research + Decision Pairs to Cross-Reference Tables
- Added LLM-specific concepts to Concept Index
- Added Backend Platform Decision and LLM Provider Decision quick lookup tables
- Corrected file names to match actual project files

---

*End of Compass Project Reference Index (IDX-00-MASTER)*
