---
id: STD-14-01-LLM
type: standard
area: 14-efn-ecosystem
title: EFN Shared Standards and Compliance Checklist (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of archetype-based standards and compliance checklists
tags: [standards, compliance, ecosystem, archetypes, llm, view]
related:
  - STD-14-01
  - DD-14-01
  - DD-12-01
  - DD-13-01
links:
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: companion
    target_id: "DD-14-01"
view: llm
source_id: STD-14-01
source_updated: 2026-02-03
staleness: fresh
---

# EFN Shared Standards and Compliance Checklist (LLM View)

## LLM Summary
STD-14 provides enforceable standards and archetype-specific checklists for EFN tools. It translates the DD-14 ecosystem taxonomy into actionable requirements for broadcast-critical, production pipeline, publishing pipeline, internal utility, analytics, and exploratory tools. The checklists cover pre-development planning, architecture and design, testing, operations, and security, with stricter requirements for higher reliability tiers. The intent is to ensure tools meet the expectations implied by their archetype before launch and during periodic audits. It also establishes shared baseline practices so teams do not invent ad hoc reliability rules per project. The result is predictable readiness across teams and tool categories. This standard is enforced during pre-launch review and ongoing compliance checks, and it sets a shared baseline across the EFN ecosystem so tools remain interoperable and reliable.

## Canonical Statements
- Every tool MUST pass the checklist for its archetype.
- Reliability tier requirements MUST be met before launch.
- Shared standards apply across all tool types.
- Compliance SHOULD be verified in pre-launch and periodic audits.

## Scope and Non-Goals
- In scope: Enforceable archetype standards and checklists.
- Out of scope: Defining the archetypes themselves (see `DD-14-01`).

## Dependencies and Interfaces
- Ecosystem definitions: `DD-14-01`.
- Repository and artifact standards: `DD-12-01`, `DD-13-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- No external citations required; standards are internal.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `STD-14-01` with no semantic changes.

## Enforcement
- Enforced via pre-launch review and periodic audits.

## Compliance Checklist
- [ ] Archetype identified and correct checklist completed.
- [ ] Reliability tier requirements satisfied.
- [ ] Operational readiness (monitoring, runbooks) verified.
- [ ] Security and access controls validated.
