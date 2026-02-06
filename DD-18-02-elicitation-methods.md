---
id: DD-18-02
type: definition
area: 18-questioning-arc
title: Elicitation Methods
status: draft
created: 2026-02-06
updated: 2026-02-06
author: compass-research
summary: Explains why Compass uses varied questioning methods during planning and provides example method categories with stage affinity guidance
tags: [questioning-arc, elicitation, methods, planning, techniques]
related:
  - DD-18-01
  - STD-18-01
links:
  - rel: related
    target_id: "DD-18-01"
  - rel: related
    target_id: "STD-18-01"
---

# Elicitation Methods

## Document Purpose

This document explains *why* Compass uses varied questioning methods during planning and provides example categories of techniques. It explicitly acknowledges that method selection is a **prompt engineering concern**—the Planning LLM is instructed to use varied, relevant techniques, and specific method choices will evolve through testing.

**What this document covers**: Rationale for varied elicitation, example method categories, and soft guidance on stage affinity.

**What this document does not cover**: Prescriptive method-to-question mappings, exhaustive technique inventories, or validation rules for method usage. There is no STD-18-02—method selection is not a standards concern.

**Audience**: Compass builders tuning the Planning LLM's prompts, and planners who want to understand why the system asks questions in varied ways.

---

## Part 1: Why Varied Methods Matter

Different questions surface different insights. A 5 Whys chain reveals root causes that a direct question might miss. A pre-mortem surfaces risks that optimism-biased planning overlooks. A SCAMPER exercise generates creative alternatives that incremental thinking wouldn't produce.

Monotonous questioning leads to shallow planning. When every question follows the same pattern ("What do you want? What else? What else?"), users disengage and provide increasingly superficial answers. Variety in questioning style keeps the user engaged and surfaces hidden assumptions, unstated preferences, and overlooked constraints.

The Planning LLM should match technique to context, not follow a fixed script. The right method depends on what stage the conversation is in, what kind of information is needed, and how the user is responding. This is fundamentally a prompt engineering problem—the LLM's instructions tell it to vary its approach, and the specific methods evolve through iteration and testing.

---

## Part 2: Example Method Categories

The following categories illustrate the range of techniques available. Each is described briefly—2-3 sentences per method. These are examples, not an exhaustive inventory.

### Foundation Methods

Techniques for surfacing assumptions, root causes, and underlying motivations.

- **Socratic Questioning**: A series of probing questions that challenge assumptions and explore the reasoning behind stated requirements. Useful for uncovering "why" behind "what."
- **5 Whys**: Repeatedly asking "why" to drill past surface-level requirements to root causes. Particularly effective when a user states a solution rather than a problem.
- **Pre-mortem**: Asking "Imagine this project has failed—what went wrong?" to surface risks and concerns that optimism might suppress. Converts vague anxiety into specific, addressable risks.

### Creative Methods

Techniques for exploring alternatives and generating options beyond the obvious.

- **SCAMPER**: A structured creativity framework (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse) applied to requirements or design choices. Generates alternatives that incremental thinking misses.
- **What-If Scenarios**: Exploring hypothetical situations ("What if your user base doubled overnight?" "What if this API became unavailable?") to reveal hidden assumptions and robustness requirements.
- **Constraint Removal**: Temporarily removing a stated constraint ("If budget were unlimited...") to reveal what the user truly prioritizes when artificial limits are lifted.

### Prioritization Methods

Techniques for forcing trade-offs and revealing true priorities.

- **MoSCoW**: Categorizing requirements as Must-have, Should-have, Could-have, or Won't-have. Forces explicit priority assignment rather than treating everything as equally important.
- **Buy-a-Feature / 100-Dollar Test**: Allocating a fixed budget across desired features, forcing trade-offs. Makes abstract prioritization concrete by introducing scarcity.
- **Pairwise Comparison**: Comparing features two at a time ("If you could only have A or B, which?") to build a ranking that avoids the "everything is priority 1" problem.

### Collaboration Methods

Techniques for surfacing multiple perspectives and stakeholder concerns.

- **Stakeholder Roundtable Simulation**: The system adopts different stakeholder perspectives in sequence ("As an end user... As an ops engineer... As a budget owner...") to surface concerns that a single-perspective conversation misses.
- **Persona Focus Group**: Creating lightweight user personas and walking through how each would experience the proposed system. Reveals edge cases and accessibility concerns.
- **Devil's Advocate**: Deliberately arguing against a proposed approach to surface weaknesses. In Compass, this is formalized as the adversarial evaluator research branch subtype (see DD-18-01 §3.5).

---

## Part 3: Stage Affinity (Guidance, Not Rules)

Certain method categories are more useful in certain stages. This is soft guidance—not a requirement or validation rule.

| Stage | Most Useful Categories | Why |
|-------|----------------------|-----|
| OPEN | Foundation methods | "Why does this matter? What's the root need?" — surfacing motivation and assumptions |
| FOLLOW | Creative + Foundation | "What if we did X? What are we assuming?" — expanding the possibility space |
| SHARPEN | Prioritization methods | "If you could only have one..." — forcing concrete trade-offs |
| BOUNDARY | Foundation methods | "Pre-mortem: what could go wrong if we include X?" — stress-testing scope decisions |
| GROUND | Structured constraint-gathering | Not really elicitation—more like systematic checklist completion |

The GROUND stage is the least elicitation-heavy. By that point, most of the creative and exploratory work is done; GROUND is about applying concrete constraints to prioritized, bounded requirements.

---

## Part 4: Non-Goals

- This document does NOT prescribe specific methods for specific questions. The Planning LLM selects methods based on conversational context.
- Method selection evolves through prompt iteration and testing. What works well in practice may differ from what seems theoretically optimal.
- There are no validation rules or standards for method usage. No STD-18-02 is needed or planned.
- This document is intentionally lightweight. It provides enough context for prompt engineers to understand the design intent without over-constraining the LLM's flexibility.

---

## Appendix A: Glossary

**Elicitation method**: A structured questioning technique used to surface specific types of information during planning conversations.

**Stage affinity**: The soft association between a questioning method category and the arc stage where it is most naturally useful.

---

## Appendix B: Related Documents

- **DD-18-01**: Questioning Arc Definition (the workflow these methods operate within)
- **STD-18-01**: Questioning Arc Standards (stage completion criteria, unaffected by method choice)
- **Compass System Definition**: §2.2 Structured Input Over Freeform Text (the guiding principle behind varied elicitation)

---

*End of Elicitation Methods (DD-18-02)*
