# LLM View Compaction Verification Report

**Date**: 2026-02-05
**Scope**: First 10 LLM view documents (ADR-01 through ADR-10)
**Standard**: PROMPT-llm-compaction.md v2.1

## Executive Summary

All 10 documents exhibit **systematic non-compliance** with compaction standard v2.1. These documents were compacted before the current standard was finalized and require remediation. The issues are consistent across all documents, indicating a need for batch re-processing rather than individual fixes.

---

## Documents Reviewed

1. `LLM-ADR-01-01-backend-selection.md`
2. `LLM-ADR-02-01-orchestration-selection.md`
3. `LLM-ADR-03-01-memory-selection.md`
4. `LLM-ADR-04-01-documentation-selection.md`
5. `LLM-ADR-05-01-pm-selection.md`
6. `LLM-ADR-06-01-research-tools-selection.md`
7. `LLM-ADR-07-01-widgets-selection.md`
8. `LLM-ADR-08-01-hosting-selection.md`
9. `LLM-ADR-09-01-llm-provider-selection.md`
10. `LLM-ADR-10-01-dev-tooling-selection.md`

---

## Universal Issues (All 10 Documents)

### 1. FLUFF: `author:` Field Included

**Standard Reference**: Appendix A - "Omit Entirely"
> `author` - Uniform across corpus; no signal

**Finding**: All documents include `author: compass-research` on line 9.

**Action**: Remove field from all documents.

---

### 2. FLUFF: `related:` Array Duplicates `links:`

**Standard Reference**: Critical Omission Rule #3
> Use `links:` array only. Do not duplicate in both `related:` and `links:`.

**Finding**: All documents include both `related:` array AND `links:` array with overlapping content.

**Example** (ADR-01-01-LLM):
```yaml
related:
  - ADR-01-01
  - RF-01-01
  - DD-14-01
  - DD-12-01
  - DD-13-01
links:
  - rel: related
    target_id: "RF-01-01"
  # ... (duplicates)
```

**Action**: Remove `related:` array from all frontmatter.

---

### 3. FLUFF: `status:` Field with Non-Signal Values

**Standard Reference**: Appendix A - "Include Only If Non-Default"
> `status` - Include when: Not "draft" (e.g., accepted, deprecated, superseded)

**Finding**:
- ADR-01-01-LLM: `status: accepted` (CORRECT - keep)
- All other 9 documents: `status: proposed` or `status: draft` (INCORRECT - remove)

**Action**: Remove `status:` field from 9 of 10 documents. Keep only in ADR-01-01-LLM.

---

### 4. FLUFF: "Evidence and Freshness" Section Included

**Standard Reference**: Critical Omission Rule #5
> Omit "Evidence and Freshness" boilerplate. If a document has no external citations, do not include a section stating "No external citations required." Staleness is tracked in frontmatter.

**Finding**: All documents include this section with boilerplate content like:
```markdown
## Evidence and Freshness
- Source updated 2026-01-25; staleness marked fresh.
- Evidence grounded in `RF-01-01` with pricing and vendor feature verification.
```

**Action**: Remove section from all documents. The `staleness:` field in frontmatter already captures this.

---

### 5. FLUFF: "Change Log" Section Included

**Standard Reference**: Critical Omission Rule #4
> Omit Change Log for LLM views. The `source_id` and `source_updated` fields capture provenance. A changelog entry saying "LLM view created" adds no information.

**Finding**: All documents include:
```markdown
## Change Log
- 2026-02-03: LLM view created from `ADR-XX-01` with no semantic changes.
```

**Action**: Remove section from all documents.

---

### 6. OMISSION: "Core Invariants" Section Missing

**Standard Reference**: Output Format specification
> ## Core Invariants
> {3-7 bullet points capturing the fundamental truths that MUST NOT be violated. These are the load-bearing walls.}

**Finding**: No documents include this required section.

**Action**: Add Core Invariants section to all documents, extracted from source ADRs.

---

## Document-Specific Issues

### ADR-01-01-LLM: Backend Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| FLUFF | Lines 57-58 | `## Open Questions\n- None.` | Critical Omission Rule #1: "Never output 'Open Questions: None'" |
| ORPHAN | Line 36 | "EFN tool ecosystem" | Entity Reference Rule #1: "Never reference undefined entities" |

**Remediation**:
- Remove Open Questions section entirely
- Replace "EFN tool ecosystem" with "the broader tooling ecosystem" or add context "(EFN, a financial news organization)"

---

### ADR-02-01-LLM: Orchestration Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| TEMPORAL | Line 38 | "2-3 weeks vs 6-10 weeks" | Appendix E: Remove time estimates |

**Remediation**:
- Transform to capability comparison: "significantly faster delivery than custom orchestration"

---

### ADR-03-01-LLM: Memory Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| TEMPORAL | Lines 35, 38, 40, 68, 71 | "Phase 1-2", "Phase 3" | Entity Reference Rule #2: "Resolve or remove temporal references" |

**Remediation**:
- Replace "Phase 1-2 requirements" with "initial planning workflow requirements"
- Replace "Phase 3 enrichment" with "if advanced temporal queries become necessary"

---

### ADR-04-01-LLM: Documentation Selection

No document-specific issues beyond universal issues.

---

### ADR-05-01-LLM: PM Integration Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| TEMPORAL | Line 36 | "Phase 4" | Entity Reference Rule #2 |

**Remediation**:
- Remove "scheduled for Phase 4" or replace with "after core planning workflows are complete"

---

### ADR-06-01-LLM: Research Tools Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| FLUFF | Lines 56-57 | `## Open Questions\n- None.` | Critical Omission Rule #1 |
| TEMPORAL | Line 36 | "Phase 1 costs", "Phase 1 and Phase 3 budget" | Entity Reference Rule #2 |

**Remediation**:
- Remove Open Questions section
- Replace phase references with budget tier descriptions

---

### ADR-07-01-LLM: Widget Selection

No document-specific issues beyond universal issues.

---

### ADR-08-01-LLM: Hosting Selection

No document-specific issues beyond universal issues.

---

### ADR-09-01-LLM: LLM Provider Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| TEMPORAL | Line 30 | "Phase 1 and Phase 3 budgets" | Entity Reference Rule #2 |

**Remediation**:
- Replace with "initial and growth budget constraints"

---

### ADR-10-01-LLM: Dev Tooling Selection

| Issue Type | Location | Content | Standard Reference |
|------------|----------|---------|-------------------|
| TEMPORAL | Line 33 | "post-MVP" | Entity Reference Rule #2 |

**Remediation**:
- Replace with "deferred until core functionality is stable"

---

## Summary Statistics

| Issue Category | Count | Documents Affected |
|----------------|-------|-------------------|
| `author:` field | 10 | All |
| `related:` array | 10 | All |
| `status:` non-signal | 9 | All except ADR-01-01 |
| Evidence and Freshness section | 10 | All |
| Change Log section | 10 | All |
| Core Invariants missing | 10 | All |
| Open Questions: None | 2 | ADR-01-01, ADR-06-01 |
| Orphaned entity (EFN) | 1 | ADR-01-01 |
| Temporal references | 5 | ADR-02, 03, 05, 06, 09, 10 |

**Total Issues**: 67 individual violations across 10 documents

---

## Recommended Remediation Approach

Given the systematic nature of these issues, recommend **batch re-compaction** using PROMPT-llm-compaction.md v2.1 with the following approach:

1. **Pattern**: Use Anchor + Satellite pattern from orchestration section
2. **Context injection**: Build shared context from SYS-00, DD-13, DD-20 before re-compacting
3. **Entity definitions**: Pre-define "EFN" and other corpus entities in shared context
4. **Validation**: Apply Haiku validation pass for schema compliance after re-compaction

### Priority Order

1. **HIGH**: Remove fluff sections (Change Log, Evidence and Freshness, empty Open Questions)
2. **HIGH**: Remove redundant frontmatter (`author:`, `related:`, non-signal `status:`)
3. **MEDIUM**: Add Core Invariants sections
4. **MEDIUM**: Transform temporal references to dependency/capability descriptions
5. **LOW**: Resolve orphaned entity references

---

## Verification Checklist Status

Per Quality Checklist in standard:

- [ ] All MUST/SHOULD/MAY statements extracted - **PASS** (present in Canonical Statements)
- [ ] All enumerations complete - **N/A** (ADRs, not definitions)
- [ ] All cross-references use consistent `{DOC-ID}` format - **PASS**
- [x] No empty sections remain - **FAIL** (Open Questions: None in 2 docs)
- [x] No undefined entities referenced without context - **FAIL** (EFN in 1 doc)
- [x] No calendar dates or time estimates remain - **FAIL** (time estimates in 1 doc)
- [x] No redundant glossary entries - **N/A** (no glossaries in ADRs)
- [x] Open Questions section omitted if empty - **FAIL** (2 docs)
- [x] Change Log section omitted entirely - **FAIL** (10 docs)
- [x] Status field omitted if "draft" - **FAIL** (9 docs)
- [x] Author field omitted - **FAIL** (10 docs)
- [ ] Ambiguities flagged, not resolved - **PASS**
- [ ] Output length is 15-40% of source - **NOT VERIFIED** (requires source comparison)
- [ ] Exception cases captured - **PASS**
- [x] Frontmatter links array populated - **PASS** (but redundant `related:`)
- [ ] Document is self-contained - **PARTIAL** (EFN reference breaks this)

**Overall Compliance**: ~60% (significant remediation required)
