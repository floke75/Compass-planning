---
id: SYS-00
type: spec
title: Compass System Definition
status: active
created: 2026-01-24
updated: 2026-02-03
author: compass-research
summary: Authoritative system specification defining what Compass is, its requirements, architecture, and constraints
tags: [system, specification, compass, architecture, core]
related:
  - DD-12-01
  - DD-13-01
  - DD-14-01
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
---

# Compass — System Definition

**Core system specification for LLM-driven planning, research, and documentation**

**Version**: 2.0

**Last updated**: 2026-01-24
⸻
## Document Purpose  
  
This document defines what Compass is, what it must accomplish, and the technical and organizational constraints it must operate within. It serves as the authoritative reference for understanding Compass as a system.  
  
This document is intentionally tool-agnostic. Where specific tools, vendors, or frameworks appear, they are treated as examples or research candidates, not decisions. Tool selection is covered in the companion document: **Compass Research Program**.  
  
### Scope  
  
This document covers:  
  
- What Compass is, why EFN needs it, and what success looks like  
- Functional and technical requirements  
- Constraints and boundaries (budget, team capacity, security, privacy, vendor independence, timeline)  
- Conceptual architecture and layer definitions  
- Glossary of terms  
  
This document does not cover:  
  
- The research program for selecting specific tools and platforms (see companion document)  
- Internal prompting or algorithmic details of how Compass conducts research  
- Implementation specifications or code  
  
### Audience  
  
- **Primary users (initial)**: 2–3 EFN builders responsible for planning, research, specs, and maintaining documentation truth  
- **Secondary users**: EFN stakeholders who consume specs and docs, and feed in bugs, requests, and operational constraints via complementary tools  
⸻  
## Part 1: Vision and Intent  
  
### 1.1 The Core Problem  
  
EFN has grown rapidly to approximately 120 people and now needs a growing set of specialized internal tools across: live broadcast and studio workflows, podcast and long-form video production, news website and analytics, print and publishing pipelines, captions and subtitles, broadcast-ready data visualization, video logging and semantic analysis, file format conversion, data aggregation, and automation glue.  
  
EFN does not have a traditional development team. Instead, EFN has product owners, builders, domain experts, and increasingly capable coding agents. The risk is drifting into "spreadsheet plus vibes" development: fast starts, brittle systems, and documentation that becomes fiction.  
  
The working hypothesis behind Compass is that LLM-driven development can produce production-quality software with a small non-traditional team if:   
  
1. Rigorous LLM-orchestrated planning and documentation replace ad-hoc vibe coding as the primary development method  
2. Specifications remain the authoritative source of truth, with implementations treated as derivative and regenerable  
3. Tool infrastructure is designed for LLM maintainability (clear patterns and documentation beats cleverness)  
4. Documentation is rigorously kept up-to-date and aligned with the code through automation, not manual work.   
  
Compass is the durable planning, research, and documentation layer that makes that hypothesis testable and operational.  
  
### 1.2 What Compass Is  
  
**One-sentence definition**: Compass is an LLM-orchestrated planning, research, and documentation system that converts vague intent into rigorous, auditable, implementation-ready specifications—then keeps the documentation as the evolving ground truth while execution platforms come and go.  
  
Compass is the foundational layer of an LLM-driven development pipeline. It produces artifacts that implementation platforms consume: specifications that are implementation-grade and testable, research documents that are current and source-backed, decision records capturing chosen and rejected options with rationale, and organizational structures including repo layout, naming, and indexes optimized for long-lived correctness and LLM retrieval.  
  
Compass serves three interconnected purposes:  
  
**Planning layer**: Transforms vague intent into rigorous engineering specs through structured questioning that surfaces assumptions, forces prioritization, and records rejected alternatives alongside chosen approaches.  
  
**Research layer**: Conducts and organizes technical, domain, and contextual research, storing outputs in formats optimized for retrieval so implementation agents use current, source-backed information rather than stale training data.  
  
**Documentation layer**: Maintains a single source of truth. Divergences during implementation are captured as deltas and folded back into docs so future work starts from reality.  
  
Core principle: **the specification is permanent; the implementation is ephemeral**. If specs remain accurate and complete, code can be regenerated later using better models or different execution platforms.  
  
### 1.3 What Compass Is Not  
  
Compass is not: a code execution or coding-orchestration platform (GSD, Auto-Claude, BMAD, and similar tools are downstream consumers), a deployment or runtime management system, a low-code builder, a bug tracker or project management replacement (it integrates with these but does not replace them), or "a chat that sometimes exports a doc."  
  
Compass is a system of artifacts, gates, memory, and structured questioning—with chat as a UI, not as truth.  
  
### 1.4 The Ecosystem Philosophy  
  
EFN's highest-value tools are deeply interconnected. The same curated financial data may feed live broadcast graphics, auto-generated article companions, and podcast research notes. Video metadata services may drive caption generation, semantic analysis, and editorial scheduling.  
  
This interconnection is not incidental; it is a competitive advantage. Compass must treat EFN's tools as an ecosystem: specs must describe tools and their integration points, research must cover cross-cutting patterns not isolated decisions, and documentation must capture data flows, contracts, and shared standards so the ecosystem stays coherent over time.  
  
### 1.5 Who Uses Compass

**Primary users (planning level)**: 2–3 people initially who run the full workflow: planning, research, specs, decisions, and documentation reconciliation.

**Secondary users (organization level)**: Broader EFN stakeholders who submit bugs and requests, track progress, and consume documentation via familiar tools. They should not need to learn the full planning interface to benefit from Compass.

**Future users (multi-team level)**: Domain experts using simplified specification flows for their areas. This is out of scope for the first iteration, but today's architecture should not make it impossible tomorrow.

#### User Role Cross-Reference

User and role definitions appear across multiple documents serving different purposes. This table maps how user types relate across the documentation:

| User Type | Governance Role (DD-15-01) | Compass Access | Tool Context (DD-14-01) |
|-----------|---------------------------|----------------|------------------------|
| **Builder** | Owner or Planner | Primary user—full planning workflow | Creates/maintains all archetypes |
| **Domain Expert** | Contributor | Future user—simplified spec flows | Varies by archetype expertise |
| **Stakeholder** | Viewer | Secondary user—consumes outputs | Consumer of tool outputs |
| **LLM Agent** | Agent (scoped by sponsor) | Automated—executes delegated tasks | Implementation platform |

**Document purpose distinctions**:

- **SYS-00 (this document)**: Defines *who uses Compass* as a system and at what access level
- **DD-15-01 (Governance)**: Defines *permissions and approval workflows* for artifact management
- **DD-14-01 (Ecosystem)**: Defines *who uses EFN tools* by archetype (broadcast producers, editors, operations)

**Cross-reference note**: When planning permissions for a new feature, consult DD-15-01 for the governance model. When classifying a tool's users, consult DD-14-01 for archetype-specific stakeholders.

### 1.6 Core Promises  
  
Compass must reliably produce and maintain:  
  
**Implementation-ready specs**: Clear scope and out-of-scope, constraints covering budget, security, reliability tier, integrations, and timeline, acceptance criteria and a verification approach, and explicit dependencies and sequencing that downstream execution tools can consume.  
  
**Continuous documentation truth**: Specs survive model churn and tooling churn, implementation changes feed back into docs as deltas and reconciled updates, and abandoned plans and rejected options remain accessible as a planning ledger, not a memory hole.  
  
**LLM-driven planning with structured friction**: Dynamic multiple-choice and interactive questioning rather than static forms, branching exploration with explicit merge gates, and anti-paralysis scaffolding so users don't get stuck in blank-page ambiguity.  
  
**Memory that actually remembers**: Cross-session, temporally-aware project memory, retrieval that resists drift and hallucination by grounding in artifacts and evidence, and strong boundaries between projects, branches, and roles.  
  
**Tool-agnostic handoffs**: Export plans to any execution platform via adapters, and import learnings back into documentation without tight coupling to a single vendor.  
  
### 1.7 Guiding Principles  
  
These are behaviors, not tool choices:  
  
**Artifacts are truth; chat is a mutation vector**: Anything important must land in a structured artifact such as a spec, decision record, research finding, or standard. Chat can propose; artifacts record and converge.  
  
**Structured input by default; free text as escape hatch**: Prefer widgets and structured choices because they produce usable requirements. Always provide a "none of these / describe instead" option to avoid dead-ends.  
  
**LLM-agnostic by design**: No hard dependency on a single model vendor or orchestration framework. Build adapter seams everywhere including LLM provider, memory, research tools, PM integration, and handoff.  
  
**Multi-agent safety and human merge gates**: Sub-agents produce proposals, not canonical truth. Humans or explicit merge policies decide what becomes authoritative.  
  
**State is externalized**: The system must reconstruct context from stored state and artifacts, not just from conversation history.  
  
**Auditability and reversibility**: Every change is attributable with who, what, and when recorded. Branch, compare, merge, and rollback are first-class capabilities.  
  
**Reliable under partial failure**: If a memory, search, or index service fails, Compass still functions in degraded but usable mode.  
  
**Privacy and data minimization by default**: Especially important for analytics, newsroom operations, and competitive intelligence.  
  
### 1.8 Critical Junctions  
  
These are the decision zones where a bad bet can derail everything:  
  
1. Memory and retrieval architecture covering quality, temporal awareness, isolation, and failure modes  
2. Artifact truth and versioning model covering how docs evolve and remain authoritative  
3. Dynamic interaction UI covering widgets, state machine, and merge gates  
4. Integration strategy covering events, retries, idempotency, secrets, and rate limits  
5. Handoff adapter design covering platform neutrality without lowest-common-denominator outputs  
6. Security and privacy posture  
7. Operational reliability tiers recognizing that live broadcast tooling differs from internal admin tools  
⸻  
## Part 2: Functional Requirements  
  
### 2.1 The Planning Workflow  
  
The core workflow transforms an initial idea into an implementation-ready specification package through structured conversation, not freeform discussion.  
  
It follows a durable planning arc (a state machine). Names can evolve; intent should not:  
  
- **OPEN**: Extract the fuzzy idea; identify motivations, users, and desired outcomes  
- **FOLLOW**: Expand and elaborate; discover requirements and use cases; gather excitement signals  
- **SHARPEN**: Prioritize; force trade-offs; reveal true priorities via structured friction  
- **BOUNDARY**: Define out-of-scope; prevent scope creep; document rejected options and deferred work  
- **GROUND**: Apply hard constraints including budget, security, reliability tier, integrations, timeline, and compliance  
  
Suggested stage cadence (typical, not mandatory): OPEN approximately 3–5 conversation turns, FOLLOW approximately 10–20 turns, SHARPEN approximately 5–8 turns, BOUNDARY approximately 4–6 turns, GROUND approximately 3–5 turns.  
  
The workflow is not purely linear: users may revisit earlier stages as new information emerges, research branches can pause the main arc and then merge findings back in, and decision branches can explore alternatives in parallel before selecting one.  
  
Each stage must: create or update one or more artifacts, record decisions with status transitions from exploring to accepted, rejected, or superseded, and expose explicit "Research this" triggers when uncertainty blocks progress.  
  
### 2.2 Structured Input Over Freeform Text  
  
Structured input produces better specs than freeform text. "Fast" and "easy" are vibes; a slider labeled "<100ms" versus "<10s" is actionable.  
  
Compass uses dynamic widgets: structured response shapes chosen by the LLM based on conversational context, not static forms designed up front.  
  
**Widget taxonomy** covering the major cognitive tasks involved in planning:  
  
Choice widgets for selecting from options: single select, multi select, ranked choice, and tournament or pairwise comparison that forces prioritization.  
  
Spectrum and allocation widgets for expressing degree: slider with labeled endpoints, opposing spectrums, and allocation such as "spend 100 points across goals."  
  
Comparative widgets for making trade-offs explicit: trade-off tables with criteria by options, and A/B comparisons.  
  
Spatial and ordering widgets for categorizing and sequencing: card sort, sequencing or dependency ordering, and quadrant placement if it proves useful.  
  
Generative widgets for constrained creation: mad-lib style completion and "fill these required fields" prompts with structure.  
  
Meta widgets for workflow control: decision gates, dealbreaker or boundary checklists, "Research this" triggers, and merge gates for accepting, editing, or rejecting branch proposals.  
  
**Minimum UX guarantees for every widget**: Escape hatch via "None of these / I'll describe instead," support via "Help me think" where the system offers framing, examples, or structured suggestions, and research via "Research this" that spawns a research branch with a defined brief.  
  
### 2.3 Research Integration  
  
Research is a first-class activity, not an afterthought. Compass must support:  
  
**Technical research**: Libraries, APIs, platforms, toolchains, and version-specific documentation.  
  
**Domain research**: Market and competitive intelligence, user behavior, and business context.  
  
**Contextual research**: EFN internal systems, repos, historical decisions, patterns, and constraints.  
  
Research must be captured as durable, retrievable artifacts with sources and timestamps so implementation agents can retrieve current truth instead of hallucinating from training data.  
  
**Research branching and merge gates**: Any uncertainty can spawn a research branch that produces a findings summary, sources and citations with access dates, recommendation and confidence, failure modes and mitigations, and impact analysis covering what changes if accepted. A merge gate then lets humans accept, edit, or reject the proposed updates before anything becomes canonical.  
  
### 2.4 Documentation as Ground Truth  
  
Documentation produced by planning becomes the authoritative record of what was decided and why. Implementation will diverge; Compass must make divergence survivable by making reconciliation normal.  
  
**Reconciliation loop**: After implementation or after any out-of-band change, collect implementation deltas including discovered constraints, scope changes, interface changes and refactors, and new operational requirements. Fold deltas back into artifacts with specs updated to reflect reality, decisions marked superseded rather than deleted, and ledger updated to preserve history.  
  
This creates a continuous cycle: planning produces specs, specs drive implementation, implementation produces deltas, deltas update docs, and the next planning starts from truth.  
  
### 2.5 Decision Records and Alternatives  
  
A spec is incomplete if it only documents what was chosen. Compass must capture why, and what was rejected, so future work avoids re-litigating old debates without context.  
  
Decision records capture: the question being answered, options considered, evaluation criteria, the selected option and rationale, explicit rejections and why, dependencies created or assumed, and reversibility rated as easy, medium, or hard with consequences.  
  
### 2.6 Branching and Exploration  
  
Compass supports parallel exploration without losing the plot:  
  
**Exploration branches**: Explore approach A versus approach B until one is selected.  
  
**Research branches**: Pause planning while external investigation occurs, then merge findings.  
  
**Rollback**: Revisit a decision by returning to an earlier state while preserving what happened.  
  
Branch management must support compare, merge, conflict detection, and archiving abandoned branches as reference rather than trash.  
  
### 2.7 Handoff to Implementation  
  
When planning completes, Compass produces a handoff bundle. Format may vary by target platform, but content must be consistent and complete.  
  
**Handoff bundle contents**: Overview covering vision, success metrics, and stakeholders. Requirements covering scope, out-of-scope, and constraints. Decision ledger covering chosen, rejected, and superseded decisions with rationale. Architecture sketch covering components, interfaces, and data flows. Acceptance criteria and verification plan. Work breakdown proposal covering phases and atomic tasks that are implementation-ready. Context pack covering sources, citations, and extracted ground truth.  
  
The handoff is a clean boundary: implementation platforms consume artifacts and execute. Feedback flows back via documentation updates and deltas, not by tightly coupling Compass to a specific execution tool.  
⸻  
## Part 3: Technical Requirements  
  
### 3.1 LLM-Driven Conversation  
  
The planning workflow is driven by an LLM, not by a static wizard. The LLM decides: what question to ask next, what widget to present, when to suggest research branches or exploration branches, and how to synthesize user input into structured artifacts.  
  
This requires:  
  
**Conversation orchestration**: Multi-turn state management; pause, branch, and resume; persistence across days and weeks.  
  
**Structured output**: Reliable generation of widget specifications and artifact updates that are schema-constrained, not freeform.  
  
**Long context strategy**: Retrieval of relevant artifacts and evidence without stuffing entire histories into prompts.  
  
**Temporal awareness**: Understanding when decisions happened and what changed since.  
  
### 3.2 Memory and Context  
  
Compass must support three layers of memory:  
  
**Session memory**: What is being discussed now.  
  
**Project memory**: Decisions, constraints, artifacts, and history for a specific project that is cross-session and long-lived.  
  
**Ecosystem memory**: Cross-project patterns, standards, and prior solutions answering "have we solved this before?"  
  
Memory is not just storage; it must support semantic and temporal retrieval such as "what changed since Monday?"  
  
**Core entities**:  
  
- **Project**: Canonical container  
- **Artifact**: A versioned document including spec, requirements, roadmap, research finding, standard, context pack, run log, and similar  
- **Decision**: Typed record with status, rationale, options considered, and dependencies  
- **Branch**: Alternate planning universe for research, architecture alternative, and similar  
- **Workflow run**: Trace of arc progression and state transitions  
- **Citation / evidence**: Reference to a source plus extracted relevant content with timestamp  
- **Profile**: User and team preferences and constraints including risk tolerance, tone, and defaults  
- **Adapter**: Import and export mapping to downstream systems and implementation platforms  
  
**Truth hierarchy**: To keep sanity, Compass maintains an explicit truth hierarchy. Intent truth covers specs, requirements, and decisions representing what we intend and why. Execution truth covers tasks, verification outputs, and release notes representing what we built and validated. Audit truth covers changelogs, branch history, and attribution trail representing how truth evolved.  
  
### 3.3 Interface Requirements  
  
The primary interface is a web application that supports: rich widget rendering as defined in Part 2, real-time conversational interaction, document viewing and editing that is artifact-centric, decision and branch visualization and management, research browsing and cross-linking, and merge gates for proposal review and acceptance.  
  
A secondary interface connects to project management tools for: organization visibility into planning progress, intake of bugs, feature requests, and operational constraints, timeline and milestone tracking, and cross-team coordination.  
  
These interfaces may be different tools. The planning interface needs deep interaction; the team interface needs familiarity and accessibility.  
  
### 3.4 State Management  
  
System state divides into:  
  
**Ephemeral state**: In-browser UI state and unsaved local inputs lost on refresh.  
  
**Durable project state**: Decisions, specs, research, and documentation artifacts that persist indefinitely.  
  
**Configuration state**: Settings, user preferences, and integration credentials that are durable but infrequently changed.  
  
The backend must support real-time synchronization when multiple sessions view the same project, conflict detection and resolution for simultaneous edits, and full version history for accountability.  
  
### 3.5 Version Control and History  
  
Everything important is versioned: specs track changes with attribution, research docs note when fetched and from where, decisions record status transitions from proposed to accepted, rejected, or superseded, and documentation shows evolution over time.  
  
Git-based version control (typically GitHub) is the natural convergence point because implementation platforms already use it, documentation can live alongside code, change tracking via diffs and attribution are native, and collaboration patterns are established.  
  
However, not all state belongs in git. The key rule is: canonical artifacts should be git-friendly, even if some operational state lives elsewhere.  
  
### 3.6 External Integrations  
  
Compass must integrate with:  
  
**Implementation platforms**: Output-only handoff of artifacts in consumable formats.  
  
**Project management**: Bidirectional sync of visibility and intake where bugs and requests become planning inputs.  
  
**Research sources**: Input-only during research from web, docs, and internal repos, producing evidence artifacts.  
  
**Authentication providers**: Internal identity, likely enterprise SSO.  
  
### 3.7 Performance and Scale  
  
Initial scale is modest: 2–3 concurrent users, dozens of projects, hundreds of documents. The architecture must handle this comfortably without enterprise-grade complexity, while not blocking future scale of 10–20 concurrent users and thousands of documents.  
  
Response time targets as guidance: widget rendering under 100ms, LLM responses under 5s typical and under 30s for complex reasoning, document retrieval under 500ms, and search results under 1s.  
  
### 3.8 Reliability and Recovery  
  
Planning work is high-value. Losing work is unacceptable.  
  
Conversation state saves continuously. Documents auto-save with conflict detection. Failed operations retry automatically where safe. Manual recovery procedures exist for edge cases.  
  
The system must degrade gracefully when external services are unavailable. If memory search is down, planning continues with reduced context. If a research source is unavailable, it is skipped with visible notification.  
⸻  
## Part 4: Constraints and Boundaries  
  
### 4.1 Budget  
  
Budget targets are intentionally modest to preserve experimentation and reversibility:  
  
**Initial**: $600–$2,000 per year for external services with usage-based preferred over high fixed subscriptions.  
  
**Proven value**: $3,000–$5,000 per year becomes reasonable for services with clear ROI.  
  
Cost categories to track: backend, database, auth, and hosting; LLM API usage; memory and search services; documentation hosting and collaboration tooling; research tools and APIs including search, scraping, and doc ingestion; and project management integration.  
  
### 4.2 Team Capacity  
  
The team understands software conceptually but does not write production code manually as a default mode. Therefore:  
  
**LLM maintainability** is a primary requirement covering common stacks, strong docs, and simple patterns.  
  
**Operational simplicity** is essential with managed services preferred and minimal self-hosting.  
  
**Debuggability** matters with explicit error handling, clear logs, and observable workflows.  
  
### 4.3 Security  
  
Compass handles internal EFN information including strategy, competitive intelligence, and operational plans. Requirements include: robust authentication with SSO preferred, explicit authorization covering who can see and do what, encryption at rest and in transit, audit logs for access and changes, and reasonable security posture from third-party services.  
  
### 4.4 Privacy and Data Ownership  
  
EFN must retain ownership of all data: specifications and documentation are EFN IP, research outputs belong to EFN, and system usage data remains under EFN control.  
  
Services that license user data for training or retain data after closure are unacceptable.  
  
### 4.5 Vendor Independence  
  
Given rapid change in LLM tooling, vendor lock-in is a strategic risk. Prefer: standard formats over proprietary ones, export capability for all data, abstraction layers that allow swapping implementations, and multiple viable alternatives for critical components.  
  
### 4.6 Timeline  
  
There is no single hard deadline, but progress should be visible within weeks. Build iteratively so each phase is usable, not just a stepping stone:  
  
**Phase 1**: Minimal viable planning workflow covering basic conversation, simple widgets, and document output.  
  
**Phase 2**: Research integration and memory covering evidence capture, retrieval, and citations.  
  
**Phase 3**: Branching and advanced widgets covering merge gates, compare and merge, and richer interactions.  
  
**Phase 4**: Project management integration and documentation reconciliation loop.  
  
**Phase 5**: Polish, scale improvements, and expanded access.  
⸻  
## Part 5: Conceptual Architecture  
  
### 5.1 The Layers  
  
**Layer 1 — Interaction layer**: Web and chat UI that renders rich widgets. Manages questioning arc state and merge gates.  
  
**Layer 2 — Authoritative state layer**: Projects, decisions, branches, workflow runs, and permissions. Versioning and audit.  
  
**Layer 3 — Artifact store (convergence layer)**: Canonical docs and handoff bundles with history. Git-friendly.  
  
**Layer 4 — Memory and retrieval layer**: Semantic and literal search. Temporal and branch-aware recall.  
  
**Layer 5 — Pristine context and evidence layer**: Verified sources, fetched docs, and extracted ground truth snippets. Designed to reduce hallucination and allow re-checking.  
  
**Layer 6 — Integration and event layer**: Webhooks, events, queues, and schedulers for syncing external systems and running workflows.  
  
**Layer 7 — Execution platforms (downstream)**: Any coding or execution toolchain that consumes artifacts and produces outputs.  
  
### 5.2 Mental Diagram  
  
```
User ↔ Interaction Layer (dynamic widgets + questioning)
          │
          ▼
Authoritative State Layer  ↔  Memory/Retrieval Layer
          │                           │
          │                           ▼
          │                    Evidence/Pristine Context
          │
          ▼
Artifact Store (canonical docs + handoff bundles)
          │
          ▼
Execution Platform Adapters → Implementation Systems → Code/Outputs
          │
          └──────────────► Reconciliation (deltas → docs truth)

```
  
  
### 5.3 Open Standards Preference  
  
To avoid vendor lock-in, prefer open standards and portable formats for tool and context integration where possible.  
  
One candidate is the Model Context Protocol (MCP), intended to standardize how LLM applications connect to tools and data sources.  
  
Reference starting points for research (not endorsement): Anthropic MCP overview at anthropic.com/news/model-context-protocol, Supermemory research notes at supermemory.ai/research, Zep Graphiti docs at help.getzep.com/graphiti/getting-started/welcome, and BMAD Claude Code guide at github.com/NoCodingAi/BMAD-METHOD-Ai-Full-Stack-Team/blob/main/docs/claude-code-guide.md.  
  
### 5.4 Reference Patterns  
  
BMAD-style workflows emphasize role-based agents and artifact-driven outputs stored as version-controlled assets. This aligns with Compass's direction of artifacts as truth and is useful as a reference pattern—not a commitment to a specific methodology or tool.  
⸻  
## Appendix A: Glossary  
  
**Artifact**: A versioned document the system treats as truth including spec, decision record, research finding, and standard.  
  
**Artifact store**: The canonical location for durable artifacts, typically git-friendly.  
  
**Audit truth**: Changelog and ledger plus branch history plus attribution trail.  
  
**Agent Pack**: A portable configuration in JSON or YAML that defines how an LLM agent should behave for a specific task, commonly used by implementation platforms.  
  
**BMAD**: An LLM development methodology using document-centric state management and phase-based prompts.  
  
**Branch**: A parallel planning universe for research, alternative architecture, and similar purposes.  
  
**Decision branch**: A workflow state where alternative approaches are explored in parallel before selecting one.  
  
**Decision gate**: A checkpoint where an explicit choice is required before proceeding.  
  
**Decision record (ADR)**: A document capturing what was decided, what alternatives were considered, and why.  
  
**Decision ledger**: The set of all decisions with status, rationale, dependencies, and history.  
  
**Escape hatch**: A widget option that exits constrained choices such as "none of these fit."  
  
**Execution truth**: Tasks, verification outputs, and release notes representing what was built and validated.  
  
**GSD (Get Stuff Done)**: A code implementation platform or pattern using structured commands and verification workflows; an example downstream consumer.  
  
**Handoff / handoff bundle**: The package of specs, decisions, research, and context exported from Compass to an implementation platform.  
  
**Implementation delta**: A discovered change during or after implementation that must be reconciled back into documentation.  
  
**Intent truth**: Specs plus requirements plus decision ledger representing what we intend and why.  
  
**MCP (Model Context Protocol)**: A proposed standard for how LLM apps connect to tools and data sources.  
  
**Merge gate**: An explicit process or UI to accept or reject a branch's proposed mutations to canonical artifacts.  
  
**Pristine context**: Verified external or internal source material stored with citations and timestamps, fetched or validated at query time.  
  
**Questioning arc**: The structured progression through OPEN, FOLLOW, SHARPEN, BOUNDARY, and GROUND stages.  
  
**Research branch**: A workflow state where planning pauses for external investigation before resuming.  
  
**Widget**: A structured input component such as slider, ranking, or comparison generated dynamically by the system.  
  
**Workflow run**: A trace of one planning journey, which may span multiple sessions over time.  
⸻  
## Appendix B: Referenced Documents  
  
The source documents referenced these additional materials:  
  
- Planning_research_1.md — prior research on tool stack architecture  
- Planning_research_2.md — prior research on LLM orchestration and memory  
- SYSTEM_CONTEXT_COMPASS_OPTIMIZED.md — detailed system specification containing specific tool choices treated as research candidates  
⸻  
*End of Compass System Definition*  
