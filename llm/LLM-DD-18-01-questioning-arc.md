---
id: DD-18-01-LLM
type: definition
area: 18-questioning-arc
title: Questioning Arc Definition (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the five-stage questioning arc and branching mechanics
tags: [questioning-arc, planning, workflow, state-machine, llm, view]
related:
  - DD-18-01
  - STD-18-01
  - DD-19-01
  - ADR-02-01
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
view: llm
source_id: DD-18-01
source_updated: 2026-02-03
staleness: fresh
---

# Questioning Arc Definition (LLM View)

## LLM Summary
DD-18 defines the questioning arc, a state-machine workflow that turns vague ideas into implementation-ready specs. It specifies five stages: OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND, with goals, artifacts produced, exit conditions, and typical turn counts. The arc supports non-linear movement, research branches for uncertainty, and explicit merge gates where humans approve changes to canonical artifacts. It distinguishes research branches (information gathering) from exploration branches (parallel option walkthroughs) and requires comparison and selection before merging. The document defines state management with conversation state, working memory, and branch context, all serialized to JSON so sessions can pause and resume without replaying full chat. It ties arc progression to widgets, research triggers, and standards in STD-18, and integrates with governance and evidence requirements. This is the core planning engine of Compass and is distinct from widget schemas or orchestration tooling.

## Canonical Statements
- The planning workflow MUST follow OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND stages.
- Each stage MUST produce or update artifacts and decisions with explicit status.
- Research branches MUST pause the main arc and merge via human-approved merge gates.
- Exploration branches MUST compare alternatives and select one path before merging.
- Arc state MUST be serializable to JSON for pause and resume.

## Scope and Non-Goals
- In scope: Stage definitions, transitions, branching, merge gates, and state persistence.
- Out of scope: Widget schema details, orchestration framework specifics, and citation standards.

## Dependencies and Interfaces
- Stage standards and completion criteria: `STD-18-01`.
- Widget taxonomy and UX guarantees: `DD-19-01` and `STD-19-01`.
- Orchestration framework context: `ADR-02-01`.
- Governance and audit logging: `DD-15-01` and `STD-15-01`.

## Evidence and Freshness
- Source updated 2026-01-26; staleness marked fresh.
- Evidence standards for research branches are defined in `DD-20-01` and `STD-20-01`.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `DD-18-01` with no semantic changes.

## Core Invariants
- Five-stage arc governs planning conversations.
- Merge gates require human approval before canonical changes.
- State is externalized and serializable.

## Glossary Snapshot
- **OPEN**: Extract the core idea and motivation.
- **FOLLOW**: Expand requirements and use cases.
- **SHARPEN**: Prioritize and force trade-offs.
- **BOUNDARY**: Define out-of-scope and rejected options.
- **GROUND**: Apply constraints and finalize handoff readiness.
- **Research branch**: Investigation detour that pauses the main arc.
- **Exploration branch**: Parallel option walkthrough before selection.
- **Merge gate**: Human checkpoint to accept, edit, reject, or defer changes.
