---
id: ADR-05-01-LLM
type: adr
area: 05-pm-integration
title: Project Management Integration Selection (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the PM integration tool decision
tags: [pm, integration, linear, github, decision, llm, view]
links:
  - rel: related
    target_id: "RF-05-01"
  - rel: related
    target_id: "DD-17-01"
  - rel: related
    target_id: "STD-17-01"
  - rel: related
    target_id: "SYS-00"
view: llm
source_id: ADR-05-01
source_updated: 2026-02-03
staleness: fresh
---

# Project Management Integration Selection (LLM View)

## LLM Summary
This ADR proposes Linear as the primary project management integration for Compass, with GitHub Issues/Projects as a budget alternative. The decision is driven by API coherence, reliable webhooks, and a strong TypeScript SDK that supports LLM-orchestrated automation, while also delivering a PM experience accessible to non-technical stakeholders. Linear Asks enables Slack or email intake without providing accounts to secondary users, which fits Compass's bidirectional integration model. GitHub is the fallback when cost sensitivity dominates, trading lower cost for more complex API patterns and weaker webhook retries. The integration is scheduled for after core planning workflows are complete and aligns with DD-17 integration standards. Consequences include higher Linear seat cost, simpler automation, and clearer stakeholder intake, with a defined alternative if budget or procurement constraints arise.

## Canonical Statements
- Compass SHOULD integrate with Linear as the primary PM tool.
- GitHub Issues/Projects SHOULD be the budget fallback.
- PM integration MUST follow DD-17 and STD-17 patterns.
- Secondary user intake MUST work without PM accounts.

## Scope and Non-Goals
- In scope: PM tool selection for Compass integration.
- Out of scope: Implementation details of the integration pipeline.

## Dependencies and Interfaces
- Research evidence: `RF-05-01`.
- Integration patterns and standards: `DD-17-01`, `STD-17-01`.
- System requirements: `SYS-00`.

## Core Invariants
- PM integration must follow DD-17/STD-17 patterns.
- Secondary users must not require PM accounts for intake.
- GitHub is the defined fallback if Linear is infeasible.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Decision
- Use Linear as the primary PM integration; use GitHub as a budget alternative.

## Drivers
- Strong API and SDK quality for LLM automation.
- Reliable webhooks with retries.
- Accessible intake workflow for secondary users.

## Alternatives and Disposition
- GitHub Issues/Projects: Accepted as budget alternative.
- Plane.so: Rejected due to rate limits and API deprecations.
- Notion: Rejected due to weak PM primitives and webhook delays.

## Consequences
- Positive: Better intake UX and simpler automation.
- Negative: Higher seat cost and reliance on Linear Business plan.
