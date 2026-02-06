---
id: IDX-00-MASTER-LLM
type: idx
area: null
title: LLM Views Index
status: active
created: 2026-02-03
updated: 2026-02-06
author: compass-research
summary: LLM-optimized navigation index listing available LLM views and guardrails
tags: [index, llm, navigation, retrieval]
related:
  - IDX-00-MASTER
links: []
view: llm
source_id: IDX-00-MASTER
source_updated: 2026-02-06
staleness: fresh
---

# LLM Views Index

## LLM Summary
This index is the preferred entry point for LLM retrieval in the Compass repository. It lists the available LLM views, which are derived, self-contained summaries of canonical artifacts designed for both whole-document reading and chunk retrieval. Use this index to find the right LLM view first, then follow the `source_id` link when you need the authoritative details. Canonical artifacts remain the source of truth; LLM views do not introduce new decisions or requirements and should never override the originals. When in doubt, compare the LLM view against its source to resolve ambiguity. The guardrails below define how to interpret status and evidence so you do not accidentally promote research findings or deprecated documents into decisions. This index will expand as more LLM views are added; if a needed document is missing, use `IDX-00-MASTER.md` to locate the canonical artifact and create an LLM view next.

## Canonical Statements
- Guardrail: Prefer `status: active` documents for requirements and system truth.
- Guardrail: Treat `RF-*` artifacts as evidence only, not decisions.
- Guardrail: Ignore `deprecated` artifacts unless explicitly requested.
- LLM views are derived and must not introduce new decisions or requirements.
- Canonical artifacts remain the authoritative source of truth.

## Scope and Non-Goals
- In scope: Navigation to available LLM views and safe retrieval guardrails.
- Out of scope: Full content of canonical artifacts and implementation details.

## Dependencies and Interfaces
| LLM View | Source ID | Status | Staleness | Canonical Source |
|---|---|---|---|---|
| `LLM-SYS-00-system-definition.md` | SYS-00 | active | fresh | `SYS-00-system-definition.md` |
| `LLM-DD-11-01-handoff-schema.md` | DD-11-01 | draft | fresh | `DD-11-01-handoff-schema.md` |
| `LLM-DD-12-01-repository-definitions.md` | DD-12-01 | draft | fresh | `DD-12-01-repository-definitions.md` |
| `LLM-DD-13-01-artifacts-definitions.md` | DD-13-01 | draft | fresh | `DD-13-01-artifacts-definitions.md` |
| `LLM-DD-14-01-ecosystem-definitions.md` | DD-14-01 | draft | fresh | `DD-14-01-ecosystem-definitions.md` |
| `LLM-DD-15-01-governance-definitions.md` | DD-15-01 | draft | fresh | `DD-15-01-governance-definitions.md` |
| `LLM-DD-16-01-reliability-tiers.md` | DD-16-01 | draft | fresh | `DD-16-01-reliability-tiers.md` |
| `LLM-DD-17-01-integration-definitions.md` | DD-17-01 | draft | fresh | `DD-17-01-integration-definitions.md` |
| `LLM-DD-18-01-questioning-arc.md` | DD-18-01 | draft | fresh | `DD-18-01-questioning-arc.md` |
| `LLM-DD-18-02-elicitation-methods.md` | DD-18-02 | draft | fresh | `DD-18-02-elicitation-methods.md` |
| `LLM-DD-19-01-widget-schema.md` | DD-19-01 | draft | fresh | `DD-19-01-widget-schema.md` |
| `LLM-DD-20-01-evidence-definitions.md` | DD-20-01 | draft | fresh | `DD-20-01-evidence-definitions.md` |
| `LLM-STD-11-01-handoff-standards.md` | STD-11-01 | draft | fresh | `STD-11-01-handoff-standards.md` |
| `LLM-STD-14-01-ecosystem-standards.md` | STD-14-01 | draft | fresh | `STD-14-01-ecosystem-standards.md` |
| `LLM-STD-15-01-governance-standards.md` | STD-15-01 | draft | fresh | `STD-15-01-governance-standards.md` |
| `LLM-STD-16-01-reliability-standard.md` | STD-16-01 | draft | fresh | `STD-16-01-reliability-standard.md` |
| `LLM-STD-17-01-integration-standards.md` | STD-17-01 | draft | fresh | `STD-17-01-integration-standards.md` |
| `LLM-STD-18-01-questioning-arc-standards.md` | STD-18-01 | draft | fresh | `STD-18-01-questioning-arc-standards.md` |
| `LLM-STD-19-01-widget-schema-standards.md` | STD-19-01 | draft | fresh | `STD-19-01-widget-schema-standards.md` |
| `LLM-STD-20-01-evidence-standards.md` | STD-20-01 | draft | fresh | `STD-20-01-evidence-standards.md` |
| `LLM-ADR-01-01-backend-selection.md` | ADR-01-01 | accepted | fresh | `ADR-01-01-backend-selection.md` |
| `LLM-ADR-02-01-orchestration-selection.md` | ADR-02-01 | draft | fresh | `ADR-02-01-orchestration-selection.md` |
| `LLM-ADR-03-01-memory-selection.md` | ADR-03-01 | proposed | fresh | `ADR-03-01-memory-selection.md` |
| `LLM-ADR-04-01-documentation-selection.md` | ADR-04-01 | proposed | fresh | `ADR-04-01-documentation-selection.md` |
| `LLM-ADR-05-01-pm-selection.md` | ADR-05-01 | proposed | fresh | `ADR-05-01-pm-selection.md` |
| `LLM-ADR-06-01-research-tools-selection.md` | ADR-06-01 | proposed | fresh | `ADR-06-01-research-tools-selection.md` |
| `LLM-ADR-07-01-widgets-selection.md` | ADR-07-01 | proposed | fresh | `ADR-07-01-widgets-selection.md` |
| `LLM-ADR-08-01-hosting-selection.md` | ADR-08-01 | proposed | fresh | `ADR-08-01-hosting-selection.md` |
| `LLM-ADR-09-01-llm-provider-selection.md` | ADR-09-01 | proposed | fresh | `ADR-09-01-llm-provider-selection.md` |
| `LLM-ADR-10-01-dev-tooling-selection.md` | ADR-10-01 | proposed | fresh | `ADR-10-01-dev-tooling-selection.md` |
| `LLM-RF-01-01-backend-findings.md` | RF-01-01 | draft | fresh | `RF-01-01-backend-findings.md` |
| `LLM-RF-02-01-orchestration-findings.md` | RF-02-01 | draft | fresh | `RF-02-01-orchestration-findings.md` |
| `LLM-RF-03-01-memory-findings.md` | RF-03-01 | draft | fresh | `RF-03-01-memory-findings.md` |
| `LLM-RF-04-01-documentation-findings.md` | RF-04-01 | draft | fresh | `RF-04-01-documentation-findings.md` |
| `LLM-RF-05-01-pm-findings.md` | RF-05-01 | draft | fresh | `RF-05-01-pm-findings.md` |
| `LLM-RF-06-01-research-tools-findings.md` | RF-06-01 | draft | fresh | `RF-06-01-research-tools-findings.md` |
| `LLM-RF-07-01-widgets-findings.md` | RF-07-01 | draft | fresh | `RF-07-01-widgets-findings.md` |
| `LLM-RF-08-01-hosting-findings.md` | RF-08-01 | draft | fresh | `RF-08-01-hosting-findings.md` |
| `LLM-RF-09-01-llm-provider-findings.md` | RF-09-01 | draft | fresh | `RF-09-01-llm-provider-findings.md` |
| `LLM-RF-10-01-dev-tooling-findings.md` | RF-10-01 | draft | fresh | `RF-10-01-dev-tooling-findings.md` |
| `LLM-RF-21-01-claude-code-cli-integration-findings.md` | RF-21-01 | draft | fresh | `RF-21-01-claude-code-cli-integration-findings.md` |

## Evidence and Freshness
- This index is derived from local artifacts only.
- Staleness is based on the source document `updated` date.

## Risk Factors Quick Reference
Risk-related content is distributed across documents. Key locations:

| Risk Category | Key Document | Section |
|---------------|--------------|---------|
| Critical decision zones | SYS-00 | § 1.8 Critical Junctions |
| Reliability tiers | DD-14-01, DD-16-01, STD-16-01 | DD-14-01 § 2.1, DD-16-01 (full), STD-16-01 (full) |
| ADR trade-offs | ADR-* | Consequences sections |
| Budget constraints | SYS-00 | § 4.1 |
| Security/privacy | SYS-00 | § 4.3–4.4 |

Key accepted risks by ADR:
- ADR-01-01 (Convex): Vendor lock-in → mitigated by abstraction layers
- ADR-02-01 (Mastra): Young framework → mitigated by XState fallback
- ADR-04-01 (Obsidian): No real-time collab → acceptable for small team
- ADR-07-01 (C1): Vendor dependency → mitigated by shadcn/ui fallback
- ADR-09-01 (Claude): Single-provider concentration → mitigated by Gemini/OpenAI fallback

See `IDX-00-MASTER § Risk Factors Index` for comprehensive cross-references.

## Open Questions
- None.

## Change Log
- 2026-02-03: Added Risk Factors Quick Reference section with key locations and ADR trade-offs.
- 2026-02-03: Initial LLM index created from Phase 1 LLM views.
- 2026-02-03: Added Phase 2 LLM views for ADR, RF, and remaining DD/STD artifacts.
