---
id: DD-15-01
type: definition
area: 15-governance
title: Governance, Roles, Permissions, and Audit
status: draft
created: 2026-01-25
updated: 2026-02-06
author: compass-research
summary: Defines roles, permissions, approval workflows, and audit requirements for Compass with emphasis on practical accountability over bureaucracy
tags: [governance, roles, permissions, audit, security]
related:
  - DD-13-01
  - DD-14-01
links:
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: companion
    target_id: "STD-15-01"
companion: STD-15-01
---

# Governance, Roles, Permissions, and Audit

## Document Purpose

This document defines governance structures for Compass: who can do what, what requires approval, what gets logged, and how reviews work. The goal is **practical accountability**, not security theater. For a team of 2–3 primary users at a ~120-person company, governance should enable work rather than create bureaucratic overhead.

**Design principles applied here:**

1. **Minimum viable governance**: Only create rules that solve real problems
2. **LLM-friendly administration**: Routine tasks should be delegable to agents
3. **Audit for reconstruction, not surveillance**: Log what's needed to understand "what happened" after the fact
4. **Human gates only where stakes justify friction**: Reserve approval workflows for genuinely consequential actions

**Why this matters**: Compass handles sensitive internal information (strategy, competitive intelligence, operational plans). Governance must balance access control with the reality that this is a small team trying to ship useful tools. Excessive process kills velocity; insufficient accountability creates risk.

---

## Part 1: Role Catalog

Compass uses five roles. Most users will have exactly one role; the system shouldn't require complex multi-role assignments.

### 1.1 Role Overview

| Role | Who | Access Level | Typical Count |
|------|-----|--------------|---------------|
| **Owner** | System administrator | Everything | 1 |
| **Planner** | Primary users running full workflow | Full planning access | 2–3 |
| **Contributor** | People who propose changes | Propose but not approve | 0–5 |
| **Viewer** | Stakeholders consuming output | Read-only | 10–50 |
| **Agent** | LLM agents acting on behalf of users | Scoped by sponsoring user | N/A |

### 1.2 Role Definitions

#### Owner

The Owner role exists for system administration, not day-to-day operations. There should be exactly one Owner (or two for bus-factor redundancy). Owners should use Planner permissions for normal work.

**Responsibilities:**
- User account management (create, disable, role changes)
- Integration configuration (API keys, webhooks, external connections)
- System configuration (defaults, policies)
- Emergency recovery procedures

**Access:** All permissions. Can see and do everything.

**Who should have this role:** The person ultimately responsible for Compass. Probably one of the primary builders.

**What this role is NOT for:** Day-to-day planning work. Using Owner permissions for routine work bypasses audit trails and makes it harder to understand what happened later.

---

#### Planner

Planners are the primary users described in the System Definition (§1.5): the 2–3 people running the full workflow of planning, research, specs, decisions, and documentation reconciliation.

**Responsibilities:**
- Run full planning workflows (OPEN → GROUND)
- Create, edit, and approve artifacts
- Manage branches (create, merge, archive)
- Conduct research and create findings
- Make decisions and record rationale

**Access:**
- Full read/write access to all projects they're assigned to
- Can approve their own work (no mandatory cross-review for small team)
- Can create new projects
- Cannot modify system configuration or user accounts

**Who should have this role:** The core team building EFN's tools via Compass.

**Note on self-approval:** For a team of 2–3 people, mandatory cross-review creates bottlenecks. Planners can approve their own artifacts. The audit log records who approved what, enabling after-the-fact review if something goes wrong. This trades process friction for velocity—appropriate for a small trusted team.

---

#### Contributor

Contributors can propose changes but cannot approve them. This role exists for:
- Domain experts providing input on specific areas
- Future expansion when more people need limited access
- Situations where you want someone's input without giving full control

**Responsibilities:**
- Propose edits to existing artifacts (creates pending change)
- Comment on artifacts and decisions
- Submit bug reports and feature requests
- Participate in planning conversations (input, not decisions)

**Access:**
- Read access to assigned projects
- Create draft artifacts (status remains `draft` until Planner approves)
- Edit artifacts they created (while still draft)
- Cannot approve artifacts or merge branches
- Cannot create new projects

**Who should have this role:** Currently no one—this is scaffolding for future expansion. Domain experts who need input access but shouldn't have approval authority.

---

#### Viewer

Viewers are the secondary users from System Definition (§1.5): broader EFN stakeholders who consume specs and docs, and submit bugs/requests via complementary tools.

**Responsibilities:**
- Read documentation
- Track progress on projects
- Submit feedback via designated channels (not direct edits)

**Access:**
- Read-only access to assigned projects
- Can view artifact history and decision rationale
- Cannot edit, create, or approve anything
- May have access to a subset of projects (not everything)

**Who should have this role:** Stakeholders who need visibility into planning progress or documentation output but aren't directly participating in planning.

---

#### Agent

Agent is a special role for LLM agents operating within Compass. Agents don't have independent permissions—they inherit permissions from their **sponsoring user** and operate within additional constraints.

**How it works:**
- Every agent action is attributed to a human user
- Agents can do anything their sponsoring user can do, except:
  - Approve artifacts (proposals require human confirmation)
  - Delete anything
  - Modify user accounts or system configuration
  - Access credentials or secrets directly

**Why this matters:** The System Definition (§1.7) specifies "multi-agent safety and human merge gates: sub-agents produce proposals, not canonical truth." Agents help with research, drafting, and organization. Humans make things official.

**Audit implications:** Agent actions are logged with both the agent identifier and the sponsoring user. "Who did this?" always traces to a human.

---

### 1.3 Role Assignment Rules

**Principle: Start narrow, expand as needed.**

| Rule | Rationale |
|------|-----------|
| New users default to Viewer | Prevents accidental over-permissioning |
| Role changes require Owner | Prevents permission creep |
| Users can have only one role | Simplifies reasoning about access |
| Role changes are logged | Accountability |

**Project-level access:** In addition to roles, users are assigned to specific projects. A Viewer for Project A doesn't automatically see Project B. This supports the System Definition requirement for "strong boundaries between projects, branches, and roles" (§1.6).

---

## Part 2: Permission Matrix

### 2.1 Core Permissions

| Action | Owner | Planner | Contributor | Viewer | Agent* |
|--------|-------|---------|-------------|--------|--------|
| **View artifacts** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **View artifact history** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Create draft artifacts** | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Edit draft artifacts** | ✓ | ✓ | Own only | ✗ | ✓ |
| **Edit active artifacts** | ✓ | ✓ | ✗ | ✗ | ✓ |
| **Submit for review** | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Approve artifacts** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Deprecate artifacts** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Delete artifacts** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Create branches** | ✓ | ✓ | ✗ | ✗ | ✓ |
| **Merge branches** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Create projects** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Archive projects** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Delete projects** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Manage integrations** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Manage users** | ✓ | ✗ | ✗ | ✗ | ✗ |
| **View audit logs** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Export data** | ✓ | ✓ | ✗ | ✗ | ✗ |

*Agent permissions inherit from sponsoring user, minus approval/delete actions.

### 2.2 Permission Rationale

**Why Planners can self-approve:** For a 2–3 person team, mandatory cross-review creates bottlenecks without proportionate benefit. The audit log provides accountability; periodic reviews catch issues; velocity matters more than process purity at this scale.

**Why Contributors can't edit active artifacts:** Active artifacts are the source of truth. Allowing direct edits would require complex merge conflict handling. Contributors propose; Planners decide.

**Why Viewers can see history:** Understanding *why* a decision was made often requires seeing how it evolved. Read access to history supports the "consume documentation" use case without adding risk.

**Why Agents can't approve:** This is the "human merge gate" principle from the System Definition. Agents can draft, research, and organize. Making things official requires human confirmation.

**Why only Owner can delete:** Deletion is irreversible and rare. Making it Owner-only prevents accidents and ensures the decision is deliberate. Note that *deprecation* (marking something superseded) doesn't require Owner—that's a normal workflow action.

---

## Part 3: Approval Workflow Definitions

Not everything needs approval. Approval workflows exist for actions where the stakes justify the friction.

### 3.1 What Requires Approval (and Why)

| Action | Approval Required? | Approver | Rationale |
|--------|-------------------|----------|-----------|
| Create draft artifact | No | — | Low risk; creates nothing authoritative |
| Submit artifact for review | No | — | Just signals "ready for eyes" |
| **Approve artifact (draft → active)** | **Implicit (Planner action)** | Planner | This IS the approval; no separate approval of approval |
| Edit active artifact | No | — | Changes are versioned; reversible |
| Create branch | No | — | Branches are safe exploration space |
| **Merge branch to canonical** | **Yes** | Planner | This is a merge gate—human confirms |
| Archive branch | No | — | Doesn't affect canonical state |
| Create project | No | — | Low risk |
| **Delete project** | **Yes** | Owner | Irreversible, high impact |
| **Change user role** | **Yes** | Owner | Security-relevant |
| **Configure integration** | **Yes** | Owner | May expose data to external systems |

### 3.2 Merge Gate Workflow

The merge gate is the most important approval workflow. It implements the System Definition principle: "Sub-agents produce proposals, not canonical truth. Humans or explicit merge policies decide what becomes authoritative."

**When it applies:** Merging any branch (research branch, exploration branch, decision branch) into the canonical state.

**How it works:**

1. **Proposal created:** User or agent completes work on a branch
2. **Review stage:** System shows diff between branch and canonical state
3. **Human decision:** Planner reviews the diff and either:
   - **Approves:** Branch changes merge to canonical
   - **Requests changes:** Branch remains open for further work
   - **Rejects:** Branch is archived without merging
4. **Audit recorded:** Decision, decider, and rationale logged

**What gets reviewed:** The diff should show:
- New artifacts being added
- Changes to existing artifacts (before/after)
- Decisions being recorded
- Any deletions or deprecations

**Who can approve:** Any Planner. Self-approval is allowed (you can merge your own branch). The audit log records who did it.

### 3.3 Lightweight Reviews

For actions that don't require formal approval but might benefit from another set of eyes:

**Optional peer review:** Any user can mark an artifact as "would appreciate review" without blocking progress. This is a social signal, not a gate.

**Periodic review:** Rather than blocking progress with mandatory reviews, schedule periodic review sessions (weekly or biweekly) where Planners review recent changes together. This catches issues without creating bottlenecks.

---

## Part 4: Audit Log Specification

### 4.1 Purpose of Audit Logging

The audit log serves **reconstruction**, not surveillance. Its job is to answer "what happened?" when something goes wrong or when understanding history matters. 

The audit log is NOT for:
- Real-time monitoring (use metrics for that)
- Performance measurement (use analytics for that)
- Micromanaging (don't)

### 4.2 What Gets Logged

**Always logged (high-value events):**

| Event Type | Why It Matters |
|------------|----------------|
| Artifact lifecycle changes (create, approve, deprecate) | Core audit trail |
| Branch operations (create, merge, archive) | Understanding how work evolved |
| User authentication (login, logout, failed attempts) | Security baseline |
| Permission changes (role assignments, project access) | Access control audit |
| Integration configuration changes | External exposure audit |
| Exports | Data movement tracking |

**Logged with minimal detail (routine events):**

| Event Type | What's Logged | What's NOT Logged |
|------------|---------------|-------------------|
| Artifact edits | Who, when, artifact ID | Full content diff (stored in version history instead) |
| Searches | Who, when | Query terms (privacy concern) |
| Views | Nothing | Viewing is not logged (noise) |

**Never logged:**

| Event Type | Why Not |
|------------|---------|
| Chat messages (non-artifact) | Ephemeral by design; creates surveillance concern |
| Draft content before save | Noise; version history captures saves |
| Mouse movements, typing | Absurd |

### 4.3 Audit Log Entry Schema

Every audit log entry contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `timestamp` | ISO 8601 datetime | When it happened (UTC) |
| `event_type` | Enum | Type of event (see STD-15-01) |
| `actor_type` | Enum | `user` or `agent` |
| `actor_id` | String | User ID or agent identifier |
| `sponsor_id` | String | For agents, the sponsoring user ID |
| `project_id` | String (nullable) | Associated project |
| `resource_type` | String (nullable) | What was affected (artifact, branch, etc.) |
| `resource_id` | String (nullable) | ID of affected resource |
| `action` | String | What happened |
| `outcome` | Enum | `success`, `failure`, `denied` |
| `context` | JSON | Additional event-specific details |
| `ip_address` | String (nullable) | For security-relevant events only |

### 4.4 Retention and Access

**Retention:** Audit logs are retained for 2 years. This balances:
- Long enough for historical investigation
- Short enough that storage costs don't compound
- Aligned with typical enterprise retention policies

**Access:**
- Owner: Full access to all audit logs
- Planner: Access to audit logs for projects they're assigned to
- Contributor/Viewer: No audit log access
- Agent: No direct audit log access

**Export:** Audit logs can be exported in JSON format for external analysis or compliance needs.

---

## Part 5: Review Process Guidelines

### 5.1 When Reviews Are Required

**Formal reviews are required for:**
- Nothing, in v1

That's not a typo. For a team of 2–3 trusted Planners, mandatory formal reviews create bottlenecks without proportionate benefit. Instead:

**Recommended practices:**
- **Informal peer check:** Before approving significant changes, mention to another Planner: "Hey, about to merge the API spec—anything I should double-check?"
- **Periodic review sessions:** Weekly or biweekly, Planners review recent changes together
- **Post-incident review:** If something goes wrong, review what happened and whether process changes would help

### 5.2 When to Consider Formal Review

Formal review (blocking approval until someone else signs off) makes sense when:
- The team grows beyond 3–4 Planners
- The work affects other teams' systems
- The stakes are unusually high (security-critical, compliance-relevant)
- Pattern of errors suggests review would help

If/when formal review becomes appropriate, it should be:
- Scoped to specific situations (not universal)
- Fast (target < 24 hours turnaround)
- Bypassable in emergencies (with audit trail)

### 5.3 Conflict Resolution

When Planners disagree:
1. **Talk it out:** Most disagreements resolve with discussion
2. **Document both perspectives:** If unresolved, record the disagreement in the relevant ADR
3. **Owner decides:** If truly stuck, Owner makes the call
4. **Move on:** Decision is logged; revisit later if evidence warrants

The system doesn't need elaborate escalation procedures because the team is small enough to talk.

---

## Part 6: LLM Agent Governance

### 6.1 Agent Principles

Agents should handle the tedious parts of governance so humans focus on decisions that matter.

**What agents CAN do:**
- Draft artifacts based on research or conversation
- Organize and categorize existing content
- Generate routine documentation (changelogs, indexes)
- Suggest edits based on detected inconsistencies
- Create branches for proposed changes
- Prepare merge gate summaries (what changed, why)

**What agents CANNOT do:**
- Approve anything
- Delete anything
- Access credentials or secrets
- Bypass permission checks
- Act without attribution to a human sponsor

**The Archivist is not an Agent**: The Archivist (defined in DD-18-01 §Part 5) is a background subsystem that monitors planning conversations, maintains the decision dependency graph, detects merge conflicts, and generates audit output. Despite operating autonomously, the Archivist is infrastructure—not an Agent per the definitions above. It does not require a sponsoring user, does not produce proposals that need merge gate approval, and does not participate in the planning conversation. Its outputs (warnings, impact analysis tables, audit records) inform human decisions but do not constitute agent proposals.

### 6.2 Agent Audit Trail

Every agent action is logged with:
- Agent identifier (which agent)
- Sponsor user ID (which human is responsible)
- Timestamp
- Action taken
- Result

This ensures "who did this?" always traces to a human, even for automated actions.

### 6.3 Agent Constraints

Agents operate under additional constraints beyond their sponsor's permissions:

| Constraint | Rationale |
|------------|-----------|
| Rate limiting | Prevent runaway automated actions |
| Scope limitation | Agents are scoped to specific tasks, not general access |
| No cascading actions | One action at a time; no "approve everything" automation |
| Confirmation for destructive actions | Even non-delete destructive actions (deprecate, archive) require human confirmation |

---

## Part 7: Implementation Notes

### 7.1 Phase 1 Implementation

For initial Compass implementation, governance can be minimal:

**Must have:**
- User accounts with roles (Owner, Planner initially)
- Basic audit logging (authentication, artifact lifecycle, exports)
- Project-level access control

**Can defer:**
- Contributor and Viewer roles (until needed)
- Formal review workflows (start with informal practices)
- Sophisticated agent permissions (start with simple scoping)

### 7.2 When to Add Complexity

Add governance complexity when:
- Team grows beyond 4–5 Planners
- External users (outside core team) need access
- Compliance requirements demand it
- Pattern of problems suggests it would help

Don't add complexity preemptively. Governance should solve observed problems, not hypothetical ones.

---

## Appendix A: Glossary

**Approval workflow**: A formal process requiring explicit human confirmation before an action takes effect.

**Audit log**: A record of significant system events for accountability and investigation.

**Merge gate**: A checkpoint where human review is required before branch changes become canonical.

**Permission**: Authorization to perform a specific action.

**Role**: A named collection of permissions assigned to users.

**Sponsor (for agents)**: The human user responsible for an agent's actions.

---

## Appendix B: Related Documents

- **STD-15-01**: Governance and audit standards (companion document with schemas and checklists)
- **DD-13-01**: Artifact taxonomy (defines artifact lifecycle states)
- **DD-14-01**: EFN ecosystem (defines tool archetypes and reliability tiers)
- **Compass System Definition**: Authoritative source for user categories and security requirements

---

*End of Governance, Roles, Permissions, and Audit (DD-15-01)*
