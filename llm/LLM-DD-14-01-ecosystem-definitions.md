---
id: DD-14-01-LLM
type: definition
area: 14-efn-ecosystem
title: EFN Tooling Ecosystem Requirements (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of EFN tooling ecosystem taxonomy and requirements
tags: [ecosystem, archetypes, reliability, integration, llm, view]
links:
  - rel: related
    target_id: "STD-14-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: companion
    target_id: "STD-14-01"
view: llm
source_id: DD-14-01
source_updated: 2026-02-03
staleness: fresh
---

# EFN Tooling Ecosystem Requirements (LLM View)

## LLM Summary
DD-14 defines the EFN tooling ecosystem taxonomy and requirements so tools are planned and built as a coherent system rather than isolated apps. It introduces archetypes such as broadcast-critical, production pipeline, publishing pipeline, internal utility, analytics and intelligence, and exploratory tools, each with different risk profiles, stakeholders, and expected lifespans. The document links archetype selection to reliability tiers and sets expectations for integration behavior, data flow consistency, and operational practices. It emphasizes that EFN tools share data across workflows, making interoperability and shared standards a competitive advantage. This definition is used to classify new projects early, inform constraints in planning, and connect to enforceable standards in STD-14. The document is foundational for reliability, governance, and integration decisions across the Compass ecosystem.

## Canonical Statements
- Every tool MUST be classified into an ecosystem archetype.
- Archetype selection MUST drive reliability tier and standards.
- Tools MUST be planned as part of an interconnected ecosystem.
- Shared data flows and integration points MUST be documented.

## Scope and Non-Goals
- In scope: Tool archetypes, reliability expectations, and ecosystem requirements.
- Out of scope: Detailed implementation standards (see STD-14-01).

## Dependencies and Interfaces
- Enforcement standard: `STD-14-01`.
- Repository and artifact standards: `DD-12-01`, `DD-13-01`.

## Core Invariants
- Archetype classification precedes detailed planning.
- Reliability tier is derived from archetype risk.
- Interoperability is a baseline requirement.

## Glossary Snapshot
- **Broadcast-critical**: Failure visible on air in real time.
- **Production pipeline**: Failure blocks content creation.
- **Publishing pipeline**: Failure delays publication.
- **Internal utility**: Failure impacts efficiency only.
- **Analytics and intelligence**: Failure degrades decisions.
- **Exploratory**: Failure is expected and acceptable.
