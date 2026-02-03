---
id: ADR-08-01-LLM
type: adr
area: 08-hosting
title: Frontend Hosting Platform Selection (LLM View)
status: proposed
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the frontend hosting decision
tags: [hosting, vercel, frontend, deployment, decision, llm, view]
related:
  - ADR-08-01
  - RF-08-01
  - ADR-01-01
links:
  - rel: related
    target_id: "RF-08-01"
  - rel: related
    target_id: "ADR-01-01"
view: llm
source_id: ADR-08-01
source_updated: 2026-02-03
staleness: fresh
---

# Frontend Hosting Platform Selection (LLM View)

## LLM Summary
This ADR proposes Vercel as the frontend hosting platform for Compass. The decision is anchored on the official Convex Marketplace integration, which automates environment variables and preview deployments with isolated backends, and on documentation alignment that reduces friction for LLM coding agents. Vercel's push-to-deploy workflow and preview URLs fit a PR-driven workflow for a small, non-technical team. Alternatives considered include Cloudflare Pages (lower cost but more manual Convex setup), Netlify (good previews but credit-based pricing and no marketplace integration), Railway (misaligned with static frontend hosting), and deferring the decision. The trade-off is higher per-seat cost and mild Next.js bias in exchange for operational simplicity and reliable, automated deployments. Consequences include faster preview testing, minimal configuration, and a dependency on Vercel's deployment model.

## Canonical Statements
- Compass SHOULD use Vercel for frontend hosting.
- Hosting MUST support preview deployments with isolated Convex backends.
- Deployment workflows MUST be low-configuration and LLM-friendly.

## Scope and Non-Goals
- In scope: Frontend hosting platform selection.
- Out of scope: Backend hosting and orchestration tooling.

## Dependencies and Interfaces
- Research evidence: `RF-08-01`.
- Backend selection: `ADR-01-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Evidence grounded in `RF-08-01` hosting comparison.

## Open Questions
- Final stakeholder approval and decision date remain pending.

## Change Log
- 2026-02-03: LLM view created from `ADR-08-01` with no semantic changes.

## Decision
- Use Vercel as the frontend hosting platform.

## Drivers
- Official Convex integration and automated preview environments.
- Alignment with LLM documentation patterns.
- Operational simplicity for a small team.

## Alternatives and Disposition
- Cloudflare Pages: Rejected due to manual Convex setup complexity.
- Netlify: Rejected due to pricing model and lack of marketplace integration.
- Railway: Rejected as misaligned with frontend hosting needs.
- Defer decision: Rejected due to delivery blockage.

## Consequences
- Positive: Automated deployments and previews with low setup burden.
- Negative: Higher per-seat cost and mild Vercel ecosystem bias.
