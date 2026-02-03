---
id: DD-18-01
type: definition
area: 18-questioning-arc
title: Questioning Arc Definition
status: draft
created: 2026-01-26
updated: 2026-02-03
author: compass-research
summary: Defines the structured questioning progression that transforms vague intent into implementation-ready specifications, including the five-stage planning workflow, research branching, and merge gate protocols
tags: [questioning-arc, planning, workflow, state-machine, conversation]
related:
  - RF-02-01
  - ADR-02-01
  - DD-13-01
  - DD-15-01
links:
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-15-01"
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
- How users move between stages (transitions and triggers)
- Research branching and merge gates for handling uncertainty
- State persistence and session management
- How the arc integrates with widgets and artifacts

**What this document does not cover**:

- Specific widget implementations (see DD-19-01)
- Orchestration framework details (see ADR-02-01)
- Evidence and citation standards (see STD-20-01)

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

**Lateral research**: When uncertainty blocks progress. "I don't know enough about X to answer that question" triggers a research branch (see Part 2).

**Convergence signals**: The system watches for signals that a stage is complete, including explicit statements ("I think we've covered the main cases"), diminishing new information (several turns without substantial additions), and completeness checks passing (see STD-18-01 for checklists).

---

## Part 2: Research Branching and Merge Gates

Not everything can be decided in a single planning session. Sometimes the right answer is "we need to find out," and Compass supports this with research branches.

### 2.1 What Research Branching Is

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

### 2.2 Triggering Research Branches

Research branches can be triggered in three ways:

**User request**: The user explicitly says they need to investigate something. "I need to research vendor options before I can answer that" or "Let me find out what the security team requires."

**System detection**: The system detects uncertainty that blocks progress. When a question gets responses like "I'm not sure" or "it depends on something I don't know," the system can offer to create a research branch.

**Widget escape hatch**: Every widget includes a "Research this" option. When users select it, the system creates a research brief and pauses for investigation.

### 2.3 Research Branch Lifecycle

A research branch follows its own lifecycle:

**Creation**: The system captures the research question, relevant context from the main arc, success criteria (what would count as a useful answer), and the insertion point (where findings will merge back).

**Investigation**: Research occurs—this might be immediate (system-assisted web research), asynchronous (user investigates and returns later), or delegated (assigned to another person or agent).

**Documentation**: Findings are captured in Research Finding format (RF-*), following STD-20-01 evidence standards. The output includes what was discovered, sources and confidence levels, recommendation and rationale, and impact on the main arc (what changes based on this).

**Merge gate**: Before findings affect the main arc, a human reviews and approves via the merge gate (see 2.4).

### 2.4 Merge Gates

Merge gates are explicit checkpoints where proposed changes to canonical artifacts require human confirmation. This is a core principle from the System Definition (§1.7): "Sub-agents produce proposals, not canonical truth."

**When merge gates appear**:

- Research findings are ready to integrate into the main arc
- A branch exploration is ready to merge
- An agent proposes significant changes to specifications
- Conflicting information needs resolution

**What happens at a merge gate**:

The system presents a summary of proposed changes, including what would change (specific artifacts or decisions), why (the source of the proposal), and what the alternative is (reject, edit, or accept). The human reviews and chooses: Accept as-is, Edit before merging, Reject and continue without changes, or Defer for later decision.

**Merge gate resolution is always logged**: who, when, what decision, and rationale. This creates the audit trail that makes planning history reconstructable.

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

## Part 3: Exploration Branching

Separate from research branches, Compass supports exploration branches for investigating alternative approaches in parallel.

### 3.1 What Exploration Branching Is

An exploration branch creates parallel planning paths to investigate different approaches before committing to one. Unlike research branches (which gather information), exploration branches work through how a decision would play out.

```
                              ┌──────────────────┐
                         ┌───>│  Explore Path A  │───┐
Main Arc: ... ─> FOLLOW ─┤    └──────────────────┘   ├─> [MERGE GATE] ─> SHARPEN ─> ...
                         └───>┌──────────────────┐───┘
                              │  Explore Path B  │
                              └──────────────────┘
```

**When exploration branching is useful**: When a significant design decision affects many downstream choices, and the right answer isn't clear without working through implications. "Should we use approach A or approach B?" becomes "Let's see what each approach would look like."

### 3.2 Exploration Branch Lifecycle

**Creation**: The system identifies the decision point and creates parallel branches. Each branch carries forward the same context but assumes a different decision.

**Parallel exploration**: Each branch proceeds through relevant planning steps independently. An implementation approach branch might work through architecture implications, dependency requirements, and integration considerations for each option.

**Comparison**: When exploration completes, the system generates a comparison summary showing how each approach played out, including trade-offs discovered, complexity differences, and risks identified.

**Merge gate**: The user reviews the comparison and selects which path to continue. The selected path becomes the main arc; the rejected path is archived (not deleted) as reference.

### 3.3 Exploration vs. Research Branches

The two branch types serve different purposes:

| Aspect | Research Branch | Exploration Branch |
|--------|-----------------|-------------------|
| Purpose | Gather information | Work through implications |
| Trigger | "I don't know X" | "A or B—let's see which" |
| Output | Findings document | Design comparison |
| Duration | Variable (hours to weeks) | Typically same session |
| Parallelism | Usually sequential | Usually parallel |

---

## Part 4: State Management

The questioning arc maintains state across multiple sessions, potentially spanning days or weeks. This section defines how state is structured and preserved.

### 4.1 State Composition

Arc state consists of three layers:

**Conversation state**: The immediate context of the current session—recent exchanges, pending questions, active widgets. This is ephemeral within a session but serialized between sessions.

**Working memory**: The accumulated decisions, requirements, and context for the current project. This persists across sessions and contains the substantive content of planning.

**Branch context**: Metadata about the current position in the arc—active stage, branching history, pending merge gates. This enables resume-from-where-you-left-off.

### 4.2 State Serialization

All arc state is serializable to JSON. This is a core architectural requirement (System Definition §1.7: "State is externalized"). The system reconstructs context from stored state, not from conversation history alone.

**Why this matters**: LLM context windows are finite and conversation histories can become large. By externalizing state, the system can resume sessions without replaying entire histories.

Per ADR-02-01, Mastra's thread-based memory provides the persistence layer. Working memory uses Zod schemas that define exactly what's stored, enabling both type safety and clear documentation of state structure.

### 4.3 Pause and Resume

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

### 4.4 State Isolation

State is isolated at multiple levels:

**Project isolation**: Each project has independent state. Decisions in Project A don't affect Project B.

**Branch isolation**: Research and exploration branches have their own state that doesn't affect the main arc until merged.

**Session isolation**: Concurrent sessions (if supported) on the same project are coordinated to prevent conflicting mutations.

---

## Part 5: Integration Points

The questioning arc integrates with several other Compass subsystems.

### 5.1 Widget System (DD-19-01)

Widgets are the primary mechanism for structured input during the questioning arc. The arc determines when to present widgets and what type; the widget system handles rendering and response collection.

**How they interact**:

- The arc's current stage and question context determine widget appropriateness
- OPEN stage typically uses free-text with optional structure
- FOLLOW stage uses exploratory widgets (multi-select, branching questions)
- SHARPEN stage uses prioritization widgets (ranking, sliders, trade-off tables)
- BOUNDARY stage uses confirmation widgets (checklists, yes/no gates)
- GROUND stage uses constraint widgets (range selectors, pre-defined option sets)

Every widget includes three guaranteed escape hatches: "None of these / describe instead," "Help me think" (system provides framing), and "Research this" (creates research branch).

### 5.2 Artifact System (DD-13-01)

The questioning arc produces and updates artifacts throughout its progression.

**Creation patterns**:

- OPEN creates initial project context artifacts
- FOLLOW creates requirement and use case artifacts
- SHARPEN creates decision records (ADRs) for significant trade-offs
- BOUNDARY updates specifications with explicit exclusions
- GROUND completes specifications with constraint details

**Artifact lifecycle interaction**: Artifacts created during the arc begin in `draft` status. They transition to `active` when the arc completes or when explicitly approved at merge gates.

### 5.3 Governance System (DD-15-01)

The questioning arc interacts with governance through three mechanisms:

**Permissions**: Only users with Planner role (or higher) can advance arc stages or approve merge gates.

**Agent constraints**: Agents can participate in the arc (drafting, research, suggestions) but cannot approve merge gates or advance to GROUND stage completion without human confirmation.

**Audit logging**: Stage transitions, merge gate decisions, and branch operations are logged per DD-15-01 audit requirements.

### 5.4 Orchestration Layer (ADR-02-01)

The questioning arc is implemented using the orchestration framework selected in ADR-02-01 (Mastra + Vercel AI SDK v6).

**Key mappings**:

- Arc stages map to Mastra workflow steps
- Stage transitions map to step transitions with conditional branching
- Research branches map to parallel workflow paths
- Merge gates map to Mastra's `suspend()` function with human-in-the-loop resume
- State persistence uses Mastra's thread-based memory with PostgreSQL backend

---

## Part 6: Conceptual Example Flows

The following examples illustrate how the questioning arc might progress for different types of projects. These are conceptual patterns, not specific implementations.

### 6.1 Example: New Internal Tool

A planner wants to create a dashboard for tracking podcast metrics.

**OPEN (3 turns)**: The conversation establishes that the core need is visibility into podcast performance, the primary users are the podcast production team, and success means producers can answer basic performance questions without asking analysts.

**FOLLOW (12 turns)**: The conversation explores what metrics matter (downloads, completion rates, audience geography), what comparisons users need (episode vs. episode, show vs. show, period vs. period), what existing data sources exist, and what level of real-time freshness matters.

**SHARPEN (6 turns)**: Widgets help prioritize: "Rank these five metric categories." "If you could only have one comparison view, which?" "Where does data freshness fall on this spectrum between 'real-time critical' and 'weekly is fine'?"

**BOUNDARY (4 turns)**: The conversation explicitly excludes predictive analytics, integration with ad platforms, and external sharing. It defers multi-show comparison views to Phase 2.

**GROUND (3 turns)**: Constraints are applied—budget ceiling of $50/month for external services, reliability tier of "internal tool," accessible to anyone with EFN SSO, target launch in 6 weeks.

### 6.2 Example: Research-Heavy Planning

A planner wants to select a video transcription service.

**OPEN (4 turns)**: The core need is automated transcription for video logging. Users are video editors and producers. Success means transcripts are accurate enough for searchability.

**FOLLOW (8 turns)**: Requirements emerge—accuracy threshold, turnaround time, integration with existing media asset management, speaker identification needs.

**[Research Branch triggered]**: The planner doesn't know current transcription service capabilities and pricing. A research branch is created with the question "What transcription services meet our accuracy and cost requirements?"

**[Research occurs over 2 days]**

**[Merge Gate]**: Research findings recommend two viable options with trade-offs. The planner accepts the findings, adding a new constraint (must support speaker diarization) and narrowing to a primary recommendation.

**SHARPEN (5 turns)**: With research complete, prioritization becomes concrete. Trade-offs between cost and accuracy are made explicit.

**BOUNDARY / GROUND (6 turns combined)**: The remaining stages proceed with research-informed context.

### 6.3 Example: Exploration Branch

A planner is designing an API but unsure whether to use REST or GraphQL.

**OPEN through FOLLOW (normal progression)**

**[Exploration Branch triggered]**: Instead of forcing a premature decision, the system creates two parallel exploration paths—one assuming REST, one assuming GraphQL. Each path works through how the design would look with that choice.

**[Merge Gate after exploration]**: Both paths return to a merge gate that presents the comparison: "With REST, the design looks like X with trade-offs A and B. With GraphQL, the design looks like Y with trade-offs C and D. Which path do you want to continue?"

**[Continue with selected path]**: The main arc continues with the chosen approach, and the rejected path is archived (not deleted—it remains accessible as reference).

---

## Part 7: Implementation Guidance

This section provides guidance for implementing the questioning arc. It bridges the conceptual definition to practical implementation patterns.

### 7.1 Stage Implementation Pattern

Each stage should be implemented as a distinct workflow step that can:

- Receive state from the previous stage (or initial state for OPEN)
- Execute stage-specific question logic
- Produce stage-specific artifacts
- Evaluate exit conditions
- Transition to the next stage or suspend for research

Stage logic should be encapsulated so that changes to one stage don't cascade to others.

### 7.2 Transition Triggers

Implement transitions as explicit triggers rather than implicit state checks:

**Forward triggers**: Exit condition checklist passes AND (user explicit signal OR system completion detection).

**Backward triggers**: User explicit request to revisit OR detected invalidation of prior decisions.

**Branch triggers**: User explicit request OR system detection of blocking uncertainty OR widget "Research this" selection.

### 7.3 Merge Gate Implementation

Merge gates require:

- Serialization of proposed changes in reviewable format
- User interface for review actions (accept/edit/reject/defer)
- Logging of decision with full context
- State mutation only after explicit acceptance
- Rollback capability if merge is later reversed

### 7.4 Degraded Operation

Per System Definition §3.8, the arc should continue functioning when subsystems fail:

**If memory retrieval fails**: Continue with session state only; flag that prior context may be incomplete.

**If research tools fail**: Allow manual research entry; note that system-assisted research is unavailable.

**If widget rendering fails**: Fall back to text-based alternatives; preserve the questions even if the presentation is basic.

---

## Appendix A: Glossary

**Convergence signal**: Indication that a stage is approaching completion, derived from user statements, information density, or checklist passage.

**Escape hatch**: A widget option that allows users to exit structured choices when none fit their needs.

**Exploration branch**: A parallel planning path created to investigate alternative approaches before committing to one.

**Merge gate**: A checkpoint requiring explicit human confirmation before proposed changes become canonical.

**Questioning arc**: The structured five-stage progression from vague intent to implementation-ready specification.

**Research branch**: A temporary divergence from the main planning workflow to investigate specific uncertainty.

**Stage**: One of the five phases of the questioning arc (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND).

**Suspension point**: A natural pause point where arc state is fully serialized and the session can safely end.

**Working memory**: The accumulated decisions, requirements, and context for a project, persisted across sessions.

---

## Appendix B: Related Documents

- **STD-18-01**: Questioning Arc Standards (companion document with checklists and validation rules)
- **DD-19-01**: Widget Schema Definition (widget types and behaviors)
- **DD-13-01**: Artifact Taxonomy (document types and lifecycle)
- **DD-15-01**: Governance Definitions (roles, permissions, and audit)
- **RF-02-01**: Orchestration Research Findings (framework selection analysis)
- **ADR-02-01**: Orchestration Selection (Mastra + AI SDK decision)
- **Compass System Definition**: Authoritative system specification (§2.1, §2.3, §2.6)

---

*End of Questioning Arc Definition (DD-18-01)*
