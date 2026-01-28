# Research Phase: Handoff Bundle Schema

**Area**: 11 | **Tier**: 4 (Integration & Handoff) | **Track**: B (Internal Design)

---

## Instructions

Copy everything below this line and paste it into a new Claude chat. Ensure the Compass System Definition is available as project context.

---

## Pre-Research Setup

### Mandatory Context (Must Be Available)
- **Compass System Definition** (`SYS-00-system-definition.md`) — Read Part 2.7 (Handoff to Implementation), Part 2.4 (Documentation as Ground Truth), and Appendix A (Glossary)
- **IDX-00-MASTER.md** — Check for completed prior research

### Required Prior Research (Include If Available)
- `DD-12-01-repository-definitions.md` — Repository structure and naming conventions
- `DD-13-01-artifacts-definitions.md` — Artifact taxonomy and frontmatter schema
- `DD-14-01-ecosystem-definitions.md` — EFN tool archetypes and requirements
- `STD-20-01-evidence-standards.md` — Evidence citation format for context packs

### Optional Context (Use If Available)
- `DD-18-01-questioning-arc.md` — How planning outputs feed handoff bundles
- `ADR-02-01-orchestration-selection.md` — Structured output format for bundles

---

## Important Instructions

1. **Read the Compass System Definition first**, particularly:
   - Part 2.7: Handoff to Implementation (bundle contents)
   - Part 2.4: Documentation as Ground Truth (reconciliation loop)
   - Part 1.7: Guiding principles (tool-agnostic handoffs)
   - Part 5.1: Architecture layers (Artifact Store layer)

2. **Do not ask the user technical questions** — synthesize the handoff schema from System Definition requirements and prior definitions.

3. **If DD-12-01 and DD-13-01 exist**, ensure schema compatibility with established frontmatter patterns and naming conventions.

4. **If DD-14-01 exists**, consider how different archetypes may need different handoff emphasis (broadcast-critical vs internal utility).

---

## Available Context (If Present)

### From DD-12-01 (Repository Structure) — Extract If Available:
- File naming conventions for handoff bundles
- Folder location for handoff artifacts
- Cross-reference patterns

### From DD-13-01 (Artifact Taxonomy) — Extract If Available:
- Handoff bundle type definition
- Required frontmatter fields
- Relationship to other artifact types

### From DD-14-01 (EFN Ecosystem) — Extract If Available:
- Project archetype definitions
- Reliability tier requirements by archetype
- Documentation requirements per archetype

### If Prior Definitions Not Available:
Use the patterns from the System Definition directly:
- HANDOFF- prefix for bundles
- Standard YAML frontmatter
- Seven required bundle sections (Part 2.7)

---

# RESEARCH TASK: Define Handoff Bundle Schema

## Context

You are helping define the handoff bundle schema for **Compass**, an LLM-orchestrated planning, research, and documentation system for EFN (a financial news broadcaster with ~120 people). The handoff bundle is what Compass produces when planning is complete — the package that implementation platforms consume.

This is a **Track B (Internal Design)** task. You are defining internal standards based on requirements, not evaluating external tools.

**Key Principle from System Definition**: "The handoff is a clean boundary: implementation platforms consume artifacts and execute. Feedback flows back via documentation updates and deltas, not by tightly coupling Compass to a specific execution tool."

## Scope

### What This Definition Must Cover

1. **Required Sections**: What must every handoff bundle include?
2. **Schema for Each Section**: What is the structure of each section?
3. **Metadata Format**: Versioning, timestamps, source references
4. **Platform-Specific Transformations**: Rules for adapting to different execution platforms
5. **Validation Criteria**: How to verify a bundle is complete

### Out of Scope
- Artifact taxonomy details (Area 13 — reference existing)
- Repository structure (Area 12 — reference existing)
- Implementation platform specifics (downstream concern)
- Questioning arc details (Area 18)

## Handoff Bundle Contents from System Definition (Part 2.7)

The System Definition specifies seven required sections:
- **Overview**: Vision, success metrics, stakeholders
- **Requirements**: Scope, out-of-scope, constraints
- **Decision ledger**: Chosen, rejected, superseded decisions with rationale
- **Architecture sketch**: Components, interfaces, data flows
- **Acceptance criteria and verification plan**
- **Work breakdown proposal**: Phases and atomic implementation-ready tasks
- **Context pack**: Sources, citations, extracted ground truth

## Required Outputs

### 1. Definition Document (DD-11-01)

**Output File**: `DD-11-01-handoff-schema.md`

**Frontmatter Schema**:
```yaml
---
id: DD-11-01
type: dd
area: 11-handoff-schema
title: Handoff Bundle Schema Definition
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Defines the schema for implementation handoff bundles
tags: [handoff, schema, implementation, bundle]
related:
  - DD-12-01
  - DD-13-01
  - DD-14-01
  - STD-20-01
---
```

**Required Sections**:

1. **Handoff Bundle Structure**
   - Top-level organization
   - Required vs optional sections
   - File/folder structure within bundle

2. **Section Schemas** (for each of the seven sections):
   - **Overview Section**: Vision, success metrics, stakeholder format
   - **Requirements Section**: Scope, out-of-scope, constraints format
   - **Decision Ledger**: ADR inclusion criteria, status filtering
   - **Architecture Sketch**: Component, interface, data flow notation
   - **Acceptance Criteria**: Testable statement format, verification plan
   - **Work Breakdown**: Phase structure, task format, dependencies
   - **Context Pack**: Evidence inclusion, citation format, staleness indicators

3. **Bundle Metadata Schema**
   - Bundle version
   - Creation timestamp
   - Source project reference
   - Planning session references

4. **Platform Adaptation Rules**
   - Base format (platform-neutral)
   - Extension mechanism for platform-specific adapters

5. **Validation Checklist**
   - Required sections verification
   - Schema compliance per section
   - Cross-reference integrity

### 2. Standard Document (STD-11-01)

**Output File**: `STD-11-01-handoff-standard.md`

**Frontmatter Schema**:
```yaml
---
id: STD-11-01
type: std
area: 11-handoff-schema
title: Handoff Bundle Standard
status: draft
created: 2026-01-XX
updated: 2026-01-XX
author: compass-research
summary: Enforceable standard for handoff bundle creation
tags: [handoff, standard, validation, compliance]
related:
  - DD-11-01
  - DD-13-01
companion: DD-11-01
enforcement: Pre-handoff validation checklist
---
```

**Required Content**:
- Validation checklist in specification form
- Minimum content requirements per section
- Quality criteria for implementation-ready work breakdowns

## Evidence Citation Format

Follow this format for all sources (per STD-20-01 if available):
```
N. **[T#/S#]** Author. "Title". Published DATE. Retrieved DATE. URL
```

## Stop Conditions

Definition is complete when:
- Schema covers all seven sections from System Definition
- Sample handoff bundle has been sketched
- Schema is compatible with DD-13-01 artifact taxonomy
- Validation checklist is complete
- Platform adaptation mechanism is defined

---

**Begin the research and produce the Definition Document and Standard.**
