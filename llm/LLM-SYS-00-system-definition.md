---
id: SYS-00-LLM
type: spec
area: null
title: Compass System Definition (LLM View)
status: active
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of the Compass system definition and core requirements
tags: [system, specification, compass, architecture, llm, view]
links:
  - rel: related
    target_id: "DD-12-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
view: llm
source_id: SYS-00
source_updated: 2026-02-06
staleness: fresh
---

# Compass System Definition (LLM View)

## LLM Summary
Compass is an LLM-orchestrated planning, research, and documentation system that turns vague intent into implementation-ready specs and keeps documentation as the evolving source of truth. It is not a code execution platform, deployment system, or PM replacement; chat is a UI while artifacts are truth. The core workflow is a five-stage questioning arc (OPEN, FOLLOW, SHARPEN, BOUNDARY, GROUND) that tracks decision dependencies via a directed graph (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) and a decision status lifecycle (EXPLORING → CHOSEN/REJECTED/BLOCKED/DEFERRED) distinct from artifact lifecycle states. The workflow supports user-controlled fast mode for pre-filled suggestions without skipping stages. Exploration branches use a Git-like fork model with dependency-graph conflict detection at merge. Research branches support subtypes (investigation, validation, specialist, adversarial). The Archivist is a background subsystem that maintains the dependency graph, detects conflicts, and generates audit output. Architecture is layered from interaction through authoritative state, artifact store, memory, evidence, integration, and execution. Constraints include $600-$2000 initial budget, privacy, vendor independence, and reversibility.

## Canonical Statements
- Compass MUST treat artifacts as the source of truth; chat is a mutation vector.
- Compass MUST produce implementation-ready specs with clear scope, constraints, and acceptance criteria.
- The questioning arc MUST progress through OPEN, FOLLOW, SHARPEN, BOUNDARY, and GROUND stages.
- Every widget MUST provide an escape hatch, help option, and research trigger.
- State MUST be externalized so context can be reconstructed without full conversation history.
- The system SHOULD remain LLM-agnostic and tool-agnostic via adapter seams.
- The system MUST support auditability, reversibility, and human merge gates.
- Decision dependencies MUST form a directed acyclic graph; cycles are invalid.
- The Archivist MUST NOT participate in the planning conversation or act as an agent.

## User Role Cross-Reference
| User Type | Governance (DD-15) | Compass Access | Tool Context (DD-14) |
|-----------|-------------------|----------------|---------------------|
| Builder | Owner/Planner | Primary user | All archetypes |
| Domain Expert | Contributor | Future user | Varies by expertise |
| Stakeholder | Viewer | Secondary user | Consumer of outputs |
| LLM Agent | Agent (scoped) | Automated | Implementation platform |

## Scope and Non-Goals
- In scope: Planning, research, and documentation workflows that yield rigorous, auditable specs.
- Out of scope: Code execution, deployment/runtime management, PM replacement, or "chat that exports docs."

## Dependencies and Interfaces
- Repository structure and navigation: `DD-12-01`.
- Artifact taxonomy and frontmatter: `DD-13-01`.
- Questioning arc workflow: `DD-18-01` and `STD-18-01`.
- Elicitation methods: `DD-18-02`.
- Widget schemas and guarantees: `DD-19-01` and `STD-19-01`.
- Evidence standards and citations: `DD-20-01` and `STD-20-01`.
- Governance and audit logging: `DD-15-01` and `STD-15-01`.

## Core Invariants
- Specification is permanent; implementation is ephemeral.
- Artifacts are truth; chat is a mutation vector.
- State is externalized and reconstructable.
- Human merge gates control changes to canonical artifacts.
- Tool and model independence are required by design.
- Decision dependencies form a DAG maintained by the Archivist.
- Decision status lifecycle is separate from artifact lifecycle.

## Architecture Layers
1. Interaction layer — Web/chat UI with rich widgets and questioning arc state.
2. Authoritative state layer — Projects, decisions, branches, workflow runs, permissions.
3. Artifact store — Canonical docs and handoff bundles with history (git-friendly).
4. Memory and retrieval layer — Semantic and literal search, temporal and branch-aware.
5. Pristine context and evidence layer — Verified sources and extracted ground truth.
6. Integration and event layer — Webhooks, events, queues for external sync.
7. Execution platforms — Downstream coding/execution toolchains consuming artifacts.

## Constraint Summary
| Constraint | Value | Source |
|-----------|-------|--------|
| Initial budget | $600–$2,000/year | §4.1 |
| Proven value budget | $3,000–$5,000/year | §4.1 |
| Primary users | 2–3 builders | §1.5 |
| LLM response time | <5s typical, <30s complex | §3.7 |
| Widget render time | <100ms | §3.7 |
| Data ownership | EFN retains all data | §4.4 |

## Glossary Snapshot
- **Questioning arc**: Five-stage planning workflow from OPEN to GROUND.
- **Artifact**: Canonical document that records decisions, requirements, or standards.
- **Decision record (ADR)**: Formal choice with alternatives and rationale.
- **Decision dependency**: Typed relationship (DEPENDS_ON, ENABLES, BLOCKS, CONFLICTS_WITH, INFORMS) between decisions.
- **Decision status**: Planning-time state (EXPLORING/ENABLED/BLOCKED/CHOSEN/REJECTED/DEFERRED), distinct from artifact lifecycle.
- **Archivist**: Background subsystem for decision filing, dependency analysis, conflict detection, and audit.
- **Fast mode**: User toggle for pre-filled suggestions; all stages and exit conditions unchanged.
- **Adversarial evaluator**: User-triggered research branch that argues against a decision to surface risks.
- **Branch**: Parallel planning path or research detour (Git-like fork model for exploration).
- **Memory layers**: Session, project, and ecosystem scopes.
- **Truth hierarchy**: Intent truth, execution truth, audit truth.
