---
id: DD-11-01
type: definition
area: 11-handoff-schema
title: Handoff Bundle Schema Definition
status: draft
created: 2026-01-28
updated: 2026-02-03
author: compass-research
summary: Defines the schema for implementation handoff bundles that transfer planning outputs to execution platforms
tags: [handoff, schema, implementation, bundle, execution, platform]
related:
  - DD-12-01
  - DD-13-01
  - DD-14-01
  - DD-18-01
  - STD-20-01
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: companion
    target_id: "STD-11-01"
companion: STD-11-01
---

# Handoff Bundle Schema Definition

## Document Purpose

This document defines the **handoff bundle schema**: the structure and content requirements for packages that transfer completed planning outputs from Compass to implementation platforms. The handoff bundle is the primary artifact that bridges planning and execution—it contains everything an implementation agent or developer needs to begin work.

**Why this matters**: The handoff is a critical boundary. A poorly structured handoff leads to implementation agents asking questions that were already answered during planning, making incorrect assumptions, or missing important constraints. A well-structured handoff enables implementation to proceed with minimal clarification while preserving full context for debugging and verification.

**Key principle from System Definition §2.7**: "The handoff is a clean boundary: implementation platforms consume artifacts and execute. Feedback flows back via documentation updates and deltas, not by tightly coupling Compass to a specific execution tool."

**What this document covers**:

- Required sections and their schemas
- Bundle metadata format
- Platform adaptation mechanisms
- Validation criteria for completeness

**What this document does not cover**:

- Specific platform adapters (downstream concern)
- Artifact lifecycle and storage (see DD-13-01)
- Repository location and naming (see DD-12-01)
- How planning produces handoff content (see DD-18-01)

**Audience**: Compass builders implementing handoff generation, implementation platforms consuming bundles, and planners reviewing handoff quality.

---

## Part 1: Bundle Overview

### 1.1 What Is a Handoff Bundle?

A handoff bundle is a self-contained package that transfers everything needed to implement a planned piece of work from Compass to an execution platform. It is the output of completed planning and the input to implementation.

**Properties of a good handoff bundle**:

- **Complete**: Contains all information an implementation agent needs to start work without asking clarifying questions
- **Self-contained**: Can be understood without access to other Compass systems
- **Traceable**: Links back to source planning sessions, decisions, and evidence
- **Platform-neutral**: Provides a base format that adapters can transform for specific platforms
- **Validatable**: Structure allows automated checking for completeness

### 1.2 When Handoff Bundles Are Created

Handoff bundles are created when:

- A project completes the GROUND stage of the questioning arc (see DD-18-01 §1.2)
- A planner explicitly requests handoff generation for a completed phase
- An approved ADR requires implementation handoff

Handoff bundles are NOT created for:

- In-progress planning (use working documents instead)
- Research tasks (use Research Briefs/Findings)
- Decisions that don't require implementation

### 1.3 Bundle Structure Overview

Every handoff bundle contains seven required sections plus metadata:

```
HANDOFF-{project}-{version}.md
├── Metadata (YAML frontmatter)
├── Section 1: Overview
├── Section 2: Requirements
├── Section 3: Decision Ledger
├── Section 4: Architecture Sketch
├── Section 5: Acceptance Criteria
├── Section 6: Work Breakdown
└── Section 7: Context Pack
```

The sections follow a logical order: understanding what we're building (Overview, Requirements), understanding why we made key choices (Decision Ledger), understanding how it fits together (Architecture), understanding what "done" means (Acceptance Criteria), understanding how to get there (Work Breakdown), and having the supporting evidence (Context Pack).

---

## Part 2: Bundle Metadata Schema

### 2.1 Frontmatter Fields

Handoff bundles use the standard Compass frontmatter (per DD-13-01 §2.1) with additional handoff-specific fields:

```yaml
---
# Standard fields (required on all artifacts)
id: HANDOFF-broadcast-viz-001
type: handoff
area: null  # Not applicable for handoff bundles
title: Broadcast Data Visualization Tool - Phase 1
status: draft  # draft | review | active | deprecated
created: 2026-01-28
updated: 2026-01-28
author: jsmith
summary: Implementation handoff for broadcast-ready data visualization from CSV/Excel/PDF sources
tags: [broadcast, visualization, data, phase-1]
related:
  - SPEC-broadcast-viz-001
  - ADR-0023
  - ADR-0024

# Handoff-specific fields (required)
bundle_version: "1.0"
target_platform: null  # null for platform-neutral, or specific platform ID
source_specs:
  - SPEC-broadcast-viz-001
  - SPEC-broadcast-viz-002
source_planning_sessions:
  - session: PS-2026-01-15-001
    completed: 2026-01-20
archetype: broadcast-critical  # Per DD-14-01 archetype catalog
reliability_tier: 1  # Per DD-14-01 §2.1

# Handoff-specific fields (optional)
prerequisite_bundles: []  # Other handoffs that must complete first
estimated_effort: "3-4 weeks"
expiration: null  # ISO date after which bundle should be reviewed for staleness
---
```

### 2.2 Field Definitions

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `bundle_version` | Yes | string | Schema version for this bundle (currently "1.0") |
| `target_platform` | Yes | string or null | Target platform if adapted; null for platform-neutral |
| `source_specs` | Yes | array | IDs of specifications this bundle implements |
| `source_planning_sessions` | Yes | array | Planning sessions that produced this bundle |
| `archetype` | Yes | string | Project archetype per DD-14-01 |
| `reliability_tier` | Yes | integer | Reliability tier (1-5) per DD-14-01 §2.1 |
| `prerequisite_bundles` | No | array | Bundles that must complete first |
| `estimated_effort` | No | string | Human-readable effort estimate |
| `expiration` | No | date | Date after which bundle should be reviewed |

### 2.3 Source Planning Sessions Format

```yaml
source_planning_sessions:
  - session: PS-2026-01-15-001  # Planning session ID
    completed: 2026-01-20        # Date planning completed
  - session: PS-2026-01-22-001
    completed: 2026-01-25
```

This enables tracing back from implementation to the original planning conversations for context or debugging.

---

## Part 3: Section Schemas

### 3.1 Overview Section

**Purpose**: Establish shared understanding of what we're building and why.

The Overview section answers: What is this project? Why does it matter? Who cares about it? How will we know it succeeded?

**Required content**:

```markdown
## Overview

### Vision Statement

[1-3 sentences describing what this project accomplishes and why it matters. 
Should be understandable by someone with no prior context.]

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric name] | [Quantifiable target] | [How we verify this] |

### Stakeholders

| Role | Who | Interest | Authority |
|------|-----|----------|-----------|
| [Role name] | [Person/team] | [Why they care] | [What they control] |

### Project Context

[2-4 sentences situating this project within the broader EFN ecosystem. 
What other tools does this relate to? What business context matters?]
```

**Schema validation rules**:

- Vision statement must be present and non-empty
- At least one success metric must be defined
- At least one stakeholder must be identified
- Project context must reference archetype alignment

**Example**:

```markdown
## Overview

### Vision Statement

Build a tool that transforms CSV, Excel, and PDF financial data into broadcast-ready graphics in under 30 seconds, enabling producers to display current market data during live broadcasts without manual graphics creation.

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Data-to-graphic time | <30 seconds | Timed test with sample datasets |
| Graphic accuracy | 100% of values correct | Automated comparison with source data |
| Broadcast reliability | Zero failures during live use | Production monitoring logs |

### Stakeholders

| Role | Who | Interest | Authority |
|------|-----|----------|-----------|
| Broadcast Producer | Production Team | Needs fast, reliable graphics | Defines priority of data types |
| Graphics Operator | Studio Team | Needs clear, usable interface | Validates workflow fit |
| Data Team | Editorial | Provides source data | Specifies data formats |

### Project Context

This tool is part of EFN's broadcast infrastructure and classified as broadcast-critical (Tier 1 reliability). It will consume data from the Financial Data Service and output to the existing broadcast graphics pipeline. The tool replaces a manual process that currently requires 5-10 minutes per graphic.
```

---

### 3.2 Requirements Section

**Purpose**: Define what is in scope, what is explicitly out, and what constraints apply.

The Requirements section answers: What must this project do? What must it NOT do? What limitations apply?

**Required content**:

```markdown
## Requirements

### Scope

#### In-Scope Requirements

- [REQ-001] [Requirement statement]
  - Priority: [must-have | should-have | nice-to-have]
  - Rationale: [Why this is needed]
  
- [REQ-002] [Requirement statement]
  - Priority: [must-have | should-have | nice-to-have]
  - Rationale: [Why this is needed]

#### Out-of-Scope

- [OUT-001] [What we are NOT doing]
  - Reason: [Why this is excluded]
  - Future: [Whether this might be addressed later]

### Constraints

| Constraint Type | Constraint | Impact |
|-----------------|------------|--------|
| Budget | [Limit] | [How this shapes decisions] |
| Timeline | [Deadline/window] | [How this shapes scope] |
| Technical | [Limitation] | [How this shapes architecture] |
| Security | [Requirement] | [How this shapes implementation] |
| Integration | [Dependency] | [How this shapes design] |
```

**Schema validation rules**:

- At least three in-scope requirements must be defined
- At least one out-of-scope item must be defined (forces explicit boundary thinking)
- Each requirement must have a unique ID (REQ-NNN)
- Each requirement must have a priority
- At least one constraint must be specified

**Requirement ID format**:

```
REQ-{NNN}  # e.g., REQ-001, REQ-042
OUT-{NNN}  # e.g., OUT-001, OUT-015
```

---

### 3.3 Decision Ledger Section

**Purpose**: Document key decisions, their rationale, and alternatives considered.

The Decision Ledger answers: What choices did we make? Why? What did we reject?

**Required content**:

```markdown
## Decision Ledger

This section summarizes key decisions made during planning. Full decision records are linked where available.

### Active Decisions

| ID | Decision | Rationale | Source |
|----|----------|-----------|--------|
| [ADR-NNNN or inline] | [What was decided] | [Brief why] | [Link to full ADR if exists] |

### Rejected Alternatives

| Related To | Alternative | Why Rejected |
|------------|-------------|--------------|
| [Decision ID] | [What we didn't do] | [Brief explanation] |

### Deferred Decisions

| Topic | Deferred Because | Revisit When |
|-------|------------------|--------------|
| [What wasn't decided] | [Why we didn't decide now] | [Trigger for revisiting] |
```

**Schema validation rules**:

- At least one active decision must be documented
- Each decision must have rationale (even if brief)
- Rejected alternatives section may be empty but must be present
- Deferred decisions section may be empty but must be present

**When to inline vs. link**:

- If a formal ADR exists: link to it, include only summary in ledger
- If decision was made during planning without formal ADR: inline the full reasoning
- If decision is trivial: brief inline entry is sufficient

---

### 3.4 Architecture Sketch Section

**Purpose**: Provide enough technical context for implementation to begin.

The Architecture Sketch answers: What are the major pieces? How do they connect? What data flows where?

**Required content**:

```markdown
## Architecture Sketch

### Components

| Component | Purpose | Technology | Owner |
|-----------|---------|------------|-------|
| [Name] | [What it does] | [Stack/framework if known] | [Team/person responsible] |

### Component Diagram

```
[ASCII or reference to diagram file]

Example:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Data Input  │────>│ Processing  │────>│ Rendering   │
│ (CSV/Excel) │     │ Engine      │     │ Pipeline    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           v
                    ┌─────────────┐
                    │ Data Store  │
                    └─────────────┘
```

### Interfaces

| Interface | Type | Direction | Contract |
|-----------|------|-----------|----------|
| [Name] | [API/Event/File/etc.] | [In/Out/Both] | [Brief description or link] |

### Data Flows

| Flow Name | Source | Destination | Data Type | Frequency |
|-----------|--------|-------------|-----------|-----------|
| [Name] | [Component] | [Component] | [What moves] | [How often] |
```

**Schema validation rules**:

- At least one component must be defined
- Component diagram must be present (ASCII acceptable)
- At least one interface must be defined for non-trivial projects
- Data flows must be defined if multiple components exist

**Architecture depth guidance**:

The sketch should provide enough detail that an implementation agent understands the major moving pieces, but not so much detail that it constrains implementation choices unnecessarily. Think "whiteboard level" not "code level."

- **Too shallow**: "This is a web app that does data visualization."
- **Right level**: Components, their responsibilities, how they connect, key interfaces.
- **Too deep**: Specific function signatures, database schema columns, CSS class names.

---

### 3.5 Acceptance Criteria Section

**Purpose**: Define testable statements that determine when implementation is complete.

The Acceptance Criteria section answers: How do we know when we're done? How do we verify it works?

**Required content**:

```markdown
## Acceptance Criteria

### Functional Criteria

- [AC-001] [Testable statement about what the system must do]
  - Verification: [How this will be tested]
  
- [AC-002] [Testable statement about what the system must do]
  - Verification: [How this will be tested]

### Non-Functional Criteria

- [AC-NF-001] [Performance/reliability/security criterion]
  - Verification: [How this will be tested]
  - Target: [Specific threshold]

### Verification Plan

| Phase | What's Verified | Method | Who |
|-------|-----------------|--------|-----|
| [Phase name] | [Criteria covered] | [Test approach] | [Responsible party] |
```

**Schema validation rules**:

- At least three acceptance criteria must be defined
- Each criterion must have a unique ID (AC-NNN or AC-NF-NNN)
- Each criterion must have a verification method
- Non-functional criteria must have measurable targets
- At least one verification phase must be planned

**Writing good acceptance criteria**:

| Bad | Good |
|-----|------|
| "Graphics look professional" | "Graphics render with anti-aliased text and consistent 16px margins" |
| "System is fast" | "Data-to-render time is under 30 seconds for datasets up to 1000 rows" |
| "Errors are handled" | "Invalid CSV input displays user-facing error message within 2 seconds" |

---

### 3.6 Work Breakdown Section

**Purpose**: Propose implementation phases and atomic tasks.

The Work Breakdown section answers: How should implementation proceed? What are the concrete tasks?

**Required content**:

```markdown
## Work Breakdown

### Implementation Phases

| Phase | Goal | Dependencies | Estimated Effort |
|-------|------|--------------|------------------|
| [Phase N] | [What this achieves] | [What must complete first] | [Time estimate] |

### Phase Details

#### Phase 1: [Name]

**Goal**: [What completing this phase achieves]

**Tasks**:

- [ ] [TASK-001] [Specific, actionable task]
  - Inputs: [What's needed to start]
  - Outputs: [What's produced when complete]
  - Acceptance: [How we know it's done]

- [ ] [TASK-002] [Specific, actionable task]
  - Inputs: [What's needed to start]
  - Outputs: [What's produced when complete]
  - Acceptance: [How we know it's done]

**Phase Exit Criteria**: [What must be true before moving to next phase]

#### Phase 2: [Name]

[Same structure as Phase 1]

### Dependencies

```
Phase 1
    └── Task 1.1 ─┬─ Task 1.2
                  └─ Task 1.3 ── Phase 2
                                    └── Task 2.1 ─── Task 2.2
```

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [What could go wrong] | [H/M/L] | [H/M/L] | [How we address it] |
```

**Schema validation rules**:

- At least one phase must be defined
- Each phase must have at least one task
- Tasks must have unique IDs (TASK-NNN)
- Each task must specify inputs, outputs, and acceptance criteria
- Dependencies must be documented if multiple phases exist

**Task granularity guidance**:

Tasks should be atomic enough that an implementation agent can complete them in a single focused work session (typically 1-4 hours of work). They should not require additional planning to break down further.

| Too coarse | Right level | Too fine |
|------------|-------------|----------|
| "Build the data processing module" | "Create CSV parser that extracts columns matching template schema" | "Write the for loop that iterates over CSV rows" |

---

### 3.7 Context Pack Section

**Purpose**: Provide supporting evidence, sources, and extracted ground truth.

The Context Pack section answers: What evidence supports this plan? Where can we verify claims?

**Required content**:

```markdown
## Context Pack

### Source Evidence

This section collects evidence gathered during planning. Citations follow STD-20-01 format.

#### Key Sources

1. **[T1/S1]** [Author]. "[Title]" [Version]. 
   Published/Updated [DATE]. Retrieved [DATE]. [URL]
   
   **Relevant excerpt**: "[Brief quote or summary of what this source establishes]"

2. **[T2/S2]** [Author]. "[Title]". 
   Published [DATE]. Retrieved [DATE]. [URL]
   
   **Relevant excerpt**: "[Brief quote or summary]"

### Extracted Ground Truth

These facts were validated during planning and should inform implementation:

| Fact | Source | Confidence | Implications |
|------|--------|------------|--------------|
| [Validated statement] | [Citation #] | [High/Medium/Low] | [How this affects implementation] |

### Research Artifacts

| Finding ID | Topic | Summary | Link |
|------------|-------|---------|------|
| [RF-XX-XX] | [What was researched] | [One-line finding] | [Link to full document] |

### Freshness Notice

**Bundle created**: [Date]
**Sources validated**: [Date]
**Review recommended if not implemented by**: [Date + freshness threshold]
```

**Schema validation rules**:

- At least one source must be cited for non-trivial bundles
- Citations must follow STD-20-01 format (see Part 4)
- Freshness notice must be present
- Research artifacts section may be empty but must be present

**What belongs in the Context Pack**:

- Evidence that influenced key decisions
- Technical documentation for chosen technologies
- Validated facts that implementation should rely on
- Research findings that shaped requirements

**What does NOT belong in the Context Pack**:

- Generic background information (link to external resources instead)
- Rejected research (summarize in Decision Ledger instead)
- Internal Compass documentation (reference by ID instead)

---

## Part 4: Citation Format in Handoff Bundles

The Context Pack uses the citation format defined in STD-20-01. Key requirements:

### 4.1 Inline Citation Format

```markdown
The API supports up to 1000 requests per minute [1]. Rate limiting uses a sliding window [2].
```

### 4.2 Source List Format

```markdown
1. **[T1/S1]** Vendor Inc. "API Rate Limits Documentation" v2.3. 
   Updated 2025-11-15. Retrieved 2026-01-25. https://docs.vendor.com/limits
   
2. **[T2/S2]** Stack Overflow. "Understanding sliding window rate limiting" (Score: 89). 
   Posted 2024-06-12. Retrieved 2026-01-25. https://stackoverflow.com/questions/12345
```

### 4.3 Tier/Reliability Quick Reference

| Prefix | Meaning | Use For |
|--------|---------|---------|
| **[T1/S1]** | Official, verified | Vendor docs, official announcements |
| **[T2/S2]** | Reputable, reliable | High-reputation community sources |
| **[T3/S3]** | Some caution needed | Secondary sources, older content |
| **[T4/S4]** | Verify before relying | Personal blogs, unverified claims |
| **[T5/S4]** | Cite with warnings | Anonymous sources, uncertain quality |

See STD-20-01 for complete specification.

---

## Part 5: Platform Adaptation

### 5.1 Platform-Neutral Base Format

The schemas defined in this document describe the **platform-neutral base format**. This format is:

- Human-readable (Markdown with YAML frontmatter)
- Machine-parseable (structured headings and tables)
- Complete (contains all information needed for any platform)

Implementation platforms may require different formats, but all should be derivable from the base format without loss of essential information.

### 5.2 Adaptation Mechanism

Platform adaptation works through **adapters**: transformations that convert the base format to platform-specific formats.

```
Platform-Neutral Bundle (base)
        │
        ├──> Claude Code Adapter ──> .claude.json format
        │
        ├──> Linear Adapter ──> Linear API payloads
        │
        ├──> GitHub Issues Adapter ──> Issue/PR templates
        │
        └──> Custom Platform Adapter ──> Platform-specific format
```

### 5.3 Adapter Requirements

Every adapter must:

1. **Preserve essential information**: All requirements, decisions, acceptance criteria, and tasks must survive transformation
2. **Maintain traceability**: Platform artifacts must link back to source bundle
3. **Handle missing features**: If platform can't represent something, document what was lost
4. **Be reversible** (where possible): Changes in platform should be capturable as deltas

### 5.4 Adapter Registration

Adapters are registered with their:

- Platform identifier (e.g., "claude-code", "linear", "github-issues")
- Input format (always base format)
- Output format description
- Known limitations
- Maintainer

**Note**: Adapter implementations are downstream concerns. This document defines what adapters must preserve, not how they work internally.

---

## Part 6: Bundle File Organization

### 6.1 Single-File Bundles (Default)

Most handoff bundles are single Markdown files:

```
handoffs/
└── HANDOFF-broadcast-viz-001.md
```

### 6.2 Multi-File Bundles

For complex projects with large diagrams, extensive source material, or multiple phases, a folder structure is acceptable:

```
handoffs/
└── HANDOFF-broadcast-viz-001/
    ├── HANDOFF-broadcast-viz-001.md    # Main bundle document
    ├── diagrams/
    │   ├── architecture.svg
    │   └── data-flow.svg
    ├── sources/
    │   └── extracted-api-spec.json
    └── phases/
        ├── phase-1-tasks.md
        └── phase-2-tasks.md
```

**Rules for multi-file bundles**:

- Main document must be at folder root with same name as folder
- Main document must be complete—supplementary files provide detail, not essential information
- All files must be referenced from main document
- Bundle remains a single logical unit even when multi-file

### 6.3 Naming Convention

Per DD-12-01 §3.1:

```
HANDOFF-{project-name}-{version}.md

Examples:
HANDOFF-broadcast-viz-001.md
HANDOFF-captions-tool-phase1.md
HANDOFF-podcast-dashboard-002.md
```

---

## Part 7: Validation Checklist

### 7.1 Completeness Validation

Every handoff bundle must pass this checklist before handoff:

**Metadata**:
- [ ] All required frontmatter fields present
- [ ] `bundle_version` is "1.0"
- [ ] `source_specs` lists at least one specification
- [ ] `archetype` matches DD-14-01 catalog
- [ ] `reliability_tier` is 1-5

**Overview Section**:
- [ ] Vision statement present and non-empty
- [ ] At least one success metric defined with measurement method
- [ ] At least one stakeholder identified
- [ ] Project context references archetype

**Requirements Section**:
- [ ] At least three in-scope requirements with IDs
- [ ] At least one out-of-scope item
- [ ] At least one constraint specified
- [ ] All requirements have priorities

**Decision Ledger**:
- [ ] At least one active decision documented
- [ ] All decisions have rationale
- [ ] Rejected alternatives section present
- [ ] Deferred decisions section present

**Architecture Sketch**:
- [ ] At least one component defined
- [ ] Component diagram present
- [ ] Interfaces defined for multi-component systems
- [ ] Data flows documented if applicable

**Acceptance Criteria**:
- [ ] At least three acceptance criteria with IDs
- [ ] All criteria have verification methods
- [ ] Non-functional criteria have measurable targets
- [ ] Verification plan includes at least one phase

**Work Breakdown**:
- [ ] At least one phase defined
- [ ] Each phase has at least one task
- [ ] All tasks have inputs, outputs, and acceptance
- [ ] Dependencies documented

**Context Pack**:
- [ ] At least one source cited (for non-trivial bundles)
- [ ] Citations follow STD-20-01 format
- [ ] Freshness notice present

### 7.2 Quality Validation

Beyond completeness, bundles should be reviewed for quality:

- [ ] Vision statement is understandable without prior context
- [ ] Requirements are specific enough to implement
- [ ] Architecture sketch matches reliability tier expectations
- [ ] Acceptance criteria are actually testable
- [ ] Tasks are atomic (completable in one focused session)
- [ ] Evidence supports key decisions

---

## Appendix A: Sample Handoff Bundle

A complete sample bundle demonstrating all sections:

```markdown
---
id: HANDOFF-file-converter-001
type: handoff
title: File Format Converter Tool - Phase 1
status: draft
created: 2026-01-28
updated: 2026-01-28
author: jsmith
summary: Implementation handoff for internal file format conversion utility
tags: [utility, converter, internal, phase-1]
related:
  - SPEC-file-converter-001

bundle_version: "1.0"
target_platform: null
source_specs:
  - SPEC-file-converter-001
source_planning_sessions:
  - session: PS-2026-01-20-003
    completed: 2026-01-25
archetype: internal-utility
reliability_tier: 4
estimated_effort: "1-2 weeks"
---

# File Format Converter Tool - Handoff Bundle

## Overview

### Vision Statement

Build a simple web-based tool that converts video files between common formats (MP4, MOV, MKV) for internal team use, reducing reliance on individual team members' local tools and ensuring consistent output settings.

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Conversion success rate | >95% | Monitoring logs over first month |
| User adoption | 10+ unique users in first month | Usage analytics |
| Time saved | >1 hour/week team-wide | User survey |

### Stakeholders

| Role | Who | Interest | Authority |
|------|-----|----------|-----------|
| Primary Users | Editorial Team | Need reliable format conversion | Define priority formats |
| Tool Owner | Operations | Maintain and support the tool | Approve feature scope |

### Project Context

This is an internal utility tool (Tier 4 reliability) that addresses a current pain point where team members use inconsistent local tools. It does not integrate with other EFN systems initially.

## Requirements

### Scope

#### In-Scope Requirements

- [REQ-001] Accept MP4, MOV, and MKV file uploads up to 2GB
  - Priority: must-have
  - Rationale: Covers 90%+ of team conversion needs

- [REQ-002] Convert to MP4, MOV, or WebM output formats
  - Priority: must-have
  - Rationale: Most common target formats requested

- [REQ-003] Provide download link for converted file
  - Priority: must-have
  - Rationale: Core functionality

- [REQ-004] Show conversion progress indicator
  - Priority: should-have
  - Rationale: Users need feedback during long conversions

#### Out-of-Scope

- [OUT-001] Audio-only file conversion
  - Reason: Different use case with different requirements
  - Future: May address in Phase 2 if demand exists

- [OUT-002] Batch processing multiple files
  - Reason: Adds complexity; single-file meets initial needs
  - Future: Phase 2 candidate

### Constraints

| Constraint Type | Constraint | Impact |
|-----------------|------------|--------|
| Budget | $0 for external services | Must use open-source tools (FFmpeg) |
| Timeline | 2 weeks to initial deploy | Limits scope to core functionality |
| Technical | Max 2GB file size | Avoids server memory issues |
| Security | EFN SSO required | No anonymous access |

## Decision Ledger

### Active Decisions

| ID | Decision | Rationale | Source |
|----|----------|-----------|--------|
| DEC-001 | Use FFmpeg for conversion | Industry standard, free, handles all required formats | Planning discussion |
| DEC-002 | Temporary file storage (24hr) | Avoids storage costs; users can re-convert if needed | Planning discussion |

### Rejected Alternatives

| Related To | Alternative | Why Rejected |
|------------|-------------|--------------|
| DEC-001 | Cloud conversion service | Budget constraint; also raises data privacy questions |
| DEC-002 | Permanent storage | Storage costs and cleanup complexity not justified |

### Deferred Decisions

| Topic | Deferred Because | Revisit When |
|-------|------------------|--------------|
| Custom encoding presets | Need usage data first | After 1 month of production use |

## Architecture Sketch

### Components

| Component | Purpose | Technology | Owner |
|-----------|---------|------------|-------|
| Web UI | File upload and download interface | React | Builder |
| Conversion Service | Execute FFmpeg conversions | Node.js + FFmpeg | Builder |
| Temp Storage | Hold files during/after conversion | Local filesystem | Builder |

### Component Diagram

```
┌─────────────────┐         ┌─────────────────┐
│    Web UI       │────────>│  Conversion     │
│  (React SPA)    │<────────│  Service        │
└─────────────────┘         └────────┬────────┘
                                     │
                                     v
                            ┌─────────────────┐
                            │  Temp Storage   │
                            │  (filesystem)   │
                            └─────────────────┘
```

### Interfaces

| Interface | Type | Direction | Contract |
|-----------|------|-----------|----------|
| Upload API | REST | In | POST /api/convert with multipart file |
| Status API | REST | Out | GET /api/status/{job-id} returns progress |
| Download API | REST | Out | GET /api/download/{job-id} returns file |

### Data Flows

| Flow Name | Source | Destination | Data Type | Frequency |
|-----------|--------|-------------|-----------|-----------|
| File Upload | Web UI | Conversion Service | Video file | Per conversion |
| Status Poll | Web UI | Conversion Service | JSON | Every 2s during conversion |
| File Download | Temp Storage | Web UI | Video file | Per conversion |

## Acceptance Criteria

### Functional Criteria

- [AC-001] User can upload an MP4, MOV, or MKV file up to 2GB
  - Verification: Test with 500MB and 1.5GB files of each format

- [AC-002] User can select MP4, MOV, or WebM as output format
  - Verification: UI shows format selector; each option produces valid output

- [AC-003] Conversion completes within 10 minutes for a 1GB file
  - Verification: Timed test with 1GB sample file

- [AC-004] Download link remains available for 24 hours
  - Verification: Test download at 1hr and 23hr marks

### Non-Functional Criteria

- [AC-NF-001] Page loads in under 3 seconds
  - Verification: Lighthouse performance audit
  - Target: Performance score >80

- [AC-NF-002] Requires EFN SSO authentication
  - Verification: Attempt access without login; verify redirect
  - Target: 100% of pages protected

### Verification Plan

| Phase | What's Verified | Method | Who |
|-------|-----------------|--------|-----|
| Unit | Individual components work | Automated tests | Builder |
| Integration | Components work together | End-to-end test | Builder |
| User Acceptance | Meets user needs | Stakeholder testing | Editorial Team |

## Work Breakdown

### Implementation Phases

| Phase | Goal | Dependencies | Estimated Effort |
|-------|------|--------------|------------------|
| Phase 1 | Core conversion working | None | 1 week |
| Phase 2 | Polish and deploy | Phase 1 | 3-5 days |

### Phase Details

#### Phase 1: Core Functionality

**Goal**: End-to-end conversion working in development environment

**Tasks**:

- [ ] [TASK-001] Set up Node.js project with FFmpeg integration
  - Inputs: Development environment
  - Outputs: Project skeleton with FFmpeg wrapper
  - Acceptance: Can convert a test file via CLI

- [ ] [TASK-002] Create file upload API endpoint
  - Inputs: Task 001 complete
  - Outputs: POST endpoint accepting multipart upload
  - Acceptance: Can upload 500MB file successfully

- [ ] [TASK-003] Create conversion job processor
  - Inputs: Task 001 complete
  - Outputs: Background job that runs FFmpeg
  - Acceptance: Queued job converts file correctly

- [ ] [TASK-004] Create status and download endpoints
  - Inputs: Task 003 complete
  - Outputs: GET endpoints for status and download
  - Acceptance: Can poll status and download result

- [ ] [TASK-005] Build React upload interface
  - Inputs: Tasks 002-004 complete
  - Outputs: Web page with upload form
  - Acceptance: Can upload via browser

**Phase Exit Criteria**: Can upload, convert, and download a file through the web interface in development

#### Phase 2: Polish and Deploy

**Goal**: Production-ready and deployed

**Tasks**:

- [ ] [TASK-006] Add progress indicator
  - Inputs: Phase 1 complete
  - Outputs: UI shows conversion progress
  - Acceptance: Progress updates during conversion

- [ ] [TASK-007] Integrate SSO authentication
  - Inputs: Phase 1 complete
  - Outputs: All routes require authentication
  - Acceptance: Unauthenticated requests redirect to SSO

- [ ] [TASK-008] Deploy to production
  - Inputs: Tasks 006-007 complete
  - Outputs: Running in production environment
  - Acceptance: Accessible at production URL

- [ ] [TASK-009] Document usage and handoff
  - Inputs: Task 008 complete
  - Outputs: User guide and operations runbook
  - Acceptance: Documentation reviewed by stakeholder

**Phase Exit Criteria**: Tool deployed, authenticated, documented, and handed to operations

### Dependencies

```
TASK-001
   ├── TASK-002
   ├── TASK-003 ── TASK-004 ── TASK-005 (Phase 1 complete)
   │                               │
   │                               ├── TASK-006
   │                               └── TASK-007 ── TASK-008 ── TASK-009
```

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| FFmpeg compatibility issues | Low | Medium | Test all format combinations early |
| Large file handling | Medium | Medium | Implement chunked upload if needed |
| SSO integration complexity | Low | Low | SSO library well-documented |

## Context Pack

### Source Evidence

1. **[T1/S1]** FFmpeg Project. "FFmpeg Documentation". 
   Retrieved 2026-01-25. https://ffmpeg.org/documentation.html
   
   **Relevant excerpt**: FFmpeg supports all required input/output formats (MP4, MOV, MKV, WebM) with comprehensive codec support.

2. **[T2/S2]** Stack Overflow. "Node.js FFmpeg wrapper comparison" (Score: 234). 
   Posted 2024-08-15. Retrieved 2026-01-25. https://stackoverflow.com/questions/example
   
   **Relevant excerpt**: fluent-ffmpeg is the most actively maintained Node.js FFmpeg wrapper.

### Extracted Ground Truth

| Fact | Source | Confidence | Implications |
|------|--------|------------|--------------|
| FFmpeg handles all required formats | [1] | High | No additional tools needed |
| fluent-ffmpeg is recommended wrapper | [2] | Medium | Use as starting point; verify current status |

### Research Artifacts

| Finding ID | Topic | Summary | Link |
|------------|-------|---------|------|
| (none) | - | - | - |

### Freshness Notice

**Bundle created**: 2026-01-28
**Sources validated**: 2026-01-25
**Review recommended if not implemented by**: 2026-04-28
```

---

## Appendix B: Glossary

**Acceptance criteria**: Testable statements that define when implementation is complete.

**Adapter**: A transformation that converts the platform-neutral bundle format to a platform-specific format.

**Base format**: The platform-neutral Markdown format defined in this document.

**Bundle**: A self-contained handoff package containing everything needed for implementation.

**Context pack**: The section of a handoff bundle containing supporting evidence and citations.

**Decision ledger**: The section documenting key choices, rationale, and rejected alternatives.

**Handoff**: The transfer of planning outputs to an implementation platform.

**Implementation platform**: A tool or system that executes work based on handoff bundles (e.g., Claude Code, human developers).

**Phase**: A logical grouping of tasks within a work breakdown.

**Platform-neutral**: A format that doesn't assume any specific implementation platform.

**Task**: An atomic unit of work within a phase.

**Work breakdown**: The section proposing implementation phases and tasks.

---

## Appendix C: Related Documents

- **STD-11-01**: Handoff Bundle Standard (companion document with compliance checklist)
- **DD-12-01**: Repository Structure (where bundles live, naming conventions)
- **DD-13-01**: Artifact Taxonomy (handoff as artifact type, frontmatter schema)
- **DD-14-01**: EFN Ecosystem (archetypes and reliability tiers)
- **DD-18-01**: Questioning Arc (how planning produces handoff content)
- **STD-20-01**: Evidence Standards (citation format for context packs)
- **Compass System Definition**: Authoritative specification (§2.7 Handoff to Implementation)

---

*End of Handoff Bundle Schema Definition (DD-11-01)*
