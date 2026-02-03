---
id: IDX-00-MASTER
type: index
title: Compass Project Reference Index
status: active
created: 2026-01-25
updated: 2026-02-03
author: compass-research
summary: Master navigation index for LLM agents traversing Compass documentation
tags: [index, navigation, reference, retrieval]
related: []
links: []
---

# Compass Project Reference Index

## Purpose

This document provides structured navigation for LLM agents working with Compass documentation. Use it to locate specific concepts, understand document relationships, and find authoritative sources for requirements.

**Navigation strategy**: Start with the Document Registry to identify relevant documents, then use Section Maps for specific content, and Concept Index for term definitions.

**LLM retrieval note**: When LLM views are available, start with `llm/LLM-INDEX.md` for optimized retrieval. Canonical artifacts remain the source of truth.

---

## Document Registry

| ID | File | Type | Domain | One-Line Purpose |
|----|------|------|--------|------------------|
| SYS-00 | `SYS-00-system-definition.md` | Core Spec | System | **Authoritative system specification**—what Compass is, requirements, architecture |
| DD-12-01 | `DD-12-01-repository-definitions.md` | Definition | Structure | Repository layout, naming conventions, git workflow |
| DD-13-01 | `DD-13-01-artifacts-definitions.md` | Definition | Documentation | Artifact types, frontmatter schema, lifecycle states, templates |
| DD-14-01 | `DD-14-01-ecosystem-definitions.md` | Definition | EFN Tools | Tool archetypes, reliability tiers, integration patterns |
| STD-14-01 | `STD-14-01-ecosystem-standards.md` | Standard | EFN Tools | Compliance checklists per archetype |
| DD-15-01 | `DD-15-01-governance-definitions.md` | Definition | Governance | Roles, permissions, approval workflows, audit requirements |
| STD-15-01 | `STD-15-01-governance-standards.md` | Standard | Governance | Audit log schema, event types, compliance verification |
| DD-17-01 | `DD-17-01-integration-definitions.md` | Definition | Integration | Webhooks, retries, error handling, secret management patterns |
| STD-17-01 | `STD-17-01-integration-standards.md` | Standard | Integration | Secret rules, error logging, pre-deployment checklists |
| DD-18-01 | `DD-18-01-questioning-arc.md` | Definition | Planning | Five-stage planning workflow, research branching, merge gates |
| STD-18-01 | `STD-18-01-questioning-arc-standards.md` | Standard | Planning | Stage completion criteria, transition rules, quality metrics |
| DD-19-01 | `DD-19-01-widget-schema.md` | Definition | Widgets | JSON schemas for all widget types, interaction logging, LLM generation |
| STD-19-01 | `STD-19-01-widget-schema-standards.md` | Standard | Widgets | Required fields, logging requirements, compliance rules |
| DD-20-01 | `DD-20-01-evidence-definitions.md` | Definition | Research | Evidence grading, source tiers, freshness rules |
| STD-20-01 | `STD-20-01-evidence-standards.md` | Standard | Research | Citation format specification, JSON schema, examples |
| RF-01-01 | `RF-01-01-backend-findings.md` | Research Finding | Backend | Backend evaluation: Convex, Supabase, Neon |
| ADR-01-01 | `ADR-01-01-backend-selection.md` | ADR | Backend | **Decision**: Convex selected as backend platform |
| RF-02-01 | `RF-02-01-orchestration-findings.md` | Research Finding | Orchestration | Orchestration evaluation: Mastra, Vercel AI SDK, LangGraph.js, Instructor |
| ADR-02-01 | `ADR-02-01-orchestration-selection.md` | ADR | Orchestration | **Decision**: Mastra + Vercel AI SDK v6 for planning workflows |
| RF-03-01 | `RF-03-01-memory-findings.md` | Research Finding | Memory | Memory/retrieval evaluation: Convex @convex-dev/rag, Zep, Supermemory, Mem0 |
| RF-04-01 | `RF-04-01-documentation-findings.md` | Research Finding | Documentation | Documentation platform evaluation: Obsidian, GitBook, VS Code/Foam, Mintlify |
| ADR-04-01 | `ADR-04-01-documentation-selection.md` | ADR | Documentation | **Decision**: Obsidian with Git selected for documentation platform |
| RF-07-01 | `RF-07-01-widgets-findings.md` | Research Finding | Widgets | Widget library evaluation: Thesys C1, CopilotKit, shadcn/ui, SurveyJS |
| ADR-07-01 | `ADR-07-01-widgets-selection.md` | ADR | Widgets | **Decision**: Thesys C1 + shadcn/ui hybrid for widget rendering |
| RF-08-01 | `RF-08-01-hosting-findings.md` | Research Finding | Hosting | Frontend hosting evaluation: Vercel, Cloudflare Pages, Netlify, Railway |
| ADR-08-01 | `ADR-08-01-hosting-selection.md` | ADR | Hosting | **Decision**: Vercel for frontend hosting |
| RF-09-01 | `RF-09-01-llm-provider-findings.md` | Research Finding | LLM | LLM provider evaluation: Claude 4.5, GPT-5.2, Gemini 3, Groq, Mistral |
| ADR-09-01 | `ADR-09-01-llm-provider-selection.md` | ADR | LLM | **Decision**: Tiered Claude strategy (Opus for planning, Haiku for orchestration) |

### Document Relationships

```
Compass System Definition (authoritative source)
    │
    ├── DD-12-01 Repository Structure
    │
    ├── DD-13-01 Artifact Taxonomy
    │       └── templates for all artifact types
    │
    ├── DD-14-01 EFN Ecosystem ←──companion──→ STD-14-01 Compliance Checklists
    │
    ├── DD-15-01 Governance ←──companion──→ STD-15-01 Audit Standards
    │
    ├── DD-17-01 Integration Patterns ←──companion──→ STD-17-01 Integration Standards
    │
    ├── DD-18-01 Questioning Arc ←──companion──→ STD-18-01 Arc Standards
    │       ├── informed by: ADR-02-01 (orchestration framework)
    │       └── integration: DD-19-01 (widget types), DD-15-01 (permissions)
    │
    ├── DD-19-01 Widget Schema ←──companion──→ STD-19-01 Widget Standards
    │       ├── informed by: RF-02-01, RF-07-01, ADR-02-01, ADR-07-01
    │       └── integration: DD-18-01 (arc stages), STD-15-01 (audit logging)
    │
    ├── DD-20-01 Evidence Standards ←──companion──→ STD-20-01 Citation Format
    │
    ├── RF-01-01 Backend Platform Evaluation (Area 01)
    │       ├── Evaluates: Convex, Supabase, Neon
    │       ├── Recommends: Convex (TypeScript-native, @convex-dev/agent)
    │       └── ADR-01-01 Backend Selection ← formalizes decision
    │
    ├── RF-02-01 LLM Orchestration Evaluation (Area 02)
    │       ├── Evaluates: Mastra, Vercel AI SDK, LangGraph.js, Instructor
    │       ├── Recommends: Mastra + Vercel AI SDK v6
    │       └── ADR-02-01 Orchestration Selection ← formalizes decision
    │
    ├── RF-03-01 Memory & Retrieval Evaluation (Area 03)
    │       ├── Evaluates: Convex @convex-dev/rag, Zep, Supermemory, Mem0
    │       └── Recommends: Convex-primary (ADR pending)
    │
    ├── RF-04-01 Documentation Platform Evaluation (Area 04)
    │       ├── Evaluates: Obsidian, GitBook, VS Code/Foam, Mintlify, Notion
    │       ├── Recommends: Obsidian with Git
    │       └── ADR-04-01 Documentation Selection ← formalizes decision
    │
    ├── RF-07-01 Widget Libraries Evaluation (Area 07)
    │       ├── Evaluates: Thesys C1, CopilotKit, shadcn/ui, SurveyJS
    │       ├── Recommends: Thesys C1 + shadcn/ui hybrid
    │       └── ADR-07-01 Widget Selection ← formalizes decision
    │
    ├── RF-08-01 Frontend Hosting Evaluation (Area 08)
    │       ├── Evaluates: Vercel, Cloudflare Pages, Netlify, Railway
    │       ├── Recommends: Vercel
    │       └── ADR-08-01 Hosting Selection ← formalizes decision
    │
    └── RF-09-01 LLM Provider Evaluation (Area 09)
            ├── Evaluates: Claude 4.5, GPT-5.2, Gemini 3, Groq, Mistral
            ├── Recommends: Tiered strategy (Opus + Haiku)
            └── ADR-09-01 LLM Provider Selection ← formalizes decision
```

---

## Section Maps

### Compass System Definition

The authoritative specification. **Read first** before any research or planning.

| Part | Sections | Key Content |
|------|----------|-------------|
| **Part 1: Vision** | 1.1–1.8 | Core problem, what Compass is/isn't, ecosystem philosophy, core promises, guiding principles, critical junctions |
| **Part 2: Functional** | 2.1–2.7 | Planning workflow (OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND), widgets, research integration, documentation truth, decision records, branching, handoff bundles |
| **Part 3: Technical** | 3.1–3.8 | LLM conversation, memory layers, interface requirements, state management, versioning, integrations, performance, reliability |
| **Part 4: Constraints** | 4.1–4.6 | Budget ($600–$2000 initial), team capacity, security, privacy, vendor independence, timeline phases |
| **Part 5: Architecture** | 5.1–5.4 | Seven layers, mental diagram, open standards (MCP), reference patterns |
| **Appendix A** | Glossary | 30+ term definitions |

**Key references by topic:**

| Topic | Section | Key Point |
|-------|---------|-----------|
| What is Compass | 1.2 | LLM-orchestrated planning/research/documentation system |
| What Compass is NOT | 1.3 | Not code execution, deployment, PM replacement, or "chat that exports docs" |
| Spec permanence | 1.2 | "Specification is permanent; implementation is ephemeral" |
| Planning arc stages | 2.1 | OPEN (3–5 turns) → FOLLOW (10–20) → SHARPEN (5–8) → BOUNDARY (4–6) → GROUND (3–5) |
| Widget types | 2.2 | Choice, spectrum, comparative, spatial, generative, meta widgets |
| Widget guarantees | 2.2 | Every widget must have: escape hatch, help, research trigger |
| Research types | 2.3 | Technical, domain, contextual |
| Memory layers | 3.2 | Session, project (cross-session), ecosystem (cross-project) |
| Core entities | 3.2 | Project, Artifact, Decision, Branch, Workflow run, Citation, Profile, Adapter |
| Truth hierarchy | 3.2 | Intent truth → Execution truth → Audit truth |
| Audit log schema | — | STD-15-01 § Part 1 (JSON schema for governance audit events) |
| Budget | 4.1 | $600–$2000/year initial; $3000–$5000 proven value |
| Architecture layers | 5.1 | Interaction → Authoritative State → Artifact Store → Memory → Evidence → Integration → Execution |

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
| Area codes (01–20) | Part 3.2 |
| Branch naming pattern | `docs/{type}/{topic}` (Part 5.2) |
| PR template | Part 5.4 |
| AGENTS.md content | Part 7.2 |

---

### DD-13-01: Artifact Taxonomy

| Part | Key Content |
|------|-------------|
| **Part 1: Type Catalog** | 8 artifact types: SPEC, ADR, RB, RF, DD, STD, HANDOFF, IDX |
| **Part 2: Frontmatter** | Universal fields (required), type-specific fields, validation rules |
| **Part 3: Lifecycle** | Four states: draft → review → active → deprecated; transition rules |
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
| **Part 4: Compliance Levels** | Level 1 (non-negotiable) → Level 4 (desired within 90 days) |

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
| **Part 1: Evidence Grading** | Three dimensions: Source Reliability (S1–S4), Information Quality (I1–I4), Confidence (High/Medium/Low) |
| **Part 2: Source Classification** | Five-tier taxonomy: T1 Authoritative → T5 Unverified |
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
| Technical blogs | 6–12 months |
| Stack Overflow | High skepticism always |

---

### STD-20-01: Citation Format Specification

| Part | Key Content |
|------|-------------|
| **Part 1: Format Spec** | Required fields, recommended fields, source_type enum, tier/reliability values |
| **Part 2: JSON Schema** | Citation object schema, full evidence artifact schema |
| **Part 3: In-Document Format** | Inline citations, source list format, tier prefix |
| **Part 4: Examples** | Correct citations for T1–T5 sources, version-specific citations |
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
| Planner | Primary users | Full planning access | 2–3 |
| Contributor | Domain experts | Propose but not approve | 0–5 |
| Viewer | Stakeholders | Read-only | 10–50 |
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
User Action → Mutation (saves intent) → Scheduler → Action (calls external API)
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

### DD-18-01: Questioning Arc Definition

| Part | Key Content |
|------|-------------|
| **Part 1: Five-Stage Workflow** | Stage overview diagram, stage definitions (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND), turn counts |
| **Part 2: Stage Transitions** | Explicit triggers, backward movement, convergence signals |
| **Part 3: Research Branching** | Branch types (research, exploration), suspension points, branch lifecycle |
| **Part 4: Merge Gates** | Checkpoint protocol, four resolution options, state mutation rules |
| **Part 5: Document Integrations** | Widget system (DD-19-01), artifact system (DD-13-01), governance (DD-15-01), orchestration (ADR-02-01) |
| **Part 6: Example Flows** | New internal tool, research-heavy planning, exploration branch scenarios |
| **Part 7: Implementation Guidance** | Stage patterns, transition triggers, merge gate implementation, degraded operation |
| **Appendix A** | Glossary (convergence signal, escape hatch, exploration branch, merge gate, etc.) |
| **Appendix B** | Related documents |

**Stage quick reference:**

| Stage | Purpose | Typical Turns | Exit Conditions |
|-------|---------|---------------|-----------------|
| OPEN | Extract fuzzy idea, establish starting point | 3–5 | Core problem articulated, user type identified |
| FOLLOW | Expand, discover requirements and use cases | 10–20 | Major use cases identified, diminishing returns |
| SHARPEN | Prioritize, force trade-offs | 5–8 | Requirements prioritized, trade-offs decided |
| BOUNDARY | Define out-of-scope, prevent creep | 4–6 | Explicit exclusions, user confirmation |
| GROUND | Apply hard constraints | 3–5 | Budget, reliability, security, timeline specified |

**Branching patterns:**

| Branch Type | When Used | Returns Via |
|-------------|-----------|-------------|
| Research branch | Uncertainty blocks progress | Merge gate with findings |
| Exploration branch | Multiple viable paths | Merge gate with comparison |

**Orchestration mapping (ADR-02-01):**

| Arc Concept | Mastra Implementation |
|-------------|----------------------|
| Arc stages | Workflow steps |
| Stage transitions | Step transitions with conditional branching |
| Research branches | Parallel workflow paths |
| Merge gates | `suspend()` with human-in-the-loop resume |
| State persistence | Thread-based memory with PostgreSQL |

---

### STD-18-01: Questioning Arc Standards

| Part | Key Content |
|------|-------------|
| **Part 1: Stage Completion Criteria** | Required elements, conversation minimums, exit validation for each stage |
| **Part 2: Transition Standards** | Forward requirements (hard/soft), backward allowances, branch requirements |
| **Part 3: Merge Gate Standards** | Required elements, resolution logging, reminder schedules |
| **Part 4: State Management Standards** | Save triggers, resume validation, schema versioning, isolation |
| **Part 5: Quality Metrics** | Project-level metrics, system-level metrics, health thresholds |
| **Part 6: Error Handling Standards** | Validation error presentation, recovery procedures, graceful degradation |
| **Part 7: Implementation Checklists** | Stage implementation, merge gate implementation, state management |
| **Part 8: Exception Handling** | Emergency bypass, incomplete arc closure, arc reset |
| **Appendix A** | Validation rule reference (OPEN-001 through BRANCH-006) |
| **Appendix B** | Related documents |

**Validation severity levels:**

| Severity | Behavior |
|----------|----------|
| Block | Cannot proceed until resolved |
| Warn | Flagged but can proceed |

**Key validation rules:**

| Rule ID | Stage | Rule | Severity |
|---------|-------|------|----------|
| OPEN-001 | OPEN | Problem statement ≥ 20 chars | Block |
| OPEN-002 | OPEN | At least 1 user type identified | Block |
| FOLLOW-001 | FOLLOW | At least 3 requirements captured | Block |
| SHARPEN-001 | SHARPEN | All requirements prioritized | Block |
| BOUNDARY-001 | BOUNDARY | At least 1 explicit exclusion | Block |
| GROUND-001 | GROUND | Budget constraint specified | Block |

**Quality metric thresholds:**

| Metric | Healthy | Warning |
|--------|---------|---------|
| Stage completion rate | > 80% | ≤ 80% |
| Backward transition rate | < 25% | ≥ 25% |
| Research branch closure | > 75% | ≤ 75% |
| Merge gate resolution | < 48 hours | ≥ 48 hours |

---

### DD-19-01: Widget Schema and Rendering Specification

| Part | Key Content |
|------|-------------|
| **Part 1: Widget Type Enumeration** | Complete registry of 18 widget types, category definitions (Choice, Spectrum, Comparative, Spatial, Generative, Meta) |
| **Part 2: Common Schema Fields** | Required fields (type, id, prompt, required), optional fields (helpText, escapeHatch, helpMeThink, researchTrigger, meta) |
| **Parts 3–10: Type-Specific Schemas** | Detailed JSON schemas for each widget type with field definitions |
| **Part 11: Response Schema** | WidgetResponse object structure, per-type response formats |
| **Part 12: LLM Generation Guidelines** | Prompt template pattern, Zod integration, common errors, validation feedback loop |
| **Part 13: Integration Notes** | Orchestration (Mastra), components (C1/shadcn), questioning arc (DD-18-01) |
| **Appendix A** | Complete schema reference with shared definitions |
| **Appendix B** | Glossary (C1, dnd-kit, escape hatch, JSON Schema, meta widget, etc.) |
| **Appendix C** | Related documents |

**Widget type registry:**

| Type Identifier | Category | Rendering |
|-----------------|----------|-----------|
| `single-select` | Choice | C1 native |
| `multi-select` | Choice | C1 native |
| `ranked-choice` | Choice | Custom |
| `pairwise-comparison` | Choice | Custom |
| `slider` | Spectrum | C1 native |
| `opposing-spectrum` | Spectrum | Custom |
| `allocation` | Spectrum | Custom |
| `tradeoff-table` | Comparative | Custom |
| `ab-comparison` | Comparative | C1 native |
| `card-sort` | Spatial | Custom |
| `sequencer` | Spatial | Custom |
| `quadrant` | Spatial | Custom |
| `madlib` | Generative | C1 native |
| `structured-fields` | Generative | C1 native |
| `decision-gate` | Meta | C1 native |
| `boundary-checklist` | Meta | C1 native |
| `research-trigger` | Meta | C1 native |
| `merge-gate` | Meta | Custom |

**UX guarantee fields (per System Definition § 2.2):**

| Field | Default Behavior | Override |
|-------|------------------|----------|
| `escapeHatch` | "None of these fit / I'll describe instead" | `enabled: false` to disable |
| `helpMeThink` | "Help me think about this" | Custom `content` |
| `researchTrigger` | "Research this" | Custom `defaultBrief` |

---

### STD-19-01: Widget Schema Standards

| Part | Key Content |
|------|-------------|
| **Part 1: Required Fields Checklist** | Identity fields, content fields, UX guarantee fields, type-specific required fields |
| **Part 2: Interaction Logging Requirements** | Mandatory events (presented, submitted), recommended events, required event fields, payloads |
| **Part 3: Schema Validation Rules** | Strict mode, value uniqueness, reference validity, constraint coherence |
| **Part 4: Content Validation** | Minimum option counts, duplicate detection, semantic validation |
| **Part 5: Testing Requirements** | Schema validation tests, response handling tests, logging compliance tests, integration tests |
| **Part 6: Quality Standards** | Prompt clarity, option distinctness, help content quality |
| **Part 7: Error Handling** | Validation error messages, recovery procedures, escalation |
| **Appendix A** | Quick reference tables (required fields by type, mandatory events, validation order) |
| **Appendix B** | Glossary |
| **Appendix C** | Related documents |

**Required fields by widget type:**

| Widget Type | Type-Specific Required Fields |
|-------------|-------------------------------|
| `single-select` | `options` (min 2) |
| `multi-select` | `options` (min 2) |
| `ranked-choice` | `items` (min 3) |
| `pairwise-comparison` | `items` (min 3) |
| `slider` | `min`, `max`, `labels` |
| `opposing-spectrum` | `poles` |
| `allocation` | `categories` (min 2) |
| `tradeoff-table` | `options` (min 2), `criteria` (min 2) |
| `ab-comparison` | `optionA`, `optionB` |
| `card-sort` | `cards` (min 3), `categories` (min 2) |
| `sequencer` | `items` (min 2) |
| `quadrant` | `items` (min 2), `axes` |
| `madlib` | `template`, `slots` (min 1) |
| `structured-fields` | `fields` (min 1) |
| `decision-gate` | (none beyond common) |
| `boundary-checklist` | `checklistType`, `items` (min 1) |
| `research-trigger` | `researchQuestion` |
| `merge-gate` | `branchType`, `branchSummary`, `proposedChanges` |

**Mandatory logging events:**

| Event | When Logged | Required Payload |
|-------|-------------|------------------|
| `widget.presented` | Widget renders | Full widget specification |
| `widget.submitted` | User submits response | Full WidgetResponse object |

**Validation priority order:**

1. Schema validation (type exists, required fields, types correct)
2. Strict mode (no extra properties)
3. Value uniqueness
4. Reference validity
5. Constraint coherence
6. Content quality

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
| **Reversibility** | Moderate—abstraction layers enable future migration if needed |

**Decision summary**: Convex is selected because the team has no SQL familiarity and relies on LLM coding agents. Convex's TypeScript-native approach and @convex-dev/agent component provide the lowest implementation complexity for an LLM-orchestrated system.

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
| **Consequences** | Positive (2–3 week integration vs 6–10 week custom), Negative (young framework risk) |

**Decision summary**: Implement two-layer architecture combining Mastra for workflow orchestration (suspend/resume, thread-based memory) and Vercel AI SDK v6 for structured output generation and provider abstraction. LangGraph.js excluded due to TypeScript quality issues affecting widget generation reliability.

---

### RF-03-01: Memory & Retrieval Evaluation

RF-03-01 evaluates memory and retrieval solutions for Compass with emphasis on Convex integration and the three-layer memory model.

| Part | Key Content |
|------|-------------|
| **Part 1: Requirements** | Three memory layers (session, project, ecosystem), temporal awareness, Convex integration |
| **Part 2: Convex @convex-dev/rag** | Built-in vector search, namespace isolation, hybrid search, $0–25/month |
| **Part 3: Zep Graphiti** | Bi-temporal knowledge graphs, entity relationships, $40–70/month self-hosted |
| **Part 4: Supermemory** | MCP integration, sub-400ms latency, $19–99/month |
| **Part 5: Mem0** | Session isolation, change history, $249/month |
| **Part 6: Recommendation** | Convex-primary architecture; external services optional for complex temporal queries |

**Solution summary:**

| Solution | Category | Key Strength | Cost | Status |
|----------|----------|--------------|------|--------|
| **Convex @convex-dev/rag** | Built-in | Native integration, namespace isolation | $0–25/month | **Recommended** |
| Zep Graphiti | External | Bi-temporal graphs, entity relationships | $40–70/month | Phase 3 option |
| Supermemory | External | MCP integration, sub-400ms latency | $19–99/month | Phase 3 option |
| Mem0 | External | Session isolation, change history | $249/month | Not recommended |

**Recommendation**: Convex-primary with @convex-dev/rag — Built-in capabilities satisfy requirements. External services (Zep, Supermemory) reserved for Phase 3 if bi-temporal or MCP requirements emerge. ADR pending.

---

### RF-04-01: Documentation Platform Evaluation

RF-04-01 evaluates documentation platforms for Compass against requirements for YAML frontmatter, Git integration, backlinks, and LLM retrieval.

| Part | Key Content |
|------|-------------|
| **Part 1: Capability Matrix** | Full comparison of Obsidian, VS Code/Foam, GitBook, Mintlify, Outline, Notion, Docusaurus |
| **Part 2: Format Compatibility** | YAML frontmatter handling, naming convention support |
| **Part 3: Candidate Analysis** | Per-platform strengths and limitations |
| **Part 4: LLM Integration** | MCP server availability, llms.txt support |
| **Part 5: Collaboration** | Real-time vs async, Git integration patterns |
| **Part 6: Cost Analysis** | Pricing comparison |
| **Part 7: Recommendation** | Obsidian with Git |

**Platform summary:**

| Platform | Key Strength | Key Limitation | Cost |
|----------|--------------|----------------|------|
| **Obsidian + Git** | Perfect frontmatter, native backlinks, multiple MCP servers | No real-time collaboration | $0 |
| **GitBook** | Bidirectional Git sync, native llms.txt | May strip custom frontmatter in web editor | ~$30–95/month |
| **VS Code + Foam** | Most direct Git, real-time via Live Share | Requires VS Code familiarity | $0 |
| **Mintlify** | Excellent AI-native features | $300/month Pro tier—over budget | Excluded |

**Decision**: Obsidian with Git selected (see ADR-04-01)

**Key factors for Obsidian selection:**
- Perfect YAML frontmatter preservation with Properties View UI
- Native wiki-link syntax (`[[artifact-id]]`) and backlinks panel
- Built-in interactive graph visualization
- Multiple mature MCP servers (cyanheads/obsidian-mcp-server)
- Zero cost for core workflow
- Plain markdown files with zero vendor lock-in

**Accepted trade-offs:**
- No real-time collaborative editing (async via Git only)
- PR creation requires GitHub web interface
- Mobile sync has performance limitations on large vaults (1000+ files)

---

### ADR-04-01: Documentation Platform Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Documentation is primary Compass output; platform must support YAML frontmatter, Git, backlinks, MCP |
| **Options** | Obsidian + Git, GitBook, VS Code + Foam, Mintlify, Plain Markdown |
| **Decision** | **Obsidian with Git** |
| **Rationale** | Perfect frontmatter preservation, native backlinks, mature MCP servers, zero cost |
| **Consequences** | Positive (zero cost, full DD-12-01/DD-13-01 compatibility), Negative (no real-time editing) |
| **Reversibility** | High—plain markdown files transfer to any platform |

**Decision summary**: Obsidian with Git is selected because it uniquely satisfies all core Compass requirements while maintaining zero cost and zero vendor lock-in. The async-via-Git collaboration model is acceptable for a 2-3 person team.

**Implementation requirements:**
1. Create GitHub repository following DD-12-01 structure
2. Install Obsidian Git plugin with repository credentials
3. Install Local REST API plugin for MCP access
4. Configure cyanheads/obsidian-mcp-server for LLM agent integration
5. Create artifact templates per DD-13-01
6. Generate initial llms.txt per DD-12-01 Section 2.3

---

### RF-07-01: Widget Component Library Evaluation

RF-07-01 evaluates widget component approaches for Compass against the 16-widget taxonomy defined in System Definition § 2.2.

| Part | Key Content |
|------|-------------|
| **Part 1: Context and Scope** | Widget taxonomy mapping, evaluation criteria |
| **Part 2: Generative UI Paradigm Shift** | Traditional vs generative approaches, three rendering paradigms |
| **Part 3: Candidate Assessment** | Thesys C1, CopilotKit, Vercel AI SDK UI patterns, shadcn/ui + dnd-kit, SurveyJS |
| **Part 4: Taxonomy Coverage** | Widget-by-widget coverage analysis |
| **Part 5: Development Estimates** | Per-widget effort, total timeline |
| **Part 6: Cost Analysis** | C1 pricing tiers, projected monthly costs |
| **Part 7: Integration Patterns** | Mastra → C1 integration, custom component registration |
| **Part 8: Recommendation** | Thesys C1 + shadcn/ui hybrid architecture |
| **Part 9: Widget Schema Implications** | Guidance for Area 19 |
| **Part 10: Implementation Roadmap** | 6-7 week development plan |

**Critical insight**: No single library covers more than 50% of Compass's widget taxonomy natively. Every approach requires custom development for ranked choice, pairwise comparison, allocation, and spatial widgets. The question is which rendering paradigm best supports custom extension.

**Framework summary:**

| Framework | Category | Key Strength | Key Limitation |
|-----------|----------|--------------|----------------|
| **Thesys C1** | Generative UI | Native Mastra integration, streaming | New product (April 2025) |
| **shadcn/ui + dnd-kit** | Component primitives | Full control, LLM maintainability | No turnkey streaming |
| CopilotKit | Agent-driven | Open-source core, A2UI protocol | No native Mastra integration |
| SurveyJS | Survey library | Native ranked choice, matrix | Styling constraints, licensing costs |

**Decision**: Thesys C1 + shadcn/ui + dnd-kit hybrid selected (see ADR-07-01)

**Key factors for hybrid selection:**
- Thesys C1 provides native Mastra integration (eliminates glue code)
- Streaming generative UI reduces time-to-interactivity
- shadcn/ui + dnd-kit provides primitives for ~8 custom planning widgets
- Clear custom component registration pattern in C1

**Custom components required:**

| Widget | Implementation Approach | Estimated Effort |
|--------|------------------------|------------------|
| RankedChoice | shadcn Card + dnd-kit Sortable | 3-4 days |
| PairwiseComparison | shadcn Card + RadioGroup + state machine | 4-5 days |
| AllocationSlider | shadcn Slider + shared state + Zod refine | 3-4 days |
| OpposingSpectrum | shadcn Slider + custom labels | 1-2 days |
| TradeoffTable | shadcn DataTable + inline inputs | 3-4 days |
| CardSort | shadcn Card + dnd-kit multiple zones | 3-4 days |
| Sequencer | shadcn + dnd-kit Sortable | 2-3 days |
| QuadrantPlacer | Custom positioning + shadcn styling | 4-5 days |

**Development estimate**: 6-7 weeks for complete taxonomy coverage; basic functionality in Week 2.

---

### ADR-07-01: Widget Component Library Selection

| Section | Key Content |
|---------|-------------|
| **Context** | Compass widget taxonomy (16 types), Mastra orchestration, streaming requirements |
| **Options** | Thesys C1 + custom, CopilotKit + custom, shadcn/ui JSON registry, SurveyJS + custom |
| **Decision** | **Thesys C1 + shadcn/ui + dnd-kit hybrid** |
| **Rationale** | Native Mastra integration, streaming support, clear custom component pattern |
| **Consequences** | Positive (faster delivery, reduced maintenance), Negative (C1 vendor dependency) |
| **Reversibility** | Moderate—maintain abstraction layer; document fallback to pure shadcn/ui |

**Decision summary**: Implement hybrid widget architecture using Thesys C1 for conversational UI and standard interactions, with custom shadcn/ui + dnd-kit components for ~8 specialized planning widgets. C1's native Mastra integration eliminates orchestration glue code, while the custom component system provides an escape valve for Compass-specific requirements.

**Cost projection:**

| Phase | C1 Tier | C1 Cost | LLM Passthrough | Total Widget Layer |
|-------|---------|---------|-----------------|-------------------|
| Phase 1 | Build | $49 | ~$10-20 | ~$60-70/month |
| Phase 3 | Grow | $499 | ~$50-100 | ~$550-600/month |

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

**Decision summary**: Vercel selected for official Convex integration and deployment simplicity. Cloudflare Pages recommended as Phase 3 alternative if cost optimization becomes priority ($20/month flat vs $100–200/month at scale).

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

**Key insight**: Planning tasks require **frontier-level reasoning** to generate well-rounded choices—not just instruction following. Orchestration tasks require **reliable instruction following** for tool use.

**Critical exclusion**: Gemini 2.0 Flash ($0.10/$0.40) is **not recommended** despite low cost—weak instruction following and deprecated March 2026.

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
| **Reversibility** | Easy—abstraction layer isolates provider-specific code |

**Decision summary**: Implement tiered model strategy using Claude Opus 4.5 for planning tasks (frontier reasoning) and Claude Haiku 4.5 for orchestration (reliable instruction following). Gemini and OpenAI serve as fallbacks for redundancy.

**Why frontier models for planning**: Planning conversations require generating well-rounded options and anticipating user needs—this demands frontier reasoning, not just instruction following.

**Why mid-tier for orchestration**: Orchestration tasks (routing, tool calling) need reliable instruction following but not deep reasoning. Haiku 4.5 at $1/$5 provides reliability at 5× lower cost than Sonnet.

---

## Concept Index

Quick lookup for key terms. Format: **Term** → Document § Section

### A–C

- **Acceptance criteria** → System Definition § 2.7 (handoff bundle contents)
- **ADR (Architecture Decision Record)** → DD-13-01 § 1.2
- **Agent component (@convex-dev/agent)** → RF-01-01 § 2.1; ADR-01-01 (built-in chat persistence, tool-based database access)
- **Agent (role)** → DD-15-01 § 1.2 (LLM agent acting on behalf of a user with scoped permissions)
- **Agent Pack** → System Definition § Appendix A
- **Allocation widget** → DD-19-01 § Part 1 (distribute fixed budget across categories)
- **Archetype (tool)** → DD-14-01 § Part 1
- **Artifact** → DD-13-01 § Part 1; System Definition § Appendix A
- **Artifact store** → System Definition § 5.1 (Layer 3)
- **Audit truth** → System Definition § 3.2
- **Audit log schema** → STD-15-01 § Part 1 (JSON schema for governance audit events)
- **Backend platform** → RF-01-01; ADR-01-01 (Convex selected)
- **Backlinks** → RF-04-01 § 1.1; ADR-04-01 (wiki-link navigation in documentation)
- **Batch API** → RF-09-01 § Part 2 (50% discount for async processing)
- **BMAD** → System Definition § 5.4, Appendix A
- **BOUNDARY (stage)** → DD-18-01 § 1.2; STD-18-01 § 1.4 (define out-of-scope, prevent creep)
- **Boundaries (always/ask first/never)** → DD-13-01 § 4.1, 6.1 template
- **Branch** → System Definition § 2.6; DD-13-01 § Appendix A
- **Broadcast-Critical** → DD-14-01 § 1.2; STD-14-01 § 1.1
- **Budget** → System Definition § 4.1 ($600–$2000 initial)
- **C1 (Thesys)** → RF-07-01; ADR-07-01 (generative UI API for widget rendering)
- **Canonical ID** → DD-12-01 § 4.2
- **Card sort widget** → DD-19-01 § Part 1 (organize items into categories)
- **Citation** → DD-20-01 § Part 3; STD-20-01 § Parts 1–4
- **Claude 4.5** → RF-09-01 § 2.1; ADR-09-01 (Opus for planning, Haiku for orchestration)
- **Compliance levels** → STD-14-01 § Part 4
- **Confidence levels** → DD-20-01 § 1.4
- **Convergence signal** → DD-18-01 § Appendix A (indication that stage is approaching completion)
- **Convex** → RF-01-01 § 2.1; ADR-01-01 (selected backend: TypeScript-native, document-relational)
- **@convex-dev/rag** → RF-03-01 § Part 2 (Convex component for vector search and retrieval)
- **CopilotKit** → RF-07-01 § 3.2 (alternative agent-driven UI framework)
- **CQRS** → RF-01-01 § Appendix B (Command Query Responsibility Segregation—queries/mutations separation)
- **Crayon SDK** → RF-07-01 (Thesys React SDK for rendering C1 UI specifications)

### D–G

- **Database branching** → RF-01-01 § 2.3 (Neon: instant branching for LLM sandboxing)
- **Decision gate widget** → DD-19-01 § Part 1 (checkpoint requiring explicit decision)
- **Decision ledger** → System Definition § 2.5
- **Decision record** → DD-13-01 § 1.2 (ADR)
- **Definition Document (DD-)** → DD-13-01 § 1.2
- **Definition of Done** → DD-13-01 § Part 4
- **Delta (implementation)** → DD-13-01 § 5.1
- **Deprecated (status)** → DD-13-01 § 3.2
- **dnd-kit** → RF-07-01 § 5.3; ADR-07-01 (drag-and-drop library for custom widgets)
- **Documentation platform** → RF-04-01; ADR-04-01 (Obsidian + Git selected)
- **Document-relational model** → RF-01-01 § 2.1 (Convex: JSON-like nested objects with relational tables)
- **Ecosystem philosophy** → System Definition § 1.4
- **Error handling standard** → DD-14-01 § 3.4; STD-14-01 § 2.5
- **Escape hatch** → System Definition § 2.2; DD-19-01 § 2.2; STD-19-01 § 1.3 (widget option when none fit)
- **Evidence artifact** → DD-20-01 § 5.1
- **Evidence grading** → DD-20-01 § Part 1
- **Execution truth** → System Definition § 3.2
- **Exit conditions** → DD-18-01 § 1.2; STD-18-01 § Part 1 (what must be true to leave a stage)
- **Exploration branch** → DD-18-01 § 3.1; Appendix A (parallel planning path for alternatives)
- **Foam** → RF-04-01 § 3.2 (VS Code extension for wiki-links and backlinks)
- **FOLLOW (stage)** → DD-18-01 § 1.2; STD-18-01 § 1.2 (expand, discover requirements)
- **Freshness** → DD-20-01 § Part 4
- **Frontier reasoning** → RF-09-01 § 6.1; ADR-09-01 (planning tasks require deep reasoning, not just instruction following)
- **Frontmatter** → DD-13-01 § Part 2
- **Gemini** → RF-09-01 § 2.3 (Google: Gemini 3 Pro for planning fallback, 2.5 Flash for orchestration)
- **Generative UI** → RF-07-01 § Part 2 (LLM describes UI intent; rendering layer interprets)
- **GitHub Flow** → DD-12-01 § 5.1
- **GitBook** → RF-04-01 § 3.3; ADR-04-01 (alternative documentation platform)
- **GPT-5** → RF-09-01 § 2.2 (OpenAI: GPT-5.2 for planning fallback, GPT-5 Mini for orchestration)
- **Graph visualization** → RF-04-01 § 1.1 (Obsidian built-in feature for document relationships)
- **GROUND (stage)** → DD-18-01 § 1.2; STD-18-01 § 1.5 (apply hard constraints)
- **GSD** → System Definition § 1.3, Appendix A

### H–M

- **Handoff bundle** → System Definition § 2.7; DD-13-01 § 1.2
- **HANDOFF- prefix** → DD-13-01 § 1.2
- **Help me think** → DD-19-01 § 2.2; STD-19-01 § 1.3 (widget support feature)
- **Hybrid strategy (LLM)** → RF-09-01 § 6; ADR-09-01 (different models for different task types)
- **Idempotency** → DD-17-01 § Part 2 (processing same operation multiple times yields same result)
- **IDX- prefix** → DD-13-01 § 1.2
- **Index document** → DD-13-01 § 1.2; DD-12-01 § 2.4
- **Information quality (I1–I4)** → DD-20-01 § 1.3
- **Instruction following** → RF-09-01 § 4.2 (critical for orchestration tasks; weak in Gemini 2.0 Flash, GPT-5 Nano)
- **Integration patterns** → DD-14-01 § 4.4
- **Integration patterns (detailed)** → DD-17-01 (webhooks, retries, error handling, secret management)
- **Intent truth** → System Definition § 3.2
- **Interaction logging** → DD-19-01 § Part 11; STD-19-01 § Part 2 (widget event logging)
- **Lifecycle states** → DD-13-01 § Part 3 (draft/review/active/deprecated)
- **llms.txt** → DD-12-01 § 2.3; RF-01-01 (LLM navigation index)
- **LLM maintainability** → RF-01-01 (evaluation criterion: how well AI assistants generate correct code)
- **LLM provider** → RF-09-01; ADR-09-01 (Claude primary, Gemini/OpenAI fallback)
- **Logging standard** → DD-14-01 § 3.3; STD-14-01 § 2.3
- **MCP (Model Context Protocol)** → System Definition § 5.3; RF-01-01; RF-04-01 § Part 4 (LLM tool integration standard)
- **Memory layers** → System Definition § 3.2 (session, project, ecosystem)
- **Merge gate** → DD-18-01 § Part 4; STD-18-01 § Part 3; DD-19-01 (checkpoint for branch proposals)
- **Meta widget** → DD-19-01 § 1.2 (workflow control, not content capture)
- **Model router** → RF-09-01 § 5; ADR-09-01 (task classification → model selection)
- **Mastra** → RF-02-01; ADR-02-01 (selected workflow orchestration framework with suspend/resume)

### N–R

- **Naming conventions** → DD-12-01 § Part 3
- **Neon** → RF-01-01 § 2.3 (serverless PostgreSQL, database branching, database-only service)
- **Obsidian** → RF-04-01; ADR-04-01 (selected documentation platform)
- **Obsidian Git plugin** → RF-04-01 § 3.1 (Git integration for Obsidian)
- **OPEN (stage)** → DD-18-01 § 1.2; STD-18-01 § 1.1 (extract fuzzy idea, establish starting point)
- **Owner (role)** → DD-15-01 § 1.2 (system administrator with full access)
- **Pairwise comparison widget** → DD-19-01 § Part 1 (compare two options repeatedly)
- **Planner (role)** → DD-15-01 § 1.2 (primary user running full planning workflow)
- **pgvector** → RF-01-01 § 2.2, 2.3 (PostgreSQL vector search extension)
- **Planning arc** → System Definition § 2.1 (OPEN→FOLLOW→SHARPEN→BOUNDARY→GROUND)
- **Pristine context** → System Definition § 5.1 (Layer 5)
- **Privacy profiles** → DD-14-01 § 2.3
- **Production Pipeline** → DD-14-01 § 1.2; STD-14-01 § 1.2
- **Prompt caching** → RF-09-01 § 2.1 (up to 90% savings on repeated context)
- **Quadrant widget** → DD-19-01 § Part 1 (place items on 2D grid with labeled axes)
- **Questioning arc** → System Definition § 2.1; DD-18-01 (five-stage workflow)
- **Questioning arc standards** → STD-18-01 (validation rules, completion criteria)
- **RB- (Research Brief)** → DD-13-01 § 1.2
- **Ranked choice widget** → DD-19-01 § Part 1 (order options by preference)
- **Real-time collaboration** → RF-01-01 § 2.1 (Convex: automatic reactivity without WebSocket config)
- **Reconciliation** → DD-13-01 § Part 5
- **Reliability tier** → DD-14-01 § 2.1
- **Research branch** → DD-18-01 § Part 3 (temporary divergence to investigate uncertainty)
- **Research Brief** → DD-13-01 § 1.2
- **Research Finding** → DD-13-01 § 1.2; DD-20-01 § Part 6
- **Research trigger** → DD-19-01 § 2.2; STD-19-01 § 1.3 (widget action to spawn research branch)
- **RF- prefix** → DD-13-01 § 1.2
- **RLS (Row Level Security)** → RF-01-01 § 2.2 (Supabase: fine-grained access control)

### S–Z

- **Secret management** → DD-17-01 § Part 6; STD-17-01 § Part 1 (environment variables, rotation, access control)
- **Sequencer widget** → DD-19-01 § Part 1 (arrange items in order)
- **Serializable isolation** → RF-01-01 § Appendix B (strictest ACID level; Convex default—prevents partial writes)
- **shadcn/ui** → RF-07-01 § 5.3; ADR-07-01 (component primitives for custom widgets)
- **SHARPEN (stage)** → DD-18-01 § 1.2; STD-18-01 § 1.3 (prioritize, force trade-offs)
- **Source reliability (S1–S4)** → DD-20-01 § 1.2
- **Source tier (T1–T5)** → DD-20-01 § 2.1
- **Spec permanence principle** → System Definition § 1.2
- **Sponsor (agent)** → DD-15-01 § Part 3 (human user responsible for agent actions)
- **SPEC- prefix** → DD-13-01 § 1.2
- **Specification** → DD-13-01 § 1.2
- **SSO (Single Sign-On)** → RF-01-01 § 2.2 (Supabase: SAML 2.0 on Pro plan)
- **Stage** → DD-18-01 § Appendix A (one of five phases of questioning arc)
- **Stage completion criteria** → STD-18-01 § Part 1 (validation rules for stage transitions)
- **Staleness** → DD-20-01 § 4.2
- **Standard (STD-)** → DD-13-01 § 1.2
- **STD- prefix** → DD-13-01 § 1.2
- **Supabase** → RF-01-01 § 2.2 (PostgreSQL BaaS, RLS security, alternative to Convex)
- **Supersede** → DD-13-01 § 5.3
- **Suspension point** → DD-18-01 § Appendix A (natural pause point where arc state is serialized)
- **Structured output** → RF-02-01 § 2.1 (schema-constrained JSON generation from LLMs)
- **Thesys C1** → RF-07-01; ADR-07-01 (selected generative UI platform for widget rendering)
- **Tiered model strategy** → RF-09-01 § 6; ADR-09-01 (frontier for planning, mid-tier for orchestration)
- **Timeline phases** → System Definition § 4.6 (Phases 1–5)
- **Token usage** → RF-09-01 § 1 (Phase 1: ~5.2M/mo, Phase 3: ~20.8M/mo)
- **Tradeoff table widget** → DD-19-01 § Part 1 (evaluate options against criteria)
- **Transition triggers** → DD-18-01 § 7.2; STD-18-01 § Part 2 (forward, backward, branch)
- **Truth hierarchy** → System Definition § 3.2
- **TypeScript-native** → RF-01-01 § 2.1; ADR-01-01 (Convex: eliminates SQL context-switching)
- **UX guarantees (widget)** → DD-19-01 § 2.2; STD-19-01 § 1.3 (escape hatch, help, research trigger)
- **Validation rules** → STD-18-01 § Appendix A; STD-19-01 § Part 3 (schema and semantic validation)
- **Vendor independence** → System Definition § 4.5; RF-01-01 § 3.5 (Convex accepted trade-off with mitigations)
- **Vendor lock-in** → RF-01-01 § 3.5 (Convex: proprietary model; mitigated by abstractions)
- **Vercel** → RF-08-01; ADR-08-01 (selected frontend hosting platform)
- **Vercel AI SDK v6** → RF-02-01; ADR-02-01 (selected LLM abstraction layer for structured output)
- **Widget response** → DD-19-01 § Part 11; STD-19-01 (structured object capturing user interaction)
- **Widget schema** → DD-19-01 (JSON schemas for widget specifications)
- **Widget specification** → DD-19-01 § Part 2 (JSON object defining widget configuration)
- **Widget taxonomy** → System Definition § 2.2; RF-07-01; DD-19-01 § Part 1 (18 widget types across 6 categories)
- **Widget Wrapper** → RF-07-01 § 9.1 (component adding UX guarantees to all widgets)
- **Wiki-links** → RF-04-01 § 1.1 (Obsidian: `[[artifact-id]]` linking syntax)
- **Workflow run** → System Definition § 3.2
- **Working memory** → DD-18-01 § Appendix A (accumulated decisions persisted across sessions)
- **Zod** → DD-19-01 § 12.2 (TypeScript-first schema validation for widget generation)

---

## Cross-Reference Tables

### Where to Find Specific Guidance

| I need to... | Go to |
|--------------|-------|
| Understand what Compass is | System Definition § 1.2–1.3 |
| Plan a new feature | System Definition § 2.1–2.7 |
| Create a specification | DD-13-01 § 6.1 (template) |
| Record an architecture decision | DD-13-01 § 6.2 (ADR template) |
| Conduct research | DD-20-01, STD-20-01 |
| Write a research finding | DD-13-01 § 6.3 (template), DD-20-01 § Part 6 |
| Classify a new EFN tool | DD-14-01 § Part 5 (flowchart) |
| Check compliance for a tool | STD-14-01 § Part 1 (checklists) |
| Name a file | DD-12-01 § Part 3 |
| Structure a repository | DD-12-01 § Part 2 |
| Cite a source properly | STD-20-01 § Parts 3–4 |
| Evaluate source quality | DD-20-01 § Parts 1–2 |
| Understand lifecycle states | DD-13-01 § Part 3 |
| Handle spec/implementation divergence | DD-13-01 § Part 5 |
| Set up git workflow | DD-12-01 § Part 5 |
| **Choose a backend platform** | RF-01-01, ADR-01-01 |
| **Choose an LLM provider** | RF-09-01, ADR-09-01 |
| **Understand model tier strategy** | RF-09-01 § 6, ADR-09-01 |
| **Evaluate LLM costs** | RF-09-01 § Part 3 |
| **Set up documentation platform** | RF-04-01, ADR-04-01 |
| **Configure Obsidian for Compass** | RF-04-01 § Part 7, ADR-04-01 |
| **Select widget library** | RF-07-01, ADR-07-01 |
| **Build custom widgets** | RF-07-01 § Parts 5, 7, 10; ADR-07-01 |
| **Understand questioning arc stages** | DD-18-01 § Part 1 |
| **Implement arc stage transitions** | DD-18-01 § Part 2, STD-18-01 § Part 2 |
| **Implement research branching** | DD-18-01 § Part 3, STD-18-01 § 2.3 |
| **Implement merge gates** | DD-18-01 § Part 4, STD-18-01 § Part 3 |
| **Define widget JSON schemas** | DD-19-01 § Parts 2–10 |
| **Implement widget logging** | DD-19-01 § Part 11, STD-19-01 § Part 2 |
| **Validate widget specifications** | STD-19-01 § Parts 3–4 |
| **Generate widgets via LLM** | DD-19-01 § Part 12 |

### Document Pairs (Definition + Standard)

| Definition | Standard | Topic |
|------------|----------|-------|
| DD-14-01 | STD-14-01 | EFN tool requirements |
| DD-15-01 | STD-15-01 | Governance and audit |
| DD-17-01 | STD-17-01 | Integration patterns |
| DD-18-01 | STD-18-01 | Questioning arc workflow |
| DD-19-01 | STD-19-01 | Widget schemas |
| DD-20-01 | STD-20-01 | Evidence/citations |

**Pattern**: DD documents explain *why* and *what*; STD documents provide *enforceable rules* and *checklists*.

### Research + Decision Pairs

| Research Finding | ADR | Topic | Decision |
|------------------|-----|-------|----------|
| RF-01-01 | ADR-01-01 | Backend Platform | Convex |
| RF-02-01 | ADR-02-01 | LLM Orchestration | Mastra + Vercel AI SDK v6 |
| RF-03-01 | *(pending)* | Memory & Retrieval | Convex-primary (recommended) |
| RF-04-01 | ADR-04-01 | Documentation Platform | Obsidian + Git |
| RF-07-01 | ADR-07-01 | Widget Libraries | Thesys C1 + shadcn/ui |
| RF-08-01 | ADR-08-01 | Frontend Hosting | Vercel |
| RF-09-01 | ADR-09-01 | LLM Provider | Claude (tiered: Opus + Haiku) |

**Pattern**: RF documents provide research and analysis; ADR documents formalize the decision with rationale and consequences.

### Required Reading by Task

| Task | Must Read | Reference As Needed |
|------|-----------|---------------------|
| First-time orientation | System Definition (full) | — |
| Planning new feature | System Definition § 2, DD-13-01 | DD-12-01 |
| Conducting research | DD-20-01, STD-20-01 | DD-13-01 § 6.3 |
| Classifying EFN tool | DD-14-01 | STD-14-01 |
| Creating any artifact | DD-13-01 | DD-12-01 |
| Setting up repository | DD-12-01 | DD-13-01 |
| **Implementing backend** | RF-01-01, ADR-01-01 | System Definition § 4 |
| **Implementing LLM layer** | RF-09-01, ADR-09-01 | System Definition § 3 |
| **Implementing orchestration** | RF-02-01, ADR-02-01 | RF-09-01 |
| **Implementing memory** | RF-03-01 | ADR-01-01 |
| **Setting up documentation** | RF-04-01, ADR-04-01 | DD-12-01, DD-13-01 |
| **Deploying frontend** | RF-08-01, ADR-08-01 | ADR-01-01 |
| **Building widgets** | RF-07-01, ADR-07-01, DD-19-01 | System Definition § 2.2, ADR-02-01 |
| **Implementing questioning arc** | DD-18-01, STD-18-01 | ADR-02-01, DD-15-01 |
| **Building integrations** | DD-17-01, STD-17-01 | DD-14-01 |
| **Setting up governance** | DD-15-01, STD-15-01 | — |

---

## Quick Lookup Tables

### Artifact Prefixes → Types

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

### Architecture Layers (System Definition § 5.1)

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

| Stage | Purpose | Typical Turns | Key Documents |
|-------|---------|---------------|---------------|
| OPEN | Extract fuzzy idea, motivations, outcomes | 3–5 | DD-18-01 § 1.2, STD-18-01 § 1.1 |
| FOLLOW | Expand, discover requirements, gather signals | 10–20 | DD-18-01 § 1.2, STD-18-01 § 1.2 |
| SHARPEN | Prioritize, force trade-offs, reveal priorities | 5–8 | DD-18-01 § 1.2, STD-18-01 § 1.3 |
| BOUNDARY | Define out-of-scope, prevent scope creep | 4–6 | DD-18-01 § 1.2, STD-18-01 § 1.4 |
| GROUND | Apply hard constraints (budget, security, timeline) | 3–5 | DD-18-01 § 1.2, STD-18-01 § 1.5 |

### Widget Categories

| Category | Purpose | Widget Types |
|----------|---------|--------------|
| Choice | Evaluate and select from options | single-select, multi-select, ranked-choice, pairwise-comparison |
| Spectrum | Express degree or magnitude | slider, opposing-spectrum, allocation |
| Comparative | Make trade-offs explicit | tradeoff-table, ab-comparison |
| Spatial | Organize and sequence | card-sort, sequencer, quadrant |
| Generative | Create structured content | madlib, structured-fields |
| Meta | Control workflow | decision-gate, boundary-checklist, research-trigger, merge-gate |

### Backend Platform Decision (RF-01-01, ADR-01-01)

| Platform | Type | Key Strength | Limitation | Status |
|----------|------|--------------|------------|--------|
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
| **Convex @convex-dev/rag** | Built-in | Native integration, namespace isolation | $0–25/month | **Recommended** |
| Zep Graphiti | External | Bi-temporal graphs, entity relationships | $40–70/month | Phase 3 option |
| Supermemory | External | MCP integration, sub-400ms latency | $19–99/month | Phase 3 option |
| Mem0 | External | Session isolation, change history | $249/month | Not recommended |

### Documentation Platform Decision (RF-04-01, ADR-04-01)

| Platform | Key Strength | Key Limitation | Cost | Status |
|----------|--------------|----------------|------|--------|
| **Obsidian + Git** | Perfect frontmatter, native backlinks, MCP servers | No real-time collaboration | $0 | **Selected** |
| GitBook | Bidirectional Git sync, native llms.txt | May strip custom frontmatter | ~$30–95/month | Alternative |
| VS Code + Foam | Most direct Git, Live Share | Requires VS Code familiarity | $0 | Alternative |
| Mintlify | Excellent AI-native features | $300/month Pro tier | Over budget | Excluded |

### Widget Library Decision (RF-07-01, ADR-07-01)

| Framework | Category | Key Strength | Key Limitation | Status |
|-----------|----------|--------------|----------------|--------|
| **Thesys C1** | Generative UI | Native Mastra integration, streaming | New product (April 2025) | **Selected** |
| **shadcn/ui + dnd-kit** | Component primitives | Full control, LLM maintainability | No turnkey streaming | **Selected** |
| CopilotKit | Agent-driven | Open-source core, A2UI protocol | No native Mastra integration | Alternative |
| SurveyJS | Survey library | Native ranked choice, matrix | Styling constraints | Alternative |

**Hybrid approach**: Thesys C1 for conversational UI and standard interactions; shadcn/ui + dnd-kit for ~8 custom planning widgets (RankedChoice, PairwiseComparison, AllocationSlider, etc.).

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
| Documentation (Obsidian) | $0 | $0 | $0 |
| Widgets (Thesys C1) | ~$49/month | ~$499/month | Included in total |
| Hosting (Vercel) | ~$40–60/month | ~$100–200/month | $50 / $150 |
| **Total** | **~$150–180/month** | **~$700–900/month** | $600–2000/year |

### Budget Reference

| Phase | LLM Budget | Backend Budget | Total Target |
|-------|------------|----------------|--------------|
| Phase 1 | <$200/month | ~$25/month | $600–$2000/year |
| Phase 3 | <$800/month | ~$75/month | $3000–$5000/year |

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
| DD-18-01 | draft | 2026-01-26 |
| STD-18-01 | draft | 2026-01-26 |
| DD-19-01 | draft | 2026-01-26 |
| STD-19-01 | draft | 2026-01-26 |
| DD-20-01 | draft | 2026-01-25 |
| STD-20-01 | draft | 2026-01-25 |
| RF-01-01 | draft | 2026-01-25 |
| **ADR-01-01** | **accepted** | 2026-01-25 |
| RF-02-01 | draft | 2026-01-25 |
| **ADR-02-01** | **draft** | 2026-01-25 |
| RF-03-01 | draft | 2026-01-25 |
| RF-04-01 | draft | 2026-01-26 |
| **ADR-04-01** | **proposed** | 2026-01-26 |
| RF-07-01 | draft | 2026-01-26 |
| **ADR-07-01** | **proposed** | 2026-01-26 |
| RF-08-01 | draft | 2026-01-25 |
| **ADR-08-01** | **proposed** | 2026-01-25 |
| RF-09-01 | draft | 2026-01-25 |
| **ADR-09-01** | **proposed** | 2026-01-25 |
| **This Index** | **1.5** | 2026-01-26 |

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

**Recent updates (v1.5):**
- Added DD-18-01 Questioning Arc Definition (five-stage workflow, research branching, merge gates)
- Added STD-18-01 Questioning Arc Standards (stage completion criteria, transition rules, quality metrics)
- Added DD-19-01 Widget Schema Definition (18 widget type schemas, interaction logging, LLM generation guidelines)
- Added STD-19-01 Widget Schema Standards (required fields, logging requirements, validation rules)
- Updated Document Relationships diagram with Area 18 and Area 19 pairs
- Added comprehensive Section Maps for all four new documents
- Added questioning arc concepts to Concept Index (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND stages, convergence signal, exploration branch, merge gate, research branch, suspension point, transition triggers, working memory)
- Added widget schema concepts to Concept Index (allocation, card sort, decision gate, pairwise comparison, quadrant, ranked choice, research trigger, sequencer, tradeoff table, widget response, widget schema, widget specification, Zod)
- Added "Where to Find Specific Guidance" entries for arc implementation and widget development
- Added DD-18-01/STD-18-01 and DD-19-01/STD-19-01 to Document Pairs table
- Added Planning Arc Stages quick lookup table with document references
- Added Widget Categories quick lookup table
- Updated Required Reading by Task with arc and widget implementation entries
- Tier 3 now 100% complete (RF-04-01/ADR-04-01 Documentation, RF-07-01/ADR-07-01 Widgets, DD-18-01 Questioning Arc, DD-19-01 Widget Schema done)

**Previous updates (v1.4):**
- Added RF-04-01 Documentation Platform Findings (Obsidian + Git recommended)
- Added ADR-04-01 Documentation Platform Selection
- Added RF-07-01 Widget Component Library Findings (Thesys C1 + shadcn/ui recommended)
- Added ADR-07-01 Widget Component Library Selection
- Updated Document Relationships diagram with all Tier 3 RF→ADR pairs
- Added Section Maps for documentation and widget research
- Added documentation and widget concepts to Concept Index (backlinks, wiki-links, Obsidian, C1, generative UI, shadcn/ui, dnd-kit, etc.)
- Added Documentation Platform Decision and Widget Library Decision quick lookup tables
- Updated Research + Decision Pairs with new entries
- Updated Required Reading by Task for documentation and widget implementation
- Updated Cost Projections Summary with documentation ($0) and widgets (~$49–499/month)

**Previous updates (v1.3):**
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
- Updated Document Relationships diagram to show RF→ADR pairs
- Added Research + Decision Pairs to Cross-Reference Tables
- Added LLM-specific concepts to Concept Index
- Added Backend Platform Decision and LLM Provider Decision quick lookup tables
- Corrected file names to match actual project files

---

*End of Compass Project Reference Index (IDX-00-MASTER)*
