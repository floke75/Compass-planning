---
id: DD-19-01-LLM
type: definition
area: 19-widget-schema
title: Widget Schema and Rendering Specification (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of widget schemas, rendering contract, and interaction logging
tags: [widgets, schema, json, rendering, llm, view]
links:
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "RF-07-01"
  - rel: related
    target_id: "ADR-07-01"
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-18-01"
  - rel: companion
    target_id: "STD-19-01"
  - rel: informed_by
    target_id: "RF-02-01"
  - rel: informed_by
    target_id: "RF-07-01"
  - rel: informed_by
    target_id: "ADR-02-01"
  - rel: informed_by
    target_id: "ADR-07-01"
view: llm
source_id: DD-19-01
source_updated: 2026-02-03
staleness: fresh
---

# Widget Schema and Rendering Specification (LLM View)

## LLM Summary
DD-19 defines the widget schema contract between LLM-generated specifications and UI rendering. It enumerates all widget types across the Compass taxonomy, identifies which are C1-native versus custom, and defines common required fields such as type, id, prompt, and required. The document provides type-specific JSON schemas, response schemas for user interactions, and logging formats for audit and analytics. It also includes validation rules for semantic correctness and guidance for prompt construction to improve structured output reliability. This schema is a critical boundary: a clear, stable contract enables both reliable LLM generation and consistent rendering. DD-19 integrates with the questioning arc and orchestration choices, and is enforced by STD-19 compliance rules. It also clarifies which widget types require custom components and why.

## Canonical Statements
- Widget specs MUST conform to the DD-19 schemas.
- Common fields (type, id, prompt, required) are mandatory for all widgets.
- Interaction responses MUST be logged in the defined format.
- Widget generation MUST align with the taxonomy and rendering capabilities.

## Scope and Non-Goals
- In scope: Widget schema definitions, response formats, and logging rules.
- Out of scope: Visual styling and component library details.

## Dependencies and Interfaces
- Orchestration context: `ADR-02-01`.
- Rendering decision: `ADR-07-01`.
- Questioning arc integration: `DD-18-01`.
- Enforcement standard: `STD-19-01`.

## Core Invariants
- Schema is the contract between LLM output and UI rendering.
- Every widget must support escape hatch, help, and research triggers.
- Logging is required for auditability and analytics.

## Glossary Snapshot
- **Widget spec**: JSON object describing a UI interaction.
- **C1 native**: Rendered by Thesys C1 without custom components.
- **Custom**: Requires shadcn/ui + dnd-kit component implementation.
