---
id: DD-12-01-LLM
type: definition
area: 12-repository-structure
title: Repository Structure and Organization (LLM View)
created: 2026-02-03
updated: 2026-02-03
summary: LLM-optimized view of repository structure, naming conventions, and navigation standards
tags: [repository, structure, naming, llms, index, llm, view]
links:
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
view: llm
source_id: DD-12-01
source_updated: 2026-02-03
staleness: fresh
---

# Repository Structure and Organization (LLM View)

## LLM Summary
DD-12 defines the Compass repository structure and conventions so both humans and LLMs can reliably find and maintain documentation. It specifies the specialized docs-only topology, folder roles, naming rules, canonical IDs, and cross-repo reference patterns. It sets GitHub Flow and branch naming for documentation changes, plus PR requirements and maintenance rhythms. It formalizes LLM navigation aids, including `llms.txt` at the repo root and per-folder `INDEX.md` files, and requires shallow nesting and self-contained sections for retrieval. It adds structured cross-linking via frontmatter `links` as the preferred mechanism while keeping `related` for legacy associations. It also defines LLM view conventions and a repeatable update workflow with staleness rules so derived views stay in sync. These conventions reduce context loss, prevent drift, and make artifact relationships explicit. The document is a structural contract for documentation organization, not content.

## Canonical Statements
- Every repository MUST include `llms.txt` at the root for LLM navigation.
- Every artifact folder MUST include an `INDEX.md` file.
- File names MUST follow `{PREFIX}-{identifier}-{descriptive-title}.md`.
- Artifacts MUST use canonical IDs that survive renames and moves.
- Repositories SHOULD keep nesting to a maximum of three levels.
- Sections SHOULD be self-contained and retrievable in isolation.
- Documentation changes MUST follow GitHub Flow with PR review.

## Scope and Non-Goals
- In scope: Repository layout, naming conventions, navigation, and LLM-friendly structure.
- Out of scope: Content of individual artifacts, tool selection, or implementation details.

## Dependencies and Interfaces
- Artifact taxonomy and frontmatter: `DD-13-01`.
- System requirements and principles: `SYS-00`.

## Core Invariants
- Shallow nesting (max three levels).
- Self-contained sections for retrieval.
- Explicit navigation via `llms.txt` and `INDEX.md`.
- Canonical IDs for stable references.

## Glossary Snapshot
- **Canonical ID**: Stable identifier that survives file moves.
- **llms.txt**: Root navigation file designed for LLM consumption.
- **RAG**: Retrieval-Augmented Generation for grounded responses.
- **INDEX.md**: Per-folder navigation index.
