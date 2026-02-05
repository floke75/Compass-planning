---
id: STD-15-01-LLM
type: standard
area: 15-governance
title: Governance and Audit Standards (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of governance audit standards and compliance rules
tags: [governance, audit, standards, logging, llm, view]
links:
  - rel: related
    target_id: "DD-15-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: companion
    target_id: "DD-15-01"
view: llm
source_id: STD-15-01
source_updated: 2026-02-03
staleness: fresh
---

# Governance and Audit Standards (LLM View)

## LLM Summary
STD-15 specifies the enforceable governance and audit logging standards for Compass. It defines the audit log schema, required fields, and event type taxonomy so all significant actions are traceable. The standard includes requirements for actor and sponsor attribution, project and resource references, outcomes, and client metadata when relevant. It also provides compliance checklists for permissions configuration and periodic review. These rules ensure auditability aligns with the governance principles in DD-15 without creating excessive process overhead. It emphasizes reconstruction and accountability over surveillance. The standard is intended to be implementable by a small team without heavy tooling. It also supports incident investigation and after-action review. Implementations must adhere to the schema and event types, and reviews must verify that logs are complete, consistent, and reconstructable.

## Canonical Statements
- All audit events MUST conform to the specified schema.
- Event types MUST use the defined enum set.
- Actor attribution MUST be recorded, including sponsors for agents.
- Governance compliance MUST be periodically reviewed.

## Scope and Non-Goals
- In scope: Audit log schema and governance compliance rules.
- Out of scope: Role definitions (see `DD-15-01`).

## Dependencies and Interfaces
- Governance definitions: `DD-15-01`.
- Artifact metadata: `DD-13-01`.

## Enforcement
- Enforced via system configuration checks and periodic review.

## Compliance Checklist
- [ ] Audit logs include all required fields and valid event types.
- [ ] Agent actions include sponsor attribution.
- [ ] Permission changes and approvals are logged.
- [ ] Periodic governance review completed.
