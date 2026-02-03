---
id: SYS-00-LLM
type: spec
area: null
title: Compass System Definition (LLM View)
status: active
created: 2026-02-03
updated: 2026-02-03
author: compass-research
summary: LLM-optimized view of the Compass system definition and core requirements
tags: [system, specification, compass, architecture, llm, view]
related:
  - SYS-00
  - DD-12-01
  - DD-13-01
  - DD-18-01
  - DD-19-01
  - DD-20-01
  - STD-15-01
  - STD-20-01
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
view: llm
source_id: SYS-00
source_updated: 2026-02-03
staleness: fresh
---

# Compass System Definition (LLM View)

## LLM Summary
Compass is an LLM-orchestrated planning, research, and documentation system that turns vague intent into implementation-ready specs and keeps documentation as the evolving source of truth. It is not a code execution platform, deployment system, or PM replacement; chat is a UI while artifacts are truth. The system serves a small non-traditional team and must remain tool-agnostic, auditable, and resilient under partial failure. The core workflow is a five-stage questioning arc (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND) that creates artifacts and decisions, supports research branches with merge gates, and applies constraints like budget, security, reliability tier, integrations, and timeline. Compass requires structured widgets with escape hatches and research triggers. Architecture is layered from interaction through authoritative state, artifact store, memory, evidence, integration, and execution. Memory spans session, project, and ecosystem scopes with a truth hierarchy of intent, execution, and audit. Constraints include $600-$2000 initial budget, privacy, vendor independence, and reversibility.

## Canonical Statements
- Compass MUST treat artifacts as the source of truth; chat is a mutation vector.
- Compass MUST produce implementation-ready specs with clear scope, constraints, and acceptance criteria.
- The questioning arc MUST progress through OPEN, FOLLOW, SHARPEN, BOUNDARY, and GROUND stages.
- Every widget MUST provide an escape hatch, help option, and research trigger.
- State MUST be externalized so context can be reconstructed without full conversation history.
- The system SHOULD remain LLM-agnostic and tool-agnostic via adapter seams.
- The system MUST support auditability, reversibility, and human merge gates.

## User Role Cross-Reference
User definitions span multiple documents with different purposes:

| User Type | Governance (DD-15) | Compass Access | Tool Context (DD-14) |
|-----------|-------------------|----------------|---------------------|
| Builder | Owner/Planner | Primary user | All archetypes |
| Domain Expert | Contributor | Future user | Varies by expertise |
| Stakeholder | Viewer | Secondary user | Consumer of outputs |
| LLM Agent | Agent (scoped) | Automated | Implementation platform |

Document purposes: SYS-00 defines *who uses Compass*; DD-15-01 defines *permissions and workflows*; DD-14-01 defines *who uses EFN tools by archetype*.

## Scope and Non-Goals
- In scope: Planning, research, and documentation workflows that yield rigorous, auditable specs.
- Out of scope: Code execution, deployment/runtime management, PM replacement, or "chat that exports docs."

## Dependencies and Interfaces
- Repository structure and navigation: `DD-12-01`.
- Artifact taxonomy and frontmatter: `DD-13-01`.
- Questioning arc workflow: `DD-18-01` and `STD-18-01`.
- Widget schemas and guarantees: `DD-19-01` and `STD-19-01`.
- Evidence standards and citations: `DD-20-01` and `STD-20-01`.
- Governance and audit logging: `DD-15-01` and `STD-15-01`.

## Evidence and Freshness
- Source updated 2026-01-24; staleness marked fresh.
- No external citations in the system definition; research evidence lives in `RF-*` and `STD-20-01`.

## Open Questions
- None.

## Change Log
- 2026-02-03: Added User Role Cross-Reference table mapping user types across documents.
- 2026-02-03: LLM view created from `SYS-00` with no semantic changes.

## Core Invariants
- Specification is permanent; implementation is ephemeral.
- Artifacts are truth; chat is a mutation vector.
- State is externalized and reconstructable.
- Human merge gates control changes to canonical artifacts.
- Tool and model independence are required by design.

## Glossary Snapshot
- **Questioning arc**: Five-stage planning workflow from OPEN to GROUND.
- **Artifact**: Canonical document that records decisions, requirements, or standards.
- **Decision record (ADR)**: Formal choice with alternatives and rationale.
- **Branch**: Parallel planning path or research detour.
- **Memory layers**: Session, project, and ecosystem scopes.
- **Truth hierarchy**: Intent truth, execution truth, audit truth.
