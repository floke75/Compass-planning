---
id: STD-18-01-LLM
type: standard
area: 18-questioning-arc
title: Questioning Arc Standards (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of questioning arc validation and completion standards
tags: [questioning-arc, standards, validation, checklists, llm, view]
related:
  - STD-18-01
  - DD-18-01
  - DD-15-01
  - STD-15-01
links:
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-15-01"
  - rel: related
    target_id: "STD-15-01"
  - rel: companion
    target_id: "DD-18-01"
view: llm
source_id: STD-18-01
source_updated: 2026-02-03
staleness: fresh
---

# Questioning Arc Standards (LLM View)

## LLM Summary
STD-18 defines enforceable validation rules and completion criteria for the questioning arc stages. It specifies required artifacts and checks for OPEN, FOLLOW, SHARPEN, BOUNDARY, and GROUND, including minimum content, transition confirmations, and quality thresholds. The standard emphasizes explicit trade-offs, boundary confirmation, and constraint completeness before progression. It also formalizes merge gate protocols and validation responsibilities across system, agents, and humans. These rules operationalize DD-18 and ensure planning workflows produce consistent, implementation-ready outputs rather than incomplete conversations. It adds practical safeguards such as minimum exchange counts and breadth checks to prevent shallow planning. It also defines explicit user confirmation prompts at key transitions. The standard is intended to be enforced by validation logic during the workflow and used by reviewers for quality assurance.

## Canonical Statements
- Stage transitions MUST pass defined completion criteria.
- Trade-offs and boundaries MUST be explicitly recorded.
- Merge gates MUST require explicit approval.
- Validation rules apply to both system and human review.

## Scope and Non-Goals
- In scope: Stage completion criteria, validation rules, and merge gate standards.
- Out of scope: The conceptual arc definition (see `DD-18-01`).

## Dependencies and Interfaces
- Arc definition: `DD-18-01`.
- Governance and audit context: `DD-15-01`, `STD-15-01`.

## Evidence and Freshness
- Source updated 2026-01-26; staleness marked fresh.
- No external citations required; standards are internal.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `STD-18-01` with no semantic changes.

## Enforcement
- Enforced by workflow validation logic and planner review.

## Compliance Checklist
- [ ] Each stage meets minimum required elements.
- [ ] Explicit confirmation obtained before stage transitions.
- [ ] Trade-offs and boundaries are documented.
- [ ] Merge gates logged with decision outcomes.
