---
id: STD-18-01
type: standard
area: 18-questioning-arc
title: Questioning Arc Standards
status: draft
created: 2026-01-26
updated: 2026-02-03
author: compass-research
summary: Establishes validation rules, completion checklists, and quality criteria for the questioning arc workflow, including stage transition requirements and merge gate protocols
tags: [questioning-arc, standards, validation, checklists, quality]
related:
  - DD-18-01
  - DD-13-01
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
companion: DD-18-01
---

# Questioning Arc Standards

## Document Purpose

This document establishes enforceable standards for the questioning arc workflow defined in DD-18-01. Where DD-18-01 explains what the questioning arc is and why it works this way, this document specifies validation rules, completion criteria, and quality thresholds that implementations must meet.

**Who enforces these standards**: The Compass system itself (via validation logic), LLM agents participating in planning, and human planners reviewing arc outputs.

**When to reference this document**: When implementing arc logic, when validating arc outputs, when auditing planning quality, or when training users on proper arc usage.

---

## Part 1: Stage Completion Criteria

Each stage has specific completion criteria. These are not just guidelines—they are checkpoints that must pass before transition is permitted.

### 1.1 OPEN Stage Completion

The OPEN stage is complete when all of the following are true:

**Required elements**:

| Element | Validation Rule | Failure Action |
|---------|-----------------|----------------|
| Problem statement | Non-empty string, minimum 20 characters | Cannot proceed |
| At least one user type | Named or described stakeholder | Cannot proceed |
| Success indicator | At least one measurable or observable outcome | Warning only |

**Conversation minimums**:

The OPEN stage should include at least 3 substantive exchanges (user input + system response). Fewer than 3 exchanges triggers a warning but does not block progression. The rationale: Extremely brief OPEN stages often indicate insufficient exploration, but some well-prepared users genuinely know what they want.

**Exit validation**:

Before transitioning from OPEN to FOLLOW, the system presents a summary of captured elements and requests explicit confirmation: "Here's what I understand so far: [summary]. Ready to explore requirements, or should we clarify anything first?"

---

### 1.2 FOLLOW Stage Completion

The FOLLOW stage is complete when:

**Required elements**:

| Element | Validation Rule | Failure Action |
|---------|-----------------|----------------|
| Requirements captured | At least 3 distinct requirements | Cannot proceed |
| Use cases identified | At least 1 primary use case | Cannot proceed |
| Integration points noted | Documented (may be "none identified") | Warning only |
| Research triggers logged | All uncertainties either resolved or flagged | Warning only |

**Diminishing returns detection**:

The system tracks new information density per turn. When 3 consecutive turns yield no new requirements, use cases, or integration points, the system suggests transitioning: "We've covered a lot of ground. Ready to prioritize, or is there more to explore?"

**Breadth check**:

Before transitioning to SHARPEN, the system runs a breadth check using category prompts: "Have we discussed [category]?" for relevant categories such as data requirements, user permissions, error handling, integrations, and performance expectations. Any uncovered category triggers a prompt before proceeding.

---

### 1.3 SHARPEN Stage Completion

The SHARPEN stage is complete when:

**Required elements**:

| Element | Validation Rule | Failure Action |
|---------|-----------------|----------------|
| Requirements prioritized | All requirements assigned must-have, nice-to-have, or out-of-scope | Cannot proceed |
| At least one trade-off decided | Explicit choice between competing concerns | Cannot proceed |
| Acceptance criteria for must-haves | Each must-have has testable acceptance criteria | Warning only |

**Trade-off documentation**:

Every trade-off decision must include what was traded (the competing concerns), which direction was chosen, the rationale (why this choice), and reversibility assessment (easy, medium, or hard to change later).

**Widget usage expectation**:

The SHARPEN stage should use at least one structured widget (ranking, slider, or trade-off table). Text-only SHARPEN stages are permitted but flagged for review—structured input produces better specifications.

---

### 1.4 BOUNDARY Stage Completion

The BOUNDARY stage is complete when:

**Required elements**:

| Element | Validation Rule | Failure Action |
|---------|-----------------|----------------|
| Out-of-scope list | At least 1 explicit exclusion | Cannot proceed |
| Deferred items documented | Documented (may be "none deferred") | Warning only |
| User confirmation | Explicit "boundaries confirmed" signal | Cannot proceed |

**Boundary validation prompt**:

Before completing BOUNDARY, the system presents the boundary summary and requests explicit confirmation: "Here's what's OUT of scope: [list]. And deferred to later: [list]. Are these boundaries correct?"

The user must explicitly confirm. Responses like "sure" or "looks good" count as confirmation. Responses that add new items ("also exclude X") reset the confirmation requirement.

---

### 1.5 GROUND Stage Completion

The GROUND stage is complete when:

**Required constraint categories**:

| Category | Validation Rule | Failure Action |
|----------|-----------------|----------------|
| Budget | Specified with numeric ceiling or "no budget constraint" | Cannot proceed |
| Reliability tier | One of: internal tool, business critical, always-on | Cannot proceed |
| Security/access | Authentication method + access scope specified | Cannot proceed |
| Timeline | Target date or "no timeline constraint" | Cannot proceed |

**Optional constraint categories** (prompted but not required):

- Compliance requirements
- Performance targets
- Deployment constraints
- Maintenance expectations

**Constraint consistency check**:

Before completing GROUND, the system validates that constraints don't contradict prioritized requirements. For example, if "real-time performance" is a must-have but timeline is "2 weeks," the system flags the conflict: "The timeline seems very tight for the real-time requirement. Should we adjust?"

---

## Part 2: Transition Standards

Stage transitions follow specific rules to ensure completeness while maintaining flexibility.

### 2.1 Forward Transition Requirements

Moving forward (OPEN→FOLLOW, FOLLOW→SHARPEN, etc.) requires:

**Hard requirements** (must be true):

- All "cannot proceed" validation rules pass for current stage
- No unresolved merge gates blocking the current stage
- No active research branches that should complete first (unless explicitly deferred)

**Soft requirements** (generate warnings but don't block):

- Recommended conversation turn count reached
- All optional validation rules pass
- Widget usage expectations met

### 2.2 Backward Transition Allowances

Moving backward (e.g., from GROUND to SHARPEN) is always permitted but requires documentation:

**Documentation requirement**: The system logs why the backward transition occurred (user request, discovered inconsistency, or new information).

**State preservation**: When moving backward, forward-stage work is preserved in a "pending" state. If the backward revisitation changes nothing relevant to the forward stage, pending work can be restored.

**Warning for significant changes**: If backward revisitation changes decisions that affect pending forward-stage work, the system warns: "The change to [decision] affects work you've done in [later stage]. Review that work?"

### 2.3 Branch Transition Requirements

Creating research or exploration branches requires:

| Branch Type | Required Information | Validation |
|-------------|---------------------|------------|
| Research | Research question + success criteria | Question must be specific enough to answer |
| Exploration | Decision point + alternatives to explore | At least 2 alternatives specified |

**Context capture**: When creating a branch, the system captures the return point (where to resume), relevant context (decisions and constraints affecting the branch), and timeout (how long before prompting about stale branches).

---

## Part 3: Merge Gate Standards

Merge gates are critical control points. These standards ensure they function correctly.

### 3.1 Merge Gate Triggering

Merge gates are mandatory in these situations:

| Trigger | Merge Gate Required | Rationale |
|---------|--------------------:|-----------|
| Research branch completion | Yes | Research findings need human validation |
| Exploration branch selection | Yes | Design choices need human commitment |
| Agent-proposed spec changes | Yes | Multi-agent safety principle |
| Conflicting information detected | Yes | Humans resolve conflicts |
| Normal stage transition | No | Checkpoints sufficient |
| User-initiated edits | No | User already confirmed intent |

### 3.2 Merge Gate Content Requirements

Every merge gate presentation must include:

**Summary of proposed changes**: What specifically would change, in plain language. Avoid technical diff notation for non-technical users.

**Source attribution**: Where the proposed changes came from (research findings ID, branch name, agent identifier).

**Impact assessment**: What downstream artifacts or decisions would be affected.

**Options presented**: All four options (Accept, Edit, Reject, Defer) must be available. None should be hidden or disabled.

### 3.3 Merge Gate Resolution Logging

Merge gate resolutions are logged with:

| Field | Required | Format |
|-------|----------|--------|
| Merge gate ID | Yes | UUID |
| Timestamp | Yes | ISO 8601 |
| Resolution | Yes | accept, edit, reject, or defer |
| Resolved by | Yes | User ID |
| Rationale | Conditional | Required for reject and defer; optional for accept and edit |
| Pre-merge state hash | Yes | For audit reconstruction |
| Post-merge state hash | Yes (if accept/edit) | For audit reconstruction |

### 3.4 Deferred Merge Gate Handling

Deferred merge gates must have a resolution deadline. Default is 7 days, configurable per project.

**Reminder schedule**: Day 3 (gentle reminder), Day 5 (warning), Day 7 (escalation to project owner).

**Auto-resolution**: Deferred merge gates do not auto-resolve. After deadline, they escalate but remain pending. Indefinitely deferred gates are periodically surfaced in project health reports.

---

## Part 4: State Persistence Standards

State management must meet these standards for reliability.

### 4.1 Save Frequency

Arc state saves in these situations:

| Event | Save Required | Timing |
|-------|---------------|--------|
| Stage transition | Yes | Before transition completes |
| Merge gate resolution | Yes | Before and after resolution |
| Branch creation | Yes | Before branch starts |
| Branch merge | Yes | Before and after merge |
| User explicit save | Yes | Immediate |
| Session end | Yes | Before session closes |
| Inactivity timeout | Yes | After 5 minutes of no input |

### 4.2 State Validation on Resume

When a session resumes, the system validates state integrity:

**Validation checks**:

- State version compatibility (schema hasn't changed incompatibly)
- Reference integrity (all referenced artifacts exist)
- Branch consistency (no orphaned branches)
- Merge gate queue validity (no stale gates without deadlines)

**Validation failure handling**: If validation fails, the system presents the issue to the user and offers recovery options including "Load last known good state," "Continue with partial state," or "Start fresh (preserve artifacts)."

### 4.3 State Schema Versioning

Arc state schemas are versioned. When schema changes:

**Backward compatibility required**: New schemas must be able to read old state. Migration logic converts old state to new format.

**Version recorded**: Every saved state includes its schema version.

**Migration on resume**: When old-version state is loaded, migration runs automatically before validation.

---

## Part 5: Quality Metrics

These metrics assess questioning arc health at project and system levels.

### 5.1 Project-Level Metrics

Track these metrics per project:

| Metric | Calculation | Health Threshold |
|--------|-------------|------------------|
| Stage completion rate | Stages completed / stages entered | > 80% |
| Backward transition rate | Backward transitions / total transitions | < 25% |
| Research branch closure rate | Branches merged / branches created | > 75% |
| Merge gate resolution time | Median time from gate creation to resolution | < 48 hours |
| Constraint consistency | GROUND constraints passing consistency check | 100% |

**Health dashboard**: Projects should display these metrics. Metrics outside healthy thresholds trigger attention flags.

### 5.2 System-Level Metrics

Track these metrics across all projects:

| Metric | Calculation | Health Threshold |
|--------|-------------|------------------|
| Arc completion rate | Projects completing GROUND / projects starting OPEN | > 60% |
| Average arc duration | Median time from OPEN start to GROUND completion | < 2 weeks |
| Widget engagement rate | Widget interactions / widget presentations | > 70% |
| Research branch utility | Branches where findings changed decisions / total branches | > 50% |

---

## Part 6: Error Handling Standards

### 6.1 Validation Error Presentation

When validation fails, the system must communicate clearly what failed (specific validation rule), why it matters (consequence of proceeding without this), and how to fix it (actionable guidance).

**Bad example**: "Validation failed: FOLLOW_REQ_COUNT"

**Good example**: "Before moving to prioritization, we need at least 3 distinct requirements captured. So far we have 2. What else should the system do?"

### 6.2 Recovery from Failures

| Failure Type | Recovery Action | User Communication |
|--------------|-----------------|-------------------|
| State save failure | Retry 3x, then alert user | "Having trouble saving—don't close this window" |
| State load failure | Offer recovery options | "There was an issue loading your session. Here are options:" |
| Widget render failure | Fall back to text | "Widget couldn't load—let me ask this as text instead" |
| Branch merge conflict | Present conflict UI | "These changes conflict. Here's what happened:" |

### 6.3 Graceful Degradation

When subsystems fail, the arc continues with reduced capability:

| Subsystem | Degradation Behavior |
|-----------|---------------------|
| Memory retrieval | Use session state only; flag incomplete context |
| Research tools | Accept manual research input; skip auto-research |
| Widget rendering | Fall back to text-based alternatives |
| Artifact system | Queue artifact updates; process when available |

---

## Part 7: Implementation Checklists

Use these checklists when implementing or auditing the questioning arc.

### 7.1 Stage Implementation Checklist

For each stage implementation, verify:

- [ ] Stage entry point accepts state from previous stage
- [ ] Stage-specific validation rules implemented
- [ ] Stage-specific artifact creation logic present
- [ ] Exit condition evaluation implemented
- [ ] Forward transition triggers work correctly
- [ ] Backward transition triggers work correctly
- [ ] Branch triggers (research/exploration) work correctly
- [ ] State saves on entry, exit, and significant changes
- [ ] Error handling follows standards
- [ ] User-facing messages are clear and actionable

### 7.2 Merge Gate Implementation Checklist

For merge gate implementation, verify:

- [ ] All four options (accept/edit/reject/defer) available
- [ ] Proposed changes summarized in plain language
- [ ] Source attribution included
- [ ] Impact assessment included
- [ ] Resolution logged with all required fields
- [ ] State saved before and after resolution
- [ ] Deferred gates tracked with deadlines
- [ ] Reminder schedule implemented
- [ ] Audit trail complete and queryable

### 7.3 State Management Checklist

For state management implementation, verify:

- [ ] All save triggers implemented
- [ ] State validation on resume implemented
- [ ] Schema version recorded in saved state
- [ ] Migration logic for schema changes exists
- [ ] Isolation enforced (project, branch, session)
- [ ] Recovery options available for load failures
- [ ] Concurrent session handling defined
- [ ] State retention policy implemented

---

## Part 8: Exception Handling

Some situations require deviation from standard flow.

### 8.1 Emergency Bypass

In genuine emergencies, Planners with Owner permission can bypass stage validation to force progression. This requires an explicit bypass reason (logged), bypass acknowledgment (user confirms they understand risks), and post-bypass review (flagged for later audit).

Emergency bypass should be rare. More than 5% bypass rate across projects indicates process problems.

### 8.2 Incomplete Arc Closure

Sometimes projects need to close without completing GROUND. This is permitted but requires explicit "Close Incomplete" action (not just abandonment), incomplete status recorded (artifacts marked as incomplete), and closure reason documented.

Incomplete projects are flagged in project listings and periodically surfaced for resolution or archival.

### 8.3 Arc Reset

Resetting an arc (starting over) is permitted but creates a new arc instance rather than overwriting history. The original arc is archived, the new arc starts fresh with optional context import, and linkage between arcs is documented.

---

## Appendix A: Validation Rule Reference

### Stage Validation Rules

| Rule ID | Stage | Rule | Severity |
|---------|-------|------|----------|
| OPEN-001 | OPEN | Problem statement >= 20 chars | Block |
| OPEN-002 | OPEN | At least 1 user type identified | Block |
| OPEN-003 | OPEN | At least 1 success indicator | Warn |
| OPEN-004 | OPEN | Minimum 3 conversation turns | Warn |
| FOLLOW-001 | FOLLOW | At least 3 requirements captured | Block |
| FOLLOW-002 | FOLLOW | At least 1 primary use case | Block |
| FOLLOW-003 | FOLLOW | Integration points documented | Warn |
| FOLLOW-004 | FOLLOW | Research triggers logged | Warn |
| SHARPEN-001 | SHARPEN | All requirements prioritized | Block |
| SHARPEN-002 | SHARPEN | At least 1 trade-off decided | Block |
| SHARPEN-003 | SHARPEN | Must-haves have acceptance criteria | Warn |
| SHARPEN-004 | SHARPEN | At least 1 structured widget used | Warn |
| BOUNDARY-001 | BOUNDARY | At least 1 explicit exclusion | Block |
| BOUNDARY-002 | BOUNDARY | Deferred items documented | Warn |
| BOUNDARY-003 | BOUNDARY | User boundary confirmation | Block |
| GROUND-001 | GROUND | Budget constraint specified | Block |
| GROUND-002 | GROUND | Reliability tier assigned | Block |
| GROUND-003 | GROUND | Security/access specified | Block |
| GROUND-004 | GROUND | Timeline specified | Block |
| GROUND-005 | GROUND | Constraint consistency check passes | Warn |

### Branch Validation Rules

| Rule ID | Branch Type | Rule | Severity |
|---------|-------------|------|----------|
| BRANCH-001 | Research | Research question specified | Block |
| BRANCH-002 | Research | Success criteria specified | Block |
| BRANCH-003 | Exploration | Decision point specified | Block |
| BRANCH-004 | Exploration | At least 2 alternatives specified | Block |
| BRANCH-005 | Any | Return point captured | Block |
| BRANCH-006 | Any | Relevant context captured | Warn |

---

## Appendix B: Related Documents

- **DD-18-01**: Questioning Arc Definition (companion document with conceptual foundations)
- **DD-13-01**: Artifact Taxonomy (artifact types created during arc)
- **DD-15-01**: Governance Definitions (roles and permissions)
- **STD-15-01**: Governance Standards (audit logging requirements)
- **DD-19-01**: Widget Schema Definition (widget types used in arc)
- **ADR-02-01**: Orchestration Selection (implementation framework)

---

*End of Questioning Arc Standards (STD-18-01)*
