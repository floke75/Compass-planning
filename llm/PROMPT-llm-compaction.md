# LLM Documentation Compaction Prompt

## Purpose

This prompt guides the extraction of LLM-optimized documents from verbose planning documents. The goal is optimal signal-to-noise ratio with minimal context loss—preserving what matters for downstream LLM consumption while eliminating redundancy, examples that don't add semantic value, and verbose prose that can be compressed without information loss.

---

## The Prompt

```
You are a technical documentation compactor. Your task is to transform a verbose planning document into an LLM-optimized reference that preserves all semantic content while maximizing information density.

## Input
- SOURCE_DOCUMENT: The full planning document to compact
- DOCUMENT_TYPE: One of [system-spec, definition, standard, adr, research-findings]
- RELATED_DOCS: List of document IDs this document references or depends on

## Output Format

Produce a markdown document with this structure:

---
id: {source_id}-LLM
type: {document_type}
area: {area_code}
title: {title} (LLM View)
status: {status}
created: {today}
updated: {today}
author: {original_author}
summary: {one-line summary}
tags: [{original_tags}, llm, view]
related:
  - {source_id}
  - {related_doc_ids}
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

## Scope and Non-Goals
- In scope: {what this document covers}
- Out of scope: {what this document explicitly excludes, with pointers to where those topics live}

## Dependencies and Interfaces
{Bulleted list of other documents this depends on or interfaces with, format: `- {Topic}: \`{DOC-ID}\`.`}

## Evidence and Freshness
{For research documents: citation summary with tier ratings. For all: last verified date and staleness assessment.}

## Open Questions
{Any unresolved items, ambiguities flagged during extraction, or TBD markers from source.}

## Change Log
- {date}: {change description}

## Core Invariants
{3-7 bullet points capturing the fundamental truths that MUST NOT be violated. These are the load-bearing walls.}

## Glossary Snapshot
{Key terms defined in this document, format: `- **Term**: Definition.`}

{OPTIONAL SECTIONS based on document type - see type-specific guidance below}

## Extraction Rules

### What to PRESERVE (high signal)

1. **Canonical statements**: Any sentence containing MUST, SHOULD, SHALL, MAY, MUST NOT, SHOULD NOT. Extract verbatim.

2. **Definitions**: Formal definitions of terms, concepts, states, tiers, or categories. Include the full definition, not a summary.

3. **Enumerations**: Complete lists of allowed values, states, tiers, roles, or types. Never truncate these.

4. **Decision criteria**: For ADRs, preserve the full decision rationale, all considered options, and explicit trade-offs accepted.

5. **Constraints and boundaries**: Budget limits, timeline constraints, security requirements, reliability tiers, integration requirements.

6. **Cross-references**: Document IDs and section numbers that establish dependencies. Format as `{DOC-ID}` for machine parsing.

7. **State machines and transitions**: Lifecycle states, stage progressions, valid transitions, and explicit backward transition rules.

8. **Exception cases**: "When NOT to use this pattern", "Unless X", "Except when Y". These are frequently missed—hunt for them.

9. **Implicit conventions made explicit**: If the document demonstrates a pattern (like ID naming) without stating the rule, extract and state the rule explicitly with a note: `[Implicit in source, made explicit]`.

### What to COMPRESS (reduce verbosity, preserve meaning)

1. **Motivational prose**: "This is important because..." → preserve the reason, drop the framing.

2. **Repeated concepts**: If the same idea appears in introduction, body, and conclusion, consolidate to single authoritative statement.

3. **Example proliferation**: Keep 1-2 canonical examples per concept. Drop redundant variations unless they illustrate edge cases.

4. **Historical context**: Compress to single line unless the history affects current interpretation.

5. **Formatting verbosity**: Tables with sparse data → bulleted lists. Nested bullets with single items → inline.

### What to OMIT (low signal for LLM consumption)

1. **Meta-commentary**: "This section will discuss..." "As mentioned above..."

2. **Placeholder content**: TBD sections with no substance (but DO flag them in Open Questions).

3. **Redundant cross-references**: If dependency is listed in frontmatter, don't repeat in body unless adding context.

4. **Stylistic choices**: Section ordering rationale, formatting decisions, document structure explanations.

5. **Acknowledgments and attribution prose**: Preserve author in frontmatter, drop prose attribution.

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

## Type-Specific Extraction Guidance

### For DEFINITION documents (DD-*)

Add section:
```
## Definition Matrix
| Term | Category | Constraints | See Also |
|------|----------|-------------|----------|
```

Focus on: Complete enumeration of defined terms, valid values for each category, explicit boundaries between categories.

Hunt for: Implicit hierarchies, unstated defaults, edge case classifications.

### For STANDARD documents (STD-*)

Add section:
```
## Compliance Checklist
- [ ] {Requirement 1}
- [ ] {Requirement 2}
```

Focus on: Testable requirements, validation criteria, required vs. optional fields.

Hunt for: "MUST include", "SHOULD validate", schema requirements, error handling expectations.

### For ADR documents (ADR-*)

Add section:
```
## Decision Record
- **Status**: {proposed|accepted|deprecated}
- **Decision**: {one-line decision statement}
- **Alternatives Rejected**: {list with brief rationale for each}
- **Consequences Accepted**: {explicit trade-offs}
```

Focus on: The actual decision, why alternatives were rejected, what trade-offs were knowingly accepted.

Hunt for: Implicit constraints that drove the decision, unstated assumptions, reversibility conditions.

### For RESEARCH FINDINGS documents (RF-*)

Add section:
```
## Evidence Summary
| Claim | Tier | Source | Freshness |
|-------|------|--------|-----------|
```

Focus on: Source tier ratings, confidence levels, methodology limitations, implications for decisions.

Hunt for: Hedged language ("may", "likely", "suggests"), unstated confidence intervals, source conflicts.

### For SYSTEM SPEC documents (SYS-*)

Add sections:
```
## Architecture Layers
{Numbered list of layers with one-line descriptions}

## Constraint Summary
| Constraint | Value | Source |
|------------|-------|--------|
```

Focus on: Layer boundaries, cross-layer dependencies, hard constraints vs. preferences.

Hunt for: Implicit ordering requirements, unstated failure modes, assumed capabilities.

## Quality Checklist

Before finalizing, verify:

- [ ] All MUST/SHOULD/MAY statements extracted
- [ ] All enumerations complete (states, tiers, roles, types)
- [ ] All cross-references formatted as `{DOC-ID}`
- [ ] No ambiguities resolved through interpretation
- [ ] Exception cases ("when NOT to") captured
- [ ] Implicit conventions made explicit and marked
- [ ] Frontmatter links array populated with valid relationships
- [ ] Glossary includes all terms defined in source
- [ ] Open Questions captures all TBDs and flagged ambiguities
- [ ] Document is self-contained (reader shouldn't need source for comprehension)

## Anti-Patterns to Avoid

1. **Over-compression**: Dropping qualifiers that change meaning. "SHOULD validate" ≠ "validates".

2. **Under-compression**: Preserving verbose prose that adds no semantic content.

3. **Interpretation creep**: Adding "clarifications" that aren't in the source.

4. **Reference decay**: Dropping section numbers from cross-references, making them unfindable.

5. **Example over-retention**: Keeping 5 examples when 1 canonical example suffices.

6. **Glossary sprawl**: Including common terms that don't have document-specific definitions.

7. **Staleness blindness**: Not flagging dated content or time-sensitive claims.

## Output Validation

The compacted document should:

1. **Enable reconstruction**: A reader with only the LLM view should understand all rules, constraints, and decisions without accessing the source.

2. **Support machine parsing**: Consistent formatting, predictable section structure, parseable frontmatter.

3. **Flag its own gaps**: Open Questions should surface anything the compactor couldn't confidently extract.

4. **Maintain traceability**: Source document ID and date in frontmatter, major sections traceable to source sections.

5. **Be ~30-50% the length of source**: If significantly longer, you're under-compressing. If significantly shorter, audit for content loss.
```

---

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

Output a structured review with specific line references.
```

---

## Rationale

This prompt structure addresses the specific extraction variance patterns identified in LLM documentation evaluation:

| Variance Pattern | Prompt Countermeasure |
|-----------------|----------------------|
| Buried information in long documents | "Hunt for" directives in type-specific guidance |
| Implicit conventions | Explicit instruction to surface and mark implicit patterns |
| Inconsistent terminology | Ambiguity protocol with flagging requirements |
| Exception cases missed | Dedicated "When NOT to" extraction rule |
| Cross-reference decay | Strict `{DOC-ID}` formatting requirement |
| Over-interpretation | "DO NOT resolve ambiguity" as primary directive |
| State/tier divergence | Complete enumeration requirement, no truncation |

---

## Parallel Orchestration Patterns

When processing documents in parallel with fresh context windows, cross-document consistency cannot be maintained during extraction. These patterns mitigate drift and enable post-hoc reconciliation.

### The Problem

| Risk | Cause | Example |
|------|-------|---------|
| **Terminology drift** | No shared glossary | Doc A extracts "lifecycle state", Doc B extracts "artifact status" for same concept |
| **Enumeration divergence** | Partial extraction | Doc A lists 5 tiers, Doc B lists 4 (missed T5) |
| **Cross-reference blindness** | Can't validate links | Doc A references DD-15 §3.2 which doesn't exist |
| **Definition inconsistency** | Same term, different definitions | "Active" defined differently in DD-13 vs DD-15 extractions |

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

## Document Map (for cross-reference validation)
{paste from SHARED-CONTEXT.yaml}
</shared_context>
```

**Pros**: Highest consistency, catches conflicts during extraction
**Cons**: Requires identifying anchor documents, sequential bottleneck in Phase 1

---

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
│   4. Generate RECONCILIATION-REPORT.md                  │
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

## Recommended Repairs
For each flagged document, specify:
- Document ID
- Section to repair
- Specific instruction
```

**Pros**: Maximum parallelism, systematic issue detection
**Cons**: Three phases, repair phase may be significant

---

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
 Extract glossary + enumerations from Wave 1 outputs
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

---

### Pattern 4: Anchor + Satellite

**When to use**: One or few "master" documents define most shared concepts.

**Process**:

```
Step 1: Compact anchor document(s) with extra rigor
┌─────────────────────────────────────────────────────────┐
│ SYS-00 compaction with ANCHOR flag                      │
│ - Extract ALL defined terms into structured glossary    │
│ - Extract ALL enumerations with completeness check      │
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
- Do not redefine anchor terms in your glossary"
```

**Pros**: Simplest model, single sequential step
**Cons**: Only works if anchor coverage is high

---

### Recommended Pattern by Corpus Type

| Corpus Characteristic | Recommended Pattern | Rationale |
|----------------------|---------------------|-----------|
| <10 documents, clear hierarchy | Dependency-Ordered Waves | Natural fit, manageable waves |
| 10-30 documents, one master doc | Anchor + Satellite | SYS-00 defines most terms |
| 30+ documents, need speed | Three-Phase Pipeline | Maximum parallelism, systematic repair |
| High consistency requirement | Pre-Flight Context Injection | Catches conflicts during extraction |
| Unknown structure | Three-Phase Pipeline | Reconciliation reveals structure |

---

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

## Canonical Glossary
{{GLOSSARY}}

## Canonical Enumerations
### Lifecycle States
{{LIFECYCLE_STATES}}

### Source Tiers
{{SOURCE_TIERS}}

### Roles
{{ROLES}}

## Document Map
{{DOCUMENT_MAP}}
</injected_context>
```

---

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
```

---

## Model Selection Strategy

Different pipeline phases have different cognitive profiles. Model selection should balance capability, context window, cost, and throughput.

### Task Cognitive Profiles

| Task | Reasoning Depth | Context Needs | Judgment Calls | Error Cost |
|------|----------------|---------------|----------------|------------|
| **Anchor extraction** | High | Medium | Many | High (propagates) |
| **Standard compaction** | Medium | High | Moderate | Medium |
| **Reconciliation** | High | Medium-High | Many | High |
| **Repair decisions** | High | Low-Medium | Many | Medium |
| **Targeted repair** | Medium | Medium | Few (directed) | Low |
| **Validation/QA** | Low-Medium | High | Few | Low |

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

| Phase | Model | Rationale |
|-------|-------|-----------|
| Anchor extraction | **Opus** | High-stakes; errors propagate to all satellites. Worth the cost. |
| Context YAML generation | **Haiku** | Mechanical transformation of extracted data. |
| Satellite compaction | **Sonnet** | Bulk parallel; needs full context window for large sources. |
| Validation pass | **Haiku** | Schema compliance, format checks. |

#### Pattern 2 (Three-Phase Pipeline)

| Phase | Model | Rationale |
|-------|-------|-----------|
| Phase 1: Raw extraction | **Sonnet** | Needs full source context; moderate judgment. |
| Phase 2: Reconciliation | **Opus** | Cross-document reasoning, conflict detection, judgment-heavy. |
| Phase 3: Targeted repair | **Sonnet** | Directed fixes with specific instructions; lower judgment. |
| Final validation | **Haiku** | Mechanical compliance checking. |

#### Pattern 3 (Dependency Waves)

| Phase | Model | Rationale |
|-------|-------|-----------|
| Wave 1 (foundations) | **Opus** | These define canonical terms; errors cascade. |
| Context extraction | **Haiku** | Mechanical YAML generation. |
| Wave 2+ (dependent docs) | **Sonnet** | Standard compaction with injected context. |
| Cross-wave validation | **Sonnet** | Check context accumulation correctness. |

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

| Validation Type | Model | Per-Doc Cost | Batch Strategy |
|-----------------|-------|--------------|----------------|
| Schema compliance | Haiku | ~$0.001 | Run on all |
| Enumeration completeness | Haiku | ~$0.002 | Run on all |
| Cross-reference validity | Haiku | ~$0.003 | Run on all |
| Semantic accuracy | Sonnet | ~$0.02 | Sample 20% |
| Deep judgment review | Opus | ~$0.15 | Only flagged |

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

| Model | Common Failure | Detection | Mitigation |
|-------|---------------|-----------|------------|
| **Haiku** | Misses nuance, over-simplifies | Spot-check samples with Sonnet | Use only for mechanical tasks |
| **Sonnet** | Resolves ambiguity instead of flagging | Check Open Questions section is populated | Strong prompt emphasis on flagging |
| **Opus** | Over-engineering, excessive detail | Output length > 50% of source | Add compression ratio check |

### Example Cost Estimation

For a 30-document corpus (Compass-scale):

| Strategy | Opus Calls | Sonnet Calls | Haiku Calls | Est. Cost |
|----------|-----------|--------------|-------------|-----------|
| All Opus | 30 | 0 | 0 | ~$4.50 |
| All Sonnet | 0 | 30 | 0 | ~$0.60 |
| Recommended mix | 5 | 25 | 30 | ~$1.10 |
| With Opus review | 5 + 10 review | 25 | 30 | ~$1.85 |

*Estimates assume ~5K tokens input, ~2K tokens output per document. Actual costs vary.*

---

## Version History

- 2026-02-03: Initial version based on LLM documentation evaluation findings
- 2026-02-03: Added parallel orchestration patterns for fresh-context-window processing
- 2026-02-03: Added model selection strategy for capability/context/cost optimization
