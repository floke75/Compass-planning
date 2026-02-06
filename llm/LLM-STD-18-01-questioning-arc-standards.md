---
id: STD-18-01-LLM
type: standard
area: 18-questioning-arc
title: Questioning Arc Standards (LLM View)
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of validation rules, completion criteria, and quality thresholds for the questioning arc including decision dependency and status rules
tags: [questioning-arc, standards, validation, checklists, quality, llm, view]
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
source_updated: 2026-02-06
staleness: fresh
---

# Questioning Arc Standards (LLM View)

## LLM Summary
STD-18-01 establishes enforceable validation rules for the questioning arc defined in DD-18-01. It specifies stage completion criteria (required elements, conversation minimums, exit validation), transition rules (forward, backward, branch), merge gate standards (triggering, content, logging, deferred handling), state persistence requirements, quality metrics, and error handling. New additions cover decision dependency validation (no cycles, DEPENDS_ON targets resolved before CHOSEN, CONFLICTS_WITH surfaced), decision status rules (CHOSEN requires resolved dependencies, BLOCKED cannot become CHOSEN, all must-haves resolved before GROUND), and exploration branch merge standards (conflict resolution presentation, staleness detection with configurable thresholds, and branch state validation before fork). Stage completion criteria are identical regardless of fast mode.

## Canonical Statements
- All "cannot proceed" validation rules MUST pass before forward stage transition.
- No unresolved merge gates MAY block the current stage during forward transition.
- OPEN MUST have: problem statement ≥20 chars, ≥1 user type.
- FOLLOW MUST have: ≥3 requirements, ≥1 primary use case.
- SHARPEN MUST have: all requirements prioritized, ≥1 trade-off decided.
- BOUNDARY MUST have: ≥1 explicit exclusion, user boundary confirmation.
- GROUND MUST have: budget, reliability tier, security/access, timeline specified.
- DEPEND-001: No dependency cycles permitted (Block).
- DEPEND-002: DEPENDS_ON targets MUST be resolved before dependent decision is CHOSEN (Block).
- DEPEND-003: CONFLICTS_WITH relationships SHOULD be surfaced before CHOSEN (Warn).
- STATUS-001: CHOSEN requires all DEPENDS_ON targets resolved (Block).
- STATUS-002: BLOCKED decisions MUST NOT transition to CHOSEN without resolving blocker (Block).
- STATUS-003: All must-have decisions MUST reach CHOSEN or DEFERRED before GROUND completion (Block).
- BRANCH-007: Branch state MUST be restorable before allowing fork (Block).
- Merge gate presentations MUST include summary, source attribution, impact assessment, and all four options.
- Merge gate resolutions MUST be logged with ID, timestamp, resolution, resolver, rationale (for reject/defer), and state hashes.
- Merge conflict resolution MUST present conflicts side-by-side with dependency graph paths and cascading changes.
- Stage completion criteria are identical regardless of mode (normal or fast).

## Dependencies and Interfaces
- Arc definition and decision tracking: `DD-18-01`.
- Artifact lifecycle: `DD-13-01`.
- Governance and audit: `DD-15-01` and `STD-15-01`.

## Core Invariants
- Validation rules are checkpoints, not guidelines—they block or warn as specified.
- Forward transitions require all "Block" rules to pass.
- Merge gates are mandatory for branch completion, exploration selection, and agent-proposed changes.
- Decision dependency and status rules enforce consistency of the decision graph.
- Fast mode does not change any validation rule.

## Compliance Checklist
- [ ] All stage validation rules implemented (OPEN-001 through GROUND-005, STATUS-003)
- [ ] All branch validation rules implemented (BRANCH-001 through BRANCH-007)
- [ ] All dependency rules implemented (DEPEND-001 through DEPEND-003)
- [ ] All status rules implemented (STATUS-001 through STATUS-003)
- [ ] Merge gate content requirements met (summary, attribution, impact, four options)
- [ ] Merge gate logging includes all required fields
- [ ] Merge conflict resolution presents side-by-side conflicts with dependency paths
- [ ] Branch staleness detection configured (default 14 days, escalation at 14/21/30)
- [ ] Fork validates branch state is restorable before proceeding
- [ ] State saves on all required events (stage transition, merge gate, branch ops, session end)
- [ ] State validation on resume checks version, references, branches, merge queue

## Glossary Snapshot
- **Block severity**: Validation failure that prevents the action from proceeding.
- **Warn severity**: Validation failure that flags an issue but allows proceeding.
- **Branch staleness**: Configurable inactivity threshold (default 14 days) after which a branch is surfaced for review.
