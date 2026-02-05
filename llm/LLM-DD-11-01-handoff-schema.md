---
id: DD-11-01-LLM
type: definition
area: 11-handoff-schema
title: Handoff Bundle Schema Definition (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of the handoff bundle schema and required sections
tags: [handoff, schema, implementation, bundle, llm, view]
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: companion
    target_id: "STD-11-01"
view: llm
source_id: DD-11-01
source_updated: 2026-02-03
staleness: fresh
---

# Handoff Bundle Schema Definition (LLM View)

## LLM Summary
DD-11 defines the handoff bundle schema that transfers completed planning outputs to execution platforms. A handoff bundle is the boundary artifact between planning and implementation: it must be complete, self-contained, traceable to decisions and evidence, platform-neutral, and validatable. Bundles are created after the GROUND stage or when a planner explicitly requests handoff, and they are not used for in-progress planning or research tasks. The schema mandates a YAML frontmatter plus seven required sections: Overview, Requirements, Decision Ledger, Architecture Sketch, Acceptance Criteria, Work Breakdown, and Context Pack. The document specifies required metadata fields (including source specs, archetype, and reliability tier) and format expectations for each section to minimize follow-up questions from implementation agents. This definition complements DD-13 artifact rules and is enforced by STD-11.

## Canonical Statements
- Handoff bundles MUST be self-contained and implementation-ready.
- Bundles MUST include all seven required sections and metadata.
- Bundles are created after GROUND or on explicit request.
- Bundles are platform-neutral and adapted via downstream adapters.

## Scope and Non-Goals
- In scope: Handoff bundle schema and required sections.
- Out of scope: Platform-specific adapters and artifact lifecycle rules.

## Dependencies and Interfaces
- Artifact schema: `DD-13-01`.
- Planning workflow: `DD-18-01`.
- Enforcement standard: `STD-11-01`.

## Core Invariants
- Handoff is a clean boundary between planning and execution.
- Completeness and traceability are required.
- Structure is fixed to support validation.

## Glossary Snapshot
- **Handoff bundle**: Package that transfers planning outputs to execution.
- **Decision ledger**: Section listing accepted and rejected choices.
- **Context pack**: Evidence and references supporting implementation.
