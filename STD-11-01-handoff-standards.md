---
id: STD-11-01
type: standard
area: 11-handoff-schema
title: Handoff Bundle Standard
status: draft
created: 2026-01-28
updated: 2026-01-28
author: compass-research
summary: Enforceable standard for handoff bundle creation, validation, and quality assurance
tags: [handoff, standard, validation, compliance, quality]
related:
  - DD-11-01
  - DD-13-01
  - DD-14-01
  - STD-20-01
companion: DD-11-01
enforcement: Pre-handoff validation checklist
---

# Handoff Bundle Standard

## Document Purpose

This document specifies the enforceable requirements for creating, validating, and maintaining handoff bundles. It is the compliance companion to DD-11-01 (Handoff Bundle Schema Definition).

**How to use this document**:

1. When creating handoff bundles, use the checklists to ensure completeness
2. When reviewing bundles, use the quality criteria to assess readiness
3. When bundles fail validation, reference the common errors section
4. When adapting bundles for specific platforms, verify minimum requirements are met

**Relationship to DD-11-01**: DD-11-01 defines what handoff bundles contain and why. This document specifies how to verify bundles meet those definitions and what "good enough" looks like.

---

## Part 1: Minimum Requirements

### 1.1 Absolute Requirements

Every handoff bundle MUST satisfy these requirements. Bundles failing any of these are not valid for handoff.

**Metadata Requirements**:

| Requirement | Check | Failure Impact |
|-------------|-------|----------------|
| `id` field matches `HANDOFF-{project}-{version}` pattern | Regex validation | Bundle cannot be tracked |
| `type` field equals `handoff` | Exact match | Bundle won't be recognized |
| `bundle_version` is "1.0" | Exact match | Schema validation fails |
| `source_specs` contains at least one ID | Non-empty array | No traceability to planning |
| `archetype` matches DD-14-01 catalog | Enum validation | Reliability requirements unknown |
| `reliability_tier` is 1-5 | Range validation | Cannot determine standards |
| `created` and `updated` are valid dates | ISO 8601 format | Cannot track currency |

**Section Requirements**:

| Section | Minimum Content | Failure Impact |
|---------|-----------------|----------------|
| Overview | Vision statement present | Implementation lacks direction |
| Overview | At least 1 success metric | Cannot verify success |
| Overview | At least 1 stakeholder | No accountability |
| Requirements | At least 3 in-scope requirements | Scope undefined |
| Requirements | At least 1 out-of-scope | Boundaries unclear |
| Requirements | At least 1 constraint | Constraints unknown |
| Decision Ledger | At least 1 decision with rationale | No context for choices |
| Architecture | At least 1 component | Structure unknown |
| Architecture | Diagram present | No visual reference |
| Acceptance | At least 3 criteria | "Done" undefined |
| Acceptance | All criteria have verification | Cannot test completion |
| Work Breakdown | At least 1 phase | No execution path |
| Work Breakdown | At least 1 task per phase | Nothing to implement |
| Context Pack | Freshness notice present | Staleness undetectable |

### 1.2 Conditional Requirements

These requirements apply based on bundle characteristics:

**For bundles with reliability_tier 1 or 2**:

- [ ] Architecture section includes failover/redundancy considerations
- [ ] Acceptance criteria include reliability-specific tests
- [ ] Work breakdown includes testing/verification phase
- [ ] Stakeholders include operations/on-call contact

**For bundles with multiple phases**:

- [ ] Phase dependencies are documented
- [ ] Exit criteria defined for each phase
- [ ] Dependency diagram present

**For bundles targeting specific platforms**:

- [ ] `target_platform` field is set
- [ ] Platform-specific formatting applied
- [ ] Platform limitations noted if any

**For bundles with external integrations**:

- [ ] Interfaces section lists all integration points
- [ ] Data flows document cross-system communication
- [ ] Constraints include integration dependencies

---

## Part 2: Quality Criteria

Beyond minimum requirements, bundles should meet quality standards that ensure implementation success.

### 2.1 Vision Statement Quality

**Good vision statements**:

- Fit in 1-3 sentences
- Explain what AND why
- Are understandable without prior context
- Include concrete benefit

**Quality check questions**:

- Can someone unfamiliar with the project understand what we're building?
- Is the "why" clear, not just the "what"?
- Is there a concrete outcome, not just activity?

**Examples**:

| Quality | Example | Issue |
|---------|---------|-------|
| ❌ Poor | "Build a data tool" | No specifics, no why |
| ⚠️ Okay | "Build a tool that converts CSV to graphics" | What but not why |
| ✅ Good | "Build a tool that converts CSV financial data to broadcast-ready graphics in under 30 seconds, enabling producers to display current market data during live broadcasts without manual graphics creation" | What, why, and concrete benefit |

### 2.2 Requirements Quality

**Good requirements**:

- Use consistent ID format (REQ-NNN)
- Are specific enough to implement
- Have clear priority
- Include rationale

**Quality check questions**:

- Could an implementation agent start work without asking clarifying questions?
- Is there ambiguity about what "done" looks like for each requirement?
- Are priorities justified, not arbitrary?

**Examples**:

| Quality | Example | Issue |
|---------|---------|-------|
| ❌ Poor | "Support various file formats" | What formats? Various how? |
| ⚠️ Okay | "Support CSV, Excel, PDF" | Missing acceptance threshold |
| ✅ Good | "[REQ-003] Accept CSV files up to 10MB with automatic delimiter detection. Priority: must-have. Rationale: CSV is 60% of producer uploads." | Specific, bounded, justified |

### 2.3 Acceptance Criteria Quality

**Good acceptance criteria**:

- Are testable (someone could write a test for them)
- Have specific thresholds (numbers, not "fast" or "reliable")
- Include verification method
- Cover functional AND non-functional requirements

**Quality check questions**:

- Can each criterion be verified objectively?
- Would two people agree on whether a criterion passes?
- Are thresholds justified by requirements?

**Examples**:

| Quality | Example | Issue |
|---------|---------|-------|
| ❌ Poor | "System is fast" | Not testable |
| ⚠️ Okay | "System responds quickly to user input" | Subjective |
| ✅ Good | "[AC-003] Data-to-graphic rendering completes in <30 seconds for datasets up to 1000 rows. Verification: Timed test with standard dataset." | Testable, threshold, method |

### 2.4 Task Quality

**Good tasks**:

- Are atomic (completable in 1-4 hours)
- Have clear inputs and outputs
- Have defined acceptance criteria
- Don't require additional breakdown

**Quality check questions**:

- Could an implementation agent start this task without planning?
- Is it clear when the task is complete?
- Does completing this task produce something tangible?

**Examples**:

| Quality | Example | Issue |
|---------|---------|-------|
| ❌ Poor | "Build the backend" | Too large, requires breakdown |
| ⚠️ Okay | "Create the API" | Still ambiguous |
| ✅ Good | "[TASK-002] Create POST /api/upload endpoint accepting multipart file upload. Inputs: Project skeleton from TASK-001. Outputs: Working endpoint. Acceptance: Can upload 500MB file via curl." | Specific, bounded, testable |

### 2.5 Architecture Quality by Tier

Different reliability tiers require different architecture depth:

| Tier | Minimum Architecture | Additional Expectations |
|------|---------------------|------------------------|
| 1 (Broadcast-critical) | Full component diagram, all interfaces, data flows, failover strategy | Redundancy design, recovery procedures, pre-broadcast checklist |
| 2 (Production pipeline) | Component diagram, key interfaces, data flows | Queue/retry strategy, monitoring hooks |
| 3 (Publishing pipeline) | Component diagram, external interfaces | Error handling approach |
| 4 (Internal utility) | Basic component list, primary interfaces | Sufficient for complexity |
| 5 (Exploratory) | Conceptual sketch acceptable | Minimal formality expected |

---

## Part 3: Pre-Handoff Validation Checklist

Use this checklist before declaring a handoff bundle ready.

### 3.1 Completeness Checklist

**Metadata**:
- [ ] All required frontmatter fields present
- [ ] `bundle_version` is "1.0"
- [ ] `source_specs` lists specifications
- [ ] `archetype` matches DD-14-01 catalog
- [ ] `reliability_tier` is appropriate (1-5)
- [ ] `source_planning_sessions` documented

**Overview Section**:
- [ ] Vision statement present (1-3 sentences)
- [ ] At least one success metric with measurement method
- [ ] At least one stakeholder with role and interest
- [ ] Project context references archetype

**Requirements Section**:
- [ ] At least three in-scope requirements with IDs
- [ ] All requirements have priority (must/should/nice-to-have)
- [ ] All requirements have rationale
- [ ] At least one out-of-scope item with reason
- [ ] At least one constraint documented

**Decision Ledger**:
- [ ] At least one active decision with rationale
- [ ] Rejected alternatives section present (may be empty)
- [ ] Deferred decisions section present (may be empty)
- [ ] ADR links provided where formal ADRs exist

**Architecture Sketch**:
- [ ] At least one component with purpose
- [ ] Component diagram present (ASCII or image)
- [ ] Interfaces documented for multi-component systems
- [ ] Data flows documented if components exchange data

**Acceptance Criteria**:
- [ ] At least three acceptance criteria with unique IDs
- [ ] All criteria have verification method
- [ ] Non-functional criteria have measurable targets
- [ ] At least one verification phase in plan

**Work Breakdown**:
- [ ] At least one phase with goal
- [ ] Each phase has at least one task
- [ ] All tasks have inputs, outputs, acceptance
- [ ] Dependencies documented for multi-phase work
- [ ] Risk factors identified (at least one for Tier 1-3)

**Context Pack**:
- [ ] At least one source cited (non-trivial bundles)
- [ ] Citations follow STD-20-01 format
- [ ] Freshness notice with creation/validation dates
- [ ] Research artifacts linked if applicable

### 3.2 Quality Checklist

- [ ] Vision statement understandable without prior context
- [ ] Requirements specific enough to implement
- [ ] Acceptance criteria actually testable
- [ ] Tasks atomic (1-4 hours each)
- [ ] Architecture depth matches reliability tier
- [ ] Evidence supports key decisions

### 3.3 Tier-Specific Checks

**Tier 1 (Broadcast-critical) additional checks**:
- [ ] Failover/redundancy documented
- [ ] Pre-broadcast verification procedure included
- [ ] Operations contact identified
- [ ] Recovery time objective stated

**Tier 2 (Production pipeline) additional checks**:
- [ ] Retry/queue strategy documented
- [ ] Monitoring approach identified
- [ ] Graceful degradation considered

**Tier 3 (Publishing pipeline) additional checks**:
- [ ] External platform dependencies noted
- [ ] Fallback procedures identified

---

## Part 4: Common Errors and Corrections

### 4.1 Metadata Errors

**Error**: Missing `source_specs`

```yaml
# ❌ Wrong
source_specs: []

# ✅ Correct
source_specs:
  - SPEC-broadcast-viz-001
```

**Why it matters**: Without source specs, there's no traceability to the planning that produced this bundle.

---

**Error**: Invalid archetype

```yaml
# ❌ Wrong
archetype: "broadcast tool"

# ✅ Correct (use exact values from DD-14-01)
archetype: broadcast-critical
```

**Valid values**: `broadcast-critical`, `production-pipeline`, `publishing-pipeline`, `internal-utility`, `analytics-intelligence`, `exploratory`

---

**Error**: Reliability tier as string

```yaml
# ❌ Wrong
reliability_tier: "Tier 1"

# ✅ Correct
reliability_tier: 1
```

**Valid values**: Integer 1-5

---

### 4.2 Content Errors

**Error**: Vague requirements without IDs

```markdown
❌ Wrong:
- Support file uploads
- Handle different formats
- Show progress

✅ Correct:
- [REQ-001] Accept CSV file uploads up to 10MB
  - Priority: must-have
  - Rationale: CSV is primary source format for 80% of use cases
```

---

**Error**: Untestable acceptance criteria

```markdown
❌ Wrong:
- System should be fast
- Interface should be intuitive
- Errors handled gracefully

✅ Correct:
- [AC-001] File processing completes in <10 seconds for files under 5MB
  - Verification: Timed tests with sample files at 1MB, 3MB, 5MB
  
- [AC-002] User can complete primary workflow without documentation
  - Verification: Usability test with 3 users unfamiliar with tool
  
- [AC-003] Invalid file upload displays error message within 2 seconds
  - Verification: Test with corrupted file; verify message text
```

---

**Error**: Tasks too large

```markdown
❌ Wrong:
- [ ] Build the data processing module

✅ Correct:
- [ ] [TASK-001] Create CSV parser extracting columns matching template schema
  - Inputs: Template schema definition
  - Outputs: Parser function with tests
  - Acceptance: Parses sample CSV correctly
  
- [ ] [TASK-002] Create validation layer checking data types
  - Inputs: TASK-001 parser
  - Outputs: Validator returning typed errors
  - Acceptance: Rejects invalid data with clear messages
```

---

**Error**: Missing verification methods

```markdown
❌ Wrong:
- [AC-005] API returns correct data format

✅ Correct:
- [AC-005] API returns JSON with `data`, `meta`, and `errors` fields per STD-03-01
  - Verification: Schema validation test against API responses
```

---

### 4.3 Citation Errors

**Error**: Missing tier/reliability prefix

```markdown
❌ Wrong:
1. FFmpeg Documentation. https://ffmpeg.org/docs

✅ Correct:
1. **[T1/S1]** FFmpeg Project. "FFmpeg Documentation". 
   Retrieved 2026-01-25. https://ffmpeg.org/documentation.html
```

---

**Error**: Missing retrieval date

```markdown
❌ Wrong:
1. **[T1/S1]** AWS. "Lambda Limits". https://docs.aws.amazon.com/lambda/limits

✅ Correct:
1. **[T1/S1]** AWS. "Lambda Quotas and Limits". 
   Retrieved 2026-01-25. https://docs.aws.amazon.com/lambda/limits
```

---

**Error**: Over-rating community sources

```markdown
❌ Wrong (Stack Overflow is not T1/S1):
1. **[T1/S1]** Stack Overflow. "Best practices for X". https://stackoverflow.com/...

✅ Correct:
1. **[T2/S2]** Stack Overflow. "Best practices for X" (Score: 156, Accepted). 
   Posted 2024-03-15. Retrieved 2026-01-25. https://stackoverflow.com/...
   Note: Community consensus; verify against current official docs.
```

---

## Part 5: Validation Automation

### 5.1 Automated Checks

These checks can be automated in CI/CD pipelines:

**Frontmatter validation**:
```javascript
// Pseudocode for frontmatter validation
const requiredFields = [
  'id', 'type', 'title', 'status', 'created', 'updated',
  'author', 'summary', 'tags', 'related',
  'bundle_version', 'source_specs', 'archetype', 'reliability_tier'
];

const validArchetypes = [
  'broadcast-critical', 'production-pipeline', 'publishing-pipeline',
  'internal-utility', 'analytics-intelligence', 'exploratory'
];

function validateFrontmatter(yaml) {
  // Check required fields exist
  for (const field of requiredFields) {
    if (!yaml[field]) return { valid: false, error: `Missing ${field}` };
  }
  
  // Check specific field values
  if (yaml.type !== 'handoff') return { valid: false, error: 'type must be handoff' };
  if (yaml.bundle_version !== '1.0') return { valid: false, error: 'bundle_version must be 1.0' };
  if (!validArchetypes.includes(yaml.archetype)) return { valid: false, error: 'Invalid archetype' };
  if (yaml.reliability_tier < 1 || yaml.reliability_tier > 5) return { valid: false, error: 'reliability_tier must be 1-5' };
  if (!Array.isArray(yaml.source_specs) || yaml.source_specs.length === 0) {
    return { valid: false, error: 'source_specs must have at least one entry' };
  }
  
  return { valid: true };
}
```

**Section presence validation**:
```javascript
const requiredSections = [
  '## Overview',
  '### Vision Statement',
  '### Success Metrics',
  '### Stakeholders',
  '## Requirements',
  '### Scope',
  '## Decision Ledger',
  '## Architecture Sketch',
  '## Acceptance Criteria',
  '## Work Breakdown',
  '## Context Pack',
  '### Freshness Notice'
];

function validateSections(markdown) {
  const missing = [];
  for (const section of requiredSections) {
    if (!markdown.includes(section)) {
      missing.push(section);
    }
  }
  return missing.length === 0 
    ? { valid: true } 
    : { valid: false, missing };
}
```

**ID format validation**:
```javascript
const idPatterns = {
  requirement: /\[REQ-\d{3}\]/g,
  outOfScope: /\[OUT-\d{3}\]/g,
  acceptance: /\[AC-(?:NF-)?\d{3}\]/g,
  task: /\[TASK-\d{3}\]/g
};

function validateIds(markdown) {
  const errors = [];
  
  // Check requirements section has properly formatted IDs
  const reqSection = extractSection(markdown, 'Requirements');
  if (!idPatterns.requirement.test(reqSection)) {
    errors.push('Requirements missing properly formatted IDs (REQ-NNN)');
  }
  
  // Similar checks for other sections...
  return errors;
}
```

### 5.2 Manual Review Checklist

Some quality aspects require human judgment:

- [ ] Vision statement is understandable to someone without context
- [ ] Requirements are specific enough to implement without clarification
- [ ] Acceptance criteria are actually testable by the proposed method
- [ ] Tasks are appropriately sized (1-4 hours)
- [ ] Architecture depth matches project complexity and tier
- [ ] Risk factors are realistic, not boilerplate

---

## Part 6: Review and Approval

### 6.1 Review Workflow

```
Bundle Created
     │
     ├──> Automated Validation
     │         │
     │         ├── Pass ──> Human Review
     │         │               │
     │         │               ├── Approved ──> Status: active
     │         │               │
     │         │               └── Changes Requested ──> Revise
     │         │                          │
     │         │                          └──> (back to Automated)
     │         │
     │         └── Fail ──> Fix Issues
     │                        │
     │                        └──> (back to Automated)
```

### 6.2 Approval Authority

| Bundle Tier | Reviewer Requirement |
|-------------|---------------------|
| Tier 1-2 | Senior builder + stakeholder |
| Tier 3-4 | Any builder |
| Tier 5 | Self-review acceptable |

### 6.3 Approval Criteria

Approver should verify:

- [ ] Automated validation passes
- [ ] Quality checklist satisfied
- [ ] Tier-appropriate depth achieved
- [ ] No blocking open questions
- [ ] Stakeholders have reviewed success metrics and acceptance criteria

---

## Part 7: Maintenance and Updates

### 7.1 When to Update a Bundle

Bundles should be updated when:

- Requirements change before implementation begins
- Significant decisions change during implementation
- New constraints are discovered
- Phase completion reveals needed adjustments

Bundles should NOT be updated when:

- Minor implementation details vary (capture as deltas instead)
- Bug fixes don't affect scope or architecture
- Implementation completes normally

### 7.2 Versioning

When updating bundles:

1. Increment version in ID: `HANDOFF-project-001` → `HANDOFF-project-002`
2. Keep old version (don't delete)
3. Link new version to old in `related` field
4. Document what changed and why

### 7.3 Staleness Handling

Bundles older than their expiration date (or 90 days if not set) should be reviewed before use:

- [ ] Are source specifications still current?
- [ ] Have cited sources changed?
- [ ] Are constraints still valid?
- [ ] Have related decisions changed?

If review reveals significant changes, create a new bundle version.

---

## Appendix A: Quick Reference Card

### Required Frontmatter Fields

```yaml
id: HANDOFF-{project}-{version}
type: handoff
bundle_version: "1.0"
source_specs: [SPEC-xxx]
archetype: {DD-14-01 value}
reliability_tier: {1-5}
```

### Required Sections (minimum content)

| Section | Minimum |
|---------|---------|
| Overview | Vision + 1 metric + 1 stakeholder |
| Requirements | 3 in-scope + 1 out-of-scope + 1 constraint |
| Decision Ledger | 1 decision with rationale |
| Architecture | 1 component + diagram |
| Acceptance | 3 criteria with verification |
| Work Breakdown | 1 phase + 1 task |
| Context Pack | Freshness notice |

### ID Formats

```
REQ-NNN     # Requirements
OUT-NNN     # Out-of-scope
AC-NNN      # Acceptance criteria
AC-NF-NNN   # Non-functional acceptance criteria
TASK-NNN    # Tasks
DEC-NNN     # Inline decisions (no formal ADR)
```

### Valid Archetypes

```
broadcast-critical
production-pipeline
publishing-pipeline
internal-utility
analytics-intelligence
exploratory
```

---

## Appendix B: Related Documents

- **DD-11-01**: Handoff Bundle Schema Definition (companion definition document)
- **DD-12-01**: Repository Structure (bundle storage and naming)
- **DD-13-01**: Artifact Taxonomy (handoff as artifact type)
- **DD-14-01**: EFN Ecosystem (archetypes and reliability tiers)
- **DD-18-01**: Questioning Arc (how planning produces bundle content)
- **STD-20-01**: Evidence Standards (citation format for context packs)

---

*End of Handoff Bundle Standard (STD-11-01)*
