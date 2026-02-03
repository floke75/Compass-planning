---
id: DD-13-01-LLM
type: definition
area: 13-artifact-taxonomy
title: Artifact Taxonomy and Frontmatter (LLM View)
status: draft
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of artifact types, frontmatter schema, lifecycle, and templates
tags: [artifacts, taxonomy, frontmatter, lifecycle, llm, view]
related:
  - DD-13-01
  - DD-12-01
  - SYS-00
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
view: llm
source_id: DD-13-01
source_updated: 2026-02-03
staleness: fresh
---

# Artifact Taxonomy and Frontmatter (LLM View)

## LLM Summary
DD-13 defines the Compass artifact taxonomy and the required structure of every document. It enumerates eight artifact types (SPEC, ADR, RB, RF, DD, STD, HANDOFF, IDX) and a decision tree for choosing which type to create. It specifies universal YAML frontmatter fields, type-specific fields, and validation rules, plus lifecycle states from draft to deprecated. It provides per-type definition-of-done checklists, reconciliation rules for handling deltas between docs and implementation, and templates for key artifacts. The goal is consistency, retrievability, and long-term documentation truth, enabling LLM agents and humans to understand, validate, and update artifacts reliably. It emphasizes frontmatter as metadata for retrieval systems, includes optional fields for LLM views, and adds a structured `links` array for typed cross-document relationships. This document defines structure, not content; standards in STD-* enforce practices.

## Canonical Statements
- Every artifact MUST include required YAML frontmatter fields.
- Artifact `type` MUST be one of: spec, adr, rb, rf, dd, std, handoff, idx.
- `status` MUST follow lifecycle states and transitions.
- IDs MUST be unique and follow prefix conventions.
- If `view: llm` is present, `source_id`, `source_updated`, and `staleness` MUST be included.
- LLM view IDs SHOULD append `-LLM` to the source ID.

## Scope and Non-Goals
- In scope: Artifact types, schemas, lifecycle, templates, and reconciliation rules.
- Out of scope: Enforcement policies, implementation details, or tool selection.

## Dependencies and Interfaces
- Repository structure and navigation: `DD-12-01`.
- System principles and core requirements: `SYS-00`.

## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- No external citations required; evidence practices live in `DD-20-01` and `STD-20-01`.

## Open Questions
- None.

## Change Log
- 2026-02-03: LLM view created from `DD-13-01` with no semantic changes.

## Core Invariants
- Artifact types are explicit and limited.
- Frontmatter is required and validated.
- Lifecycle states govern document maturity.

## Glossary Snapshot
- **SPEC**: Implementation-ready specification.
- **ADR**: Decision record with options and rationale.
- **RF**: Research findings and conclusions.
- **RB**: Research brief with questions and success criteria.
- **DD**: Definition of concepts or taxonomies.
- **STD**: Enforceable standard or rule.
- **HANDOFF**: Package for implementation transfer.
- **IDX**: Navigation and cross-reference index.
