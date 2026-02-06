---
id: DD-18-02-LLM
type: definition
area: 18-questioning-arc
title: Elicitation Methods (LLM View)
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of elicitation method rationale, example categories, and stage affinity guidance
tags: [questioning-arc, elicitation, methods, planning, llm, view]
links:
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-18-01"
view: llm
source_id: DD-18-02
source_updated: 2026-02-06
staleness: fresh
---

# Elicitation Methods (LLM View)

## LLM Summary
DD-18-02 explains why Compass uses varied questioning methods during planning and provides example method categories with soft stage affinity guidance. Method selection is a prompt engineering concern—the Planning LLM selects techniques based on conversational context, and choices evolve through testing. There are no validation rules for method usage (no STD-18-02). Four method categories are described: Foundation (Socratic Questioning, 5 Whys, Pre-mortem), Creative (SCAMPER, What-If, Constraint Removal), Prioritization (MoSCoW, Buy-a-Feature, Pairwise Comparison), and Collaboration (Stakeholder Roundtable, Persona Focus Group, Devil's Advocate). Each stage has natural affinity: OPEN and BOUNDARY favor Foundation; FOLLOW favors Creative + Foundation; SHARPEN favors Prioritization; GROUND is systematic constraint-gathering.

## Canonical Statements
- Method selection is a prompt engineering concern, not a validation rule.
- The Planning LLM SHOULD use varied, contextually appropriate techniques.
- Stage affinity is guidance, not a requirement.
- No STD-18-02 is needed or planned.
- The adversarial evaluator (DD-18-01 §3.5) is the formalized version of the Devil's Advocate technique.

## Scope and Non-Goals
- In scope: Rationale for varied elicitation, example method categories, stage affinity guidance.
- Out of scope: Prescriptive method-to-question mappings, exhaustive technique inventories, validation rules for method usage.

## Dependencies and Interfaces
- Questioning arc stages: `DD-18-01`.
- Stage completion criteria (unaffected by method choice): `STD-18-01`.
- Structured input principle: `SYS-00` §2.2.

## Core Invariants
- Method variety prevents shallow planning from monotonous questioning.
- Method selection evolves through prompt iteration and testing.
- No enforcement mechanism exists for method usage.

## Definition Matrix
| Category | Methods | Best Stage Affinity |
|----------|---------|-------------------|
| Foundation | Socratic Questioning, 5 Whys, Pre-mortem | OPEN, BOUNDARY |
| Creative | SCAMPER, What-If Scenarios, Constraint Removal | FOLLOW |
| Prioritization | MoSCoW, Buy-a-Feature, Pairwise Comparison | SHARPEN |
| Collaboration | Stakeholder Roundtable, Persona Focus Group, Devil's Advocate | FOLLOW |

## Glossary Snapshot
- **Elicitation method**: A structured questioning technique used to surface specific types of information during planning.
- **Stage affinity**: Soft association between a method category and the arc stage where it is most useful.
