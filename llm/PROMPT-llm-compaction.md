# LLM Documentation Compaction Prompt

## Purpose

This prompt guides the extraction of LLM-optimized documents from verbose planning documents. The goal is optimal signal-to-noise ratio with minimal context loss—preserving what matters for downstream LLM consumption while eliminating redundancy, examples that don't add semantic value, and verbose prose that can be compressed without information loss.

**Target consumer:** LLM agents performing planning, spec generation, and code generation—NOT humans.

-----

## The Prompt

```
You are a technical documentation compactor. Your task is to transform a verbose planning document into an LLM-optimized reference that preserves all semantic content while maximizing information density.

## Input
- SOURCE_DOCUMENT: The full planning document to compact
- DOCUMENT_TYPE: One of [system-spec, definition, standard, adr, research-findings]
- RELATED_DOCS: List of document IDs this document references or depends on
- CORPUS_GLOSSARY: (Optional) Shared glossary of terms defined elsewhere

## Output Format

Produce a markdown document with this structure:

---
id: {source_id}-LLM
type: {document_type}
area: {area_code}
title: {title} (LLM View)
status: {status}  # OMIT if "draft"—only include if status carries signal (accepted, deprecated, etc.)
created: {today}
updated: {today}
summary: {one-line summary}
tags: [{original_tags}, llm, view]
links:
  - rel: {relationship_type}
    target_id: "{target_id}"
view: llm
source_id: {source_id}
source_updated: {source_date}
staleness: fresh
---

# {Title} (LLM View)

## LLM Summary
{2-4 sentence executive summary answering: What is this? What does it define/decide/require? Why does it matter? What are the key constraints?}

## Canonical Statements
{Bulleted list of MUST/SHOULD/MAY statements extracted verbatim or minimally paraphrased. These are the non-negotiable rules.}

## Dependencies
{Bulleted list of document dependencies, format: `- {Topic}: \`{DOC-ID}\`.`}

## Open Questions
{Any unresolved items or ambiguities. OMIT THIS SECTION ENTIRELY if there are no open questions—do not include "None."}

## Core Invariants
{3-7 bullet points capturing the fundamental truths that MUST NOT be violated. These are the load-bearing walls.}

## Glossary Snapshot
{Key terms NEWLY defined in this document. OMIT terms that exist in corpus glossary. Format: `- **Term**: Definition.`}

{TYPE-SPECIFIC SECTIONS based on document type - see type-specific guidance below}

## Extraction Rules

### Critical Omission Rules

These rules address common fluff patterns that add no signal for LLM consumption:

1. **Omit empty sections entirely.** Never output "Open Questions: None" or "Change Log: Initial creation." If a section has no meaningful content, exclude it.

2. **Omit uniform-value frontmatter fields.** If every document in the corpus has the same author, omit `author:`. If all documents are `status: draft`, omit status—only include when it signals something (accepted, deprecated, superseded).

3. **Omit redundant relationship tracking.** Use `links:` array only. Do not duplicate in both `related:` and `links:`.

4. **Omit Change Log for LLM views.** The `source_id` and `source_updated` fields capture provenance. A changelog entry saying "LLM view created" adds no information.

5. **Omit "Evidence and Freshness" boilerplate.** If a document has no external citations, do not include a section stating "No external citations required." Staleness is tracked in frontmatter.

6. **Omit "Scope and Non-Goals" when redundant.** If the dependency graph makes clear what this document does NOT cover, do not restate. Only include when out-of-scope boundaries are non-obvious or frequently confused.

7. **Omit Glossary Snapshot for corpus-defined terms.** If a term (e.g., "Canonical ID", "Handoff bundle") is defined in the shared corpus glossary, do not redefine. Only include terms that are NEW or SPECIFIC to this document.

### Entity Reference Rules

These rules prevent orphaned references and human-centric temporal framing:

1. **Never reference undefined entities.** If the source uses an acronym, organization name, or project codename, either:
   - Include minimal context: "EFN (a financial news organization)"
   - Remove the reference entirely if organizational identity isn't architecturally relevant
   - Replace with generic equivalent: "the broader tooling ecosystem" instead of orphaned "EFN ecosystem"

2. **Resolve or remove temporal references.**
   - REMOVE: Calendar dates, time estimates, "Phase 2 starts in March", "by end of Q2"
   - PRESERVE: Dependency sequences ("requires X before Y"), capability gates ("cannot implement until Z is integrated"), budget thresholds
   - TRANSFORM: "Phase 1" → describe by capability milestone or dependency cluster, not timeline

3. **When referencing external systems, tools, or vendors:**
   - If the reference matters architecturally, include the reference
   - If it's just an example that could be any equivalent, generalize or omit

### What to PRESERVE (high signal)

1. **Canonical statements**: Any sentence containing MUST, SHOULD, SHALL, MAY, MUST NOT, SHOULD NOT. Extract verbatim.

2. **Definitions**: Formal definitions of terms, concepts, states, tiers, or categories. Include the full definition, not a summary.

3. **Enumerations**: Complete lists of allowed values, states, tiers, roles, or types. Never truncate these.

4. **Decision criteria**: For ADRs, preserve the full decision rationale, all considered options, and explicit trade-offs accepted.

5. **Constraints and boundaries**: Budget limits, capability requirements, security requirements, reliability tiers, integration requirements.

6. **Cross-references**: Document IDs that establish dependencies. Format as `{DOC-ID}` for machine parsing.

7. **State machines and transitions**: Lifecycle states, stage progressions, valid transitions, and explicit backward transition rules.

8. **Exception cases**: "When NOT to use this pattern", "Unless X", "Except when Y". These are frequently missed—hunt for them.

9. **Implicit conventions made explicit**: If the document demonstrates a pattern (like ID naming) without stating the rule, extract and state the rule explicitly with a note: `[Implicit in source, made explicit]`.

10. **Interface contracts**: Required fields, schema definitions, enum values, validation rules. These are load-bearing for downstream code generation.

11. **Rejected alternatives with rationale**: In ADRs, WHY something was rejected matters as much as WHAT was decided.

### What to COMPRESS (reduce verbosity, preserve meaning)

1. **Motivational prose**: "This is important because..." → preserve the reason, drop the framing.

2. **Repeated concepts**: If the same idea appears in introduction, body, and conclusion, consolidate to single authoritative statement.

3. **Example proliferation**: Keep 1-2 canonical examples per concept. Drop redundant variations unless they illustrate edge cases.

4. **Historical context**: Compress to single line unless the history affects current interpretation.

5. **Formatting verbosity**: Tables with sparse data → bulleted lists. Nested bullets with single items → inline.

6. **Human-oriented explanations of technical terms**: An LLM knows what "idempotency" and "webhook" mean. Don't explain standard technical vocabulary.

### What to OMIT (low signal for LLM consumption)

1. **Meta-commentary**: "This section will discuss..." "As mentioned above..."

2. **Placeholder content**: TBD sections with no substance (but DO flag unresolved items in Open Questions if substantive).

3. **Redundant cross-references**: If dependency is listed in frontmatter, don't repeat in body unless adding context.

4. **Stylistic choices**: Section ordering rationale, formatting decisions, document structure explanations.

5. **Acknowledgments and attribution prose**: Drop entirely—LLMs don't need to know who wrote what.

6. **Human onboarding context**: "For those unfamiliar with X..." "This may seem complex at first..."

7. **Temporal planning artifacts**: Sprint timelines, phase calendars, "by end of Q2" commitments. Preserve dependencies, drop dates.

8. **Stakeholder identification prose**: "The CTO will approve..." → only preserve IF the approval gate itself matters architecturally.

### Ambiguity Protocol

When you encounter ambiguity in the source:

1. **DO NOT resolve ambiguity through interpretation.** Your job is extraction, not gap-filling.

2. **Flag ambiguities explicitly** in the Open Questions section:
```
- [AMBIGUITY] Source uses both "accepted" and "active" for ADR status without clarifying relationship. See {DOC-ID}:§{section} and {DOC-ID}:§{section}.
```
3. **When terms are used inconsistently**, extract all usages and note the inconsistency:
```
- [INCONSISTENCY] "Community forum" classified as T3 in §2.1 but T4 in §4.2 example.
```
4. **When cross-references point to non-existent sections**, flag:
```
- [BROKEN REF] Reference to DD-XX-01 §3.4 but document has no §3.4.
```
5. **When undefined entities are referenced**, flag:
```
- [UNDEFINED] "EFN" referenced throughout but never defined in source or corpus glossary.
```
## Type-Specific Extraction Guidance

### For DEFINITION documents (DD-*)

Add section ONLY if document defines multiple related terms:
```
## Definition Matrix
|Term|Category|Constraints|See Also|
|----|--------|-----------|--------|
```
Focus on: Complete enumeration of defined terms, valid values for each category, explicit boundaries between categories.

Hunt for: Implicit hierarchies, unstated defaults, edge case classifications.

OMIT: Glossary Snapshot if all terms are in corpus glossary.

### For STANDARD documents (STD-*)

Add section:
```
## Compliance Checklist
- [ ] {Requirement 1}
- [ ] {Requirement 2}
```
Add section:
```
## Enforcement
{How/where this standard is enforced—validation layer, review gate, automated check, etc.}
```
Focus on: Testable requirements, validation criteria, required vs. optional fields.

Hunt for: "MUST include", "SHOULD validate", schema requirements, error handling expectations.

### For ADR documents (ADR-*)

Add section:
```
## Decision
{One-line decision statement}

## Drivers
{What requirements/constraints drove this decision}

## Alternatives and Disposition
{List with brief rationale for rejection/deferral of each}

## Consequences
- Positive: {benefits accepted}
- Negative: {trade-offs accepted}
```
Focus on: The actual decision, why alternatives were rejected, what trade-offs were knowingly accepted.

Hunt for: Implicit constraints that drove the decision, unstated assumptions, reversibility conditions.

OMIT: "Status: proposed" if that's the default—only note accepted/deprecated/superseded.

### For RESEARCH FINDINGS documents (RF-*)

Add section:
```
## Findings
{Key discoveries, 3-7 bullets}

## Limitations
{Methodology gaps, confidence caveats}

## Recommendation
{What action this research supports}
```
Focus on: Source tier ratings, confidence levels, methodology limitations, implications for decisions.

Hunt for: Hedged language ("may", "likely", "suggests"), unstated confidence intervals, source conflicts.

OMIT: Detailed citation metadata if captured in structured evidence artifacts elsewhere.

### For SYSTEM SPEC documents (SYS-*)

Add sections:
```
## Architecture Layers
{Numbered list of layers with one-line descriptions}

## Constraint Summary
|Constraint|Value|Source|
|----------|-----|------|
```
Focus on: Layer boundaries, cross-layer dependencies, hard constraints vs. preferences.

Hunt for: Implicit ordering requirements, unstated failure modes, assumed capabilities.

## Quality Checklist

Before finalizing, verify:

- [ ] All MUST/SHOULD/MAY statements extracted
- [ ] All enumerations complete (no "etc." or "and more")
- [ ] All cross-references use consistent `{DOC-ID}` format
- [ ] No empty sections remain (remove them)
- [ ] No undefined entities referenced without context
- [ ] No calendar dates or time estimates remain (unless they're hard deadlines that function as constraints)
- [ ] No redundant glossary entries for corpus-defined terms
- [ ] Open Questions section omitted if empty
- [ ] Change Log section omitted entirely
- [ ] Status field omitted if "draft"
- [ ] Author field omitted (unless authorship matters for the content)
- [ ] Ambiguities flagged, not resolved
- [ ] Compression ratio is 60-85% of source (flag if outside this range)
- [ ] Exception cases ("when NOT to") captured
- [ ] Implicit conventions made explicit and marked
- [ ] Frontmatter links array populated with valid relationships
- [ ] Document is self-contained (reader shouldn't need source for comprehension)

## Anti-Patterns to Avoid

1. **Over-compression**: Dropping qualifiers that change meaning. "SHOULD validate" ≠ "validates".

2. **Under-compression**: Preserving verbose prose that adds no semantic content.

3. **Interpretation creep**: Adding "clarifications" that aren't in the source.

4. **Reference decay**: Dropping section numbers from cross-references, making them unfindable.

5. **Example over-retention**: Keeping 5 examples when 1 canonical example suffices.

6. **Glossary sprawl**: Including common terms that don't have document-specific definitions.

7. **Staleness blindness**: Not flagging dated content or time-sensitive claims.

8. **Orphaned entities**: Preserving acronyms or project names without context.

9. **Temporal preservation**: Keeping calendar dates and phase timelines that are human coordination artifacts.

10. **Empty section retention**: Including sections that say "None" or contain only boilerplate.

## Output Validation

The compacted document should:

1. **Enable reconstruction**: A reader with only the LLM view should understand all rules, constraints, and decisions without accessing the source.

2. **Support machine parsing**: Consistent formatting, predictable section structure, parseable frontmatter.

3. **Flag its own gaps**: Open Questions should surface anything the compactor couldn't confidently extract.

4. **Maintain traceability**: Source document ID and date in frontmatter, major sections traceable to source sections.

5. **Be 15-40% the length of source**: Target ~20-30%. If significantly longer, you're under-compressing. If significantly shorter, audit for content loss.
```

-----

## Usage

### Single Document Compaction

```
<source_document>
{paste full document content}
</source_document>

<document_type>definition</document_type>

<related_docs>
- DD-13-01
- STD-15-01
</related_docs>

<corpus_glossary>
{optional: paste shared glossary terms this document should NOT redefine}
</corpus_glossary>

Apply the LLM Documentation Compaction Prompt to produce an LLM-optimized view.
```

### Batch Compaction with Consistency Check

When compacting multiple related documents, add:

```
<consistency_check>
After compacting, verify cross-document consistency:
1. Terms defined in multiple documents have compatible definitions
2. Cross-references resolve to actual sections
3. Tier/state/role enumerations match across documents
4. No contradictory MUST statements between related documents
5. No orphaned entity references (acronyms, project names without context)

Flag any inconsistencies in a final CROSS-DOCUMENT ISSUES section.
</consistency_check>
```

### Compaction Review (for validating existing LLM views)

```
<source_document>
{paste full source document}
</source_document>

<llm_view>
{paste existing LLM-optimized document}
</llm_view>

Review the LLM view against the source. Identify:
1. Content present in source but missing from LLM view (OMISSION)
2. Content in LLM view that misrepresents source (DISTORTION)
3. Ambiguities in source that LLM view incorrectly resolved (INTERPRETATION)
4. Content that should have been compressed further (VERBOSITY)
5. Empty sections that should have been removed (FLUFF)
6. Undefined entities preserved without context (ORPHAN)
7. Temporal references that should have been converted or removed (TEMPORAL)

Output a structured review with specific line references.
```

-----

## Rationale

This prompt structure addresses the specific extraction variance patterns identified in LLM documentation evaluation:

|Variance Pattern                    |Prompt Countermeasure                                         |
|------------------------------------|--------------------------------------------------------------|
|Buried information in long documents|"Hunt for" directives in type-specific guidance               |
|Implicit conventions                |Explicit instruction to surface and mark implicit patterns    |
|Inconsistent terminology            |Ambiguity protocol with flagging requirements                 |
|Exception cases missed              |Dedicated "When NOT to" extraction rule                       |
|Cross-reference decay               |Strict `{DOC-ID}` formatting requirement                      |
|Over-interpretation                 |"DO NOT resolve ambiguity" as primary directive               |
|State/tier divergence               |Complete enumeration requirement, no truncation               |
|Empty section bloat                 |Critical omission rules for boilerplate removal               |
|Orphaned entity references          |Entity reference rules requiring context or removal           |
|Temporal artifact preservation      |Explicit rules to remove dates, convert phases to dependencies|
|Glossary duplication                |Corpus glossary injection, local omission rule                |

-----

## Parallel Orchestration Patterns

When processing documents in parallel with fresh context windows, cross-document consistency cannot be maintained during extraction. These patterns mitigate drift and enable post-hoc reconciliation.

### The Problem

|Risk                         |Cause                           |Example                                                                            |
|-----------------------------|--------------------------------|-----------------------------------------------------------------------------------|
|**Terminology drift**        |No shared glossary              |Doc A extracts "lifecycle state", Doc B extracts "artifact status" for same concept|
|**Enumeration divergence**   |Partial extraction              |Doc A lists 5 tiers, Doc B lists 4 (missed T5)                                     |
|**Cross-reference blindness**|Can't validate links            |Doc A references DD-15 §3.2 which doesn't exist                                    |
|**Definition inconsistency** |Same term, different definitions|"Active" defined differently in DD-13 vs DD-15 extractions                         |
|**Entity context loss**      |No corpus-wide awareness        |Doc A defines "EFN", Doc B references it without context                           |

### Pattern 1: Pre-Flight Context Injection

**When to use**: You have identified "anchor documents" that define terms used across the corpus.

**Process**:

```
Phase 1: Extract shared context (sequential, single context)
┌─────────────────────────────────────────────────────────┐
│ Input: SYS-00, DD-13, DD-15, DD-20 (foundational docs)  │
│ Output: SHARED-CONTEXT.yaml                             │
│   - canonical_glossary: {term: definition}              │
│   - canonical_enumerations:                             │
│       lifecycle_states: [draft, review, active, ...]    │
│       source_tiers: [T1, T2, T3, T4, T5]               │
│       roles: [Owner, Planner, Contributor, ...]         │
│   - entity_definitions:                                 │
│       EFN: "a financial news organization"              │
│       Compass: "the planning and documentation system"  │
│   - document_map: {id: {title, sections[]}}            │
└─────────────────────────────────────────────────────────┘

Phase 2: Parallel compaction with injected context
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ DD-17 + CTX  │  │ DD-18 + CTX  │  │ RF-01 + CTX  │  ...
└──────────────┘  └──────────────┘  └──────────────┘
       │                 │                 │
       ▼                 ▼                 ▼
   LLM-DD-17         LLM-DD-18         LLM-RF-01
```

**Context injection prompt addition**:

```
<shared_context>
Use the following canonical definitions. Do NOT define these terms differently.
If the source document contradicts these definitions, flag as [CONFLICT WITH CANONICAL].

## Canonical Glossary
{paste from SHARED-CONTEXT.yaml}

## Canonical Enumerations
{paste from SHARED-CONTEXT.yaml}

## Entity Definitions
{paste from SHARED-CONTEXT.yaml - use these for context when entities are referenced}

## Document Map (for cross-reference validation)
{paste from SHARED-CONTEXT.yaml}
</shared_context>
```

**Pros**: Highest consistency, catches conflicts during extraction
**Cons**: Requires identifying anchor documents, sequential bottleneck in Phase 1

-----

### Pattern 2: Three-Phase Pipeline (Extract → Compact → Reconcile)

**When to use**: Large corpus, maximize parallelism, accept post-hoc repair.

**Process**:

```
Phase 1: Parallel extraction (raw signal capture)
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Doc A  │ │ Doc B  │ │ Doc C  │ │ Doc D  │  ... (all parallel)
└────────┘ └────────┘ └────────┘ └────────┘
     │          │          │          │
     ▼          ▼          ▼          ▼
  RAW-A      RAW-B      RAW-C      RAW-D

Phase 2: Automated reconciliation (single context)
┌─────────────────────────────────────────────────────────┐
│ Input: All RAW-* outputs                                │
│ Tasks:                                                  │
│   1. Build unified glossary, flag conflicts             │
│   2. Merge enumerations, flag incomplete extractions    │
│   3. Validate all cross-references                      │
│   4. Identify orphaned entity references                │
│   5. Generate RECONCILIATION-REPORT.md                  │
└─────────────────────────────────────────────────────────┘

Phase 3: Targeted repair (parallel, only flagged docs)
┌──────────────────┐  ┌──────────────────┐
│ RAW-B + REPORT   │  │ RAW-D + REPORT   │  (only docs with issues)
└──────────────────┘  └──────────────────┘
         │                     │
         ▼                     ▼
     LLM-B (fixed)        LLM-D (fixed)
```

**Reconciliation prompt**:

```
You are a documentation reconciliation agent. You have received multiple
independently-extracted LLM views. Your task is to identify inconsistencies
WITHOUT modifying the extractions.

Input: {all RAW-* documents}

Output a RECONCILIATION-REPORT.md with:

## Glossary Conflicts
| Term | Doc A Definition | Doc B Definition | Resolution Needed |
|------|-----------------|-----------------|-------------------|

## Enumeration Gaps
| Enumeration | Expected Values | Doc | Missing Values |
|-------------|----------------|-----|----------------|

## Cross-Reference Failures
| Source Doc | Reference | Target | Issue |
|------------|-----------|--------|-------|

## Orphaned Entities
| Entity | Docs Referencing | Context Provided | Action |
|--------|-----------------|------------------|--------|

## Recommended Repairs
For each flagged document, specify:
- Document ID
- Section to repair
- Specific instruction
```

**Pros**: Maximum parallelism, systematic issue detection
**Cons**: Three phases, repair phase may be significant

-----

### Pattern 3: Dependency-Ordered Waves

**When to use**: Clear dependency hierarchy, moderate corpus size.

**Process**:

```
Wave 1: Foundation (no dependencies)
┌────────┐ ┌────────┐ ┌────────┐
│ SYS-00 │ │ DD-13  │ │ DD-20  │  (parallel)
└────────┘ └────────┘ └────────┘
     │          │          │
     ▼          ▼          ▼
 Extract glossary + enumerations + entity definitions from Wave 1 outputs
                    │
                    ▼
              WAVE-1-CONTEXT

Wave 2: Core definitions (depend on Wave 1)
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ DD-14 + W1-CTX  │ │ DD-15 + W1-CTX  │ │ DD-17 + W1-CTX  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                    │
                    ▼
              WAVE-2-CONTEXT (merged)

Wave 3: Standards + Research (depend on Wave 1-2)
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ STD-* + W2-CTX  │ │ RF-* + W2-CTX   │ │ ADR-* + W2-CTX  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Wave assignment heuristic**:

```python
def assign_wave(doc_id, dependency_graph):
    """Assign document to earliest valid wave."""
    if not dependency_graph[doc_id]:
        return 1  # No dependencies → Wave 1

    max_dep_wave = max(
        assign_wave(dep, dependency_graph)
        for dep in dependency_graph[doc_id]
    )
    return max_dep_wave + 1
```

**Pros**: Natural dependency respect, incremental context building
**Cons**: Requires dependency graph, sequential wave boundaries

-----

### Pattern 4: Anchor + Satellite

**When to use**: One or few "master" documents define most shared concepts.

**Process**:

```
Step 1: Compact anchor document(s) with extra rigor
┌─────────────────────────────────────────────────────────┐
│ SYS-00 compaction with ANCHOR flag                      │
│ - Extract ALL defined terms into structured glossary    │
│ - Extract ALL enumerations with completeness check      │
│ - Extract ALL entity definitions with context           │
│ - Generate ANCHOR-CONTEXT.yaml as side output           │
└─────────────────────────────────────────────────────────┘

Step 2: Parallel satellite compaction
┌────────────────────┐ ┌────────────────────┐
│ DD-* + ANCHOR-CTX  │ │ RF-* + ANCHOR-CTX  │  ... (all parallel)
└────────────────────┘ └────────────────────┘

Satellite instruction addition:
"This document is a SATELLITE. The anchor document (SYS-00) defines
canonical terms. When extracting:
- Use anchor terminology, not local synonyms
- Flag any term that SHOULD be in anchor but isn't as [ANCHOR GAP]
- Do not redefine anchor terms in your glossary
- Use anchor entity definitions for context when referencing organizations/projects"
```

**Pros**: Simplest model, single sequential step
**Cons**: Only works if anchor coverage is high

-----

### Recommended Pattern by Corpus Type

|Corpus Characteristic          |Recommended Pattern         |Rationale                             |
|-------------------------------|----------------------------|--------------------------------------|
|<10 documents, clear hierarchy |Dependency-Ordered Waves    |Natural fit, manageable waves         |
|10-30 documents, one master doc|Anchor + Satellite          |SYS-00 defines most terms             |
|30+ documents, need speed      |Three-Phase Pipeline        |Maximum parallelism, systematic repair|
|High consistency requirement   |Pre-Flight Context Injection|Catches conflicts during extraction   |
|Unknown structure              |Three-Phase Pipeline        |Reconciliation reveals structure      |

-----

### Context Injection Template

For any pattern requiring context injection, use this template:

```
<injected_context>
## Instructions
You are receiving pre-extracted canonical definitions. These are AUTHORITATIVE.

1. Use these exact terms when the source discusses the same concepts
2. If source uses a synonym, map to canonical term and note: [LOCAL: "x" → CANONICAL: "y"]
3. If source contradicts canonical definition, flag: [CONFLICT] and preserve both
4. If source defines a term NOT in canonical list, extract normally to your glossary
5. Validate cross-references against the document map; flag failures
6. Use entity definitions to provide context when referencing organizations/projects

## Canonical Glossary
{{GLOSSARY}}

## Canonical Enumerations
### Lifecycle States
{{LIFECYCLE_STATES}}

### Source Tiers
{{SOURCE_TIERS}}

### Roles
{{ROLES}}

## Entity Definitions
{{ENTITIES}}

## Document Map
{{DOCUMENT_MAP}}
</injected_context>
```

-----

### Reconciliation Report Schema

For post-hoc reconciliation (Patterns 2 and 3), generate structured output:

```yaml
# RECONCILIATION-REPORT.yaml
generated: 2026-02-03
documents_processed: 24
issues_found: 7

glossary_conflicts:
  - term: "active"
    definitions:
      DD-13-LLM: "Artifact is canonical and authoritative"
      DD-15-LLM: "User account is enabled"
    resolution: "Context-dependent; add qualifier (artifact-active vs user-active)"

enumeration_gaps:
  - enumeration: "source_tiers"
    canonical: [T1, T2, T3, T4, T5]
    document: RF-03-LLM
    extracted: [T1, T2, T3, T4]
    missing: [T5]
    action: "Re-extract §Evidence Summary from RF-03"

cross_reference_failures:
  - source: LLM-DD-17
    reference: "DD-15-01 §3.4"
    issue: "DD-15-01 has no §3.4; likely meant §3.2 (Approval Requirements)"
    action: "Flag as [BROKEN REF] in LLM-DD-17 Open Questions"

orphaned_entities:
  - entity: "EFN"
    documents: [LLM-DD-14, LLM-RF-03]
    context_provided: false
    action: "Add context 'EFN (a financial news organization)' or remove reference"

repair_queue:
  - document: RF-03-LLM
    priority: high
    instructions:
      - "Re-extract Evidence Summary table"
      - "Ensure all 5 source tiers represented"
  - document: LLM-DD-17
    priority: low
    instructions:
      - "Add [BROKEN REF] note to Open Questions"
  - document: LLM-DD-14
    priority: medium
    instructions:
      - "Add context for EFN reference or generalize to 'the organization'"
```

-----

## Model Selection Strategy

Different pipeline phases have different cognitive profiles. Model selection should balance capability, context window, cost, and throughput.

### Task Cognitive Profiles

|Task                   |Reasoning Depth|Context Needs|Judgment Calls|Error Cost       |
|-----------------------|---------------|-------------|--------------|-----------------|
|**Anchor extraction**  |High           |Medium       |Many          |High (propagates)|
|**Standard compaction**|Medium         |High         |Moderate      |Medium           |
|**Reconciliation**     |High           |Medium-High  |Many          |High             |
|**Repair decisions**   |High           |Low-Medium   |Many          |Medium           |
|**Targeted repair**    |Medium         |Medium       |Few (directed)|Low              |
|**Validation/QA**      |Low-Medium     |High         |Few           |Low              |

### Model Capability vs. Context Trade-off

When a high-capability model (Opus) has smaller context than a mid-tier model (Sonnet):

```
                    ┌─────────────────────────────────────────┐
                    │         CONTEXT WINDOW SIZE             │
                    │  Small ◄─────────────────────► Large    │
                    └─────────────────────────────────────────┘
                              │                   │
     ┌────────────────────────┼───────────────────┼────────────────────────┐
     │                        │                   │                        │
HIGH │   Opus: Anchor         │                   │   Sonnet: Large doc    │
     │   extraction,          │                   │   compaction where     │
R    │   reconciliation,      │                   │   full context needed  │
E    │   ambiguity judgment   │                   │                        │
A    │                        │                   │                        │
S    ├────────────────────────┼───────────────────┼────────────────────────┤
O    │                        │                   │                        │
N    │   Sonnet: Standard     │                   │   Sonnet: Bulk         │
I    │   compaction,          │                   │   parallel processing  │
N    │   repair execution     │                   │                        │
G    │                        │                   │                        │
     ├────────────────────────┼───────────────────┼────────────────────────┤
     │                        │                   │                        │
LOW  │   Haiku: Schema        │                   │   Haiku: Format        │
     │   validation,          │                   │   validation,          │
     │   frontmatter checks   │                   │   batch QA passes      │
     │                        │                   │                        │
     └────────────────────────┴───────────────────┴────────────────────────┘
```

### Recommended Model Assignment by Phase

#### Pattern 1 & 4 (Pre-Flight / Anchor + Satellite)

|Phase                  |Model     |Rationale                                                       |
|-----------------------|----------|----------------------------------------------------------------|
|Anchor extraction      |**Opus**  |High-stakes; errors propagate to all satellites. Worth the cost.|
|Context YAML generation|**Haiku** |Mechanical transformation of extracted data.                    |
|Satellite compaction   |**Sonnet**|Bulk parallel; needs full context window for large sources.     |
|Validation pass        |**Haiku** |Schema compliance, format checks.                               |

#### Pattern 2 (Three-Phase Pipeline)

|Phase                   |Model     |Rationale                                                    |
|------------------------|----------|-------------------------------------------------------------|
|Phase 1: Raw extraction |**Sonnet**|Needs full source context; moderate judgment.                |
|Phase 2: Reconciliation |**Opus**  |Cross-document reasoning, conflict detection, judgment-heavy.|
|Phase 3: Targeted repair|**Sonnet**|Directed fixes with specific instructions; lower judgment.   |
|Final validation        |**Haiku** |Mechanical compliance checking.                              |

#### Pattern 3 (Dependency Waves)

|Phase                   |Model     |Rationale                                    |
|------------------------|----------|---------------------------------------------|
|Wave 1 (foundations)    |**Opus**  |These define canonical terms; errors cascade.|
|Context extraction      |**Haiku** |Mechanical YAML generation.                  |
|Wave 2+ (dependent docs)|**Sonnet**|Standard compaction with injected context.   |
|Cross-wave validation   |**Sonnet**|Check context accumulation correctness.      |

### Context Window Strategies

When source document exceeds high-capability model's context window:

#### Strategy A: Chunked Extraction with Opus Synthesis

```
┌─────────────────────────────────────────────────────────┐
│ Large source document (exceeds Opus context)            │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ Chunk 1 │     │ Chunk 2 │     │ Chunk 3 │  ← Sonnet extracts
    │ Sonnet  │     │ Sonnet  │     │ Sonnet  │    each chunk
    └─────────┘     └─────────┘     └─────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
              ┌─────────────────────┐
              │ Opus synthesizes    │  ← Opus merges chunk
              │ chunk extractions   │    outputs (fits context)
              │ into final LLM view │
              └─────────────────────┘
```

**Chunk extraction prompt addition**:

```
You are extracting from CHUNK {n} of {total} of document {DOC-ID}.

Additional instructions:
- Extract all content as if standalone, but note [CONTINUES FROM PREVIOUS]
  or [CONTINUES IN NEXT] for split sections
- Do not attempt to summarize content from other chunks
- Preserve all cross-references even if target is in another chunk
- Output structured extraction, not final prose
```

**Synthesis prompt**:

```
You are synthesizing {n} chunk extractions into a single LLM view.

Chunk extractions:
{chunk_1_output}
{chunk_2_output}
...

Instructions:
- Merge overlapping content, preferring more complete version
- Resolve [CONTINUES] markers into coherent sections
- Deduplicate repeated content (from chunk overlap)
- Ensure all cross-references are preserved
- Apply standard LLM view formatting
```

#### Strategy B: Sonnet Full-Context with Opus Review

```
┌─────────────────────────────────────────────────────────┐
│ Large source document                                    │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Sonnet compacts     │  ← Full context available
              │ (draft LLM view)    │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Opus reviews        │  ← LLM view fits Opus context
              │ draft + source      │    even if source didn't
              │ excerpts for QA     │
              └─────────────────────┘
```

**Opus review prompt**:

```
You are reviewing an LLM view extraction for quality.

Draft LLM view:
{sonnet_output}

Source document excerpts (high-signal sections):
{key_sections_from_source}

Review for:
1. [OMISSION] Important content in source excerpts missing from draft
2. [DISTORTION] Content that misrepresents source meaning
3. [INTERPRETATION] Ambiguities resolved without flagging
4. [VERBOSITY] Content that should be further compressed
5. [ORPHAN] Entity references without context
6. [TEMPORAL] Calendar dates or phase timelines that should be removed

Output: List of specific issues with line references, or "APPROVED" if none.
```

### Cost Optimization Strategies

#### 1. Haiku Pre-Filter

Before expensive Opus processing, use Haiku to classify documents:

```
Haiku classification prompt:
"Analyze this document and classify:
- SIMPLE: Straightforward structure, few cross-references, no ambiguities
- MODERATE: Standard complexity, some judgment needed
- COMPLEX: Dense cross-references, ambiguous content, high-stakes definitions

Output only: SIMPLE, MODERATE, or COMPLEX"
```

Route:

- SIMPLE → Sonnet only
- MODERATE → Sonnet + Haiku validation
- COMPLEX → Opus (or Sonnet + Opus review)

#### 2. Selective Opus Escalation

Use Sonnet for all extractions, but escalate to Opus when Sonnet flags uncertainty:

```
Sonnet extraction addition:
"If you encounter content where you have LOW CONFIDENCE in correct extraction,
flag the section as [NEEDS REVIEW: reason] and continue with best effort.

Do not attempt to resolve unclear content—flag it."
```

Then route only flagged documents/sections to Opus for targeted review.

#### 3. Batch Validation Economics

For large corpus, validation cost matters:

|Validation Type         |Model |Per-Doc Cost|Batch Strategy|
|------------------------|------|------------|--------------|
|Schema compliance       |Haiku |~$0.001     |Run on all    |
|Enumeration completeness|Haiku |~$0.002     |Run on all    |
|Cross-reference validity|Haiku |~$0.003     |Run on all    |
|Orphaned entity check   |Haiku |~$0.002     |Run on all    |
|Semantic accuracy       |Sonnet|~$0.02      |Sample 20%    |
|Deep judgment review    |Opus  |~$0.15      |Only flagged  |

### Model Selection Decision Tree

```
START: Document to compact
  │
  ├─► Is this an anchor/foundation document?
  │     YES → Use Opus
  │     NO ──┐
  │          │
  │          ├─► Does source exceed Sonnet context?
  │          │     YES → Chunked extraction (Sonnet) + Opus synthesis
  │          │     NO ──┐
  │          │          │
  │          │          ├─► Is document COMPLEX (per Haiku classification)?
  │          │          │     YES → Sonnet extraction + Opus review
  │          │          │     NO ──┐
  │          │          │          │
  │          │          │          └─► Sonnet extraction + Haiku validation
  │          │          │
  │          │          └─► Did Sonnet flag [NEEDS REVIEW]?
  │          │                YES → Route flagged sections to Opus
  │          │                NO → Accept Sonnet output
  │          │
  │          └─► For reconciliation phase → Always Opus
  │
  └─► For validation/QA passes → Always Haiku
```

### Failure Mode Handling by Model

|Model     |Common Failure                        |Detection                                |Mitigation                        |
|----------|--------------------------------------|-----------------------------------------|----------------------------------|
|**Haiku** |Misses nuance, over-simplifies        |Spot-check samples with Sonnet           |Use only for mechanical tasks     |
|**Sonnet**|Resolves ambiguity instead of flagging|Check Open Questions section is populated|Strong prompt emphasis on flagging|
|**Sonnet**|Preserves orphaned entities           |Grep for undefined acronyms              |Add entity check to validation    |
|**Opus**  |Over-engineering, excessive detail    |Output length > 50% of source            |Add compression ratio check       |

### Example Cost Estimation

For a 30-document corpus (Compass-scale):

|Strategy        |Opus Calls   |Sonnet Calls|Haiku Calls|Est. Cost|
|----------------|-------------|------------|-----------|---------|
|All Opus        |30           |0           |0          |~$4.50   |
|All Sonnet      |0            |30          |0          |~$0.60   |
|Recommended mix |5            |25          |30         |~$1.10   |
|With Opus review|5 + 10 review|25          |30         |~$1.85   |

*Estimates assume ~5K tokens input, ~2K tokens output per document. Actual costs vary.*

-----

## Appendix A: Frontmatter Field Reference

### Always Include

|Field           |Purpose                             |
|----------------|------------------------------------|
|`id`            |Unique identifier with `-LLM` suffix|
|`type`          |Document type for routing           |
|`area`          |Area code for grouping              |
|`title`         |With "(LLM View)" suffix            |
|`summary`       |One-line description                |
|`tags`          |Must include `llm`, `view`          |
|`links`         |Typed relationships to other docs   |
|`view`          |Always `llm`                        |
|`source_id`     |Original document ID                |
|`source_updated`|When source was last modified       |
|`staleness`     |`fresh`, `stale`, or `unknown`      |

### Include Only If Non-Default

|Field    |Include When                                        |
|---------|----------------------------------------------------|
|`status` |Not "draft" (e.g., accepted, deprecated, superseded)|
|`created`|Different from source created date                  |
|`updated`|Different from today                                |

### Omit Entirely

|Field    |Reason                          |
|---------|--------------------------------|
|`author` |Uniform across corpus; no signal|
|`related`|Superseded by `links` array     |

-----

## Appendix B: Compression Ratio Guidelines

|Document Type  |Target Ratio|Acceptable Range|Flag If                                            |
|---------------|------------|----------------|---------------------------------------------------|
|Definition (DD)|25%         |15-35%          |<10% (likely lost content) or >40% (likely verbose)|
|Standard (STD) |25%         |15-35%          |<10% (lost requirements) or >40% (redundant)       |
|ADR            |30%         |20-40%          |<15% (lost rationale) or >45% (didn't compress)    |
|Research (RF)  |20%         |15-30%          |<10% (lost evidence) or >35% (verbose)             |
|System Spec    |35%         |25-45%          |<20% (lost architecture) or >50% (no compression)  |

Compression ratio = (LLM view token count) / (Source token count)

-----

## Appendix C: Common Failure Modes

|Failure                     |Detection                                           |Correction                        |
|----------------------------|----------------------------------------------------|----------------------------------|
|Undefined entity preserved  |Grep for acronyms not in glossary                   |Add context or remove             |
|Empty section included      |Section contains only "None" or equivalent          |Delete section                    |
|Temporal reference preserved|Grep for month names, "Q[1-4]", "Phase N" with dates|Convert to dependency or remove   |
|Glossary term redefined     |Term exists in corpus glossary                      |Remove from local glossary        |
|Ambiguity silently resolved |Open Questions empty but source had hedged language |Re-extract with ambiguity flagging|
|Changelog boilerplate       |Section contains only "LLM view created"            |Delete section                    |
|Redundant relationships     |Same doc in both `related:` and `links:`            |Keep only `links:`                |
|Status: draft included      |Uniform status across corpus                        |Remove field                      |
|Author field included       |Uniform author across corpus                        |Remove field                      |

-----

## Appendix D: Entity Context Templates

When an entity must be referenced but isn't self-explanatory:

```
# Organization
"{ACRONYM} (a {industry} organization)"
"EFN (a financial news organization)"

# Project/Product
"{NAME}, the {brief description}"
"Compass, the planning and documentation system"

# External Tool (when specific tool matters)
"{Tool} for {purpose}"
"Linear for project management"

# External Tool (when any equivalent would work)
"a project management tool"  # Don't name specific tool if it's just an example

# Phase/Milestone (transform from temporal)
"after core memory is implemented"  # Not "in Phase 2"
"once the questioning arc supports branching"  # Not "by March"
"requires completion of {dependency}"  # Not "scheduled for Q3"
```

-----

## Appendix E: Temporal Reference Handling

### Remove Entirely

- Calendar dates: "January 2026", "by March", "Q2 2026"
- Sprint references: "Sprint 14", "next sprint"
- Relative time: "in 3 weeks", "last month"
- Meeting references: "discussed on Tuesday"

### Transform to Dependencies

|Before                   |After                               |
|-------------------------|------------------------------------|
|"Phase 2 starts in March"|"requires Phase 1 completion"       |
|"Will implement after Q1"|"depends on {specific capability}"  |
|"Scheduled for Sprint 15"|"blocked by {blocker}"              |
|"Target: end of quarter" |OMIT (or convert to capability gate)|

### Preserve

- Hard deadlines that function as architectural constraints: "must support 2024 tax year reporting"
- Version-specific behaviors: "deprecated in v3.0"
- Historical facts affecting interpretation: "decided before X existed"

-----

## Version History

- 2026-02-03: Initial version based on LLM documentation evaluation findings
- 2026-02-03: Added parallel orchestration patterns for fresh-context-window processing
- 2026-02-03: Added model selection strategy for capability/context/cost optimization
- 2026-02-04: v2 — Added Critical Omission Rules, Entity Reference Rules, temporal handling, frontmatter optimization based on compaction methodology review; adjusted compression ratios; added failure mode detection patterns; added entity context templates
