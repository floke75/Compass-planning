---
id: STD-22-01
type: standard
area: 22-llm-implementability
title: LLM-Implementability Evaluation Standards
status: draft
created: 2026-02-06
updated: 2026-02-06
author: compass-research
summary: Enforceable compliance rules for LLM-Implementability assessments in Research Findings and ADRs, including applicability rules, scoring discipline, threshold enforcement, complexity profile requirements, and review checklists
tags: [llm-implementability, evaluation, compliance, standard, scoring, technology-selection, agent-development]
related:
  - DD-22-01
  - DD-20-01
  - DD-13-01
  - DD-14-01
  - STD-20-01
  - SYS-00
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
companion: DD-22-01
enforcement: RF and ADR review checklists
---

# LLM-Implementability Evaluation Standards

## Document Purpose

This document specifies enforceable rules for LLM-Implementability (LI) assessments across Compass documentation. It is the enforcement companion to DD-22-01 (LLM-Implementability Evaluation Framework), which defines the six LI criteria, the 0-3 scoring rubric, thresholds, weighting rules, and evidence mapping.

DD-22-01 defines *what* LLM-implementability is and *how* to measure it. This document specifies *when* an LI assessment is required, *what constitutes a compliant assessment*, and *what happens when scores cross thresholds*. Without this enforcement layer, the LI framework remains advisory.

**How to use this document:**
1. Before creating or updating an RF: check Part 1 to determine if an LI assessment is required
2. When writing an LI assessment: follow the RF compliance checklist in Part 2
3. When writing an ADR: follow the ADR compliance checklist in Part 3
4. When reviewing RF or ADR documents: use the review checklist in Part 7
5. When scores cross thresholds: follow the enforcement rules in Part 5
6. When replacing timeline estimates: follow the complexity profile requirements in Part 6

**Enforcement**: RF and ADR review checklists. A document that fails the applicable checklist is non-compliant and must be revised before acceptance.

---

## Part 1: Applicability Rules

### 1.1 When an LI Assessment Is Required

An LI assessment using the full DD-22-01 framework (all six criteria scored, evidence cited, risk classification stated) is **required** in:

1. **All new Research Findings** (RF documents) that evaluate libraries, frameworks, services, or tools that LLM coding agents will use to build Compass. This includes backend platforms, orchestration frameworks, widget libraries, development tooling, memory systems, and any technology that will appear in implementation code.

2. **All ADR decision rationale sections** that select or reject a technology. The ADR need not repeat the full scoring table but MUST reference the LI scores and risk classification from the underlying RF, address LI risks in the Consequences section, and compare LI scores when explaining why alternatives were rejected.

3. **Ecosystem tool evaluations** per DD-14-01. When a new tool is proposed for the EFN ecosystem, its LI profile must be assessed before inclusion. This applies whether the evaluation appears in a standalone RF or in an ecosystem assessment note.

4. **Updates to existing RFs** that materially change technology recommendations. If an RF is revised and the revision alters which technology is recommended, the LI assessment must be updated or created for the revised recommendation.

### 1.2 When an LI Assessment Is Optional

An LI assessment is **optional** (but encouraged) for:

1. **Hosting and infrastructure RFs** (e.g., RF-08-01) where the technology choice does not affect code that LLM agents generate. If the hosting platform requires no application-level code changes (only configuration or deployment scripts), a brief LI note explaining why the full assessment is not applicable is sufficient.

2. **LLM provider evaluations** (e.g., RF-09-01) where the subject of evaluation is the LLM itself rather than a library the LLM uses. LI criteria measure how well a technology supports LLM *implementation*; they do not measure the LLM's own capabilities.

3. **Minor ADR confirmation notes** that reaffirm an existing decision without introducing new technology. If the ADR records "we confirmed our earlier selection of X," no new LI assessment is needed provided the original assessment is still current.

4. **Research findings that are purely informational** and do not lead to technology selection (e.g., landscape surveys, trend analyses).

### 1.3 The Brief LI Note (For Optional Cases)

When a full LI assessment is not required, the RF or ADR SHOULD include a brief note explaining why:

```markdown
### LLM-Implementability Note

A full LI assessment is not applicable to this evaluation because [hosting
configuration does not affect LLM-generated application code / this RF is
a landscape survey without technology selection / etc.]. See STD-22-01 §1.2
for applicability rules.
```

This note prevents reviewers from flagging the omission and documents the intentional decision to skip the assessment.

---

## Part 2: RF Compliance Checklist

A conforming LI assessment section in a Research Findings document MUST include all of the following. Use the assessment templates from DD-22-01 §3.4.

### 2.1 Required Elements

For each technology evaluated:

- [ ] All six criteria (LI-1 through LI-6) are scored on the 0-3 scale
- [ ] Each score cites primary evidence (a specific URL, metric, or verifiable fact—not "general impression")
- [ ] The raw total (sum of six scores, max 18) is calculated and stated
- [ ] The weighted total is calculated when Compass-specific weighting applies (LI-1 × 1.5 + LI-2 + LI-3 × 1.5 + LI-4 + LI-5 + LI-6, max 21)
- [ ] The risk classification is stated (Low Risk / Moderate Risk / High Risk / Exclusion Zone) per DD-22-01 §3.3 thresholds
- [ ] Assessment notes address concentrated weaknesses (any criterion scored 0 or 1 must be explicitly discussed)
- [ ] Half-point scores (0.5, 1.5, 2.5) are used only when evidence supports an intermediate assessment; they must not be used to avoid committing to a whole-number score

### 2.2 Comparative Evaluations

When an RF evaluates multiple technologies:

- [ ] All technologies use the same scoring template (side-by-side format from DD-22-01 §3.4)
- [ ] The same evidence standard is applied to each technology (one technology must not receive inflated scores due to more thorough investigation)
- [ ] The RF explicitly states which technology scores best on LI and whether LI scores change the recommendation relative to functional fit alone

### 2.3 Evidence Requirements per Score Level

| Score | Minimum Evidence Required |
|-------|--------------------------|
| **0** | Statement that the capability is absent. Evidence of absence (e.g., "no `llms.txt` found at {URL}, no MCP server listed in {vendor docs}") is acceptable. |
| **1** | At least one specific signal from the DD-22-01 Part 2 signal hierarchy for the relevant criterion, at any source tier. |
| **2** | At least one T1 or T2 evidence source per DD-20-01. General impressions or unsourced claims are non-compliant. |
| **3** | At least one T1 or T2 evidence source per DD-20-01, plus at least one additional corroborating signal. A score of 3 represents "Excellent" and must be clearly earned. |

---

## Part 3: ADR Compliance Checklist

A conforming ADR that selects or rejects a technology MUST include the following LI-related elements.

### 3.1 Decision Rationale

- [ ] LI scores from the underlying RF are referenced by number (e.g., "Mastra scored 14/18, Low Risk")
- [ ] The rationale explicitly states whether LLM-implementability influenced the selection
- [ ] If a technology with lower functional fit was selected over one with higher functional fit due to superior LI scores, the trade-off is explained

### 3.2 Consequences Section

- [ ] LI risks for the selected technology are documented in the Consequences section
- [ ] Any criterion scored 0 or 1 has a stated mitigation strategy (e.g., "LI-1 scored 1/3; mitigate by providing supplementary documentation in the agent context window")
- [ ] If the selected technology scores below 14/18 (Low Risk threshold), the ADR states what additional measures will be taken during implementation

### 3.3 Rejected Alternatives

- [ ] When rejecting an alternative with adequate functional fit, the ADR compares LI scores if they differ meaningfully (≥ 3 points)
- [ ] The comparison states which specific criteria drove the LI difference

### 3.4 Template for ADR LI Reference

```markdown
### LLM-Implementability Consideration

[Selected technology] scored [X/18 raw, Y/21 weighted] ([risk classification])
in [RF-XX-XX]. Key LI strengths: [list]. Key LI risks: [list with mitigation].

[Rejected alternative] scored [X/18 raw, Y/21 weighted] ([risk classification]).
The [N-point] LI gap was driven by [specific criteria].
```

---

## Part 4: Scoring Discipline

These rules prevent score inflation and ensure consistency across assessments.

### 4.1 Prohibited Scoring Practices

The following are **non-compliant** and must be corrected during review:

1. **"General impression" scores.** A score accompanied only by vague justification ("seems well-documented," "probably familiar") is non-compliant. Every score must reference at least one specific, verifiable signal from DD-22-01 Part 2.

2. **Rounding up without evidence.** Assigning a score of 2 when evidence only supports 1.5 (or a half-point score when evidence only supports a round number lower). If the evidence is ambiguous, score conservatively and explain the uncertainty in assessment notes.

3. **Asymmetric scrutiny.** Applying stricter evidence standards to one technology than another in the same comparative evaluation. If Technology A's LI-5 is scored using npm download data, Technology B's LI-5 must also reference npm download data (or equivalent metrics), not "probably well-known."

4. **Conflating functional quality with LI scores.** A library can be excellent for human developers and score poorly on LI (e.g., beautiful documentation site that is not machine-parseable). LI scores measure LLM-implementability, not overall technical quality.

5. **Ignoring version-specific evidence.** Scoring LI-5 (familiarity) or LI-6 (hallucination risk) without considering which library version is being evaluated. A library may have high familiarity for v2 but low familiarity for v3 if v3 introduced breaking changes after the LLM's training cutoff.

### 4.2 Score Calibration Guidance

To maintain consistency across assessments:

- A score of 3 on any criterion means the technology is among the best available for that criterion in the relevant ecosystem. If most technologies in a category would score 3, the criterion is not being assessed critically enough.
- A score of 0 means the capability is absent, not merely "below average." Use 1 for "present but limited."
- When uncertain between two adjacent scores, prefer the lower score with an explanatory note over the higher score. Conservative scoring with honest notes is more useful than optimistic scoring.

---

## Part 5: Threshold Enforcement

### 5.1 Below 8/18 Raw (High Risk)

When a technology scores below 8/18 on the raw total (or below 9/21 on the Compass-weighted total):

1. The RF MUST flag the technology as "High Risk — LLM Implementation" in the assessment section.
2. The RF MUST include a brief analysis of whether alternative technologies exist that score higher.
3. If the technology is still recommended despite the High Risk classification, the RF MUST include a mitigation plan addressing each criterion scored 0 or 1.
4. The corresponding ADR MUST explicitly acknowledge the High Risk classification and document the rationale for proceeding.

### 5.2 Below 4/18 Raw (Exclusion Zone)

When a technology scores below 4/18 on the raw total (or below 5/21 on the Compass-weighted total):

1. The technology MUST be excluded from selection unless all of the following conditions are met:
   - No alternative technology exists that meets the functional requirements
   - The capability provided by the technology is essential to Compass (not merely desirable)
   - The ADR includes an explicit risk acceptance statement signed off by the project lead
2. The risk acceptance statement MUST include: the specific LI scores, the anticipated implementation challenges, the planned mitigation strategies, and the estimated additional token budget required.

### 5.3 Concentrated Weakness Override

Regardless of total score, any technology with a score of 0 on LI-4 (Testability) or LI-6 (Hallucination Risk) MUST be flagged for additional review. These two criteria represent the LLM's ability to self-verify and the risk of undetectable errors—weaknesses that cannot be compensated by strength in other criteria.

A technology scoring 14/18 overall but 0 on LI-6 presents a qualitatively different risk than one scoring 14/18 with all scores ≥ 2. The assessment notes MUST address this explicitly.

---

## Part 6: Complexity Profile Requirements

### 6.1 When Complexity Profiles Are Required

A complexity profile (as defined in DD-22-01 §7.2) is **required** when:

1. An RF includes implementation feasibility analysis for a recommended technology
2. An ADR estimates implementation effort in the Consequences section
3. Any document would otherwise include a calendar-based timeline estimate ("2-3 weeks," "1 sprint")

Calendar-based timelines (days, weeks, sprints) MUST NOT appear in RF or ADR documents for work that will be performed by LLM coding agents. If a calendar timeline is needed for human coordination purposes (e.g., "the research phase takes 1 week of human review"), it must be clearly separated from LLM implementation estimates.

### 6.2 Minimum Profile Dimensions

A compliant complexity profile MUST include at least these dimensions:

| Dimension | Description | Required? |
|-----------|-------------|-----------|
| **Concept count** | Number of distinct concepts the LLM must correctly implement | Yes |
| **Integration points** | Number of subsystem boundaries the implementation crosses | Yes |
| **Pattern conventionality** | Reference to LI-3 and LI-5 scores | Yes |
| **Expected iteration cycles** | Estimated generate-test-fix loops, referencing LI-3 and LI-4 | Yes |
| **Token budget estimate** | Order-of-magnitude token consumption | Yes |
| **Test coverage feasibility** | Percentage of testable code, referencing LI-4 | Recommended |

### 6.3 Template

```markdown
### Complexity Profile

[Technology name] requires implementing ~[N] distinct concepts ([list key
concepts]). The implementation crosses [N] integration points ([list
boundaries]). Patterns are [conventional/mixed/novel] (LI-3: X/3, LI-5:
Y/3), with [good/limited/no] test utilities (LI-4: Z/3). Expected
iteration cycles: [N-M]. Estimated token budget: [range]K tokens.
```

---

## Part 7: Review Checklist

Use this checklist when reviewing RF or ADR documents for LI compliance. A document must pass all applicable items to be considered compliant.

### 7.1 RF Review Checklist

- [ ] **Applicability**: LI assessment is present if required per §1.1, or a brief LI note per §1.3 explains why it is omitted
- [ ] **Completeness**: All six criteria scored for each evaluated technology
- [ ] **Evidence**: Each score cites specific evidence per the requirements in §2.3
- [ ] **No inflation**: Scores of 2+ are backed by T1/T2 evidence; scores of 3 have corroborating signals
- [ ] **Risk classification**: Stated and consistent with DD-22-01 §3.3 thresholds
- [ ] **Concentrated weaknesses**: Any criterion scored 0 or 1 is discussed in assessment notes
- [ ] **Threshold compliance**: Technologies below 8/18 are flagged per §5.1; technologies below 4/18 are handled per §5.2
- [ ] **No calendar timelines**: Implementation estimates use complexity profiles per §6, not calendar durations
- [ ] **Consistency**: In comparative evaluations, the same evidence standards apply to all technologies
- [ ] **Weighting**: Compass-specific weighting applied correctly if applicable (LI-1 × 1.5, LI-3 × 1.5)

### 7.2 ADR Review Checklist

- [ ] **LI reference**: ADR rationale references LI scores from the underlying RF
- [ ] **Risk acknowledgment**: LI risks documented in Consequences section
- [ ] **Mitigation**: Each concentrated weakness (criteria scored 0 or 1) has a stated mitigation strategy
- [ ] **Rejected alternatives**: LI scores compared when rejecting alternatives with adequate functional fit
- [ ] **Threshold compliance**: High Risk or Exclusion Zone technologies have the required documentation per §5.1 or §5.2

---

## Part 8: Common Mistakes

### 8.1 Confusing Documentation Quality with Documentation Quantity

❌ **Non-compliant:**
> LI-1: 3/3. The library has extensive documentation with hundreds of pages.

✅ **Compliant:**
> LI-1: 2/3. The library has extensive human-readable documentation but no `llms.txt`, no MCP docs server, and no machine-readable API reference. Code examples are present but some are incomplete snippets. The volume of documentation is a moderate positive but the lack of LLM-specific access mechanisms prevents a score of 3.

**Why it matters:** LI-1 measures documentation quality *for LLM consumption*, not documentation volume. Hundreds of prose pages that an LLM cannot efficiently parse may score lower than a single well-structured `llms.txt` file.

### 8.2 Treating Popularity as Proof of LLM Familiarity

❌ **Non-compliant:**
> LI-5: 3/3. The library is very popular and widely used.

✅ **Compliant:**
> LI-5: 2/3. npm weekly downloads: 850K (moderate proxy for training data presence). GitHub stars: 8,200. First released 2022, pre-dating current LLM training cutoffs. However, a major API rewrite in v3 (2025) means LLM training data likely reflects v2 patterns. Scored 2 rather than 3 due to version transition risk.

**Why it matters:** Popularity metrics are proxies, not direct measures. Version changes, API rewrites, and training data cutoffs can make a popular library less familiar to an LLM than its download count suggests.

### 8.3 Scoring Hallucination Risk Without Specific Failure Modes

❌ **Non-compliant:**
> LI-6: 2/3. Hallucination risk seems moderate.

✅ **Compliant:**
> LI-6: 2/3. Primary risk factors: (1) Two major versions (v2, v3) with incompatible middleware registration patterns, creating version confusion risk. (2) Configuration object has 15+ optional fields with subtle interactions. Mitigating factors: (1) Strong TypeScript types catch most configuration errors at compile time. (2) Error messages include the specific configuration field that failed validation. Net assessment: moderate risk, manageable with version pinning and typed configuration.

**Why it matters:** LI-6 requires analysis of specific hallucination vectors. "Seems moderate" provides no actionable information and cannot be verified.

### 8.4 Omitting the Assessment for "Obviously Good" Technologies

❌ **Non-compliant:**
> [No LI assessment section] — Note: TypeScript is well-known and doesn't need an LI assessment.

✅ **Compliant:**
> Even well-known technologies receive the full assessment. A familiar technology may score poorly on LI-2 (no MCP server) or LI-4 (testing requires complex setup), and these weaknesses only surface through systematic evaluation.

**Why it matters:** The purpose of systematic assessment is to surface unexpected weaknesses. Skipping the assessment for technologies that "seem fine" defeats this purpose.

### 8.5 Using Calendar Timelines Alongside Complexity Profiles

❌ **Non-compliant:**
> Complexity Profile: 8 concepts, 3 integration points, 4-6 iteration cycles.
> Estimated implementation time: 2-3 weeks.

✅ **Compliant:**
> Complexity Profile: 8 concepts (client setup, agent definitions, tool registration, workflow state machine, persistence adapter, error handling, test harness, deployment configuration). 3 integration points (Convex backend, LLM provider, MCP tools). Conventional patterns (LI-3: 2/3) with good test utilities (LI-4: 2/3). Expected iteration cycles: 4-6. Estimated token budget: 200K-500K tokens.

**Why it matters:** Calendar timelines are meaningless for LLM agent work and create false comparability with human development estimates. Once a calendar timeline appears, readers anchor on it rather than the complexity profile.

---

## Part 9: Examples

### 9.1 Compliant RF Assessment (Single Technology)

```markdown
### LLM-Implementability Assessment: Mastra

| Criterion | Score | Primary Evidence |
|-----------|-------|-----------------|
| LI-1: Documentation Quality | 3/3 | `llms.txt` (full + lite variants) at mastra.ai/llms.txt; MCP docs server (`@mastra/mcp-docs-server`); complete TypeScript examples throughout docs |
| LI-2: MCP Tool Availability | 2/3 | Official MCP docs server; CLAUDE.md integration guide; no Context7 entry found |
| LI-3: Code Complexity | 2/3 | TypeScript-native with Zod validation; ~12 concepts per typical agent task; conventional async/await patterns |
| LI-4: Testability | 2/3 | Test utilities documented; Vitest support; in-memory mode for agent testing |
| LI-5: LLM Familiarity | 1/3 | npm weekly downloads: ~15K (low); GitHub stars: ~4,800; first release 2024 (post some training cutoffs) |
| LI-6: Hallucination Risk | 2/3 | Opinionated API reduces wrong-path risk; TypeScript catches type errors; minor version confusion between v0.x and v1.x |
| **Raw Total** | **12/18** | |
| **Weighted Total** | **15.5/21** | LI-1 (3 × 1.5 = 4.5) + LI-2 (2) + LI-3 (2 × 1.5 = 3) + LI-4 (2) + LI-5 (1) + LI-6 (2) |
| **Risk Classification** | **Moderate Risk** | Weighted 15.5/21 → Moderate Risk (9-15 range) |

**Assessment notes**: Concentrated weakness on LI-5 (familiarity).
Mastra is a newer framework and may not be deeply represented in LLM
training data. Mitigation: leverage the strong LI-1 score by ensuring
the MCP docs server is available in the agent context during
implementation. The weighted score is borderline between Moderate
and Low Risk; the LI-1 strength partially compensates for the LI-5
weakness because the LLM can query current documentation rather
than relying on training data alone.
```

### 9.2 Compliant Comparative Assessment

```markdown
### Comparative LLM-Implementability Assessment

| Criterion | Graphiti | Mem0 | Mastra Memory |
|-----------|---------|------|---------------|
| LI-1: Documentation Quality | 1/3 | 2/3 | 3/3 |
| LI-2: MCP Tool Availability | 2/3 | 1/3 | 2/3 |
| LI-3: Code Complexity | 2/3 | 1/3 | 2/3 |
| LI-4: Testability | 1/3 | 1/3 | 2/3 |
| LI-5: LLM Familiarity | 1/3 | 1/3 | 1/3 |
| LI-6: Hallucination Risk | 2/3 | 1/3 | 2/3 |
| **Raw Total** | **9/18** | **7/18** | **12/18** |
| **Risk Classification** | Moderate | High Risk ⚠️ | Moderate |

**Assessment notes**: Mem0 scores below the 8/18 threshold and is
flagged as High Risk per STD-22-01 §5.1. Key weaknesses: limited
documentation structure (LI-1), managed-service complexity reducing
code predictability (LI-3), and no dedicated test utilities (LI-4).
If Mem0 is still considered, a mitigation plan must be included
per §5.1 requirements. Graphiti's moderate score is driven by
Docker-based MCP setup (strong LI-2) offsetting weaker
documentation (LI-1: 1/3). Mastra Memory benefits from the
broader Mastra ecosystem's documentation and tooling.
```

### 9.3 Non-Compliant Assessment (With Corrections)

❌ **Non-compliant:**
```markdown
### LLM Assessment

Library X seems pretty good for LLM development. It's well-known
and has decent docs. Score: ~13/18. Should be fine.
```

**Problems:**
1. No individual criterion scores
2. No evidence cited for any score
3. No risk classification
4. "Seems pretty good" and "decent docs" are general impressions, not evidence
5. "~13" is imprecise—each criterion must be scored individually
6. No assessment notes addressing weaknesses

✅ **Corrected:** Use the template from DD-22-01 §3.4. Score each criterion individually. Cite evidence per §2.3 of this standard. State the risk classification. Discuss any concentrated weaknesses.

---

## Appendix A: Quick Reference

### Applicability Decision Tree

```
Is this an RF evaluating technology for LLM agent implementation?
  → YES: Full LI assessment required (§1.1)
  → NO: Is this an ADR selecting/rejecting technology?
    → YES: LI reference in rationale required (§1.1, §3)
    → NO: Is this a hosting/infrastructure RF?
      → YES: Brief LI note explaining non-applicability (§1.2, §1.3)
      → NO: LI assessment optional (§1.2)
```

### Scoring Evidence Quick Reference

| Score | Evidence Floor |
|-------|---------------|
| 0 | Documented absence |
| 1 | One specific signal from DD-22-01 Part 2 |
| 2 | T1 or T2 evidence per DD-20-01 |
| 3 | T1/T2 evidence + corroborating signal |

### Threshold Actions Quick Reference

| Raw Score | Action |
|-----------|--------|
| 14-18 | Standard process |
| 8-13 | Proceed with caution; note in ADR Consequences |
| 4-7 | Flag High Risk; require mitigation plan; explore alternatives |
| 0-3 | Exclude unless essential + no alternatives + explicit risk acceptance |

---

## Appendix B: Related Documents

- **DD-22-01**: LLM-Implementability Evaluation Framework (definitions, criteria, rubric, templates)
- **DD-20-01**: Evidence Standards for Citations and Sources (S1-S4, I1-I4, Confidence levels)
- **STD-20-01**: Evidence Citation Format Specification (citation format rules)
- **DD-13-01**: Artifact Taxonomy (RF and ADR artifact type definitions)
- **DD-14-01**: EFN Ecosystem Definitions (ecosystem tool evaluation context)
- **SYS-00**: System Definition (establishes LLM-agent-first development model, §1.1)

---

*End of LLM-Implementability Evaluation Standards (STD-22-01)*
