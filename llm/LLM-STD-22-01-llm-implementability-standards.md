---
id: STD-22-01-LLM
type: standard
area: 22-llm-implementability
title: LLM-Implementability Evaluation Standards (LLM View)
created: 2026-02-06
updated: 2026-02-06
summary: LLM-optimized view of enforceable compliance rules for LI assessments in Research Findings and ADRs
tags: [llm-implementability, evaluation, compliance, standard, scoring, technology-selection, llm, view]
links:
  - rel: companion
    target_id: "DD-22-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "SYS-00"
view: llm
source_id: STD-22-01
source_updated: 2026-02-06
staleness: fresh
---

# LLM-Implementability Evaluation Standards (LLM View)

## LLM Summary
STD-22-01 enforces DD-22-01's LLM-Implementability framework by specifying when LI assessments are required, what constitutes a compliant assessment, and what happens at score thresholds. Full assessments are mandatory for all RFs evaluating technology for LLM agent implementation, all ADRs selecting or rejecting technology, and ecosystem tool evaluations per DD-14-01. Assessments are optional for hosting/infrastructure RFs and LLM provider evaluations. RF compliance requires all six criteria scored with cited evidence, risk classification stated, and concentrated weaknesses discussed. ADR compliance requires LI scores in rationale, risks in Consequences, and LI comparison when rejecting alternatives. Scores of 2+ require T1/T2 evidence; scores of 3 require corroboration. Technologies below 8/18 must be flagged with mitigation plans; below 4/18 must be excluded unless essential with explicit risk acceptance. Calendar timelines are prohibited for LLM agent work; complexity profiles are required instead.

## Canonical Statements
- All new RFs evaluating technology for LLM agent implementation MUST include a full LI assessment (all six criteria scored, evidence cited, risk classification stated).
- ADR decision rationale MUST reference LI scores, address LI risks in Consequences, and compare LI scores when rejecting alternatives.
- Scores of 2 or 3 MUST be supported by T1/T2 evidence per DD-20-01. Scores of 3 additionally require corroborating signals.
- "General impression" scores without specific, verifiable evidence are non-compliant.
- Technologies scoring below 8/18 raw MUST be flagged as High Risk with a mitigation plan.
- Technologies scoring below 4/18 raw MUST be excluded unless essential + no alternatives + explicit risk acceptance.
- Any technology scoring 0 on LI-4 (Testability) or LI-6 (Hallucination Risk) MUST be flagged regardless of total score.
- Calendar-based timeline estimates MUST NOT appear for LLM agent work; complexity profiles are required instead.
- When a full LI assessment is not required, a brief LI note explaining why SHOULD be included.

## Scope and Non-Goals
- In scope: Applicability rules, RF and ADR compliance checklists, scoring discipline, threshold enforcement actions, complexity profile requirements, review checklists, common mistakes, and compliant/non-compliant examples.
- Out of scope: Defining the LI criteria themselves or the scoring rubric (see DD-22-01). Evidence grading philosophy (see DD-20-01). Citation formats (see STD-20-01).

## Dependencies and Interfaces
- LI criteria definitions, scoring rubric, thresholds, weighting, templates: `DD-22-01`.
- Evidence grading (S1-S4, T1-T5, Confidence): `DD-20-01`.
- Citation format requirements: `STD-20-01`.
- Artifact type definitions (RF, ADR): `DD-13-01`.
- Ecosystem tool evaluation context: `DD-14-01`.
- System definition (LLM-agent-first model): `SYS-00` §1.1.

## Applicability Quick Reference

| Document Type | LI Requirement |
|--------------|----------------|
| RF evaluating technology for LLM implementation | Full assessment required |
| ADR selecting/rejecting technology | LI reference in rationale required |
| Ecosystem tool evaluation (DD-14-01) | Full assessment required |
| RF update changing recommendation | Updated assessment required |
| Hosting/infrastructure RF | Optional; brief LI note explaining omission |
| LLM provider evaluation | Optional |
| Minor ADR confirmation | Not required if original assessment is current |
| Informational survey RF | Optional |

## Scoring Evidence Floors

| Score | Minimum Evidence |
|-------|-----------------|
| 0 | Documented absence of capability |
| 1 | One specific signal from DD-22-01 Part 2 |
| 2 | T1 or T2 evidence per DD-20-01 |
| 3 | T1/T2 evidence + at least one corroborating signal |

## Threshold Enforcement Actions

| Raw Score | Weighted Score | Classification | Required Action |
|-----------|---------------|----------------|-----------------|
| 14-18 | 16-21 | Low Risk | Standard process |
| 8-13 | 9-15 | Moderate Risk | Note in ADR Consequences |
| 4-7 | 5-8 | High Risk | Flag + mitigation plan + explore alternatives |
| 0-3 | 0-4 | Exclusion | Exclude unless essential + no alternatives + risk acceptance |

## RF Review Checklist (Condensed)
- [ ] LI assessment present (or brief note per §1.3 explaining omission)
- [ ] All six criteria scored per technology
- [ ] Evidence cited per score level (§2.3)
- [ ] No general-impression scores; all evidence is specific and verifiable
- [ ] Risk classification stated and matches DD-22-01 thresholds
- [ ] Concentrated weaknesses (0 or 1 scores) discussed in notes
- [ ] Threshold actions followed (§5.1 for <8, §5.2 for <4)
- [ ] No calendar timelines; complexity profiles used instead
- [ ] Consistent evidence standards across compared technologies
- [ ] Compass weighting applied correctly if applicable

## ADR Review Checklist (Condensed)
- [ ] LI scores referenced in rationale
- [ ] LI risks in Consequences section
- [ ] Mitigation stated for criteria scored 0 or 1
- [ ] LI compared when rejecting alternatives with adequate functional fit
- [ ] Threshold documentation present if applicable

## Prohibited Scoring Practices
1. General impression scores without specific evidence
2. Rounding up without supporting evidence
3. Asymmetric scrutiny (stricter standards for one technology than another)
4. Conflating functional quality with LI scores
5. Ignoring version-specific evidence for LI-5 and LI-6

## Complexity Profile Minimum Dimensions
Required: concept count, integration points, pattern conventionality (LI-3/LI-5), expected iteration cycles (LI-3/LI-4), token budget estimate. Recommended: test coverage feasibility (LI-4).

## Evidence and Freshness
- Source document created 2026-02-06. This LLM view is current.
- Enforcement mechanism: RF and ADR review checklists.
- Evidence standards for LI scores align with DD-20-01 source tier system.

## Open Questions
- Whether the concentrated weakness override (§5.3) should extend beyond LI-4 and LI-6 to other criteria.
- How to handle LI assessments for technologies that span multiple categories (e.g., a platform that is both a backend and an orchestration framework).
- Whether retroactive LI assessment is required for existing RFs created before DD-22-01.

## Change Log
- 2026-02-06: Initial creation. Enforcement companion to DD-22-01 covering applicability rules, RF/ADR compliance checklists, scoring discipline, threshold enforcement, complexity profile requirements, review checklists, common mistakes, and examples.
