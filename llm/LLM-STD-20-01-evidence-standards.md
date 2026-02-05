---
id: STD-20-01-LLM
type: standard
area: 20-evidence-standards
title: Evidence Citation Format Specification (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of citation format requirements and compliance rules
tags: [evidence, citations, format, compliance, llm, view]
links:
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: companion
    target_id: "DD-20-01"
view: llm
source_id: STD-20-01
source_updated: 2026-02-03
staleness: fresh
---

# Evidence Citation Format Specification (LLM View)

## LLM Summary
STD-20 specifies the enforceable citation format for Compass documentation. It defines required fields (id, source_url, title, source_type, retrieved_at) and recommended fields (author, date_published, version, excerpt, tier, reliability), along with allowed enum values for source_type, tier, and reliability. It provides JSON schema for citation objects and optional evidence artifacts, and prescribes inline citation usage with numbered brackets plus a standardized Sources section using [T#/S#] prefixes. The standard includes examples for official docs, community answers, blogs, and low-quality sources with warnings, plus guidance for version-specific citations. It lists common errors such as missing retrieved dates, missing tier or reliability, and citing secondary sources, and includes a compliance checklist for reviewers. This document enforces DD-20's evidence philosophy and is mandatory for Research Findings.

## Canonical Statements
- Every citation MUST include `id`, `source_url`, `title`, `source_type`, and `retrieved_at`.
- Inline citations MUST use numbered brackets, and sources MUST be listed in a `## Sources` section.
- Every source list entry MUST include the `[T#/S#]` prefix.
- Source types MUST use the enumerated values defined in this standard.
- Citation JSON MUST validate against the provided schema.

## Scope and Non-Goals
- In scope: Citation fields, formats, schema, examples, and compliance checks.
- Out of scope: Evidence grading philosophy and tier definitions (see `DD-20-01`).

## Dependencies and Interfaces
- Evidence grading and source taxonomy: `DD-20-01`.
- Artifact metadata rules: `DD-13-01`.

## Enforcement
- Enforced via Research Finding review checklist.

## Compliance Checklist
- [ ] All citations include required fields.
- [ ] All inline citations use numbered brackets.
- [ ] Sources section exists and uses `[T#/S#]` prefixes.
- [ ] `retrieved_at` dates are present and in ISO 8601 format.
- [ ] Source types and tiers use allowed enum values.
