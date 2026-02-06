---
id: DD-13-01
type: definition
area: 13-artifact-taxonomy
title: Artifact Taxonomy and Documentation Standards
status: draft
created: 2026-01-25
updated: 2026-02-06
author: compass-research
summary: Defines the canonical artifact types, frontmatter schema, lifecycle states, and reconciliation protocols for Compass documentation
tags: [artifacts, taxonomy, documentation, standards, lifecycle]
related:
  - DD-12-01
  - DD-14-01
  - DD-20-01
  - STD-20-01
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
---

# Artifact Taxonomy and Documentation Standards

## Document Purpose

This document establishes the authoritative taxonomy of artifact types, frontmatter schema, lifecycle states, and quality standards for all Compass documentation. Every document in the Compass system conforms to these standards.

**Why this matters**: Consistent artifact structure enables both humans and LLM agents to find, understand, and maintain documentation effectively. Without clear standards, documentation drifts into inconsistency, becomes harder to retrieve, and loses its value as a source of truth.

**Audience**: Anyone creating, reviewing, or maintaining Compass artifacts.

---

## Part 1: Artifact Type Catalog

Compass recognizes eight canonical artifact types. Each serves a distinct purpose in the planning-to-implementation pipeline.

### 1.1 Overview

| Type | Prefix | Purpose | When to Create |
|------|--------|---------|----------------|
| **Specification** | SPEC- | Defines what to build | Before any new feature or significant change |
| **Architecture Decision Record** | ADR- | Captures why a decision was made | When choosing between meaningful options |
| **Research Brief** | RB- | Defines a research task | When investigation is needed |
| **Research Finding** | RF- | Documents investigation results | When research completes |
| **Definition Document** | DD- | Establishes foundational concepts | When defining taxonomies, frameworks, or core concepts |
| **Standard** | STD- | Establishes enforceable conventions | When a practice must be consistently followed |
| **Handoff Bundle** | HANDOFF- | Packages context for implementation | When work transfers to an implementation platform |
| **Index** | IDX- | Provides navigation and cross-references | When organizing related artifacts |

### 1.2 Type Definitions

#### Specification (SPEC-)

**Purpose**: Implementation-ready instructions that tell an LLM agent or developer exactly what to build.

**Content includes**:
- Clear objective (what and why)
- Success criteria (testable outcomes)
- Technical requirements (stack, dependencies, constraints)
- Boundaries (always/ask first/never rules)
- Acceptance criteria

**Relationships**:
- May reference ADRs for decision rationale
- May be derived from Research Findings
- Produces Handoff Bundles when ready for implementation
- Updated through reconciliation after implementation

**Owner**: The person who will verify implementation meets the spec.

---

#### Architecture Decision Record (ADR-)

**Purpose**: Captures why a decision was made, including alternatives considered and rejected.

**Content includes**:
- Context (what forces required a decision)
- Options considered (at least 2, including "do nothing")
- Evaluation criteria
- Chosen option with rationale
- Consequences (positive, negative, neutral)

**Relationships**:
- Referenced by Specifications that implement the decision
- May supersede earlier ADRs
- Informed by Research Findings

**Owner**: The decision maker(s).

**Key principle**: ADRs are never deleted or overwritten. When a decision changes, create a new ADR that supersedes the old one. This preserves the decision history.

---

#### Research Brief (RB-)

**Purpose**: Defines a research task before investigation begins. Sets scope, questions, and success criteria.

**Content includes**:
- Research question(s)
- Scope and boundaries
- Success criteria (what would constitute a useful answer)
- Time box (how long to spend)
- Expected output format

**Relationships**:
- Produces Research Findings when complete
- May be triggered by Specifications or ADRs that need more information

**Owner**: The person requesting the research.

---

#### Research Finding (RF-)

**Purpose**: Documents the results of an investigation with explicit confidence levels and limitations.

**Content includes**:
- Executive summary
- Methodology
- Findings with confidence levels
- Limitations
- Implications for decision-making
- Sources with quality notes

**Relationships**:
- Responds to a Research Brief
- Informs ADRs and Specifications
- Must follow evidence standards in DD-20-01 and STD-20-01

**Owner**: The researcher.

---

#### Definition Document (DD-)

**Purpose**: Establishes foundational concepts, taxonomies, or frameworks that other artifacts reference.

**Content includes**:
- Concept definitions
- Taxonomies or categorizations
- Frameworks for thinking about a domain
- Rationale for the chosen structure

**Relationships**:
- Referenced by many other artifacts
- Often paired with a Standard (STD-) that makes the definitions enforceable
- Updated rarely; stability is a virtue

**Owner**: Typically a senior builder or the person who established the concept.

**Examples**: This document (DD-13-01) is a Definition Document. DD-14-01 (EFN Ecosystem) is another.

---

#### Standard (STD-)

**Purpose**: Establishes enforceable conventions, patterns, or rules that must be consistently followed.

**Content includes**:
- What the standard requires
- Rationale (why this standard exists)
- Compliance criteria (how to know if you're following it)
- Examples of correct application
- Common mistakes to avoid

**Relationships**:
- Often companions to Definition Documents
- Referenced by Specifications for required practices
- Checked during reviews

**Owner**: The team collectively; changes require broader review.

**Examples**: STD-14-01 (EFN Compliance Checklist), STD-20-01 (Evidence Citation Standards).

---

#### Handoff Bundle (HANDOFF-)

**Purpose**: Packages everything an implementation platform needs to execute work.

**Content includes**:
- Overview (vision, success metrics, stakeholders)
- Requirements (scope, out-of-scope, constraints)
- Decision ledger (relevant ADRs)
- Architecture sketch
- Acceptance criteria
- Work breakdown
- Context pack (sources, citations)

**Relationships**:
- Derived from Specifications and ADRs
- Consumed by implementation platforms (coding agents, development tools)
- Feedback flows back via reconciliation

**Owner**: The person handing off the work.

---

#### Index (IDX-)

**Purpose**: Provides navigation and cross-references across related artifacts.

**Content includes**:
- Document listings with summaries
- Status tracking
- Cross-reference tables
- Recently updated sections

**Relationships**:
- References all artifact types
- Lives in `indexes/` folder or as INDEX.md in artifact folders

**Owner**: Maintained collectively; anyone can update.

**Examples**: COMPASS-00-REFERENCE-INDEX.md, folder-level INDEX.md files.

---

### 1.3 Type Selection Guide

When creating a new document, use this decision tree:

```
Is this defining WHAT to build?
    YES → Specification (SPEC-)
    NO ↓

Is this explaining WHY a choice was made?
    YES → Architecture Decision Record (ADR-)
    NO ↓

Is this defining a TASK for investigation?
    YES → Research Brief (RB-)
    NO ↓

Is this reporting RESULTS of investigation?
    YES → Research Finding (RF-)
    NO ↓

Is this establishing FOUNDATIONAL CONCEPTS?
    YES → Definition Document (DD-)
    NO ↓

Is this setting ENFORCEABLE RULES?
    YES → Standard (STD-)
    NO ↓

Is this PACKAGING WORK for implementation?
    YES → Handoff Bundle (HANDOFF-)
    NO ↓

Is this providing NAVIGATION across documents?
    YES → Index (IDX-)
    NO → Reconsider if this needs to be a formal artifact
```

---

## Part 2: Frontmatter Schema

Every Compass artifact has YAML frontmatter that provides metadata for both humans and retrieval systems.

### 2.1 Universal Fields (Required on All Artifacts)

```yaml
---
id: "SPEC-auth-001"              # Unique identifier, never reused
type: spec                       # spec | adr | rb | rf | dd | std | handoff | idx
area: "01-backend"               # Research area code (optional for some types)
title: "OAuth2 Authentication Flow"
status: draft                    # draft | review | active | deprecated (ADRs may also use: proposed | accepted)
created: 2026-01-25
updated: 2026-01-25
author: "jsmith"                 # Primary author or "compass-research" for generated
summary: "Defines OAuth2 login with JWT refresh tokens for the broadcast tools API"
tags: ["authentication", "security", "api", "broadcast-tools"]
related:
  - "ADR-0012"                   # Links to related artifacts by ID
  - "RF-01-03"
---
```

**Field definitions:**

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier following prefix conventions. Never reuse IDs. |
| `type` | Yes | One of: spec, adr, rb, rf, dd, std, handoff, idx |
| `area` | Sometimes | Research area code. Required for RF, RB, DD, STD. Optional for others. |
| `title` | Yes | Human-readable title |
| `status` | Yes | Current lifecycle state (see Part 3) |
| `created` | Yes | Date created (YYYY-MM-DD) |
| `updated` | Yes | Date last modified (YYYY-MM-DD) |
| `author` | Yes | Primary author username or "compass-research" |
| `summary` | Yes | Single sentence describing what this document covers |
| `tags` | Yes | Array of relevant keywords for search and filtering |
| `related` | Yes | Array of related artifact IDs (can be empty: `[]`) |

### 2.1a Optional Fields for LLM Views

LLM views are derived, LLM-optimized versions of canonical artifacts. When `view: llm` is present, include the following fields:

```yaml
view: llm                      # Marks this artifact as an LLM view
source_id: "DD-12-01"           # Canonical artifact ID
source_updated: 2026-01-25      # Last updated date of the canonical artifact
staleness: fresh                # fresh | review | stale
```

**ID convention for LLM views:** Append `-LLM` to the source artifact ID (for example, `DD-12-01-LLM`). This preserves lineage and keeps IDs unique.

**Validation note:** If `view: llm` is present, `source_id`, `source_updated`, and `staleness` are required.

### 2.1b Structured Cross-Links (Optional)

Artifacts may include a structured `links` array to encode typed relationships between documents. This is the preferred structured cross-linking mechanism; the legacy `related` list remains for broad associations.

**Schema:**

```yaml
links:
  - rel: companion
    target_id: "STD-14-01"
    note: "Compliance checklist for this definition"
  - rel: informed_by
    target_id: "RF-02-01"
    target_section: "Executive Summary"
```

**Required fields:**
- `rel` (enum): Relationship type
- `target_id` (string): Target artifact ID

**Optional fields:**
- `target_section` (string): Section name in the target document
- `target_doc` (string): Alternate file name if needed
- `note` (string): Short explanation of the relationship
- `strength` (string): Qualifier such as `primary` or `secondary`

**Allowed `rel` values:**
`related`, `companion`, `responds_to`, `implications_for`, `informed_by`, `supersedes`, `superseded_by`, `implements`, `depends_on`, `blocks`, `references`, `contradicts`, `duplicates`

### 2.2 Type-Specific Fields

**Specifications (SPEC-)** add:

```yaml
implements: "FEATURE-AUTH-001"   # What feature/requirement this implements
prerequisites: ["SPEC-db-001"]   # Must be implemented first
boundaries:
  always:
    - "Run tests before commits"
    - "Use existing auth components"
  ask_first:
    - "New dependencies"
    - "Schema changes"
  never:
    - "Modify core auth without security review"
acceptance_criteria:
  - "User can log in via OAuth2 provider"
  - "Refresh tokens extend session without re-login"
  - "Invalid tokens return 401 with clear error message"
```

**Architecture Decision Records (ADR-)** add:

```yaml
decision_date: 2026-01-20        # When decision was finalized (null if proposed)
deciders: ["jsmith", "mjones"]   # Who made the decision
supersedes: "ADR-0003"           # If replacing an earlier decision
```

**Research Findings (RF-)** add:

```yaml
confidence: moderate             # high | moderate | low | very_low
methodology: "Comparative analysis of 12 vendor solutions"
limitations:
  - "Limited to English-language sources"
  - "No hands-on testing"
responds_to: "RB-03-01"          # Research Brief this responds to
implications_for: ["ADR-03-01", "SPEC-memory-001"]
```

**Research Briefs (RB-)** add:

```yaml
time_box: "4 hours"              # Maximum time to spend
questions:
  - "What memory solutions support temporal queries?"
  - "What are the cost implications at our scale?"
success_criteria:
  - "Identify at least 3 viable options"
  - "Compare on cost, complexity, and capabilities"
```

**Standards (STD-)** add:

```yaml
companion: "DD-14-01"            # Definition document this enforces
enforcement: "PR review checklist"
```

**Handoff Bundles (HANDOFF-)** add:

```yaml
target_platform: "Claude Code"   # Intended execution platform
source_specs:
  - "SPEC-auth-001"
  - "SPEC-auth-002"
```

### 2.3 Frontmatter Validation

Every artifact must pass these validation rules:

- [ ] `id` is unique across all artifacts
- [ ] `id` follows the correct prefix for its type
- [ ] `type` is a valid type value
- [ ] `status` is a valid status value
- [ ] `created` and `updated` are valid dates
- [ ] `updated` is not before `created`
- [ ] `summary` is a single sentence (no line breaks)
- [ ] `tags` is an array with at least one tag
- [ ] `related` is an array (can be empty)
- [ ] Type-specific required fields are present

### 2.4 Document ID Naming Convention

Document IDs follow a structured format that encodes document type, domain area, and version:

**Format**: `{TYPE}-{AREA}-{VERSION}`

| Component | Description | Format |
|-----------|-------------|--------|
| **TYPE** | Document type prefix | Uppercase letters (e.g., DD, RF, ADR, STD, SPEC) |
| **AREA** | Domain area code | Two-digit number (01–99) |
| **VERSION** | Document version | Two-digit number starting at 01 |

**Examples**:

| ID | Breakdown | Meaning |
|----|-----------|---------|
| `DD-14-01` | DD / 14 / 01 | Definition Document, area 14 (EFN Ecosystem), version 1 |
| `RF-09-01` | RF / 09 / 01 | Research Finding, area 09 (LLM Provider), version 1 |
| `ADR-01-01` | ADR / 01 / 01 | Architecture Decision Record, area 01 (Backend), version 1 |
| `STD-20-01` | STD / 20 / 01 | Standard, area 20 (Evidence), version 1 |

**Versioning rules**:

- **VERSION-01** indicates the first major version of a document
- When a document is superseded, the replacement receives VERSION-02, VERSION-03, etc.
- Minor updates to an active document do NOT increment the version; use the `updated` frontmatter field instead
- Version increments only when a document is formally superseded (see Part 5.3)

**Special cases**:

- **System documents** (SYS-00) use `00` as the area code
- **Index documents** (IDX-00) use `00` as the area code
- **Specifications** (SPEC-) may use descriptive identifiers instead of area codes (e.g., `SPEC-auth-001`)
- **Handoff bundles** (HANDOFF-) typically use project or feature identifiers

**Area code registry**: See IDX-00-MASTER § Quick Lookup Tables for the complete list of area codes (01–20).

---

## Part 3: Lifecycle States

### 3.1 The Four-State Model

Compass uses four lifecycle states with clear meanings and transition rules:

```
                 ┌─────────────────────────────────────────────┐
                 │                                             │
    ┌────────┐   │   submit    ┌────────┐   approve   │   ┌────────┐
    │ DRAFT  │───┼────────────►│ REVIEW │─────────────┼──►│ ACTIVE │
    └────────┘   │             └────────┘             │   └────────┘
         ▲       │                  │                 │        │
         │       │    request       │                 │        │
         │       │    changes       │                 │        │ supersede
         └───────┼──────────────────┘                 │        │ or retire
                 │                                    │        ▼
                 │                                    │   ┌────────────┐
                 └────────────────────────────────────┘   │ DEPRECATED │
                                                          └────────────┘
```

### 3.2 State Definitions

| State | Meaning | Who Can See | Can Reference |
|-------|---------|-------------|---------------|
| **draft** | Work in progress, not ready for use | Authors and reviewers | No—don't reference drafts |
| **review** | Complete, awaiting peer evaluation | All team members | Cautiously, noting "pending review" |
| **proposed** | (ADR-specific) Decision documented, awaiting evaluation | All team members | Cautiously, noting "proposed decision" |
| **active** | Approved and authoritative | Everyone | Yes—this is the source of truth |
| **accepted** | (ADR-specific) Decision finalized and authoritative | Everyone | Yes—this is the source of truth |
| **deprecated** | Superseded or retired, preserved for history | Everyone | Only for historical context |

**Decision status vs. artifact status**: The lifecycle states defined here (draft, review, active, deprecated) apply to *artifacts*—the documents that record decisions, requirements, and specifications. These are distinct from *decision statuses* (EXPLORING, ENABLED, BLOCKED, CHOSEN, REJECTED, DEFERRED), which track a decision's progress within a planning arc. An ADR artifact can be in `active` status while the decision it records is still `EXPLORING`. See DD-18-01 §2.2 for the decision status lifecycle.

### 3.3 Transition Rules

| From | To | Trigger | Who | Required Actions |
|------|-----|---------|-----|------------------|
| (new) | draft | Create document | Anyone | Complete frontmatter |
| draft | review | Submit for review | Author | Pass validation, request reviewer |
| review | draft | Request changes | Reviewer | Document what needs work |
| review | active | Approve | Reviewer (not author) | Verify completeness, set `updated` date |
| active | deprecated | Supersede or retire | Author or team | Link to replacement (if any), document reason |
| deprecated | (none) | — | — | Deprecated is final |

**Key rules:**
- No self-approval: someone other than the author must approve
- No skipping review: drafts cannot go directly to active
- No deletion: deprecated documents remain in the repository
- No resurrection: deprecated documents stay deprecated; create new documents instead

### 3.4 Living Documents

Some documents (like Standards and Definitions) remain in `active` status for long periods while receiving updates. For these:

- Use `updated` date to track changes
- Document significant changes in a changelog section
- Consider version numbering for major revisions
- Don't change status just because content was updated

### 3.5 ADR-Specific Status Values

Architecture Decision Records (ADRs) use domain-specific status terminology that maps to the general lifecycle model:

| ADR Status | Equivalent | Meaning |
|------------|------------|---------|
| **draft** | draft | Decision being researched and documented |
| **proposed** | review | Decision documented, awaiting stakeholder evaluation |
| **accepted** | active | Decision finalized and authoritative |
| **deprecated** | deprecated | Decision superseded or retired |

**ADR Transition Rules:**

| From | To | Trigger | Required Actions |
|------|-----|---------|------------------|
| draft | proposed | Author completes decision documentation | All options evaluated, recommendation stated |
| proposed | draft | Stakeholder requests changes | Document feedback |
| proposed | accepted | Stakeholder approval | Set `decision_date`, record `deciders` |
| accepted | deprecated | New decision supersedes | Link to replacement via `superseded_by` |

**Why different terminology?**

ADR conventions follow industry standards (MADR, Documenting Architecture Decisions). The terms `proposed` and `accepted` communicate decision-specific meaning: a "proposed" decision is actively under consideration, while an "accepted" decision has been formally adopted. This aligns with how ADRs are used in the broader software engineering community.

---

## Part 4: Definition of Done

Each artifact type has specific completeness criteria that must be satisfied before moving to `active` status.

### 4.1 Specification Definition of Done

- [ ] Clear objective stated in first paragraph
- [ ] Success criteria are testable (can determine pass/fail)
- [ ] Technical requirements specify stack, dependencies, constraints
- [ ] Boundaries section defines Always/Ask First/Never rules
- [ ] At least one peer has reviewed and approved
- [ ] Related ADRs linked for any non-obvious decisions
- [ ] Code examples are complete and runnable (not pseudocode)
- [ ] Acceptance criteria can be verified

### 4.2 ADR Definition of Done

- [ ] Context explains what forces require a decision
- [ ] At least 2 alternatives considered (including "do nothing" if applicable)
- [ ] Each alternative lists pros and cons
- [ ] Chosen option clearly stated with reasoning
- [ ] Consequences (positive and negative) documented
- [ ] Links to superseded decisions (if any)
- [ ] Decision date and deciders recorded

### 4.3 Research Brief Definition of Done

- [ ] Research question(s) clearly stated
- [ ] Scope defines what's in and out of bounds
- [ ] Time box specified
- [ ] Success criteria describe what a useful answer looks like
- [ ] Expected output format specified

### 4.4 Research Finding Definition of Done

- [ ] Executive summary captures key findings in 3-5 bullets
- [ ] Confidence level explicitly stated with rationale
- [ ] Methodology explains how research was conducted
- [ ] Sources follow evidence standards (DD-20-01, STD-20-01)
- [ ] Limitations section acknowledges gaps
- [ ] Implications for decision-making stated
- [ ] Responds to a Research Brief (linked in frontmatter)

### 4.5 Definition Document Definition of Done

- [ ] Scope clearly defined (what this defines)
- [ ] All key terms defined
- [ ] Structure/taxonomy is complete and consistent
- [ ] Rationale explains why this structure was chosen
- [ ] Examples demonstrate application
- [ ] Cross-references to related documents

### 4.6 Standard Definition of Done

- [ ] Scope clearly defined (what this applies to)
- [ ] Rationale explains why this standard exists
- [ ] Requirements are specific and actionable
- [ ] Compliance criteria explain how to verify conformance
- [ ] Examples demonstrate correct application
- [ ] Non-examples clarify common mistakes
- [ ] Enforcement mechanism specified

### 4.7 Handoff Bundle Definition of Done

- [ ] Overview explains vision, success metrics, stakeholders
- [ ] All source specifications linked and summarized
- [ ] Relevant ADRs included with key decisions highlighted
- [ ] Architecture sketch shows components and data flow
- [ ] Acceptance criteria listed with verification approach
- [ ] Work breakdown provides actionable tasks
- [ ] Context pack includes necessary sources and citations

### 4.8 Index Definition of Done

- [ ] All relevant artifacts listed
- [ ] Status is current for each entry
- [ ] Summaries accurately describe each artifact
- [ ] Navigation structure is logical
- [ ] Recently updated section reflects actual recent changes

---

## Part 5: Reconciliation Protocol

When implementation diverges from specification, Compass uses a reconciliation protocol to keep documentation aligned with reality.

### 5.1 When to Reconcile

Reconciliation is required:
- After any implementation completes
- When discovering that implementation differs from spec
- When operational experience reveals spec inadequacies
- When merging learnings from related projects

### 5.2 Reconciliation Process

**Step 1: Identify Deltas**

Compare specification to implementation and document each difference:

| Section | Spec Said | Implementation Does | Classification |
|---------|-----------|---------------------|----------------|
| Token expiry | 1 hour | 30 minutes | Spec improvement |
| Error format | JSON only | JSON + human message | Agent enhancement |
| Rate limiting | Not specified | 100 req/min | Gap in spec |

**Step 2: Classify Each Delta**

| Classification | Meaning | Resolution |
|----------------|---------|------------|
| **Spec error** | Spec was wrong or incomplete | Update spec to match correct implementation |
| **Implementation error** | Code doesn't match valid spec | Fix implementation (not a doc issue) |
| **Agent enhancement** | Agent made valid improvement | Update spec; consider for standards |
| **Gap in spec** | Spec didn't address this | Update spec; improve templates |
| **Acceptable deviation** | Different but equally valid | Document in spec as "implementation notes" |

**Step 3: Update Artifacts**

For each delta requiring documentation update:
1. Update the specification with new information
2. If the change affects decisions, update or create ADRs
3. If the change reveals patterns, consider updating standards
4. Update `updated` date in frontmatter
5. Note the reconciliation in commit message

**Step 4: Record the Reconciliation**

Add a reconciliation record to the specification:

```markdown
## Reconciliation History

### 2026-01-25: Post-implementation reconciliation

**Spec**: SPEC-auth-001
**Implementation**: PR #247, merged 2026-01-24
**Reconciled by**: jsmith

| Delta | Classification | Resolution |
|-------|----------------|------------|
| Token expiry reduced to 30min | Agent enhancement | Spec updated |
| Rate limiting added | Gap in spec | Spec updated |
| Error format enhanced | Agent enhancement | Spec updated, ADR-0015 created |
```

### 5.3 When to Update vs. Supersede

**Update the existing document when:**
- Changes are additive (new information, not contradictions)
- Less than 50% of content changes
- The document's core purpose remains unchanged

**Create a new document (supersede) when:**
- Core architecture or approach fundamentally changes
- The old version must be preserved for active reference
- Multiple implementations exist targeting different versions
- Major version increment is appropriate

When superseding:
1. Create new document with new ID
2. Set old document status to `deprecated`
3. Add `superseded_by` to old document's frontmatter
4. Add `supersedes` to new document's frontmatter

---

## Part 6: Templates

### 6.1 Specification Template

```markdown
---
id: "SPEC-{project}-{feature}"
type: spec
title: "[Feature name]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "[username]"
summary: "[One sentence: what this enables users to do]"
tags: []
related: []
implements: "[Feature/requirement ID]"
prerequisites: []
boundaries:
  always: []
  ask_first: []
  never: []
acceptance_criteria: []
---

# [Feature name]

## Objective

[What are we building and why? User-centric framing. 2-3 sentences.]

## Success Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## Technical Requirements

### Stack and Dependencies

- [Framework/library versions]
- [External services]

### Data Model

[If applicable, describe data structures]

### API Surface

[If applicable, describe endpoints/interfaces]

## Implementation Guidance

### Approach

[High-level implementation strategy]

### Code Examples

```[language]
// Minimal working example showing expected patterns
```

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| [Edge case 1] | [Behavior] |

## Boundaries

### Always

- [Mandatory practice 1]

### Ask First

- [Requires human approval]

### Never

- [Prohibited action]

## Related Documents

- [Link to ADR explaining key decisions]
- [Link to related specs]

## Reconciliation History

[Added after implementation; see Part 5]
```

### 6.2 ADR Template

```markdown
---
id: "ADR-{NNNN}"
type: adr
title: "[Decision title as action phrase]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "[username]"
summary: "[One sentence: what we decided and why it matters]"
tags: []
related: []
decision_date: null
deciders: []
supersedes: null
---

# [Decision title]

## Status

[Draft | Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

[What forces are at play? What problem needs solving?
Factual, neutral tone. 2-4 sentences.]

## Options Considered

### Option 1: [Name]

[Brief description]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]

### Option 2: [Name]

[Brief description]

**Pros:**
- [Advantage 1]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

### Option 3: Do Nothing

**Pros:**
- No implementation effort

**Cons:**
- [Why this doesn't work]

## Decision

We will use **[Option N]** because [primary reason].

[Additional reasoning if needed, 1-2 sentences.]

## Consequences

### Positive

- [Good outcome 1]
- [Good outcome 2]

### Negative

- [Trade-off or risk we accept]

### Neutral

- [Side effect that's neither good nor bad]

## Related Documents

- Supersedes: [ADR-NNNN] (if applicable)
- Informs: [SPEC-xxx, SPEC-yyy]
```

### 6.3 Research Finding Template

```markdown
---
id: "RF-{area}-{NN}"
type: rf
area: "{area-code}"
title: "[Research question as statement]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "[username]"
summary: "[One sentence: key finding]"
tags: []
related: []
confidence: moderate
methodology: "[Brief description]"
limitations: []
responds_to: "RB-{area}-{NN}"
implications_for: []
---

# [Research question]

## Executive Summary

- [Key finding 1]
- [Key finding 2]
- [Key finding 3]
- [Primary implication/recommendation]

## Confidence Assessment

**Overall confidence**: [High | Moderate | Low | Very Low]

**Rationale**: [1-2 sentences explaining why this confidence level]

## Context and Question

[Why was this research needed? What question does it answer? 2-3 sentences.]

## Methodology

**Approach**: [How research was conducted]
**Sources**: [Key sources with quality notes]
**Time period**: [When research was conducted]

## Findings

### Finding 1: [Statement]

**Evidence**: [Supporting data/sources per STD-20-01]
**Confidence**: [H/M/L]

### Finding 2: [Statement]

**Evidence**: [Supporting data/sources per STD-20-01]
**Confidence**: [H/M/L]

## Limitations

- [Limitation 1 and its impact on findings]
- [Limitation 2 and its impact on findings]
- [What this research does NOT address]

## Implications for Decision-Making

✓ This research supports: [Decision/action]
✗ This research does NOT support: [Decision/action]

## Open Questions

- [Question requiring further research]

## Sources

[Follow citation format per STD-20-01]

1. [Source with reliability tier and quality note]
2. [Source with reliability tier and quality note]
```

### 6.4 Standard Template

```markdown
---
id: "STD-{area}-{NN}"
type: std
area: "{area-code}"
title: "[Standard name]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "[username]"
summary: "[One sentence: what this standard ensures]"
tags: []
related: []
companion: "[DD-xx-xx if applicable]"
enforcement: "[How compliance is verified]"
---

# [Standard name]

## Purpose

[Why this standard exists. What problem it solves. 2-3 sentences.]

## Scope

**Applies to**: [What artifacts, tools, or processes this covers]
**Does not apply to**: [Explicit exclusions]

## Requirements

### Requirement 1: [Name]

[Specific, actionable requirement]

**Rationale**: [Why this is required]

### Requirement 2: [Name]

[Specific, actionable requirement]

**Rationale**: [Why this is required]

## Compliance Checklist

- [ ] [Verifiable criterion 1]
- [ ] [Verifiable criterion 2]
- [ ] [Verifiable criterion 3]

## Examples

### Correct Application

[Example showing proper compliance]

### Common Mistakes

[Example showing what NOT to do and why]

## Enforcement

[How and when compliance is checked]

## Related Documents

- Companion definition: [DD-xx-xx]
- Related standards: [STD-xx-xx]
```

---

## Appendix A: Glossary

**Active**: Lifecycle state indicating an artifact is approved and authoritative.

**ADR (Architecture Decision Record)**: Document capturing why a decision was made, including alternatives considered.

**Artifact**: A versioned document the system treats as truth.

**Boundaries**: Rules defining what an implementation always/ask first/never does.

**Definition of Done**: Completeness criteria that must be satisfied before an artifact can become active.

**Delta**: A difference between specification and implementation discovered during reconciliation.

**Deprecated**: Lifecycle state indicating an artifact is no longer authoritative but preserved for history.

**Draft**: Lifecycle state indicating work in progress.

**Frontmatter**: YAML metadata at the beginning of a document.

**Lifecycle state**: One of: draft, review, active, deprecated.

**Reconciliation**: The process of updating documentation to match implementation reality.

**Review**: Lifecycle state indicating an artifact is complete and awaiting approval.

**Supersede**: To replace an artifact with a newer version while preserving the original.

---

## Appendix B: Related Documents

- **DD-12-01**: Repository structure and organization standards
- **DD-14-01**: EFN tooling ecosystem requirements
- **DD-20-01**: Evidence standards for citations and sources
- **STD-20-01**: Evidence citation format specification
- **Compass System Definition**: Authoritative system specification

---

*End of Artifact Taxonomy and Documentation Standards (DD-13-01)*
