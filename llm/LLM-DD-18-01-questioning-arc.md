---
id: DD-18-01-LLM
type: definition
area: 18-questioning-arc
title: Questioning Arc Definition (LLM View)
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of the five-stage questioning arc, decision tracking, Git-like branching, the Archivist, and merge gate mechanics
tags: [questioning-arc, planning, workflow, state-machine, decisions, branching, llm, view]
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
view: llm
source_id: DD-18-01
source_updated: 2026-02-06
staleness: fresh
---

# Questioning Arc Definition (LLM View)

## LLM Summary
DD-18-01 defines the questioning arc, a state-machine workflow that turns vague ideas into implementation-ready specs. It specifies five stages (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND) with goals, artifacts, exit conditions, and typical turn counts. The arc supports a user-controlled fast mode that pre-fills suggestions without skipping stages. Decisions are tracked through a dependency graph with five relationship types (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) and a status lifecycle (EXPLORING → CHOSEN/REJECTED/BLOCKED/DEFERRED) distinct from artifact lifecycle states. Research branches support four subtypes (investigation, validation, specialist, adversarial) with merge gates for human approval. Exploration branches use a Git-like fork model: users can navigate to any prior decision point, fork planning state, build out an alternative path, and merge back with dependency-graph-driven conflict detection. The Archivist is a background subsystem (not an agent) that maintains the dependency graph, detects cycles and conflicts, files decisions, links research, and generates audit output. All state is serializable to JSON for pause/resume across sessions.

## Canonical Statements
- The planning workflow MUST follow OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND stages.
- Each stage MUST produce or update artifacts and decisions with explicit status.
- Fast mode MUST NOT skip stages, reduce output quality, or auto-accept without user confirmation.
- Decision dependencies form a directed graph; cycles MUST be detected and are invalid.
- DEPENDS_ON targets MUST be resolved before a dependent decision is CHOSEN.
- CONFLICTS_WITH relationships MUST be surfaced before a decision is CHOSEN.
- A BLOCKED decision MUST NOT transition to CHOSEN without resolving the blocker.
- All must-have decisions MUST reach CHOSEN or DEFERRED before GROUND completion.
- Research branches MUST pause the main arc and merge via human-approved merge gates.
- Exploration branches MUST use fork-from-decision-point model with dependency-graph conflict detection at merge.
- Arc state MUST be serializable to JSON for pause and resume.
- Merge gate resolution MUST trigger registered integration handlers per `DD-17-01`.
- The Archivist MUST NOT participate in the planning conversation or require a sponsoring user.

## Scope and Non-Goals
- In scope: Stage definitions, transitions, fast mode, decision dependencies, decision statuses, research branching with subtypes, Git-like exploration branching, the Archivist, merge gates, and state persistence.
- Out of scope: Widget schema details (`DD-19-01`), orchestration framework specifics (`ADR-02-01`), citation standards (`STD-20-01`), and elicitation method prescriptions (`DD-18-02`).

## Dependencies and Interfaces
- Stage standards and completion criteria: `STD-18-01`.
- Elicitation method guidance: `DD-18-02`.
- Widget taxonomy and UX guarantees: `DD-19-01` and `STD-19-01`.
- Orchestration framework context: `ADR-02-01`.
- Governance and audit logging: `DD-15-01` and `STD-15-01`.
- Integration handler triggering: `DD-17-01`.
- Evidence and citation format: `DD-20-01`.

## Core Invariants
- Five-stage arc governs planning conversations.
- Decision dependencies form a directed acyclic graph maintained by the Archivist.
- Decision status lifecycle (EXPLORING/ENABLED/BLOCKED/CHOSEN/REJECTED/DEFERRED) is separate from artifact lifecycle (draft/review/active/deprecated).
- Merge gates require human approval before canonical changes.
- State is externalized and serializable.
- The Archivist is infrastructure, not an agent.

## Definition Matrix
| Concept | Values | Constraints |
|---------|--------|-------------|
| Stages | OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND | Sequential with backward revisitation allowed |
| Decision dependencies | DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS | Directed acyclic graph; cycles invalid |
| Decision statuses | EXPLORING, ENABLED, BLOCKED, CHOSEN, REJECTED, DEFERRED | History preserved; transitions triggered by user action, dependency resolution, or merge |
| Research branch subtypes | investigation, validation, specialist, adversarial | Same lifecycle; output format varies |
| Merge gate actions | Accept, Edit, Reject, Defer | All four always available |
| Fast mode | Normal (default), Fast (user toggle) | Same stages, same exit conditions, same output quality |

## Glossary Snapshot
- **OPEN**: Extract the core idea and motivation (3-5 turns).
- **FOLLOW**: Expand requirements and use cases (10-20 turns).
- **SHARPEN**: Prioritize and force trade-offs (5-8 turns).
- **BOUNDARY**: Define out-of-scope and rejected options (4-6 turns).
- **GROUND**: Apply constraints and finalize handoff readiness (3-5 turns).
- **Decision dependency**: Typed relationship (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) between decisions.
- **Decision status**: Planning-time state of a decision (EXPLORING → CHOSEN/REJECTED/BLOCKED/DEFERRED), distinct from artifact lifecycle.
- **Archivist**: Background subsystem for decision filing, dependency analysis, conflict detection, and audit generation.
- **Fast mode**: User toggle that pre-fills suggestions; stages and exit conditions unchanged.
- **Adversarial evaluator**: User-triggered branch subtype that argues against a decision to surface risks.
- **Research branch**: Investigation detour that pauses the main arc.
- **Exploration branch**: Git-like fork from a decision point to explore an alternative path.
- **Merge gate**: Human checkpoint to accept, edit, reject, or defer changes.
