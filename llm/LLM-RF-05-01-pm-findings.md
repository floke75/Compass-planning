---
id: RF-05-01-LLM
type: rf
area: 05-pm-integration
title: Project Management Integration Research Findings (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of PM integration research findings
tags: [pm, integration, linear, github, research, llm, view]
view: llm
source_id: RF-05-01
source_updated: 2026-02-01
staleness: fresh
---

# Project Management Integration Research Findings (LLM View)

## LLM Summary
This research evaluates PM tools for Compass integration, focusing on API quality, webhook reliability, pricing, and DD-17 compliance. The recommendation is Linear as the primary integration with GitHub Issues/Projects as a budget alternative. Linear offers a coherent GraphQL API, a mature TypeScript SDK, automatic webhook retries, and Linear Asks for stakeholder intake without accounts. GitHub provides strong SDK maturity and lower cost but has more complex API patterns and weaker webhook retry behavior. Plane.so is rejected due to low rate limits and impending API deprecations, and Notion is rejected due to weaker PM primitives and webhook delays. Both Linear and GitHub fit budget constraints when scoped to 2-3 primary users. These findings inform ADR-05-01 and integration scheduled after core planning workflows.

## Canonical Statements
- Linear is the primary PM integration recommendation.
- GitHub Issues/Projects is the budget alternative.
- Webhook reliability and API coherence are critical requirements.
- Secondary user intake should not require PM accounts.

## Scope and Non-Goals
- In scope: PM tool evaluation for Compass integration.
- Out of scope: Implementation details of the integration pipeline.

## Dependencies and Interfaces
- Integration patterns: `DD-17-01`, `STD-17-01`.
- Decision output: `ADR-05-01`.

## Findings
- Linear provides the best webhook reliability and intake workflow.
- GitHub offers lower cost but more complex integration paths.
- Plane.so and Notion are not suitable for Compass requirements.

## Evidence Quality
- API documentation: T1/S1 (official sources)
- Webhook reliability: T2/S2 (based on documentation and community reports)
- Pricing data: T1/S2 (verified February 2026)

## Limitations
- Pricing may change over time.
- Some vendor API details may evolve.

## Recommendation
- Recommend Linear with GitHub as budget fallback.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
