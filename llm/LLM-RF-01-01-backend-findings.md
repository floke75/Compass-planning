---
id: RF-01-01-LLM
type: rf
area: 01-backend
title: Backend Platform Research Findings (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of backend platform research findings
tags: [backend, database, convex, supabase, neon, research, llm, view]
related:
  - RF-01-01
  - ADR-01-01
  - DD-14-01
  - DD-12-01
  - DD-13-01
view: llm
source_id: RF-01-01
source_updated: 2026-01-25
staleness: fresh
---

# Backend Platform Research Findings (LLM View)

## LLM Summary
This research evaluates Convex, Supabase, and Neon as backend platforms for Compass, with a focus on LLM maintainability, agent tooling, persistence, and real-time collaboration. The primary recommendation is Convex due to its TypeScript-native model, built-in agent infrastructure, and strong transactional safety that reduces risk from AI-generated code. Supabase offers PostgreSQL portability and a large ecosystem but requires more custom work for agent workflows and LLM access to production data. Neon provides powerful database branching and strong LLM documentation but is database-only and would require assembling multiple services for auth, storage, and realtime. Cost is within budget across options, with Convex estimated around $25-75/month at Phase 3 scale. The key trade-off accepted is vendor lock-in versus velocity and LLM-first developer experience. These findings support ADR-01-01.

## Canonical Statements
- Convex is the primary recommendation for Compass backend.
- LLM maintainability and agent tooling are critical selection criteria.
- Supabase and Neon are viable but require more integration work.
- Cost is acceptable across all evaluated options.

## Scope and Non-Goals
- In scope: Backend platform evaluation for Compass and EFN tools.
- Out of scope: Frontend hosting or orchestration frameworks.

## Dependencies and Interfaces
- System requirements: `SYS-00`.
- Artifact standards: `DD-12-01`, `DD-13-01`.
- Decision output: `ADR-01-01`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Pricing verified January 25, 2026; subject to change.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `RF-01-01` with no semantic changes.

## Findings
- Convex best fits LLM-native development with built-in agent and realtime features.
- Supabase prioritizes portability but adds custom orchestration and LLM-access work.
- Neon excels at branching but lacks full platform coverage.

## Limitations
- Pricing may change; verified as of 2026-01-25.
- No hands-on implementation testing performed.
- Some vendor features are beta or evolving.

## Recommendation
- Recommend Convex as the backend platform for Compass.
- Evidence rating: S/I not explicitly rated in source; Confidence = high.
