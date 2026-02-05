---
id: DD-20-01-LLM
type: definition
area: 20-evidence-standards
title: Evidence Standards for Citations and Sources (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of evidence grading, source taxonomy, and freshness rules
tags: [evidence, citations, sources, research, llm, view]
links:
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: companion
    target_id: "STD-20-01"
view: llm
source_id: DD-20-01
source_updated: 2026-02-03
staleness: fresh
---

# Evidence Standards for Citations and Sources (LLM View)

## LLM Summary
DD-20 defines evidence standards for Compass research and citations. It introduces a three-part grading framework: Source Reliability (S1-S4), Information Quality (I1-I4), and overall Confidence (high/medium/low) with estimative language guidance. It provides a five-tier source taxonomy (T1-T5) from authoritative vendor docs to unverified sources and warns against over-trusting community answers, noting high obsolescence risk. The document specifies rules for assigning ratings, recommends using multiple corroborating sources for I1, and emphasizes staleness control with `retrieved_at`, version context, and content hashes to detect changes. It also defines freshness expectations, version pinning guidance, and how evidence supports decision-making in RF and ADR artifacts. It provides language patterns to communicate uncertainty and probability. DD-20 is the conceptual foundation; STD-20 provides the enforceable citation format and compliance checklist.

## Canonical Statements
- Every research claim MUST be assessed for source reliability, information quality, and overall confidence.
- Sources MUST be classified into tiers T1-T5.
- Citations MUST include `retrieved_at` to track freshness.
- Version context SHOULD be recorded when software behavior is version-specific.
- Content hashes SHOULD be stored to detect changes in cited sources.

## Scope and Non-Goals
- In scope: Evidence grading, source taxonomy, and staleness rules.
- Out of scope: Exact citation formats and JSON schema details (see `STD-20-01`).

## Dependencies and Interfaces
- Citation format specification: `STD-20-01`.
- Artifact metadata requirements: `DD-13-01`.

## Core Invariants
- Evidence quality is multi-dimensional (S/I/Confidence).
- Source tiers communicate trust at a glance.
- Freshness and version context are required to prevent drift.

## Glossary Snapshot
- **S1-S4**: Source reliability scale from established to questionable.
- **I1-I4**: Information quality scale from verified to unverified.
- **T1-T5**: Source tier taxonomy from authoritative to unverified.
- **retrieved_at**: Timestamp of when a source was accessed.
