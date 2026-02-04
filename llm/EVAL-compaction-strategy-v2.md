# Evaluation: Compaction Strategy v2 vs v1

**Date**: 2026-02-04
**Evaluator**: Claude (Opus 4.5)
**Documents Compared**:
- v1: `PROMPT-llm-compaction.md` (2026-02-03)
- v2: Proposed update (2026-02-04)

**Status**: Evaluation complete. Suggestions from "Concerns and Suggestions" section have been applied in v2.1.

---

## Summary

Version 2 represents a significant improvement focused on three core themes:
1. **Fluff elimination** - New rules targeting empty sections, boilerplate, and redundant fields
2. **Entity hygiene** - New handling for orphaned references and undefined acronyms
3. **Temporal sanitization** - Explicit rules to strip calendar dates and phase timelines

---

## Key Improvements

### 1. Critical Omission Rules (NEW)

v1 lacked explicit guidance on what structural elements to remove. v2 adds 7 concrete omission rules:

| Rule | Impact |
|------|--------|
| Empty sections → delete entirely | Eliminates "Open Questions: None" noise |
| Uniform frontmatter → omit | Removes `author`, `status: draft` when constant |
| Change Log for LLM views → omit | Removes "LLM view created" boilerplate |
| "Evidence and Freshness" → omit when empty | Cuts sections with no citations |
| Glossary corpus terms → omit | Prevents glossary duplication |

**Assessment**: Strong addition. These rules directly address observed fluff patterns in existing LLM views.

### 2. Entity Reference Rules (NEW)

v1 had no guidance for orphaned entities. v2 adds explicit handling:

```
# v1: No guidance → orphaned references preserved
# v2: Three options
- Add minimal context: "EFN (a financial news organization)"
- Remove entirely if not architecturally relevant
- Generalize: "the broader tooling ecosystem"
```

**Assessment**: Critical addition. Orphaned acronyms and project names create confusion for downstream LLM consumers.

### 3. Temporal Reference Handling (NEW)

v1 preserved temporal artifacts. v2 explicitly strips them:

| Before (v1) | After (v2) |
|-------------|------------|
| "Phase 2 starts in March" | "requires Phase 1 completion" |
| "Sprint 15" | Removed or converted to dependency |
| "Q2 2026" | Removed entirely |

**Assessment**: Important for LLM views' longevity. Calendar dates become misleading after they pass.

### 4. Compression Ratio Adjustment

| Version | Target Output Length | Compression |
|---------|---------------------|-------------|
| v1 | 30-50% of source | 50-70% reduction |
| v2 | 15-40% of source | 60-85% reduction |

**Assessment**: v2 targets more aggressive compression, which aligns with the "fluff elimination" theme. The per-document-type ratios in Appendix B provide useful calibration.

### 5. Expanded Ambiguity Protocol

v2 adds two new flag types:
- `[UNDEFINED]` - Entity referenced but never defined
- `[ORPHAN]` - Acronym without context (used in Compaction Review)

**Assessment**: Extends flagging vocabulary to catch entity hygiene issues.

### 6. Frontmatter Streamlining

| Field | v1 | v2 |
|-------|----|----|
| `author` | Required | Omit (uniform) |
| `related` | Required | Omit (use `links` only) |
| `status` | Always | Omit if "draft" |
| `Change Log` | Required | Omit entirely |

**Assessment**: Reduces boilerplate significantly. Frontmatter in v2 carries only signal.

---

## Type-Specific Guidance Changes

### ADR Documents

v2 restructures ADR sections from a single "Decision Record" block to separate sections:

```markdown
# v2 structure
## Decision
{one-line}

## Drivers
{what forced the decision}

## Alternatives and Disposition
{why rejected}

## Consequences
- Positive: {benefits}
- Negative: {trade-offs}
```

**Assessment**: Better separation of concerns. Consequences split (positive/negative) is more actionable.

### Research Findings

v2 replaces the "Evidence Summary" table with:
- Findings (key discoveries)
- Limitations
- Recommendation

**Assessment**: More practical for LLM consumption. The table format in v1 was verbose for documents with few citations.

---

## New Appendices

v2 adds four appendices that function as quick-reference material:

| Appendix | Purpose | Value |
|----------|---------|-------|
| A: Frontmatter Reference | Always/conditional/omit guidance | High - prevents field drift |
| B: Compression Ratios | Per-type targets | Medium - calibration aid |
| C: Failure Modes | Detection + correction | High - operationalizes QA |
| D: Entity Templates | How to add context | High - examples for edge cases |
| E: Temporal Handling | Remove/transform/preserve | High - decision tree for dates |

---

## Parallel Orchestration Enhancements

v2 extends orchestration patterns to handle entity context:

1. **SHARED-CONTEXT.yaml** now includes `entity_definitions` section
2. **Context injection template** adds entity definitions
3. **Reconciliation Report** adds `orphaned_entities` tracking
4. **Anchor + Satellite** instructions include entity awareness

**Assessment**: These changes integrate entity hygiene into the pipeline rather than treating it as a post-hoc fix.

---

## Model Selection Additions

v2 adds one new failure mode and corresponding mitigation:

| Model | New in v2 |
|-------|-----------|
| Sonnet | "Preserves orphaned entities" → Detection: Grep for undefined acronyms |

**Assessment**: Minor but useful addition.

---

## Concerns and Suggestions

> **Note**: All suggestions below have been applied in v2.1.

### 1. Compression Ratio Terminology ✓ APPLIED

The wording around compression ratios could be clearer:

- Quality Checklist says: "Compression ratio is 60-85% of source"
- Output Validation says: "Be 15-40% the length of source"
- Appendix B says: "Target 25%" (which is ~75% compression)

**Recommendation**: Standardize terminology. Use "target output length: X% of source" consistently throughout.

**Resolution**: Quality Checklist now says "Output length is 15-40% of source".

### 2. Human-Oriented Explanations Rule ✓ APPLIED

v2 adds: "Don't explain standard technical vocabulary." This is reasonable but could be over-applied.

**Recommendation**: Add guidance on threshold—domain-specific terms still need definition even if LLMs "know" them, since usage may differ from standard meaning.

**Resolution**: Added clarification: "However, DO preserve definitions for domain-specific terms even if they use common words—'active' may have a corpus-specific meaning that differs from general usage."

### 3. "Scope and Non-Goals" Removal ✓ APPLIED

v2 moves this from required to "omit when redundant." However, scope boundaries are frequently misunderstood.

**Recommendation**: Consider keeping this as optional-but-encouraged rather than omit-by-default.

**Resolution**: Changed to: "'Scope and Non-Goals' is optional but encouraged... err toward inclusion—scope boundaries are frequently misunderstood."

### 4. Evidence and Freshness Removal ✓ APPLIED

For research findings, v2 removes the Evidence and Freshness section. This information is valuable for downstream decision-making.

**Recommendation**: For RF-* documents specifically, preserve evidence tier ratings even without the boilerplate framing.

**Resolution**: Added "Evidence Quality" section to RF-* template with tier ratings. Added explicit PRESERVE directive for evidence tier ratings.

---

## Overall Assessment

| Dimension | v1 | v2 | Change |
|-----------|----|----|--------|
| Fluff handling | Implicit | Explicit rules | ++ |
| Entity hygiene | Absent | Comprehensive | +++ |
| Temporal handling | Absent | Comprehensive | +++ |
| Frontmatter clarity | Verbose | Streamlined | ++ |
| Type-specific guidance | Basic | Refined | + |
| Appendices | None | Extensive | ++ |
| Clarity/parsability | Good | Better | + |

**Verdict**: v2 is a meaningful improvement. The additions address real failure modes observed in practice. The compression ratio language should be clarified, but the substance is sound.

---

## Change Summary

### Added in v2
- Critical Omission Rules (7 rules)
- Entity Reference Rules (3 rules)
- Temporal Reference Handling
- Expanded "What to PRESERVE" (interface contracts, rejected alternatives)
- Expanded "What to COMPRESS" (human-oriented explanations)
- Expanded "What to OMIT" (onboarding context, temporal artifacts, stakeholder prose)
- `[UNDEFINED]` ambiguity flag
- Corpus glossary input parameter
- Appendix A: Frontmatter Field Reference
- Appendix B: Compression Ratio Guidelines
- Appendix C: Common Failure Modes
- Appendix D: Entity Context Templates
- Appendix E: Temporal Reference Handling
- Entity definitions in orchestration patterns
- Orphaned entities in reconciliation report

### Removed in v2
- `author` field (uniform)
- `related` field (redundant with `links`)
- Change Log section
- "Scope and Non-Goals" as required section
- "Evidence and Freshness" as required section

### Modified in v2
- Compression ratio targets (more aggressive)
- ADR section structure (separated concerns)
- Research Findings format (Findings/Limitations/Recommendation)
- Quality checklist (expanded)
- Anti-patterns list (3 new patterns)
- Compaction Review categories (3 new types)
