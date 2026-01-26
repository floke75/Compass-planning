---
id: DD-12-01
type: definition
area: 12-repository-structure
title: Repository Structure and Organization Standards
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Defines the repository structure, naming conventions, and organization patterns for Compass documentation and artifacts
tags: [repository, structure, naming, git, organization]
related:
  - DD-13-01
  - DD-14-01
---

# Repository Structure and Organization Standards

## Document Purpose

This document establishes the authoritative repository structure, naming conventions, and organizational patterns for EFN's Compass system. It defines where different artifact types live, how files are named, how cross-repository references work, and how the repository supports both human navigation and LLM retrieval.

**Why this matters**: Repository structure directly impacts how effectively LLM agents can find and use documentation. Poor organization leads to missed context, duplicated work, and documentation that drifts from reality. Good organization makes artifacts discoverable, relationships clear, and maintenance sustainable.

**Audience**: Builders, product owners, and anyone creating or maintaining Compass artifacts.

---

## Part 1: Repository Topology

### 1.1 The Specialized Pattern

EFN uses the **specialized documentation pattern**: a dedicated documentation repository with strategic links to implementation repositories.

**What this means in practice:**

- Planning artifacts (specs, requirements, decisions, research) live in a central `compass` repository
- Implementation code lives in separate repositories per tool/project
- The `compass` repository is the source of truth for *intent*; implementation repos are the source of truth for *execution*
- Bidirectional links connect planning artifacts to their implementations

**Why this pattern:**

| Alternative | Why Not |
|-------------|---------|
| Docs alongside code (sidecar) | Planning artifacts evolve at different pace than code; review workflows differ |
| Completely separate docs (orthogonal) | Loses connection between planning and implementation |
| Distributed docs, central aggregation (federated) | Too complex for 2-3 person team |

The specialized pattern recognizes that specifications and code have different lifecycles. A spec might be written weeks before implementation and revised after implementation completes. Keeping them in the same repository creates merge conflicts and unclear ownership.

### 1.2 Spec-Driven Development

Specifications are the single source of truth for humans and AI agents. The workflow is:

```
Intent → Specification → Implementation → Reconciliation → Updated Specification
```

This means:
- No significant implementation begins without a specification
- Implementation must match spec, or spec must be updated
- Specs survive implementation—they remain authoritative even after code ships
- When code diverges from spec, the spec is updated to reflect reality (see DD-13-01 for reconciliation protocol)

---

## Part 2: Folder Structure

### 2.1 Complete Repository Layout

```
compass/
├── llms.txt                              # AI navigation index (see 2.3)
├── INDEX.md                              # Master navigation for humans
├── README.md                             # Repository overview and quickstart
│
├── specs/                                # SPEC- prefix artifacts
│   ├── INDEX.md                          # Spec navigation
│   ├── SPEC-{project}-{feature}.md       # Feature specifications
│   └── stories/                          # User stories (optional subdivision)
│       └── SPEC-{project}-{story}.md
│
├── decisions/                            # ADR- prefix artifacts
│   ├── INDEX.md                          # Decision log navigation
│   ├── ADR-0000-use-madr-format.md       # First ADR: format choice
│   └── ADR-{NNNN}-{decision-title}.md    # Numbered decisions
│
├── research/                             # RF- and RB- prefix artifacts
│   ├── INDEX.md                          # Research navigation
│   ├── briefs/                           # Research briefs (RB-)
│   │   └── RB-{area}-{topic}.md          # Research task definitions
│   └── findings/                         # Research findings (RF-)
│       └── RF-{area}-{topic}.md          # Completed research
│
├── definitions/                          # DD- prefix artifacts
│   ├── INDEX.md                          # Definition navigation
│   └── DD-{area}-{topic}.md              # Definition documents
│
├── standards/                            # STD- prefix artifacts
│   ├── INDEX.md                          # Standards navigation
│   └── STD-{area}-{topic}.md             # Enforceable standards
│
├── handoffs/                             # HANDOFF- prefix artifacts
│   ├── INDEX.md                          # Handoff navigation
│   └── HANDOFF-{project}-{version}.md    # Implementation handoff bundles
│
├── indexes/                              # IDX- prefix artifacts
│   ├── IDX-master.md                     # Cross-cutting index
│   └── IDX-{domain}.md                   # Domain-specific indexes
│
├── guidelines/                           # AI coding guidelines
│   ├── AGENTS.md                         # Global agent instructions
│   ├── coding.guideline.md               # Always-apply coding rules
│   └── domain/                           # Domain-specific guidelines
│       └── {area}.guideline.md
│
├── templates/                            # Document templates
│   ├── SPEC-template.md
│   ├── ADR-template.md
│   ├── RF-template.md
│   ├── DD-template.md
│   ├── STD-template.md
│   └── HANDOFF-template.md
│
└── .github/                              # GitHub configuration
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── lint-docs.yaml                # Automated validation
```

### 2.2 Folder-to-Artifact-Type Mapping

| Folder | Artifact Type | Prefix | Purpose |
|--------|---------------|--------|---------|
| `specs/` | Specification | SPEC- | Implementation-ready instructions |
| `decisions/` | Architecture Decision Record | ADR- | Why decisions were made |
| `research/briefs/` | Research Brief | RB- | Research task definitions |
| `research/findings/` | Research Finding | RF- | Completed research results |
| `definitions/` | Definition Document | DD- | Foundational definitions and taxonomies |
| `standards/` | Standard | STD- | Enforceable conventions |
| `handoffs/` | Handoff Bundle | HANDOFF- | Implementation packages |
| `indexes/` | Index | IDX- | Navigation and cross-reference documents |
| `guidelines/` | Guideline | (none) | AI agent instructions |
| `templates/` | Template | (none) | Document templates |

**Why these folders exist:**

- **specs/**: The core output of Compass planning—what to build
- **decisions/**: The reasoning behind choices—why we chose this approach
- **research/**: Investigation outputs—what we learned
- **definitions/**: Foundational concepts—what terms mean
- **standards/**: Shared rules—how we do things consistently
- **handoffs/**: Transition packages—everything an implementation agent needs
- **indexes/**: Navigation aids—how to find things
- **guidelines/**: Agent instructions—how LLMs should behave
- **templates/**: Starting points—how to create new documents

### 2.3 The llms.txt Navigation Index

Every Compass repository includes an `llms.txt` file at the root. This file provides structured navigation for LLM agents, reducing token consumption and improving retrieval accuracy.

**Format:**

```markdown
# Compass Documentation

> LLM-orchestrated planning, research, and documentation system for EFN

## Quick Links

- [Master Index](INDEX.md): Start here for navigation
- [Agent Instructions](guidelines/AGENTS.md): Rules for LLM agents

## Specifications
- [specs/INDEX.md](specs/INDEX.md): All feature specifications

## Decisions
- [decisions/INDEX.md](decisions/INDEX.md): Architecture decision log

## Research
- [research/INDEX.md](research/INDEX.md): Research briefs and findings

## Standards
- [standards/INDEX.md](standards/INDEX.md): Enforceable conventions

## Definitions
- [definitions/INDEX.md](definitions/INDEX.md): Foundational definitions
```

**Why llms.txt:**
- Provides a single entry point for AI tools
- Reduces context window consumption (10x fewer tokens than HTML)
- Works with Cursor, Claude, ChatGPT, and other LLM interfaces
- Human-readable as a bonus

### 2.4 Index Documents

Every folder containing artifacts has an INDEX.md file. These indexes serve both humans and LLMs:

**INDEX.md structure:**

```markdown
# [Folder Name] Index

## Purpose
[What artifacts live here and why]

## Document List

| ID | Title | Status | Last Updated | Summary |
|----|-------|--------|--------------|---------|
| SPEC-001 | Authentication Flow | active | 2026-01-24 | OAuth2 login implementation |
| SPEC-002 | Data Visualization | draft | 2026-01-25 | Broadcast graphics pipeline |

## Recently Updated
- [SPEC-002](SPEC-002-data-visualization.md) - 2026-01-25

## See Also
- [Related folder](../related/)
```

---

## Part 3: Naming Conventions

### 3.1 File Naming Rules

**Format:** `{PREFIX}-{identifier}-{descriptive-title}.md`

**Case:** kebab-case (lowercase with hyphens)

**Examples:**
- `SPEC-auth-oauth2-flow.md`
- `ADR-0001-use-postgresql-database.md`
- `RF-03-memory-architecture.md`
- `DD-14-ecosystem-requirements.md`
- `STD-14-compliance-checklist.md`

**Rules:**

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Use kebab-case | `user-authentication.md` | `user_authentication.md`, `UserAuthentication.md` |
| Include prefix | `SPEC-auth-login.md` | `auth-login.md` |
| Keep under 50 characters | `ADR-0001-use-postgres.md` | `ADR-0001-use-postgresql-for-primary-database-storage.md` |
| Use descriptive titles | `SPEC-api-rate-limiting.md` | `SPEC-feature-42.md` |
| Alphanumerics and hyphens only | `RF-01-vendor-analysis.md` | `RF-01-vendor_analysis (draft).md` |

### 3.2 Prefix Conventions

| Prefix | Usage | Numbering |
|--------|-------|-----------|
| SPEC- | Specifications | Project + feature identifier |
| ADR- | Architecture Decision Records | Sequential 4-digit number (0001, 0002...) |
| RB- | Research Briefs | Area code + sequential number |
| RF- | Research Findings | Area code + sequential number |
| DD- | Definition Documents | Area code + sequential number |
| STD- | Standards | Area code + sequential number |
| HANDOFF- | Handoff Bundles | Project + version |
| IDX- | Indexes | Domain name |

**Area codes** correspond to the Compass Research Program areas:
- 01: Backend Platform
- 02: LLM Orchestration
- 03: Memory & Retrieval
- 04: Documentation Platform
- 05: PM Integration
- 06: Research Tools
- 07: Widget Libraries
- 08: Hosting
- 09: LLM Provider
- 10: Dev Tooling
- 11: Handoff Schema
- 12: Repository Structure
- 13: Artifact Taxonomy
- 14: EFN Ecosystem
- 15: Governance
- 16: Reliability Tiers
- 17: Integration Patterns
- 18: Questioning Arc
- 19: Widget Schema
- 20: Evidence Standards

### 3.3 ADR Numbering

ADRs use sequential 4-digit numbers because decision order matters for understanding evolution:

```
ADR-0000-use-madr-format.md       # First decision: how to record decisions
ADR-0001-select-backend.md        # Platform choice
ADR-0002-authentication-approach.md
ADR-0003-supersede-auth-approach.md  # Supersedes ADR-0002
```

**Never reuse ADR numbers.** If ADR-0005 is superseded, the replacement is ADR-0010 (or whatever the next number is), not a new ADR-0005.

### 3.4 Title Conventions

Use **active voice** and **descriptive nouns** in titles:

| Good | Bad | Why |
|------|-----|-----|
| `use-postgresql-for-database` | `database-selection` | Active voice indicates decision |
| `adopt-github-flow` | `branching-strategy` | Describes what, not just topic |
| `authentication-oauth2-flow` | `auth-stuff` | Specific and searchable |

---

## Part 4: Cross-Repository References

### 4.1 Reference Patterns

**Within the compass repository:** Use relative links.

```markdown
See [Authentication Spec](../specs/SPEC-auth-oauth2-flow.md) for details.
This implements [ADR-0001](../decisions/ADR-0001-select-backend.md).
```

**To implementation repositories:** Use full URLs.

```markdown
Implementation: [github.com/efn/broadcast-tools](https://github.com/efn/broadcast-tools)
```

**From implementation to compass:** Reference by artifact ID.

```python
# Implements SPEC-broadcast-data-viz
# See: https://github.com/efn/compass/specs/SPEC-broadcast-data-viz.md
```

### 4.2 Canonical IDs

Every artifact has a canonical ID in its frontmatter. Use these IDs for references that need to survive file moves:

```markdown
This decision is documented in ADR-0001.
```

If the file is renamed or moved, the ID remains stable. Tooling can resolve IDs to current file locations.

### 4.3 Avoiding Broken Links

**Prevention:**
- Use relative links within repos
- Use IDs for cross-repo references
- Run link validation on every PR

**Detection:**
- `markdownlint` for Markdown syntax
- Link checker tools in CI pipeline
- Periodic full-repo validation

**Recovery:**
- When links break, update the reference
- Consider adding redirects for commonly-linked documents
- Log broken link fixes in commit messages for traceability

---

## Part 5: Git Workflow

### 5.1 GitHub Flow for Documentation

EFN uses GitHub Flow for documentation:

1. Create a branch for your change
2. Make changes and commit
3. Open a Pull Request
4. Get review from at least one other team member
5. Merge to main

**Why GitHub Flow:**
- Simple enough for non-traditional developers
- Provides review checkpoint for quality
- Creates clear audit trail
- Works with standard GitHub tooling

### 5.2 Branch Naming

**Pattern:** `docs/{type}/{topic}`

| Type | Usage | Example |
|------|-------|---------|
| `feature` | New content | `docs/feature/authentication-spec` |
| `decision` | ADR in progress | `docs/decision/choose-database` |
| `research` | Research investigation | `docs/research/memory-architecture` |
| `fix` | Corrections | `docs/fix/broken-links` |
| `update` | Updates to existing docs | `docs/update/api-reference` |

### 5.3 Decision Branch Workflow

Decision branches have special handling because ADRs shouldn't merge until a decision is actually made:

1. Create branch: `docs/decision/choose-auth-provider`
2. Create draft ADR with options being evaluated
3. Use PR description to track evaluation status
4. Keep branch open during evaluation period
5. When decision is made:
   - Update ADR with chosen option and rationale
   - Change ADR status from `proposed` to `accepted`
   - Merge the PR
6. If decision is deferred or rejected:
   - Update ADR with outcome
   - Close PR (preserves history)
   - ADR file stays in branch for reference

### 5.4 Pull Request Requirements

**Every PR must have:**
- Clear title describing the change
- Description of what changed and why
- Link to related artifacts (if updating existing docs)
- At least one reviewer (no self-approval)

**PR template:**

```markdown
## What changed
[Brief description]

## Type of change
- [ ] New artifact
- [ ] Update to existing artifact
- [ ] Fix/correction
- [ ] Restructuring

## Related artifacts
- [Link to related specs, ADRs, etc.]

## Checklist
- [ ] Frontmatter is complete and correct
- [ ] Links are valid
- [ ] Spell check passed
- [ ] Status is appropriate
```

### 5.5 Commit Message Conventions

Use clear, descriptive commit messages:

```
Add SPEC-broadcast-data-viz for graphics pipeline

- Defines data flow from CSV/Excel to broadcast-ready graphics
- Includes acceptance criteria and constraints
- References ADR-0005 for format decisions
```

**Format:**
- First line: summary (imperative mood, <72 characters)
- Blank line
- Body: details, context, references

---

## Part 6: Validation and Quality

### 6.1 Automated Validation

The following checks run on every PR:

| Check | Tool | What It Catches |
|-------|------|-----------------|
| Markdown syntax | markdownlint | Formatting errors |
| Frontmatter validation | Custom script | Missing required fields |
| Link checking | markdown-link-check | Broken internal links |
| Spell check | cspell | Typos |

### 6.2 Validation Checklist

Before submitting any document for review:

**Frontmatter:**
- [ ] `id` is unique and follows prefix conventions
- [ ] `type` matches the artifact type
- [ ] `status` is appropriate (usually `draft` for new docs)
- [ ] `created` and `updated` dates are correct
- [ ] `author` is identified
- [ ] `summary` is a single, clear sentence
- [ ] `tags` are relevant and consistent with existing tags
- [ ] `related` links to connected artifacts

**Content:**
- [ ] Document follows the template for its type
- [ ] Links use relative paths within repo
- [ ] Cross-references use artifact IDs
- [ ] No placeholder text remains
- [ ] Spelling and grammar checked

**Structure:**
- [ ] File is in the correct folder
- [ ] Filename follows naming conventions
- [ ] Relevant INDEX.md is updated

### 6.3 Periodic Maintenance

**Monthly:**
- Review and update indexes
- Check for stale documents (not updated in 90+ days)
- Validate all cross-repo links

**Quarterly:**
- Full link validation across all repos
- Review tag taxonomy for consistency
- Archive deprecated documents
- Update templates based on lessons learned

---

## Part 7: LLM Optimization

### 7.1 Principles for LLM-Friendly Structure

**Shallow nesting:** Maximum 3 levels deep. LLMs work better with flatter structures.

**Self-contained sections:** Each major section should be understandable without the full document. This enables RAG systems to retrieve relevant sections effectively.

**Explicit navigation:** Every folder has an INDEX.md. Every document has clear frontmatter. Never assume the reader has seen other documents.

**Semantic naming:** File names describe content. Avoid generic names like `notes.md` or `draft-v2.md`.

### 7.2 AGENTS.md File

The `guidelines/AGENTS.md` file provides global instructions for LLM agents:

```markdown
# Agent Instructions for Compass

## Document Hierarchy
1. **Specifications** in `specs/` are implementation-ready. Follow them precisely.
2. **ADRs** in `decisions/` explain why. Consult when specs seem unclear.
3. **Standards** in `standards/` are mandatory conventions. Always follow.
4. **Definitions** in `definitions/` explain concepts. Reference for understanding.

## Boundaries

### Always
- Check for existing specs before proposing new work
- Follow standards in STD- documents
- Update related specs when implementation deviates
- Use templates for new documents

### Ask First
- Creating new artifact types not in the taxonomy
- Changing document structure or conventions
- Modifying standards documents

### Never
- Delete or overwrite ADRs (create superseding documents)
- Merge without review
- Use placeholder content in merged documents

## When Specifications Are Ambiguous
1. Check related ADRs for context
2. Check Standards for conventions
3. Document your interpretation in implementation notes
4. Flag for human review
```

### 7.3 Chunking-Aware Writing

Write sections that can stand alone when retrieved:

**Good:**
```markdown
## OAuth2 Token Refresh

This section describes how clients refresh expired access tokens.

### Prerequisites
- Valid refresh token in secure cookie
- Client ID configured in environment

### Process
1. Client detects 401 response
2. Client calls POST /auth/refresh
3. Server validates and issues new token
4. Client retries original request
```

**Bad:**
```markdown
## Token Refresh

As mentioned above, this builds on the previous section.
See the earlier discussion for prerequisites.
The process is similar to what we described before.
```

The good example can be understood in isolation. The bad example requires context that may not be retrieved together.

---

## Appendix A: Glossary

**Canonical ID**: The unique identifier in a document's frontmatter that survives file renames.

**GitHub Flow**: A lightweight branching workflow where all changes go through branches and pull requests.

**kebab-case**: Lowercase words separated by hyphens (like-this-example).

**llms.txt**: A navigation index file designed for LLM consumption.

**RAG**: Retrieval-Augmented Generation—using retrieved documents to ground LLM responses.

**Specialized pattern**: Repository topology where documentation and implementation live in separate repos with explicit links.

---

## Appendix B: Related Documents

- **DD-13-01**: Artifact taxonomy and documentation standards
- **DD-14-01**: EFN tooling ecosystem requirements
- **STD-14-01**: EFN shared standards and compliance checklist
- **Compass System Definition**: Authoritative system specification

---

## Appendix C: Research Foundation

This document synthesizes patterns from:
- BMAD Method repository organization (31,600+ GitHub stars)
- Google, 18F, and Harvard data management naming conventions
- llms.txt standard by Jeremy Howard (Answer.AI)
- GitHub Flow documentation practices
- Kubernetes Enhancement Proposals (KEP) structure
- MADR (Markdown Architectural Decision Records) v4.0

---

*End of Repository Structure and Organization Standards (DD-12-01)*
