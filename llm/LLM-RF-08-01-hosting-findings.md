---
id: RF-08-01-LLM
type: rf
area: 08-hosting
title: Frontend Hosting Platform Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of frontend hosting research findings
tags: [hosting, vercel, cloudflare, netlify, research, llm, view]
related:
  - RF-08-01
  - ADR-08-01
  - ADR-01-01
view: llm
source_id: RF-08-01
source_updated: 2026-01-25
staleness: fresh
---

# Frontend Hosting Platform Research Findings (LLM View)

## LLM Summary
This research evaluates frontend hosting platforms for a Convex-backed Compass app and recommends Vercel. The key differentiator is Convex integration quality: Vercel offers official Marketplace integration, automated environment variable management, and seamless preview deployments with isolated backends. Cloudflare Pages is the best cost-optimized alternative with flat pricing and a large CDN, but requires more manual configuration for Convex. Netlify is viable with strong previews but has a credit-based pricing model and lacks marketplace integration. Railway is not recommended for this use case because it is optimized for containerized full-stack apps rather than static frontends. The trade-off is higher per-seat cost and mild Next.js bias in exchange for simpler operations and stronger LLM documentation alignment. This choice prioritizes deployment simplicity over raw CDN scale. These findings support ADR-08-01.

## Canonical Statements
- Vercel is the recommended frontend hosting platform.
- Convex integration quality and preview deployments are critical requirements.
- Cloudflare Pages is the primary cost-optimized alternative.

## Scope and Non-Goals
- In scope: Frontend hosting evaluation for Compass.
- Out of scope: Backend hosting or orchestration tooling.

## Dependencies and Interfaces
- Backend selection: `ADR-01-01`.
- Decision output: `ADR-08-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Pricing verified January 25, 2026; subject to change.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-08-01` with no semantic changes.

## Findings
- Vercel provides the best Convex integration and lowest deployment friction.
- Cloudflare Pages trades integration effort for lower cost.
- Netlify is viable but pricing adds complexity.

## Limitations
- No hands-on deployment testing performed.
- Pricing may evolve, especially for Netlify credits.

## Recommendation
- Recommend Vercel as primary hosting, with Cloudflare Pages as cost fallback.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
