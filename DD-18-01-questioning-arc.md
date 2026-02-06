---
id: DD-18-01
type: definition
area: 18-questioning-arc
title: Questioning Arc Definition
status: draft
created: 2026-01-26
updated: 2026-02-06
author: compass-research
summary: Defines the structured questioning progression that transforms vague intent into implementation-ready specifications, including the five-stage planning workflow, decision dependency tracking, decision status lifecycle, Git-like exploration branching, the Archivist subsystem, research branching with subtypes, and merge gate protocols
tags: [questioning-arc, planning, workflow, state-machine, conversation, decisions, branching]
related:
  - RF-02-01
  - ADR-02-01
  - DD-13-01
  - DD-15-01
  - DD-18-02
links:
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-15-01"
  - rel: related
    target_id: "DD-18-02"
  - rel: companion
    target_id: "STD-18-01"
  - rel: informed_by
    target_id: "ADR-02-01"
companion: STD-18-01
informed_by: [ADR-02-01]
---

# Questioning Arc Definition

## Document Purpose

This document defines the **questioning arc**: the structured progression through which Compass transforms vague ideas into rigorous, implementation-ready specifications. The questioning arc is the core mechanism that distinguishes Compass from simple chat-based documentation—it's a state machine that ensures planning conversations produce actionable outputs rather than drift into endless discussion.

**Why this matters**: Without structured questioning, planning conversations tend to either skip important considerations (leading to incomplete specs) or circle indefinitely without converging (leading to paralysis). The questioning arc provides guardrails that guide conversations toward completeness while preserving flexibility to explore alternatives.

**What this document covers**:

- The five-stage planning workflow (OPEN through GROUND)
- User-controlled fast mode for streamlined input
- Decision dependency tracking between planning decisions
- Decision status lifecycle within the planning arc
- Research branching with subtypes and merge gates
- Git-like exploration branching with fork, divergence, and merge conflict detection
- The Archivist background subsystem for automated housekeeping
- State persistence and session management
- How the arc integrates with widgets, artifacts, and governance

**What this document does not cover**:

- Specific widget implementations (see DD-19-01)
- Orchestration framework details (see ADR-02-01)
- Evidence and citation standards (see STD-20-01)
- Elicitation method guidance (see DD-18-02)

**Audience**: Compass builders, planners, and LLM agents operating within the system.

---

## Part 1: The Five-Stage Planning Workflow

The planning workflow follows a consistent arc from initial idea to implementation-ready specification. Each stage has a distinct purpose, and together they ensure that planning conversations address everything an implementation agent needs.

### 1.1 Stage Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUESTIONING ARC FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌───────┐    ┌────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐   │
│    │ OPEN  │───>│ FOLLOW │───>│ SHARPEN  │───>│ BOUNDARY │───>│ GROUND │   │
│    └───┬───┘    └────┬───┘    └────┬─────┘    └────┬─────┘    └────┬───┘   │
│        │             │             │               │               │        │
│        v             v             v               v               v        │
│    Extract       Expand &      Prioritize      Define out      Apply hard  │
│    the idea      elaborate     & trade off     of scope        constraints │
│                                                                             │
│    3-5 turns     10-20 turns   5-8 turns       4-6 turns       3-5 turns   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                                    │
                                    │ At any point
                                    v
                        ┌───────────────────────┐
                        │   RESEARCH BRANCH     │
                        │   (pause, investigate,│
                        │    then resume)       │
                        └───────────────────────┘
```

The arc is not purely linear. Users can revisit earlier stages when new information emerges, and research branches can pause the main arc to investigate uncertainty before resuming.

### 1.2 Stage Definitions

#### OPEN Stage

**Purpose**: Extract the fuzzy idea and establish the starting point.

The OPEN stage is about understanding what the user is trying to accomplish. At this point, the idea is often vague or incomplete—that's expected. The goal is not to refine yet, but to get the initial concept onto the table with enough context to know what questions to ask next.

**What happens in OPEN**:

The system asks exploratory questions to understand the core motivation. Why does this matter? Who will use it? What does success look like? The questions are intentionally broad, designed to surface the underlying need rather than jump to solutions.

**Artifacts created**:

- Initial project context (captured in working memory)
- Preliminary user/stakeholder identification
- High-level success indicators (even if vague)

**Typical duration**: 3–5 conversation turns.

**Exit conditions**:

- The core problem or opportunity is articulated
- At least one user type is identified
- The user signals readiness to explore deeper ("Let's figure out what we need" or similar)

**Example of what a conversation might address**:

> What's the core problem you're trying to solve?
> Who experiences this problem most directly?
> What would it look like if this were working well?
> What prompted this idea now?

---

#### FOLLOW Stage

**Purpose**: Expand and elaborate; discover requirements and use cases.

The FOLLOW stage is where the idea grows. Having understood the core intent, the system now explores the space: what features are needed, what users will do, what the system should and shouldn't handle. This is the longest stage, where most of the substance emerges.

**What happens in FOLLOW**:

The system asks questions that uncover requirements without yet forcing prioritization. "What should happen when...?" "Would users ever need to...?" "What about the case where...?" The goal is breadth—surfacing all the relevant considerations before narrowing down.

**Artifacts created**:

- Emerging requirements list
- Use case descriptions
- Initial dependencies and integration points
- Research triggers (uncertainties flagged for later investigation)

**Typical duration**: 10–20 conversation turns.

**Exit conditions**:

- Major use cases are identified (even if not fully detailed)
- Requirements are captured (even if not yet prioritized)
- The user has expressed everything they think is important (for now)
- The system detects diminishing new information ("We've covered the main scenarios")

**Example of what a conversation might address**:

> What's the most common way someone would use this?
> Are there different types of users with different needs?
> What other systems does this need to work with?
> What happens if [edge case]?
> What's something that might seem related but you definitely don't want?

---

#### SHARPEN Stage

**Purpose**: Prioritize and force trade-offs; reveal true priorities.

The SHARPEN stage introduces structured friction. Having gathered requirements, the system now helps the user decide what matters most. This is where widgets become particularly useful—sliders, rankings, and trade-off tables make abstract preferences concrete.

**What happens in SHARPEN**:

The system presents choices that require prioritization: "If you could only have two of these three features, which two?" "Where on this spectrum do you fall?" "Rank these capabilities from most to least critical." The goal is to surface genuine priorities, not collect a wish list.

**Artifacts created**:

- Prioritized requirements (must-have vs. nice-to-have vs. out-of-scope)
- Explicit trade-off decisions with rationale
- Acceptance criteria for high-priority items
- Decision records for significant trade-offs

**Typical duration**: 5–8 conversation turns.

**Exit conditions**:

- Core requirements are clearly prioritized
- At least one significant trade-off has been explicitly decided
- The user can articulate what would make this "done" vs. "great"

**Example of what a conversation might address**:

> Of these five capabilities, which three are essential for launch?
> If speed and thoroughness conflict, which wins?
> What's the minimum viable version that would still be useful?
> What would you sacrifice to hit a faster timeline?

---

#### BOUNDARY Stage

**Purpose**: Define out-of-scope; prevent scope creep; document rejected options.

The BOUNDARY stage makes explicit what the project will not do. This is psychologically harder than it sounds—most planning conversations avoid this stage, leading to creeping scope during implementation. Compass makes boundaries a first-class concern.

**What happens in BOUNDARY**:

The system asks directly about exclusions: "We've discussed X; is that in or out for this iteration?" "What adjacent problems are not this project's job to solve?" "What's a common assumption about systems like this that we're explicitly rejecting?" The goal is to create a clear "no" list that implementation agents respect.

**Artifacts created**:

- Explicit out-of-scope list
- Documented rejected alternatives (with rationale)
- Deferred items (things for later, not now)
- Boundary validation (confirmation that the user agrees with these limits)

**Typical duration**: 4–6 conversation turns.

**Exit conditions**:

- Out-of-scope items are explicitly listed
- At least one "commonly expected" feature is explicitly excluded (if applicable)
- Deferred vs. rejected distinction is clear
- The user confirms: "Yes, these boundaries are correct"

**Example of what a conversation might address**:

> What's something users might expect that we're intentionally not doing?
> Is [adjacent capability] in scope or out?
> What should happen when someone asks for something outside these boundaries?
> What's explicitly deferred to a later phase?

---

#### GROUND Stage

**Purpose**: Apply hard constraints—budget, security, reliability tier, integrations, timeline, and compliance.

The GROUND stage anchors the specification to reality. Every prior stage involves aspirations; GROUND introduces the constraints that aspirations must fit within. This is where handoff bundle content becomes concrete.

**What happens in GROUND**:

The system walks through each constraint category systematically: "What's the budget for this?" "What reliability tier does this need?" "What security requirements apply?" "What's the timeline?" The questions are often multiple-choice or slider-based because constraints have defined ranges.

**Artifacts created**:

- Budget and resource constraints
- Security and privacy requirements
- Reliability tier assignment (per DD-14-01)
- Timeline and milestone targets
- Compliance requirements (if any)
- Integration specifications

**Typical duration**: 3–5 conversation turns.

**Exit conditions**:

- All relevant constraint categories are addressed
- Constraints are specific enough to be testable
- No fundamental conflicts exist between constraints and prioritized requirements
- All must-have decisions have reached CHOSEN or DEFERRED status
- The specification is ready for handoff bundle generation

**Example of what a conversation might address**:

> What's the budget ceiling for external services?
> What reliability tier does this need—internal tool, business critical, or always-on?
> Who can access this, and how do they authenticate?
> What's the target launch date, and how firm is it?
> Are there regulatory or compliance requirements to consider?

---

### 1.3 Stage Transition Logic

Movement between stages follows predictable patterns, though the system supports flexibility.

**Forward progression**: The default direction. When exit conditions for a stage are met and the user signals readiness, the system moves to the next stage.

**Backward revisitation**: When new information invalidates earlier assumptions. The user might say "Actually, thinking about that constraint changes what I said about priorities." The system can return to SHARPEN while preserving GROUND progress.

**Lateral research**: When uncertainty blocks progress. "I don't know enough about X to answer that question" triggers a research branch (see Part 3).

**Convergence signals**: The system watches for signals that a stage is complete, including explicit statements ("I think we've covered the main cases"), diminishing new information (several turns without substantial additions), and completeness checks passing (see STD-18-01 for checklists).

### 1.4 User-Controlled Fast Mode

The questioning arc supports a **fast mode** that changes how the system interacts with the user. Fast mode is a user-controlled setting—the user toggles it on or off, and it is not triggered by system signal detection.

**Normal mode** (default): Open exploration. The system asks broad questions, invites the user to think through options, and uses varied elicitation methods (see DD-18-02). The user's role is primarily that of an author generating content.

**Fast mode** (user toggle): Pre-filled suggestions. The system does more of the cognitive work for the user:

- Instead of "What features do you need?", the system presents "Based on the context so far, these features seem relevant: [pre-filled list]. Accept, modify, or replace."
- Instead of open-ended prioritization, the system presents a pre-ranked list the user can adjust.
- Stage turn counts may naturally be shorter, but stages are NOT skipped—all five stages still apply.
- Exit conditions are the same as normal mode.

**Fast mode does NOT**:

- Skip stages
- Reduce the quality or completeness of the output
- Auto-accept suggestions without user confirmation

**Fast mode DOES**:

- Shift the user's role from "author" to "editor"
- Reduce cognitive load for users who know roughly what they want
- Produce the same artifacts and decisions as normal mode

---

## Part 2: Decision Tracking

During the planning arc, decisions emerge, evolve, and interact. This part defines how decisions relate to each other through typed dependencies and how each decision progresses through its own lifecycle.

### 2.1 Decision Dependency Types

Decisions within a planning workflow can have typed relationships that affect how the arc state machine manages them. These are **decision-to-decision** relationships within a planning workflow, distinct from DD-13-01's artifact-to-artifact `links` (which handle document navigation and cross-referencing between artifacts).

| Type | Semantics | Example |
|------|-----------|---------|
| DEPENDS_ON | Hard prerequisite — can't finalize X without Y resolved | DB schema depends on hosting choice |
| ENABLES | Unlocks options — choosing X makes Y possible | Choosing AWS enables Lambda |
| BLOCKS | Eliminates options — choosing X makes Y impossible | Choosing serverless blocks VMs |
| CONFLICTS_WITH | Mutually exclusive — X and Y can't both be CHOSEN | OAuth conflicts with custom auth |
| INFORMS | Soft influence — X makes Y more or less likely | Budget informs scope ambition |

**How dependencies are used**:

- Dependencies are recorded as decisions are captured during the arc. The Archivist (see Part 5) maintains the dependency graph.
- The system warns when a user tries to finalize a decision whose DEPENDS_ON targets are unresolved.
- BLOCKS and CONFLICTS_WITH relationships surface automatically when a choice eliminates options.
- Dependencies form a directed graph; cycles are invalid and must be detected (Archivist responsibility).
- ENABLES relationships unlock new decisions for consideration: when a decision is CHOSEN, any decisions it ENABLES may transition to the ENABLED status.
- INFORMS relationships are advisory only—they surface context but do not create hard constraints.

### 2.2 Decision Status Lifecycle

Decisions within a planning arc progress through their own lifecycle that is **separate from** DD-13-01's artifact lifecycle (`draft → review → active → deprecated`). An artifact (such as an ADR) can be in `active` status while the decision it records is still `EXPLORING`—these are different systems tracking different concerns.

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

**Status definitions**:

| Status | Meaning |
|--------|---------|
| EXPLORING | Actively under consideration; options being evaluated |
| ENABLED | Unlocked by another decision but not yet actively considered |
| BLOCKED | Cannot be finalized because a BLOCKS dependency prevents it |
| CHOSEN | Selected as the decision for this planning arc |
| REJECTED | Explicitly ruled out, with rationale recorded |
| DEFERRED | Postponed to a later planning phase |

**Transition triggers**:

- **User action**: EXPLORING → CHOSEN, REJECTED, or DEFERRED
- **Dependency resolution**: → ENABLED (when an ENABLES source is CHOSEN) or → BLOCKED (when a BLOCKS source is CHOSEN)
- **Merge gate results**: Branch merge may trigger status changes for affected decisions

**Consistency rules**:

- A CHOSEN decision must not have unresolved DEPENDS_ON dependencies.
- A BLOCKED decision cannot be CHOSEN without first resolving the blocking relationship.
- Status history is preserved—a decision that was EXPLORING, then BLOCKED, then ENABLED, then CHOSEN retains that full history for audit.
- All must-have decisions must reach CHOSEN or DEFERRED before GROUND stage completion.

---

## Part 3: Research Branching and Merge Gates

Not everything can be decided in a single planning session. Sometimes the right answer is "we need to find out," and Compass supports this with research branches.

### 3.1 What Research Branching Is

A research branch is a temporary divergence from the main planning workflow to investigate a specific question. The main arc pauses, research occurs (potentially over days), findings are summarized, and then the main arc resumes with new information.

```
Main Arc:  OPEN ─> FOLLOW ─> [UNCERTAINTY] ─────────────> [RESUME] ─> SHARPEN ─> ...
                                   │                          ↑
                                   │     Research Branch      │
                                   └────> [investigate] ──────┘
                                          [document]
                                          [summarize]
```

**Why this matters**: Without explicit research branching, uncertainty either blocks progress (paralysis) or gets papered over with assumptions (brittle specs). Research branches make "we need to find out" a legitimate and trackable response.

### 3.2 Triggering Research Branches

Research branches can be triggered in three ways:

**User request**: The user explicitly says they need to investigate something. "I need to research vendor options before I can answer that" or "Let me find out what the security team requires."

**System detection**: The system detects uncertainty that blocks progress. When a question gets responses like "I'm not sure" or "it depends on something I don't know," the system can offer to create a research branch.

**Widget escape hatch**: Every widget includes a "Research this" option. When users select it, the system creates a research brief and pauses for investigation.

### 3.3 Research Branch Lifecycle

A research branch follows its own lifecycle:

**Creation**: The system captures the research question, relevant context from the main arc, success criteria (what would count as a useful answer), and the insertion point (where findings will merge back).

**Investigation**: Research occurs—this might be immediate (system-assisted web research), asynchronous (user investigates and returns later), or delegated (assigned to another person or agent).

**Documentation**: Findings are captured in Research Finding format (RF-*), following STD-20-01 evidence standards. The output includes what was discovered, sources and confidence levels, recommendation and rationale, and impact on the main arc (what changes based on this).

**Merge gate**: Before findings affect the main arc, a human reviews and approves via the merge gate (see §3.6).

### 3.4 Research Branch Subtypes

Research branches support a `branchSubtype` property that indicates the expected output format. All subtypes follow the same lifecycle (create → investigate → merge gate → resolve) but differ in expected output:

| Subtype | Purpose | Output | Example |
|---------|---------|--------|---------|
| `investigation` (default) | General inquiry | Findings document | "What transcription services exist?" |
| `validation` | Test a hypothesis | Pass/fail report | "Can this API handle our throughput?" |
| `specialist` | Domain expert input | Targeted recommendation | "Security review of auth approach" |
| `adversarial` | Challenge a decision | Counterargument analysis | "What could go wrong with choosing Convex?" |

All four subtypes use the same branch infrastructure (state isolation, merge gates). The subtype affects the output template and merge gate presentation, not the branch lifecycle. The Archivist tracks subtype for reporting purposes.

### 3.5 The Adversarial Evaluator

The `adversarial` subtype deserves particular attention. It is a **user-triggered** branch that takes a specific decision (typically one in EXPLORING or CHOSEN status) and deliberately argues against it. The purpose is to surface risks, hidden assumptions, and overlooked alternatives before a choice becomes costly to reverse.

**How the adversarial evaluator works**:

1. The user triggers it on a specific decision ("Challenge this choice").
2. The system examines the decision, its rationale, and the rejected alternatives.
3. It produces a structured counterargument covering:
   - Strongest arguments against the current choice
   - Risks that the planning conversation may have glossed over
   - Scenarios where a rejected alternative would have been better
   - Reversibility assessment (how hard would it be to change this later?)
4. The output feeds back through a merge gate—the user can accept the concerns (which may reopen the decision), acknowledge-and-proceed (logging the risk), or dismiss.

This is NOT an autonomous "devil's advocate" that interrupts the flow. It is an on-demand tool the user activates when they want a second perspective on a decision they're about to commit to.

### 3.6 Merge Gates

Merge gates are explicit checkpoints where proposed changes to canonical artifacts require human confirmation. This is a core principle from the System Definition (§1.7): "Sub-agents produce proposals, not canonical truth."

**When merge gates appear**:

- Research findings are ready to integrate into the main arc
- A branch exploration is ready to merge
- An agent proposes significant changes to specifications
- Conflicting information needs resolution

**What happens at a merge gate**:

The system presents a summary of proposed changes, including what would change (specific artifacts or decisions), why (the source of the proposal), and what the alternative is (reject, edit, or accept). The human reviews and chooses: Accept as-is, Edit before merging, Reject and continue without changes, or Defer for later decision.

**Merge gate resolution is always logged**: who, when, what decision, and rationale. This creates the audit trail that makes planning history reconstructable.

**Integration requirement**: Merge gate resolution is a state mutation event that must trigger registered integration handlers per DD-17-01. The specific integration chain is an implementation detail determined by ADR-01-01 and ADR-05-01.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MERGE GATE                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Research Branch: "Backend vendor comparison"                               │
│  Status: Complete                                                           │
│                                                                             │
│  PROPOSED CHANGES:                                                          │
│  ─────────────────                                                          │
│  • Requirement R-12: Add "PostgreSQL compatibility" (new)                   │
│  • Constraint C-03: Budget ceiling → $200/month (was: $150)                 │
│  • Decision D-05: Recommend Supabase over Firebase (new ADR)                │
│                                                                             │
│  SOURCES:                                                                   │
│  ────────                                                                   │
│  RF-01-01 (Backend Platform Research) - Confidence: High                    │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   ACCEPT    │  │    EDIT     │  │   REJECT    │  │    DEFER    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Exploration Branching

Separate from research branches, Compass supports exploration branches for investigating alternative approaches. Exploration branches follow a Git-like branching model where users can fork, build out, and merge entire planning states.

### 4.1 Fork (Time Travel)

A user can navigate back to any prior decision point in the planning history and create a fork. The system:

- Restores the full context/memory state as it was at that decision point
- Creates a new branch from that snapshot
- The branch proceeds independently from that point forward

The key insight: the user isn't just "comparing two options"—they're replaying planning from a different starting assumption. If they chose PostgreSQL on main but want to explore MongoDB, the fork restores the state *before* the database decision and lets them make a different choice. All downstream decisions (ORM selection, schema design, query patterns) then play out under the new assumption.

### 4.2 Branch Divergence

As the branch progresses, decisions accumulate that may differ from main. The system tracks:

- **Decisions shared with main**: Made before the fork point; identical on both branches.
- **Decisions unique to the branch**: Made after fork, potentially different from main.
- **Decision dependencies that cross the fork boundary**: Dependencies involving both shared and branch-specific decisions.

### 4.3 Merge and Conflict Detection

When a branch is ready to merge back into main, the system (via the Archivist) performs impact analysis using the decision dependency graph:

**Clean merge**: The branch's decisions are compatible with main. No CONFLICTS_WITH or BLOCKS relationships exist between branch decisions and main decisions. The branch decisions can be incorporated directly.

**Merge conflict**: A decision on the branch CONFLICTS_WITH or is BLOCKED by a decision on main. These must be resolved before merging:

- The system presents the conflicting decisions side-by-side.
- The user chooses which to keep (which may cascade further changes).
- Resolution is logged and the dependency graph is updated.

**Cascading changes**: A different choice on the branch ENABLES or BLOCKS different downstream decisions than what exists on main. The system identifies which main decisions are affected and presents them for review.

### 4.4 Merge Gate for Branches

The existing merge gate concept applies, but the UI must show:

- Which decisions change (with before/after status)
- Which decisions conflict (with resolution required)
- Impact analysis table (decision ID, status on main, status on branch, merge result)
- The Archivist's conflict detection output

### 4.5 Multiple Concurrent Branches

Multiple branches can exist simultaneously. Each is isolated. Branches can be compared side-by-side without merging. Stale branches (not touched for a configurable period) are surfaced by the Archivist for review or archival.

Rejected branches are archived, not deleted—they remain accessible as reference for why an alternative was considered and ultimately not selected.

### 4.6 Exploration vs. Research Branches

The two branch types serve different purposes:

| Aspect | Research Branch | Exploration Branch |
|--------|-----------------|-------------------|
| Purpose | Gather information | Work through implications |
| Trigger | "I don't know X" | "A or B—let's see which" |
| Output | Findings document | Design comparison |
| Duration | Variable (hours to weeks) | Typically same session |
| Parallelism | Usually sequential | Usually parallel |
| Model | Linear investigation | Git-like fork and merge |

---

## Part 5: The Archivist Subsystem

The Archivist is a **background subsystem** that silently monitors the planning conversation and performs automated housekeeping. It is not a named agent, not conversational, and it rarely interacts with the user directly. It is infrastructure, not a persona.

**Important distinction**: The Archivist is NOT an Agent per DD-15-01's role definitions. It does not require a sponsoring user, does not produce proposals that need merge gate approval, and does not participate in the planning conversation. It produces *analysis* that informs merge gate decisions and *warnings* when it detects problems.

### 5.1 Functions

| Function | What It Does | Output |
|----------|-------------|--------|
| Decision Filing | Captures and organizes decisions as they emerge from conversation | Decision records with status, dependencies, rationale |
| Dependency Analysis | Maintains the decision dependency graph; detects cycles and broken references | Warnings surfaced to the user only when problems are found |
| Merge Conflict Detection | Analyzes branch merges against the dependency graph | Impact analysis tables presented at merge gates |
| Research Linking | Connects decisions to the research findings and evidence that informed them | Citation chains for audit |
| Audit Generation | Produces decision changelogs and planning history | Queryable decision history |

### 5.2 Triggers

| Trigger | Actions |
|---------|---------|
| Decision captured | File decision, update dependency graph, check for new conflicts |
| Branch created | Snapshot state, initialize branch tracking |
| Merge gate opened | Run conflict detection, generate impact analysis |
| Periodic (configurable) | Check for stale branches, orphaned decisions, broken references |
| Manual request | Generate audit report, decision changelog |

### 5.3 Interaction Model

**The Archivist does NOT**:

- Participate in the planning conversation
- Have a persona or conversational style
- Require a sponsoring user in the DD-15-01 sense (it's infrastructure, not an agent)

**The Archivist DOES**:

- Surface warnings when it detects problems (conflicts, cycles, staleness)
- Produce structured outputs consumed by other parts of the system (merge gate UI, audit logs)
- Run deterministic validation (cycle detection, reference integrity) plus LLM-assisted analysis (impact summarization)

**Output format**: The Archivist's outputs conform to DD-15-01 audit log requirements and STD-15-01 event type enumerations. Research linking outputs follow DD-20-01 citation format.

---

## Part 6: State Management

The questioning arc maintains state across multiple sessions, potentially spanning days or weeks. This section defines how state is structured and preserved.

### 6.1 State Composition

Arc state consists of three layers:

**Conversation state**: The immediate context of the current session—recent exchanges, pending questions, active widgets. This is ephemeral within a session but serialized between sessions.

**Working memory**: The accumulated decisions, requirements, and context for the current project. This persists across sessions and contains the substantive content of planning.

**Branch context**: Metadata about the current position in the arc—active stage, branching history, pending merge gates. This enables resume-from-where-you-left-off.

### 6.2 State Serialization

All arc state is serializable to JSON. This is a core architectural requirement (System Definition §1.7: "State is externalized"). The system reconstructs context from stored state, not from conversation history alone.

**Why this matters**: LLM context windows are finite and conversation histories can become large. By externalizing state, the system can resume sessions without replaying entire histories.

Per ADR-02-01, Mastra's thread-based memory provides the persistence layer. Working memory uses Zod schemas that define exactly what's stored, enabling both type safety and clear documentation of state structure.

### 6.3 Pause and Resume

Planning sessions can be paused at any point and resumed later—hours, days, or weeks later.

**What's preserved on pause**:

- Current stage and position within stage
- All accumulated artifacts and decisions
- Pending questions and incomplete widgets
- Research branch status
- Merge gate queue

**What happens on resume**:

The system reloads state and provides orientation: "We were in the SHARPEN stage, discussing priority ranking. You had ranked 3 of 5 requirements. Ready to continue?"

**Suspension points**: Per RF-02-01, Mastra's `suspend()` function maps to natural pause points. Stage transitions and human-input-required moments (like merge gates) are natural suspension points where state is fully serialized.

### 6.4 State Isolation

State is isolated at multiple levels:

**Project isolation**: Each project has independent state. Decisions in Project A don't affect Project B.

**Branch isolation**: Research and exploration branches have their own state that doesn't affect the main arc until merged.

**Session isolation**: Concurrent sessions (if supported) on the same project are coordinated to prevent conflicting mutations.

---

## Part 7: Integration Points

The questioning arc integrates with several other Compass subsystems.

### 7.1 Widget System (DD-19-01)

Widgets are the primary mechanism for structured input during the questioning arc. The arc determines when to present widgets and what type; the widget system handles rendering and response collection.

**How they interact**:

- The arc's current stage and question context determine widget appropriateness
- OPEN stage typically uses free-text with optional structure
- FOLLOW stage uses exploratory widgets (multi-select, branching questions)
- SHARPEN stage uses prioritization widgets (ranking, sliders, trade-off tables)
- BOUNDARY stage uses confirmation widgets (checklists, yes/no gates)
- GROUND stage uses constraint widgets (range selectors, pre-defined option sets)

Every widget includes three guaranteed escape hatches: "None of these / describe instead," "Help me think" (system provides framing), and "Research this" (creates research branch).

### 7.2 Artifact System (DD-13-01)

The questioning arc produces and updates artifacts throughout its progression.

**Creation patterns**:

- OPEN creates initial project context artifacts
- FOLLOW creates requirement and use case artifacts
- SHARPEN creates decision records (ADRs) for significant trade-offs
- BOUNDARY updates specifications with explicit exclusions
- GROUND completes specifications with constraint details

**Artifact lifecycle interaction**: Artifacts created during the arc begin in `draft` status. They transition to `active` when the arc completes or when explicitly approved at merge gates.

### 7.3 Governance System (DD-15-01)

The questioning arc interacts with governance through three mechanisms:

**Permissions**: Only users with Planner role (or higher) can advance arc stages or approve merge gates.

**Agent constraints**: Agents can participate in the arc (drafting, research, suggestions) but cannot approve merge gates or advance to GROUND stage completion without human confirmation.

**Audit logging**: Stage transitions, merge gate decisions, and branch operations are logged per DD-15-01 audit requirements.

### 7.4 Orchestration Layer (ADR-02-01)

The questioning arc is implemented using the orchestration framework selected in ADR-02-01 (Mastra + Vercel AI SDK v6).

**Key mappings**:

- Arc stages map to Mastra workflow steps
- Stage transitions map to step transitions with conditional branching
- Research branches map to parallel workflow paths
- Merge gates map to Mastra's `suspend()` function with human-in-the-loop resume
- State persistence uses Mastra's thread-based memory with PostgreSQL backend

---

## Part 8: Conceptual Example Flows

The following examples illustrate how the questioning arc might progress for different types of projects. These are conceptual patterns, not specific implementations.

### 8.1 Example: New Internal Tool

A planner wants to create a dashboard for tracking podcast metrics.

**OPEN (3 turns)**: The conversation establishes that the core need is visibility into podcast performance, the primary users are the podcast production team, and success means producers can answer basic performance questions without asking analysts.

**FOLLOW (12 turns)**: The conversation explores what metrics matter (downloads, completion rates, audience geography), what comparisons users need (episode vs. episode, show vs. show, period vs. period), what existing data sources exist, and what level of real-time freshness matters.

**SHARPEN (6 turns)**: Widgets help prioritize: "Rank these five metric categories." "If you could only have one comparison view, which?" "Where does data freshness fall on this spectrum between 'real-time critical' and 'weekly is fine'?"

**BOUNDARY (4 turns)**: The conversation explicitly excludes predictive analytics, integration with ad platforms, and external sharing. It defers multi-show comparison views to Phase 2.

**GROUND (3 turns)**: Constraints are applied—budget ceiling of $50/month for external services, reliability tier of "internal tool," accessible to anyone with EFN SSO, target launch in 6 weeks.

### 8.2 Example: Research-Heavy Planning

A planner wants to select a video transcription service.

**OPEN (4 turns)**: The core need is automated transcription for video logging. Users are video editors and producers. Success means transcripts are accurate enough for searchability.

**FOLLOW (8 turns)**: Requirements emerge—accuracy threshold, turnaround time, integration with existing media asset management, speaker identification needs.

**[Research Branch triggered]**: The planner doesn't know current transcription service capabilities and pricing. A research branch is created with the question "What transcription services meet our accuracy and cost requirements?"

**[Research occurs over 2 days]**

**[Merge Gate]**: Research findings recommend two viable options with trade-offs. The planner accepts the findings, adding a new constraint (must support speaker diarization) and narrowing to a primary recommendation.

**SHARPEN (5 turns)**: With research complete, prioritization becomes concrete. Trade-offs between cost and accuracy are made explicit.

**BOUNDARY / GROUND (6 turns combined)**: The remaining stages proceed with research-informed context.

### 8.3 Example: Exploration Branch

A planner is designing an API but unsure whether to use REST or GraphQL.

**OPEN through FOLLOW (normal progression)**

**[Exploration Branch triggered]**: Instead of forcing a premature decision, the system creates a fork at the API design decision point. The user explores the REST path first, then returns to the fork point and explores GraphQL. Each path works through how the design would look with that choice.

**[Merge Gate after exploration]**: Both paths return to a merge gate that presents the comparison, including the decision dependency impact: "With REST, decisions D-12 through D-15 were made this way. With GraphQL, they differ at D-13 and D-14. Here are the conflicts to resolve."

**[Continue with selected path]**: The main arc continues with the chosen approach, and the rejected path is archived (not deleted—it remains accessible as reference).

---

## Part 9: Implementation Guidance

This section provides guidance for implementing the questioning arc. It bridges the conceptual definition to practical implementation patterns.

### 9.1 Stage Implementation Pattern

Each stage should be implemented as a distinct workflow step that can:

- Receive state from the previous stage (or initial state for OPEN)
- Execute stage-specific question logic
- Produce stage-specific artifacts
- Evaluate exit conditions
- Transition to the next stage or suspend for research

Stage logic should be encapsulated so that changes to one stage don't cascade to others.

### 9.2 Transition Triggers

Implement transitions as explicit triggers rather than implicit state checks:

**Forward triggers**: Exit condition checklist passes AND (user explicit signal OR system completion detection).

**Backward triggers**: User explicit request to revisit OR detected invalidation of prior decisions.

**Branch triggers**: User explicit request OR system detection of blocking uncertainty OR widget "Research this" selection.

### 9.3 Merge Gate Implementation

Merge gates require:

- Serialization of proposed changes in reviewable format
- User interface for review actions (accept/edit/reject/defer)
- Logging of decision with full context
- State mutation only after explicit acceptance
- Rollback capability if merge is later reversed

### 9.4 Degraded Operation

Per System Definition §3.8, the arc should continue functioning when subsystems fail:

**If memory retrieval fails**: Continue with session state only; flag that prior context may be incomplete.

**If research tools fail**: Allow manual research entry; note that system-assisted research is unavailable.

**If widget rendering fails**: Fall back to text-based alternatives; preserve the questions even if the presentation is basic.

---

## Appendix A: Glossary

**Adversarial evaluator**: A user-triggered research branch subtype that deliberately argues against a decision to surface risks and hidden assumptions.

**Archivist**: A background subsystem that silently monitors planning, files decisions, maintains the dependency graph, detects merge conflicts, and generates audit output. Not an agent per DD-15-01's role definitions.

**Convergence signal**: Indication that a stage is approaching completion, derived from user statements, information density, or checklist passage.

**Decision dependency**: A typed relationship (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) between two decisions within a planning arc.

**Decision status**: The planning-time state of a decision (EXPLORING, ENABLED, BLOCKED, CHOSEN, REJECTED, DEFERRED)—distinct from artifact lifecycle status.

**Escape hatch**: A widget option that allows users to exit structured choices when none fit their needs.

**Exploration branch**: A Git-like fork of the planning state created to investigate an alternative approach from a prior decision point.

**Fast mode**: A user-controlled setting where the system pre-fills suggestions for the user to edit rather than asking open-ended questions. All stages still apply.

**Merge gate**: A checkpoint requiring explicit human confirmation before proposed changes become canonical.

**Questioning arc**: The structured five-stage progression from vague intent to implementation-ready specification.

**Research branch**: A temporary divergence from the main planning workflow to investigate specific uncertainty.

**Stage**: One of the five phases of the questioning arc (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND).

**Suspension point**: A natural pause point where arc state is fully serialized and the session can safely end.

**Working memory**: The accumulated decisions, requirements, and context for a project, persisted across sessions.

---

## Appendix B: Related Documents

- **STD-18-01**: Questioning Arc Standards (companion document with checklists and validation rules)
- **DD-18-02**: Elicitation Methods (guidance on varied questioning techniques)
- **DD-19-01**: Widget Schema Definition (widget types and behaviors)
- **DD-13-01**: Artifact Taxonomy (document types and lifecycle)
- **DD-15-01**: Governance Definitions (roles, permissions, and audit)
- **DD-20-01**: Evidence Standards (citation format and research linking)
- **RF-02-01**: Orchestration Research Findings (framework selection analysis)
- **ADR-02-01**: Orchestration Selection (Mastra + AI SDK decision)
- **Compass System Definition**: Authoritative system specification (§2.1, §2.3, §2.6)

---

*End of Questioning Arc Definition (DD-18-01)*
