# LLM View Compaction Remediation Task List

**Generated**: 2026-02-05
**Standard**: PROMPT-llm-compaction.md v2.1
**Total Documents**: 37
**Total Tasks**: 37

---

## Usage Instructions

Each numbered task is atomic and can be processed by a parallel LLM agent. Tasks are independent and can run concurrently.

**Agent Instructions**: For each task:
1. Read the specified LLM view file
2. Apply ALL listed fixes
3. Save the corrected file
4. Report completion

**Fix Types**:
- `REMOVE_FIELD`: Delete the specified frontmatter field entirely
- `REMOVE_SECTION`: Delete the entire section (header + content)
- `ADD_SECTION`: Add the specified section with extracted content
- `TRANSFORM_TEMPORAL`: Convert phase/date references to capability/dependency language
- `ADD_ENTITY_CONTEXT`: Add context for orphaned entity references
- `KEEP_STATUS`: Exception - keep status field (signal value)

---

## Universal Fixes (Apply to ALL documents unless noted)

These fixes apply to every document. Document-specific tasks list additional fixes.

| Fix ID | Type | Target | Action |
|--------|------|--------|--------|
| U1 | REMOVE_FIELD | `author:` | Delete `author: compass-research` line from frontmatter |
| U2 | REMOVE_FIELD | `related:` | Delete entire `related:` array from frontmatter |
| U3 | REMOVE_FIELD | `status:` | Delete `status: draft` or `status: proposed` (UNLESS noted as signal value) |
| U4 | REMOVE_SECTION | `## Evidence and Freshness` | Delete section entirely |
| U5 | REMOVE_SECTION | `## Change Log` | Delete section entirely |
| U6 | REMOVE_SECTION | `## Open Questions` | Delete section IF content is only "None." or "- None." |

---

## Task List by Document Type

### ADR Documents (10 tasks)

#### Task 1: LLM-ADR-01-01-backend-selection.md

**File**: `llm/LLM-ADR-01-01-backend-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: **SKIP** - `status: accepted` is a signal value, KEEP IT
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Core Invariants" section after Dependencies:
  ```markdown
  ## Core Invariants
  - Backend platform must be Convex; no alternative without new ADR.
  - LLM-native development patterns are required, not optional.
  - Vendor lock-in is an accepted trade-off; reversal requires migration plan.
  ```
- ADD_ENTITY_CONTEXT: Replace "EFN tool ecosystem" with "the broader tooling ecosystem" OR add "(EFN, a financial news organization)" after first EFN reference

---

#### Task 2: LLM-ADR-02-01-orchestration-selection.md

**File**: `llm/LLM-ADR-02-01-orchestration-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Orchestration must support suspend/resume and branching.
  - Structured outputs are mandatory for widget generation.
  - Fallback to AI SDK + XState must remain viable.
  ```
- TRANSFORM_TEMPORAL: Replace "2-3 weeks vs 6-10 weeks" with "significantly faster delivery than custom orchestration"

---

#### Task 3: LLM-ADR-03-01-memory-selection.md

**File**: `llm/LLM-ADR-03-01-memory-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Memory must live within Convex for initial implementation.
  - Namespace isolation prevents cross-layer data leakage.
  - External services require documented justification.
  ```
- TRANSFORM_TEMPORAL: Replace all "Phase 1-2" with "initial planning workflow requirements"
- TRANSFORM_TEMPORAL: Replace all "Phase 3" with "if advanced temporal queries become necessary"
- TRANSFORM_TEMPORAL: Replace "$10-30/month vs $100-400/month" cost comparisons - KEEP (these are constraints, not timelines)

---

#### Task 4: LLM-ADR-04-01-documentation-selection.md

**File**: `llm/LLM-ADR-04-01-documentation-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - YAML frontmatter must be preserved without loss.
  - Wiki-links and backlinks are required for navigation.
  - MCP access is mandatory for LLM retrieval.
  ```

---

#### Task 5: LLM-ADR-05-01-pm-selection.md

**File**: `llm/LLM-ADR-05-01-pm-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - PM integration must follow DD-17/STD-17 patterns.
  - Secondary users must not require PM accounts for intake.
  - GitHub is the defined fallback if Linear is infeasible.
  ```
- TRANSFORM_TEMPORAL: Remove "Phase 4" reference or replace with "after core planning workflows are complete"

---

#### Task 6: LLM-ADR-06-01-research-tools-selection.md

**File**: `llm/LLM-ADR-06-01-research-tools-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Evidence outputs must transform to DD-20/STD-20 citation format.
  - Tool selection must fit budget constraints.
  - Version-specific documentation coverage is required.
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 1 costs" with "initial budget constraints"
- TRANSFORM_TEMPORAL: Replace "Phase 1 and Phase 3 budget constraints" with "budget constraints across growth stages"

---

#### Task 7: LLM-ADR-07-01-widgets-selection.md

**File**: `llm/LLM-ADR-07-01-widgets-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Widget rendering must support streaming and schema-driven specs.
  - Custom components required where C1 lacks coverage.
  - Thesys C1 is the primary layer; shadcn/ui fills gaps.
  ```

---

#### Task 8: LLM-ADR-08-01-hosting-selection.md

**File**: `llm/LLM-ADR-08-01-hosting-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Preview deployments must have isolated Convex backends.
  - Deployment workflows must be low-configuration.
  - Convex Marketplace integration is required.
  ```

---

#### Task 9: LLM-ADR-09-01-llm-provider-selection.md

**File**: `llm/LLM-ADR-09-01-llm-provider-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Architecture must remain provider-agnostic with fallbacks.
  - Planning tasks require frontier-capable models.
  - Budget models with weak compliance are not acceptable.
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 1 and Phase 3 budgets" with "initial and growth budget constraints"

---

#### Task 10: LLM-ADR-10-01-dev-tooling-selection.md

**File**: `llm/LLM-ADR-10-01-dev-tooling-selection.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: proposed` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- ADD_SECTION: Add "Core Invariants" section:
  ```markdown
  ## Core Invariants
  - Testing must use Vitest with convex-test.
  - Biome is the single linting/formatting tool.
  - CI validates only; deployment is Vercel-managed.
  ```
- TRANSFORM_TEMPORAL: Replace "post-MVP" with "deferred until core functionality is stable"

---

### DD Documents (9 tasks)

#### Task 11: LLM-DD-11-01-handoff-schema.md

**File**: `llm/LLM-DD-11-01-handoff-schema.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 12: LLM-DD-12-01-repository-definitions.md

**File**: `llm/LLM-DD-12-01-repository-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 13: LLM-DD-13-01-artifacts-definitions.md

**File**: `llm/LLM-DD-13-01-artifacts-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section (NOTE: this one has substantive content about Document ID Format addition - KEEP the Document ID Format section content but REMOVE the Change Log section header and boilerplate)
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 14: LLM-DD-14-01-ecosystem-definitions.md

**File**: `llm/LLM-DD-14-01-ecosystem-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: "EFN" is defined in this document's title/area - acceptable
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 15: LLM-DD-15-01-governance-definitions.md

**File**: `llm/LLM-DD-15-01-governance-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 16: LLM-DD-17-01-integration-definitions.md

**File**: `llm/LLM-DD-17-01-integration-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 17: LLM-DD-18-01-questioning-arc.md

**File**: `llm/LLM-DD-18-01-questioning-arc.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 18: LLM-DD-19-01-widget-schema.md

**File**: `llm/LLM-DD-19-01-widget-schema.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

#### Task 19: LLM-DD-20-01-evidence-definitions.md

**File**: `llm/LLM-DD-20-01-evidence-definitions.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

### RF Documents (10 tasks)

#### Task 20: LLM-RF-01-01-backend-findings.md

**File**: `llm/LLM-RF-01-01-backend-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section after Findings (required for RF-*):
  ```markdown
  ## Evidence Quality
  - Vendor documentation: T1/S1 (official sources)
  - Pricing data: T1/S2 (verified January 2026, subject to change)
  - Community assessments: T3/S2 (forums and reports)
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 3 scale" with "growth-stage scale"

---

#### Task 21: LLM-RF-02-01-orchestration-findings.md

**File**: `llm/LLM-RF-02-01-orchestration-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Vendor documentation: T1/S1 (official sources)
  - Framework comparisons: T2/S2 (based on docs and community reports)
  - TypeScript assessments: T3/S2 (community reports, not benchmarked)
  ```
- TRANSFORM_TEMPORAL: Replace "2-3 week integration versus 6-10 weeks" with "significantly faster integration than custom orchestration"

---

#### Task 22: LLM-RF-03-01-memory-findings.md

**File**: `llm/LLM-RF-03-01-memory-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- NOTE: "Open Questions" has substantive content - KEEP
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Vendor documentation: T1/S1 (official sources)
  - Pricing estimates: T2/S2 (verified January 2026)
  - Self-hosted cost estimates: T3/S3 (estimates based on similar deployments)
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 1-2" with "initial implementation"
- TRANSFORM_TEMPORAL: Replace "Phase 3" with "advanced capability stage"

---

#### Task 23: LLM-RF-04-01-documentation-findings.md

**File**: `llm/LLM-RF-04-01-documentation-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Platform documentation: T1/S1 (official sources)
  - Feature comparisons: T2/S2 (based on documentation review)
  - Collaboration assessments: T3/S3 (not independently verified)
  ```

---

#### Task 24: LLM-RF-05-01-pm-findings.md

**File**: `llm/LLM-RF-05-01-pm-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - API documentation: T1/S1 (official sources)
  - Webhook reliability: T2/S2 (based on documentation and community reports)
  - Pricing data: T1/S2 (verified February 2026)
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 4 integration timeline" with "integration scheduled after core planning workflows"

---

#### Task 25: LLM-RF-06-01-research-tools-findings.md

**File**: `llm/LLM-RF-06-01-research-tools-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Tool documentation: T1/S1 (official sources)
  - MCP server availability: T2/S2 (verified against registries)
  - Coverage assessments: T3/S2 (based on documentation, not exhaustive testing)
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 1 and Phase 3 budgets" with "budget constraints across implementation stages"

---

#### Task 26: LLM-RF-07-01-widgets-findings.md

**File**: `llm/LLM-RF-07-01-widgets-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Library documentation: T1/S1 (official sources)
  - Integration assessments: T2/S2 (based on documentation review)
  - Custom component estimates: T3/S3 (based on similar projects)
  ```

---

#### Task 27: LLM-RF-08-01-hosting-findings.md

**File**: `llm/LLM-RF-08-01-hosting-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Platform documentation: T1/S1 (official sources)
  - Integration quality: T2/S2 (based on Convex Marketplace verification)
  - Pricing data: T1/S2 (verified January 2026)
  ```

---

#### Task 28: LLM-RF-09-01-llm-provider-findings.md

**File**: `llm/LLM-RF-09-01-llm-provider-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Provider documentation: T1/S1 (official sources)
  - Pricing data: T1/S2 (verified January 2026, subject to frequent change)
  - Model capability assessments: T2/S2 (based on benchmarks and documentation)
  ```
- TRANSFORM_TEMPORAL: Replace "Phase 3 scale" with "growth-stage scale"

---

#### Task 29: LLM-RF-10-01-dev-tooling-findings.md

**File**: `llm/LLM-RF-10-01-dev-tooling-findings.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- ADD_SECTION: Add "Evidence Quality" section:
  ```markdown
  ## Evidence Quality
  - Tool documentation: T1/S1 (official sources)
  - Ecosystem assessments: T2/S2 (based on community adoption)
  - LLM familiarity claims: T3/S3 (subjective, based on training data assumptions)
  ```

---

### STD Documents (7 tasks)

#### Task 30: LLM-STD-11-01-handoff-standards.md

**File**: `llm/LLM-STD-11-01-handoff-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 31: LLM-STD-14-01-ecosystem-standards.md

**File**: `llm/LLM-STD-14-01-ecosystem-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 32: LLM-STD-15-01-governance-standards.md

**File**: `llm/LLM-STD-15-01-governance-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 33: LLM-STD-17-01-integration-standards.md

**File**: `llm/LLM-STD-17-01-integration-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 34: LLM-STD-18-01-questioning-arc-standards.md

**File**: `llm/LLM-STD-18-01-questioning-arc-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 35: LLM-STD-19-01-widget-schema-standards.md

**File**: `llm/LLM-STD-19-01-widget-schema-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

#### Task 36: LLM-STD-20-01-evidence-standards.md

**File**: `llm/LLM-STD-20-01-evidence-standards.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: Remove `status: draft` field
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Enforcement and Compliance Checklist already present - KEEP

---

### SYS Document (1 task)

#### Task 37: LLM-SYS-00-system-definition.md

**File**: `llm/LLM-SYS-00-system-definition.md`

**Fixes**:
- U1: Remove `author:` field
- U2: Remove `related:` array
- U3: **SKIP** - `status: active` is a signal value, KEEP IT
- U4: Remove "Evidence and Freshness" section
- U5: Remove "Change Log" section (NOTE: has substantive User Role addition - content is already in body, remove section)
- U6: Remove "Open Questions" section (contains "None.")
- NOTE: Core Invariants and Glossary Snapshot already present - KEEP

---

## Summary Statistics

| Document Type | Count | Core Invariants Status | Special Notes |
|---------------|-------|----------------------|---------------|
| ADR | 10 | MISSING - must add | 1 has signal status (accepted) |
| DD | 9 | Present | - |
| RF | 10 | N/A (use Evidence Quality) | Must add Evidence Quality section |
| STD | 7 | N/A (use Compliance Checklist) | - |
| SYS | 1 | Present | Has signal status (active) |
| **Total** | **37** | | |

---

## Fix Counts by Type

| Fix Type | Count |
|----------|-------|
| Remove `author:` | 37 |
| Remove `related:` | 37 |
| Remove `status:` (non-signal) | 35 |
| Remove "Evidence and Freshness" | 37 |
| Remove "Change Log" | 37 |
| Remove "Open Questions: None" | 35 |
| Add "Core Invariants" | 10 (ADRs only) |
| Add "Evidence Quality" | 10 (RFs only) |
| Transform temporal references | 12 |
| Add entity context | 1 |

**Total individual fixes**: ~251 operations across 37 documents

---

## Parallel Execution Strategy

**Recommended batch size**: 10 documents per agent

**Batch assignments**:
- Agent A: Tasks 1-10 (ADR documents)
- Agent B: Tasks 11-19 (DD documents)
- Agent C: Tasks 20-29 (RF documents)
- Agent D: Tasks 30-37 (STD + SYS documents)

**Validation**: After all tasks complete, run a Haiku validation pass to verify:
1. No `author:` fields remain
2. No `related:` arrays remain
3. No `status: draft` or `status: proposed` remain
4. No "Evidence and Freshness" sections remain
5. No "Change Log" sections remain
6. No "Open Questions: None" sections remain
7. All ADRs have "Core Invariants" section
8. All RFs have "Evidence Quality" section
