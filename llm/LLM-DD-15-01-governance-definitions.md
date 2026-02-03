---
id: DD-15-01-LLM
type: definition
area: 15-governance
title: Governance, Roles, Permissions, and Audit (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of governance roles, permissions, and audit principles
tags: [governance, roles, permissions, audit, llm, view]
related:
  - DD-15-01
  - STD-15-01
  - DD-13-01
  - DD-14-01
links:
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: companion
    target_id: "STD-15-01"
view: llm
source_id: DD-15-01
source_updated: 2026-02-03
staleness: fresh
---

# Governance, Roles, Permissions, and Audit (LLM View)

## LLM Summary
DD-15 defines governance for Compass with a focus on practical accountability rather than heavy bureaucracy. It establishes five roles (Owner, Planner, Contributor, Viewer, Agent), describes who can create, approve, and modify artifacts, and sets approval expectations appropriate for a small 2-3 person team. The document emphasizes minimum viable governance, LLM-friendly administration, audit logs for reconstruction rather than surveillance, and human gates only where stakes justify friction. It clarifies that planners can self-approve to avoid bottlenecks, while audit logging preserves accountability. Governance is tied to project boundaries, branch management, and artifact lifecycle rules in DD-13. It also frames governance as a velocity enabler rather than a security theater exercise. This definition is enforced by STD-15, which specifies audit log schemas and compliance checks.

## Canonical Statements
- Governance must balance accountability with velocity for a small team.
- Roles MUST be explicit and limited to a small, clear set.
- Audit logging MUST enable reconstruction of what happened.
- Human approval gates SHOULD be used only for high-stakes changes.

## Scope and Non-Goals
- In scope: Roles, permissions, approvals, and audit principles.
- Out of scope: Specific audit log schema and enforcement (see STD-15-01).

## Dependencies and Interfaces
- Artifact lifecycle: `DD-13-01`.
- Ecosystem requirements: `DD-14-01`.
- Enforcement standard: `STD-15-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- No external citations required; governance is internal.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `DD-15-01` with no semantic changes.

## Core Invariants
- Minimum viable governance over heavy process.
- Explicit roles with scoped permissions.
- Audit logs prioritize traceability.

## Glossary Snapshot
- **Owner**: System administrator role.
- **Planner**: Primary user with full planning access.
- **Contributor**: Can propose changes but not approve.
- **Viewer**: Read-only stakeholder.
- **Agent**: LLM acting on behalf of a user.
