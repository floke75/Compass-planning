---
id: STD-19-01-LLM
type: standard
area: 19-widget-schema
title: Widget Schema Standards (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of widget schema compliance standards
tags: [widgets, schema, standards, validation, llm, view]
links:
  - rel: related
    target_id: "DD-19-01"
  - rel: related
    target_id: "RF-02-01"
  - rel: related
    target_id: "ADR-02-01"
  - rel: related
    target_id: "RF-07-01"
  - rel: related
    target_id: "ADR-07-01"
  - rel: companion
    target_id: "DD-19-01"
view: llm
source_id: STD-19-01
source_updated: 2026-02-03
staleness: fresh
---

# Widget Schema Standards (LLM View)

## LLM Summary
STD-19 defines the mandatory compliance rules for all Compass widget specifications. It lists required identity and content fields, enforces the escape hatch, help, and research-trigger UX guarantees, and specifies type-specific required fields for each widget category. The standard also requires interaction logging and validation procedures to ensure generated widget specs are structurally correct and usable. It clarifies default behaviors when optional fields are missing and prevents silently malformed widgets from reaching users. It establishes a predictable contract for both LLM generation and UI rendering. It also ensures analytics can rely on consistent interaction payloads across widgets. These rules are enforced in the orchestration layer, providing a quality floor regardless of who generates the widgets. STD-19 operationalizes the schemas in DD-19 and ensures rendering, analytics, and audit systems receive consistent inputs.

## Canonical Statements
- Every widget spec MUST include required common fields.
- UX guarantees (escape hatch, help, research trigger) MUST be present.
- Type-specific fields MUST match the registered schema.
- Specifications MUST be validated before rendering.

## Scope and Non-Goals
- In scope: Widget schema compliance rules and validation checks.
- Out of scope: Widget taxonomy definition (see `DD-19-01`).

## Dependencies and Interfaces
- Schema definition: `DD-19-01`.
- Orchestration and rendering context: `ADR-02-01`, `ADR-07-01`.

## Enforcement
- Enforced by schema validation in the orchestration layer.

## Compliance Checklist
- [ ] Required fields present and valid for all widgets.
- [ ] Escape hatch, help, and research trigger included or defaulted.
- [ ] Type-specific fields match schema requirements.
- [ ] Interaction logging fields captured.
