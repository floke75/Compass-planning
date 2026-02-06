---
id: DD-22-01-LLM
type: definition
area: 22-llm-implementability
title: LLM-Implementability Evaluation Framework (LLM View)
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of the six LI criteria, scoring rubric, thresholds, weighting rules, and evidence mapping for evaluating technology choices when the primary developer is an LLM coding agent
tags: [llm-implementability, evaluation, methodology, scoring, technology-selection, agent-development, llm, view]
links:
  - rel: companion
    target_id: "STD-22-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "SYS-00"
  - rel: informed_by
    target_id: "RF-03-02"
view: llm
source_id: DD-22-01
source_updated: 2026-02-06
staleness: fresh
---

# LLM-Implementability Evaluation Framework (LLM View)

## LLM Summary
DD-22 defines a six-criterion framework for evaluating how well a technology supports implementation by LLM coding agents. The criteria are: LI-1 Documentation Quality for LLM Consumption (llms.txt, MCP docs servers, structured examples), LI-2 MCP Tool Availability (official MCP servers, Context7 entries, CLAUDE.md guides), LI-3 Code Complexity and Structural Quality (API surface area, type safety, naming predictability, pattern conventionality), LI-4 Testability and Self-Verification (in-memory test backends, tight feedback loops, example tests), LI-5 LLM Familiarity from Training Data (npm downloads, GitHub stars, library age as proxies), and LI-6 Hallucination Risk Profile (version confusion, API consistency, silent failure modes, error diagnostics). Each criterion scores 0-3. Raw total thresholds: 14-18 Low Risk, 8-13 Moderate, 4-7 High Risk, 0-3 Exclusion. For Compass, LI-1 and LI-3 carry 1.5× weight (max 21), shifting thresholds to 16-21/9-15/5-8/0-4. The framework supplements functional evaluation—it does not replace it. Calendar timeline estimates are replaced by complexity profiles measuring concept count, integration points, iteration cycles, and token budgets. Evidence for LI scores maps to DD-20-01's S1-S4/I1-I4/Confidence grading. Originated from RF-03-02 findings where the LLM-implementability lens materially changed technology selection outcomes.

## Canonical Statements
- Every RF document MUST include an LI-1 through LI-6 assessment for each evaluated technology using the standardized template.
- Technologies scoring below 8/18 (raw) MUST be flagged as High Risk in the RF and ADR.
- Technologies scoring below 4/18 (raw) MUST be excluded unless no alternatives exist, with explicit risk acceptance in the ADR.
- ADR decision rationale MUST address LLM-implementability alongside functional fit.
- LI scores of 2 or 3 MUST be supported by at least one T1 or T2 evidence source per DD-20-01.
- Calendar timeline estimates SHOULD be replaced by complexity profiles (concept count, integration points, iteration cycles, token budget).
- For Compass evaluations, LI-1 and LI-3 carry 1.5× weight; weighted thresholds apply.
- LLM-implementability does NOT replace functional evaluation; it is an additional dimension.

## Scope and Non-Goals
- In scope: Evaluation criteria, scoring rubric, thresholds, weighting, evidence mapping, complexity profiles, and assessment templates for technology choices where the primary developer is an LLM coding agent.
- Out of scope: Evaluation of LLM models themselves (see RF-09-01, ADR-09-01). Enforceable compliance rules (see planned STD-22-01). Content quality evaluation for Compass outputs consumed by humans (see DD-18-01, DD-19-01).

## Dependencies and Interfaces
- Evidence grading framework: `DD-20-01` (S1-S4, I1-I4, Confidence).
- Citation format: `STD-20-01`.
- Artifact taxonomy (RF and ADR definitions): `DD-13-01`.
- Ecosystem tool evaluation context: `DD-14-01`.
- System definition (LLM-agent-first development model): `SYS-00` §1.1.
- Enforcement companion: `STD-22-01` (planned).
- Origin research: `RF-03-02`.

## The Six LI Criteria (Quick Reference)

| Criterion | Core Question | Key Signals (Score 3) | Key Signals (Score 0) |
|-----------|--------------|----------------------|----------------------|
| LI-1: Documentation Quality | Can the LLM parse and act on the docs? | `llms.txt` full+lite, MCP docs server, complete examples, machine-readable API refs | No public documentation |
| LI-2: MCP Tool Availability | Can the LLM access the library through MCP? | Official MCP server, Context7 entry, CLAUDE.md | No MCP presence |
| LI-3: Code Complexity | How many ways can the LLM go wrong? | TypeScript-native with strict types, <10 concepts per task, opinionated API | Custom DSL, many optional params, no types |
| LI-4: Testability | Can the LLM verify its own output? | In-memory test backends, standard frameworks (Vitest/Jest), example tests | No testing guidance or utilities |
| LI-5: LLM Familiarity | Is it in the training data? | npm >1M weekly, GitHub >10K stars, pre-2023 release | npm <100K, GitHub <1K, post-2025 release |
| LI-6: Hallucination Risk | How detectable are LLM mistakes? | Opinionated API, diagnostic errors, no version confusion | Permissive API, silent failures, major version divergence |

## Scoring and Thresholds

### Raw Scores (unweighted)
| Range | Classification | Implication |
|-------|---------------|-------------|
| 14-18 | Low Risk | Standard development practices apply |
| 8-13 | Moderate Risk | Requires detailed specs, supplementary docs, more iteration budget |
| 4-7 | High Risk | Consider alternatives; plan extensive prompt engineering if no alternative |
| 0-3 | Exclusion | Do not select unless absolutely required with explicit risk acceptance |

### Compass Weighted Scores (LI-1 × 1.5, LI-3 × 1.5)
| Range | Classification |
|-------|---------------|
| 16-21 | Low Risk |
| 9-15 | Moderate Risk |
| 5-8 | High Risk |
| 0-4 | Exclusion |

## Complexity Profile Dimensions (Replacing Timeline Estimates)
- **Concept count**: Distinct concepts LLM must implement correctly
- **Integration points**: Subsystem boundaries the implementation crosses
- **Pattern conventionality**: LI-3 + LI-5 scores
- **Test coverage feasibility**: LI-4 score + percentage of testable code
- **Expected iteration cycles**: Low complexity + high testability = 2-3 cycles; high complexity + low testability = 8-12 cycles
- **Token budget estimate**: Concept count × iteration cycles × 2K-10K tokens per concept per cycle

## Prior Rubric Mapping
RF-01-01's MCP Server/llms.txt/Cursor Rules/TypeScript Types/LLM Error Prevention map to LI-2/LI-1/LI-2/LI-3/LI-6. RF-02-01's 7-criterion rubric maps to LI-1/LI-3/LI-3/LI-1+LI-2/LI-6/LI-5/LI-1. See DD-22-01 Appendix C for full mapping tables.

## Core Invariants
- LLM-implementability is a composite of six independently scored criteria.
- The framework supplements, never replaces, functional evaluation.
- Scores require evidence; a score without cited evidence is an opinion.
- Thresholds are guidelines, not hard gates; score distribution matters alongside totals.
- Calendar timelines are replaced by complexity profiles for LLM-agent development contexts.

## Glossary Snapshot
- **LI-1 through LI-6**: The six LLM-Implementability criteria.
- **Concept count**: Distinct concepts an LLM must combine correctly for a task.
- **Complexity profile**: Structured replacement for calendar timeline estimates.
- **Hallucination risk**: Probability of plausible but incorrect LLM-generated code.
- **`llms.txt`**: Standardized file for LLM-friendly documentation (per llmstxt.org).
- **MCP**: Model Context Protocol for connecting LLM agents to external tools.
- **Token budget**: Estimated total token consumption for an implementation task.

## Evidence and Freshness
- Source document created 2026-02-06. This LLM view is current.
- LI evidence maps to DD-20-01 grading: `llms.txt` = T1/S1, MCP server listing = T1/S1, npm downloads = T1/S2, GitHub stars = T1/S2, Context7 listing = T2/S2, community MCP server = T4/S3.
- Minimum evidence: LI scores of 2-3 require T1/T2 evidence. Overall High confidence requires 4+ of 6 criteria evidenced at T1/T2.

## Open Questions
- STD-22-01 (companion enforcement standard) is planned but not yet created.
- Whether LI weighting should vary by EFN project archetype (DD-14-01) beyond the Compass-specific 1.5× for LI-1/LI-3.
- How to handle rapidly evolving libraries where LI-5 (familiarity) changes between model versions.

## Change Log
- 2026-02-06: Initial creation. Framework defined with six criteria, scoring rubric, thresholds, Compass-specific weighting, evidence mapping, complexity profiles, and prior rubric mappings.
