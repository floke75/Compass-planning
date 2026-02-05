---
id: DD-13-01-LLM
type: definition
area: 13-artifact-taxonomy
title: Artifact Taxonomy and Frontmatter (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of artifact types, frontmatter schema, lifecycle, and templates
tags: [artifacts, taxonomy, frontmatter, lifecycle, llm, view]
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
- Document IDs MUST follow format `{TYPE}-{AREA}-{VERSION}` where TYPE is the prefix, AREA is a two-digit domain code, and VERSION is a two-digit version starting at 01.
- If `view: llm` is present, `source_id`, `source_updated`, and `staleness` MUST be included.
- LLM view IDs SHOULD append `-LLM` to the source ID.

## Document ID Format
| Component | Description | Example |
|-----------|-------------|---------|
| TYPE | Document type prefix | DD, RF, ADR, STD, SPEC |
| AREA | Two-digit domain code (01–99) | 14 = EFN Ecosystem |
| VERSION | Two-digit version (starts at 01) | 01 = first version |

Examples: `DD-14-01` (Definition, area 14, version 1), `RF-09-01` (Research Finding, area 9, version 1), `ADR-01-01` (ADR, area 1, version 1).

Special cases: SYS-00 and IDX-00 use `00` as area code. SPEC and HANDOFF may use descriptive identifiers. Version increments only on formal supersession, not minor updates.

## Scope and Non-Goals
- In scope: Artifact types, schemas, lifecycle, templates, and reconciliation rules.
- Out of scope: Enforcement policies, implementation details, or tool selection.

## Dependencies and Interfaces
- Repository structure and navigation: `DD-12-01`.
- System principles and core requirements: `SYS-00`.

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
