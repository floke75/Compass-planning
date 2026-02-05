# Integration Plan: Restore Planning Flow Details

**Status**: Agreed — ready for implementation
**Date**: 2026-02-05
**Scope**: DD-18-01, STD-18-01, SYS-00, DD-15-01, DD-13-01, IDX-00-MASTER, new DD-18-02, and corresponding LLM views

---

## Context

Key aspects of the planning phase were lost while detailing the rest of the system. This plan restores those aspects — particularly around decision dependency tracking, Git-like exploration branching, decision status lifecycle, the Archivist subsystem, elicitation method guidance, and user-controlled fast mode. Each change below reflects an agreed-upon decision.

Each change includes a **Required Context** block listing the exact document sections the implementation LLM must read before making that change. These are designed to be grep-able: use the file path and section heading to locate the content without loading entire documents.

---

## Change 1: Decision Dependency Types

**Document**: DD-18-01 (new section, after current Part 1)
**Nature**: New content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 1: The Five-Stage Planning Workflow (§1.1–1.3) | Understand stage flow; new section follows this |
| `DD-18-01-questioning-arc.md` | Part 2: Research Branching and Merge Gates (§2.1–2.4) | Dependencies affect branch and merge logic |
| `DD-18-01-questioning-arc.md` | Part 5: Integration Points (§5.1–5.3) | How arc integrates with widgets, artifacts, governance |
| `DD-13-01-artifacts-definitions.md` | Part 2 §2.1b: Structured Cross-Links | Understand artifact-level `links` and allowed `rel` values — the new decision dependencies are distinct from these |
| `STD-18-01-questioning-arc-standards.md` | Appendix A: Validation Rule Reference | Naming pattern (BRANCH-NNN, OPEN-NNN etc.) for new validation rules |

### What to Write

Add a section defining five typed relationships between decisions that the arc state machine uses during planning:

| Type | Semantics | Example |
|------|-----------|---------|
| DEPENDS_ON | Hard prerequisite — can't finalize X without Y resolved | DB schema depends on hosting choice |
| ENABLES | Unlocks options — choosing X makes Y possible | Choosing AWS enables Lambda |
| BLOCKS | Eliminates options — choosing X makes Y impossible | Choosing serverless blocks VMs |
| CONFLICTS_WITH | Mutually exclusive — X and Y can't both be CHOSEN | OAuth conflicts with custom auth |
| INFORMS | Soft influence — X makes Y more or less likely | Budget informs scope ambition |

The section must clarify:
- These are **decision-to-decision** relationships within a planning workflow, distinct from DD-13-01's artifact-to-artifact `links` (which handle document navigation)
- Dependencies are recorded as decisions are captured during the arc
- The system warns when a user tries to finalize a decision whose DEPENDS_ON targets are unresolved
- BLOCKS and CONFLICTS_WITH relationships surface automatically when a choice eliminates options
- Dependencies form a directed graph; cycles are invalid and must be detected (Archivist responsibility — see Change 4)

**Also update**: STD-18-01 — add validation rules to Appendix A:
- DEPEND-001: No dependency cycles permitted (Block)
- DEPEND-002: DEPENDS_ON targets must be resolved before dependent decision is CHOSEN (Block)
- DEPEND-003: CONFLICTS_WITH relationships surfaced before CHOSEN (Warn)

---

## Change 2: Decision Status Lifecycle

**Document**: DD-18-01 (new section, adjacent to Change 1)
**Nature**: New content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-13-01-artifacts-definitions.md` | Part 3: Lifecycle States (§3.1–3.3) | The artifact lifecycle this is distinct from |
| `DD-13-01-artifacts-definitions.md` | Part 3 §3.5: ADR-Specific Status Values | Precedent for type-specific status terminology layered on the base model |
| `DD-18-01-questioning-arc.md` | Part 5 §5.2: Artifact System (DD-13-01) | How the arc currently creates/updates artifacts at each stage |
| `STD-18-01-questioning-arc-standards.md` | Part 1 §1.5: GROUND Stage Completion | The final stage completion criteria that the new STATUS-003 rule ties into |

### What to Write

Add a decision-level status lifecycle that is **separate from** DD-13-01's artifact lifecycle (`draft → review → active → deprecated`). Decisions within a planning arc progress through:

```
EXPLORING ──→ CHOSEN
    │             │
    │             └──→ (arc complete)
    │
    ├──→ REJECTED (explicit, with rationale)
    │
    ├──→ BLOCKED (by another decision via BLOCKS dependency)
    │
    ├──→ DEFERRED (postponed to a later phase)
    │
    └──→ ENABLED (unlocked by another decision via ENABLES dependency)
              │
              └──→ EXPLORING (when user begins considering it)
```

Key points to document:
- An artifact (ADR) can be in `active` status while the decision it records is `EXPLORING` — these are different systems
- Status transitions are triggered by: user action (EXPLORING → CHOSEN/REJECTED/DEFERRED), dependency resolution (→ ENABLED or → BLOCKED), and merge gate results
- The Archivist validates consistency: a CHOSEN decision must not have unresolved DEPENDS_ON dependencies; a BLOCKED decision cannot be CHOSEN without resolving the blocking relationship first
- Status history is preserved — a decision that was EXPLORING, then BLOCKED, then ENABLED, then CHOSEN retains that full history for audit

**Also update**: STD-18-01 Appendix A — add validation rules:
- STATUS-001: CHOSEN requires all DEPENDS_ON targets resolved (Block)
- STATUS-002: BLOCKED decisions cannot transition to CHOSEN without resolving blocker (Block)
- STATUS-003: All must-have decisions must reach CHOSEN or DEFERRED before GROUND completion (Block)

**Also update**: DD-13-01 Part 3 (Lifecycle States) — add a short clarifying note (a paragraph and cross-reference) explicitly distinguishing artifact status from decision status, referencing DD-18-01 for the latter.

### Required Context for DD-13-01 Update

| File | Section | Why |
|------|---------|-----|
| `DD-13-01-artifacts-definitions.md` | Part 3 §3.2: State Definitions | Where to insert the clarifying note |

---

## Change 3: Git-Like Exploration Branching (Major Rewrite)

**Document**: DD-18-01 Part 3 (Exploration Branching) — substantial rewrite
**Nature**: Rewrite and expansion of existing content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 3: Exploration Branching (§3.1–3.3) | The current content being rewritten — understand what to preserve |
| `DD-18-01-questioning-arc.md` | Part 2: Research Branching and Merge Gates (§2.1–2.4) | The Research vs. Exploration distinction table to keep |
| `DD-18-01-questioning-arc.md` | Part 4: State Management (§4.1–4.4) | State serialization and isolation — branching depends on snapshotting state |
| `DD-19-01-widget-schema.md` | Part 8 §8.4: Merge Gate widget schema | The merge-gate widget JSON schema — branch merge UI is built on this |
| `STD-18-01-questioning-arc-standards.md` | Part 3: Merge Gate Standards (§3.1–3.4) | Merge gate content requirements and logging — branching must satisfy these |
| `DD-15-01-governance-definitions.md` | Part 3 §3.2: Merge Gate Workflow | Governance perspective on who can approve merges |

### What to Write

The current Part 3 describes exploration branches as "parallel planning paths." Rewrite to describe a Git-like branching model where users can fork, build out, and merge entire planning states. This is the most significant change in this plan.

**3.1 — Fork (Time Travel)**

A user can navigate back to any prior decision point in the planning history and create a fork. The system:
- Restores the full context/memory state as it was at that decision point
- Creates a new branch from that snapshot
- The branch proceeds independently from that point forward

The key insight: the user isn't just "comparing two options" — they're replaying planning from a different starting assumption. If they chose PostgreSQL on main but want to explore MongoDB, the fork restores the state *before* the database decision and lets them make a different choice. All downstream decisions (ORM selection, schema design, query patterns) then play out under the new assumption.

**3.2 — Branch Divergence**

As the branch progresses, decisions accumulate that may differ from main. The system tracks:
- Decisions shared with main (made before the fork point)
- Decisions unique to the branch (made after fork, potentially different from main)
- Decision dependencies that cross the fork boundary

**3.3 — Merge and Conflict Detection**

When a branch is ready to merge back into main, the system (via the Archivist) performs impact analysis using the decision dependency graph:

*Clean merge*: The branch's decisions are compatible with main. No CONFLICTS_WITH or BLOCKS relationships exist between branch decisions and main decisions. The branch decisions can be incorporated directly.

*Merge conflict*: A decision on the branch CONFLICTS_WITH or is BLOCKED by a decision on main. These must be resolved before merging:
- The system presents the conflicting decisions side-by-side
- The user chooses which to keep (which may cascade further changes)
- Resolution is logged and the dependency graph is updated

*Cascading changes*: A different choice on the branch ENABLES or BLOCKS different downstream decisions than what exists on main. The system identifies which main decisions are affected and presents them for review.

**3.4 — Merge Gate for Branches**

The existing merge gate concept applies, but the UI must show:
- Which decisions change (with before/after status)
- Which decisions conflict (with resolution required)
- Impact analysis table (decision ID, status on main, status on branch, merge result)
- The Archivist's conflict detection output

**3.5 — Multiple Concurrent Branches**

Multiple branches can exist simultaneously. Each is isolated. Branches can be compared side-by-side without merging. Stale branches (not touched for a configurable period) are surfaced by the Archivist for review or archival.

**What to Preserve from Current Part 3**: Keep the Research vs. Exploration branch distinction table (§3.3). Keep the concept of archiving (not deleting) rejected branches. Remove or rewrite the simple "parallel paths" framing.

**Also update**: STD-18-01 — add to Part 3 (Merge Gate Standards) or a new Part:
- Merge conflict resolution standards (what information must be presented, what the user must confirm)
- Branch staleness detection rules and escalation schedule
- Validation that branch state is restorable before allowing fork

### Required Context for STD-18-01 Update

| File | Section | Why |
|------|---------|-----|
| `STD-18-01-questioning-arc-standards.md` | Part 2 §2.3: Branch Transition Requirements | Existing branch validation rules to extend |
| `STD-18-01-questioning-arc-standards.md` | Part 3: Merge Gate Standards (§3.1–3.4) | Existing merge gate standards to extend |
| `STD-18-01-questioning-arc-standards.md` | Part 3 §3.4: Deferred Merge Gate Handling | Precedent for staleness/timeout rules |

---

## Change 4: The Archivist Subsystem

**Document**: DD-18-01 (new section, after branching)
**Nature**: New content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-15-01-governance-definitions.md` | Part 6: LLM Agent Governance (§6.1–6.3) | What agents are in this system — the Archivist is NOT one |
| `DD-15-01-governance-definitions.md` | Part 4 §4.2–4.3: Audit Log What Gets Logged + Schema | Output format for the audit generation function |
| `STD-15-01-governance-standards.md` | Part 1 §1.3: Event Type Enumeration | Audit event types — the Archivist's outputs must conform to these |
| `DD-20-01-evidence-definitions.md` | Part 3: Citation Format (§3.1–3.4) | For the research linking function — how citations are structured |
| `DD-18-01-questioning-arc.md` | Part 5 §5.3: Governance System (DD-15-01) | How the arc currently interacts with governance — Archivist extends this |

### What to Write

Define the Archivist as a **background subsystem** (not a named agent, not conversational). It silently monitors the planning conversation and performs automated housekeeping. It rarely interacts with the user directly.

**Functions**:

| Function | What It Does | Output |
|----------|-------------|--------|
| Decision Filing | Captures and organizes decisions as they emerge from conversation | Decision records with status, dependencies, rationale |
| Dependency Analysis | Maintains the decision dependency graph; detects cycles and broken references | Warnings surfaced to the user only when problems are found |
| Merge Conflict Detection | Analyzes branch merges against the dependency graph | Impact analysis tables presented at merge gates |
| Research Linking | Connects decisions to the research findings and evidence that informed them | Citation chains for audit |
| Audit Generation | Produces decision changelogs and planning history | Queryable decision history |

**Triggers**:

| Trigger | Actions |
|---------|---------|
| Decision captured | File decision, update dependency graph, check for new conflicts |
| Branch created | Snapshot state, initialize branch tracking |
| Merge gate opened | Run conflict detection, generate impact analysis |
| Periodic (configurable) | Check for stale branches, orphaned decisions, broken references |
| Manual request | Generate audit report, decision changelog |

**Interaction Model**:

The Archivist does NOT:
- Participate in the planning conversation
- Have a persona or conversational style
- Require a sponsoring user in the DD-15-01 sense (it's infrastructure, not an agent)

The Archivist DOES:
- Surface warnings when it detects problems (conflicts, cycles, staleness)
- Produce structured outputs consumed by other parts of the system (merge gate UI, audit logs)
- Run deterministic validation (cycle detection, ref integrity) plus LLM-assisted analysis (impact summarization)

**Also update**: DD-15-01 Part 6 (LLM Agent Governance) — add a brief note clarifying that the Archivist is a background subsystem, not an Agent per DD-15-01's role definitions. It doesn't require a sponsoring user and doesn't produce proposals that need merge gate approval — it produces *analysis* that informs merge gate decisions.

### Required Context for DD-15-01 Update

| File | Section | Why |
|------|---------|-----|
| `DD-15-01-governance-definitions.md` | Part 1 §1.2: Role Definitions → Agent | The Agent role definition that the Archivist explicitly isn't |
| `DD-15-01-governance-definitions.md` | Part 6 §6.1: Agent Principles | Where to add the Archivist clarification |

---

## Change 5: User-Controlled Fast Mode

**Document**: DD-18-01 (add to Part 1, Stage Definitions or new subsection)
**Nature**: New content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 1 §1.2: Stage Definitions (all five stages) | Each stage's purpose — fast mode changes *how* each stage asks questions, not *what* it asks |
| `STD-18-01-questioning-arc-standards.md` | Part 1: Stage Completion Criteria (§1.1–1.5) | Confirm these don't change in fast mode |
| `SYS-00-system-definition.md` | Part 2 §2.1: The Planning Workflow | Where to add the SYS-00 fast mode mention |
| `SYS-00-system-definition.md` | Part 2 §2.2: Structured Input Over Freeform Text | Relevant guiding principle — pre-filling is a form of structured input |

### What to Write

Define Fast Mode as a **user-controlled setting** (not triggered by LLM signal detection). When enabled, the system changes its questioning approach:

**Normal mode** (default): Open exploration. The system asks broad questions, invites the user to think through options, uses varied elicitation methods.

**Fast mode** (user toggle): Pre-filled suggestions. The system does more of the cognitive work for the user:
- Instead of "What features do you need?", presents "Based on the context so far, these features seem relevant: [pre-filled list]. Accept, modify, or replace."
- Instead of open-ended prioritization, presents a pre-ranked list the user can adjust
- Stage turn counts may naturally be shorter, but stages are NOT skipped — all five stages still apply
- Exit conditions are the same as normal mode

Fast mode does NOT:
- Skip stages
- Reduce the quality or completeness of the output
- Auto-accept suggestions without user confirmation

Fast mode DOES:
- Shift the user's role from "author" to "editor"
- Reduce cognitive load for users who know roughly what they want
- Produce the same artifacts and decisions as normal mode

**Also update**: STD-18-01 — add a note (in Part 1 preamble or a new subsection) that stage completion criteria are identical regardless of mode. Fast mode affects questioning style, not validation rules.

**Also update**: SYS-00 §2.1 — add a brief mention that the planning workflow supports a user-controlled fast mode for streamlined input.

---

## Change 6: Elicitation Methods (New Document DD-18-02)

**New document**: DD-18-02-elicitation-methods.md
**Nature**: New lightweight document

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 1 §1.2: Stage Definitions (all five stages) | Each stage's purpose — needed for the stage affinity mapping |
| `SYS-00-system-definition.md` | Part 2 §2.2: Structured Input Over Freeform Text | The guiding principle behind varied elicitation |
| `DD-13-01-artifacts-definitions.md` | Part 1 §1.1: Artifact Type Catalog + Part 2 §2.1: Universal Fields | Correct artifact type and frontmatter for a new DD document |
| `llm/PROMPT-llm-compaction.md` | Full document | Rules for creating the corresponding LLM view |

### What to Write

This document explains *why* Compass uses varied questioning methods and provides a few examples. It explicitly acknowledges that method selection is a **prompt engineering concern** — the Planning LLM is instructed to use varied, relevant techniques, and specific method choices will evolve through testing.

**Part 1: Why Varied Methods Matter**
- Different questions surface different insights (a 5 Whys chain reveals root causes; a pre-mortem reveals risks; a SCAMPER exercise reveals creative alternatives)
- Monotonous questioning leads to shallow planning — variety keeps the user engaged and surfaces hidden assumptions
- The Planning LLM should match technique to context, not follow a fixed script

**Part 2: Example Method Categories**
Brief descriptions only — 2-3 sentences per method, 3-4 methods per category:
- **Foundation**: Socratic Questioning, 5 Whys, Pre-mortem (surface assumptions and risks)
- **Creative**: SCAMPER, What-If Scenarios (explore creative alternatives)
- **Prioritization**: MoSCoW, Buy-a-Feature / 100-Dollar Test (force trade-offs)
- **Collaboration**: Stakeholder Roundtable simulation, Persona Focus Group (surface multiple perspectives)

**Part 3: Stage Affinity (Guidance, Not Rules)**
A soft mapping of which categories are most useful in which stages:
- OPEN: Foundation methods (why does this matter? what's the root need?)
- FOLLOW: Creative + Foundation (what if we did X? what are we assuming?)
- SHARPEN: Prioritization (if you could only have one...)
- BOUNDARY: Foundation (pre-mortem: what could go wrong if we include X?)
- GROUND: Structured constraint-gathering (not really elicitation — more like checklist)

**Part 4: Non-Goals**
- This document does NOT prescribe specific methods for specific questions
- Method selection evolves through prompt iteration and testing
- No validation rules or standards for method usage (no STD-18-02 needed)

**Also create**: llm/LLM-DD-18-02-elicitation-methods.md (using compaction rules in `llm/PROMPT-llm-compaction.md`)
**Also update**: IDX-00-MASTER document registry — add DD-18-02 row
**Also update**: llm/LLM-INDEX.md — add DD-18-02 entry

### Required Context for IDX-00-MASTER Update

| File | Section | Why |
|------|---------|-----|
| `IDX-00-MASTER.md` | Document Registry table | Add DD-18-02 row in the correct position (after DD-18-01, STD-18-01) |
| `IDX-00-MASTER.md` | Document Relationships tree | Add DD-18-02 under DD-18-01 |

---

## Change 7: Research Branch Subtypes + Adversarial Evaluator

**Document**: DD-18-01 Part 2 (Research Branching)
**Nature**: Enhancement to existing content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 2: Research Branching and Merge Gates (§2.1–2.4) | The current research branch content being enhanced |
| `DD-18-01-questioning-arc.md` | Part 3 §3.3: Exploration vs. Research Branches table | The distinction to preserve |
| `DD-20-01-evidence-definitions.md` | Part 1: Evidence Grading Framework (§1.1–1.5) | Output format and confidence levels for research findings |
| `STD-18-01-questioning-arc-standards.md` | Part 2 §2.3: Branch Transition Requirements | Existing branch validation rules |

### What to Write

Add a `branchSubtype` concept to research branches. All subtypes follow the same lifecycle (create → investigate → merge gate → resolve) but differ in expected output:

| Subtype | Purpose | Output | Example |
|---------|---------|--------|---------|
| `investigation` (default) | General inquiry | Findings document | "What transcription services exist?" |
| `validation` | Test a hypothesis | Pass/fail report | "Can this API handle our throughput?" |
| `specialist` | Domain expert input | Targeted recommendation | "Security review of auth approach" |
| `adversarial` | Challenge a decision | Counterargument analysis | "What could go wrong with choosing Convex?" |

The **adversarial evaluator** subtype deserves particular attention. It is a user-triggered branch that takes a specific decision (typically one in EXPLORING or CHOSEN status) and deliberately argues against it. The purpose is to surface risks, hidden assumptions, and overlooked alternatives before a choice becomes costly to reverse.

How the adversarial evaluator works:
- The user triggers it on a specific decision ("Challenge this choice")
- The system examines the decision, its rationale, and the rejected alternatives
- It produces a structured counterargument covering: strongest arguments against the current choice, risks that the planning conversation may have glossed over, scenarios where a rejected alternative would have been better, and reversibility assessment (how hard would it be to change this later?)
- The output feeds back through a merge gate — the user can accept the concerns (which may reopen the decision), acknowledge-and-proceed (logging the risk), or dismiss

This is NOT an autonomous "devil's advocate" that interrupts the flow. It is an on-demand tool the user activates when they want a second perspective on a decision they're about to commit to.

Clarify for all subtypes that:
- All four subtypes use the same branch infrastructure (state isolation, merge gates)
- The subtype affects the output template and merge gate presentation, not the branch lifecycle
- The Archivist tracks subtype for reporting purposes

---

## Change 8: Merge Gate Integration Requirement

**Document**: DD-18-01 Part 2 §2.4 (Merge Gates)
**Nature**: Minor addition to existing content

### Required Context

| File | Section | Why |
|------|---------|-----|
| `DD-18-01-questioning-arc.md` | Part 2 §2.4: Merge Gates | The section being amended |
| `DD-17-01-integration-definitions.md` | Part 1 §1.1–1.2: Integration Type Overview + Standard Integration Pattern | The integration pattern being referenced |

### What to Write

Add a single paragraph stating that merge gate resolution is a state mutation event that must trigger registered integration handlers per DD-17-01. Do NOT reference specific tools (Convex, Linear). The specific integration chain is an implementation detail determined by ADR-01-01 and ADR-05-01.

---

## Change 9: SYS-00 Enhancements

**Document**: SYS-00
**Nature**: Minor updates to existing sections

### Required Context

| File | Section | Why |
|------|---------|-----|
| `SYS-00-system-definition.md` | Part 2 §2.1: The Planning Workflow | Section being enhanced with decision dependencies, status lifecycle, fast mode |
| `SYS-00-system-definition.md` | Part 2 §2.6: Branching and Exploration | Section being enhanced with Git-like branching model |
| `SYS-00-system-definition.md` | Part 1 §1.7: Guiding Principles | Context for where Archivist aligns (auditability, state externalization) |
| `SYS-00-system-definition.md` | Appendix A: Glossary | Where to add new terms |

### What to Write

**§2.1 (The Planning Workflow)** — add:
- Brief mention of decision dependency tracking (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) with reference to DD-18-01
- Brief mention of decision status lifecycle (EXPLORING → CHOSEN/REJECTED/BLOCKED/DEFERRED) as distinct from artifact lifecycle
- Brief mention of user-controlled fast mode

**§2.6 (Branching and Exploration)** — enhance to describe the Git-like branching model:
- Users can fork planning at any prior decision point (time travel)
- Branches carry full context/memory state from the fork point
- Decision dependencies enable merge conflict detection
- Resolution required before merging back to main
- Reference DD-18-01 for full specification

**Appendix A: Glossary** — add:
- **Archivist**: A background subsystem that silently monitors planning, files decisions, maintains the dependency graph, detects merge conflicts, and generates audit output.
- **Decision dependency**: A typed relationship (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) between two decisions within a planning arc.
- **Decision status**: The planning-time state of a decision (EXPLORING, ENABLED, BLOCKED, CHOSEN, REJECTED, DEFERRED) — distinct from artifact lifecycle status.
- **Fast mode**: A user-controlled setting where the system pre-fills suggestions for the user to edit rather than asking open-ended questions. All stages still apply.
- **Adversarial evaluator**: A user-triggered research branch subtype that deliberately argues against a decision to surface risks and hidden assumptions.

---

## Change 10: LLM View Updates

All modified canonical documents require corresponding LLM view regeneration.

### Required Context

| File | Section | Why |
|------|---------|-----|
| `llm/PROMPT-llm-compaction.md` | Full document | Compaction rules, output format, extraction guidance |
| Each existing LLM view being regenerated | Full document | Understand current format and what changes |

### What to Regenerate

| Canonical Document | LLM View | Action |
|---|---|---|
| DD-18-01 | `llm/LLM-DD-18-01-questioning-arc.md` | Regenerate — major changes: add decision dependencies, decision statuses, Git-like branching, Archivist, fast mode, research subtypes + adversarial evaluator to canonical statements and glossary |
| STD-18-01 | `llm/LLM-STD-18-01-questioning-arc-standards.md` | Regenerate — new validation rules for dependencies, statuses, merge conflicts |
| SYS-00 | `llm/LLM-SYS-00-system-definition.md` | Regenerate — add decision dependencies, branching model, Archivist, fast mode to canonical statements and glossary |
| DD-15-01 | `llm/LLM-DD-15-01-governance-definitions.md` | Regenerate — Archivist is not an Agent clarification |
| DD-13-01 | `llm/LLM-DD-13-01-artifacts-definitions.md` | Regenerate — decision status vs artifact status distinction |
| DD-18-02 (new) | `llm/LLM-DD-18-02-elicitation-methods.md` | Create new LLM view |
| IDX-00-MASTER | `llm/LLM-INDEX.md` | Update to include DD-18-02 |

---

## Implementation Order

Changes have dependencies. Recommended order:

1. **DD-18-01: Decision Dependencies + Decision Status Lifecycle** (Changes 1 & 2) — foundational, everything else builds on these
2. **DD-18-01: Exploration Branching rewrite** (Change 3) — depends on dependency types being defined
3. **DD-18-01: Archivist subsystem** (Change 4) — depends on branching and dependencies being defined
4. **DD-18-01: Fast Mode + Merge Gate integration note + Research subtypes with adversarial evaluator** (Changes 5, 7, 8) — independent additions
5. **STD-18-01: New validation rules** (from Changes 1, 2, 3, 5) — depends on DD-18-01 being updated
6. **DD-18-02: Elicitation Methods** (Change 6) — independent, can be done in parallel with step 5
7. **SYS-00, DD-15-01, DD-13-01 updates** (Changes 4, 9) — after DD-18-01 is stable
8. **LLM view regeneration** (Change 10) — last, after all canonical documents are finalized

Steps 1-4 can be a single commit since they're all DD-18-01 changes. Steps 5-7 can be parallel. Step 8 is a final pass.

---

## What This Plan Does NOT Change

- **DD-19-01** (Widget Schema): No changes. Widget taxonomy is adequate.
- **Signal routing**: Scrapped. Responsiveness to user signals is a prompt engineering concern for the Planning LLM.
- **Elicitation method enumeration**: No exhaustive list. Method selection evolves through testing.
- **Specific tool references in arc documents**: No "Convex → Linear" chains — integration details are determined by ADRs.
- **Confidence scoring**: No changes to merge gate schema. Categorical levels (high/medium/low) are sufficient.

---

*End of Integration Plan*
