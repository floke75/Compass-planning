---
id: DD-20-01
type: definition
area: 20-evidence-standards
title: Evidence Standards for Citations and Sources
status: draft
created: 2026-01-25
updated: 2026-02-03
author: compass-research
summary: Defines evidence grading, source classification, citation formats, and staleness rules for Compass research artifacts
tags: [evidence, citations, sources, research, quality]
related:
  - STD-20-01
  - DD-13-01
  - DD-12-01
links:
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-12-01"
  - rel: companion
    target_id: "STD-20-01"
companion: STD-20-01
---

# Evidence Standards for Citations and Sources

## Document Purpose

This document establishes the evidence standards for Compass documentation. It defines how sources are classified, how evidence quality is assessed, how citations are formatted, and when information becomes stale. These standards ensure that research findings are credible, verifiable, and appropriately qualified.

**Why this matters**: LLM-driven development depends on accurate, current information. Poor evidence practices lead to hallucinated facts, outdated recommendations, and decisions based on unreliable sources. Rigorous evidence standards enable implementation agents to trust research outputs and make the documentation credible over time.

**Audience**: Anyone conducting research, creating Research Findings, or reviewing documentation that includes citations.

**Companion document**: STD-20-01 provides the enforceable citation format specification with examples and a compliance checklist.

---

## Part 1: Evidence Grading Framework

Compass uses a three-dimensional framework to assess evidence quality. Each dimension captures a different aspect of credibility.

### 1.1 The Three Dimensions

| Dimension | Question Answered | Scale |
|-----------|------------------|-------|
| **Source Reliability** | How trustworthy is this source in general? | S1–S4 |
| **Information Quality** | How well-supported is this specific claim? | I1–I4 |
| **Confidence** | How certain are we overall? | High / Medium / Low |

Using all three dimensions prevents common errors:
- A reliable source (S1) can still provide unverified information (I4) on a specific claim
- Multiple unreliable sources (S3) can corroborate each other to produce supported information (I2)
- Overall confidence synthesizes source reliability, information quality, and practical judgment

### 1.2 Source Reliability (S1–S4)

Source reliability measures the general trustworthiness of a source based on track record, editorial oversight, and expertise.

| Rating | Label | Definition | Examples |
|--------|-------|------------|----------|
| **S1** | Established | Official vendor source, verified expertise, consistent accuracy track record | Official documentation, published APIs, peer-reviewed papers |
| **S2** | Credible | Reputable source with editorial oversight, generally reliable | Major tech publications, established expert blogs, high-vote Stack Overflow |
| **S3** | Uncertain | Unknown track record, requires independent verification | Personal blogs, low-vote forum answers, unfamiliar sources |
| **S4** | Questionable | Anonymous, biased, or previously inaccurate—use with explicit caution | Anonymous forums, known-biased sources, AI-generated content without verification |

**Assignment rules:**

1. **Is it from the official vendor/maintainer?** → S1
2. **Does it have peer review or high community validation (50+ votes)?** → S2
3. **Is it from an established platform with editorial oversight?** → S3
4. **None of the above?** → S4

### 1.3 Information Quality (I1–I4)

Information quality measures how well-supported a specific claim is, regardless of source reliability.

| Rating | Label | Definition | What It Requires |
|--------|-------|------------|------------------|
| **I1** | Verified | Confirmed by 2+ independent sources, internally consistent, documented | Multiple corroborating sources, no contradictions |
| **I2** | Supported | Logical, consistent with related information, from single reliable source | One solid source, fits established patterns |
| **I3** | Plausible | Not contradicted, reasonable, but limited corroboration | Makes sense but single-sourced or poorly documented |
| **I4** | Unverified | Cannot confirm, potentially inconsistent—treat as hypothesis | Speculation, untested claims, contradicts other evidence |

**Assignment rules:**

1. **Can you cite 2+ independent sources that agree?** → I1
2. **Is it from one reliable source and fits known patterns?** → I2
3. **Is it plausible but poorly supported?** → I3
4. **Is it speculative or contradicted?** → I4

### 1.4 Confidence Levels

Overall confidence synthesizes source reliability, information quality, and practical judgment.

| Level | Meaning | When to Use | Language Patterns |
|-------|---------|-------------|-------------------|
| **High** | Strong evidence, minimal gaps | S1/S2 + I1/I2 ratings, no significant uncertainty | "According to X...", "The documentation confirms..." |
| **Medium** | Reasonable evidence, some uncertainty | S2/S3 + I2/I3 ratings, gaps acknowledged | "Based on available evidence...", "Likely..." |
| **Low** | Significant gaps, use cautiously | S3/S4 or I3/I4 ratings, major uncertainty | "May...", "Possibly...", "Unverified reports suggest..." |

**Estimative language** (from intelligence analysis best practices):

| Phrase | Approximate Probability |
|--------|------------------------|
| "Almost certainly" | ~95% |
| "Likely" / "Probably" | ~70% |
| "Possibly" | ~50% |
| "Unlikely" | ~25% |
| "Remote chance" | ~10% |

### 1.5 Combined Ratings

Express evidence quality as a combined rating: `S#-I#-Confidence`

**Examples:**

| Rating | Interpretation | Example Usage |
|--------|----------------|---------------|
| S1-I1-High | Official source, verified information | "According to AWS documentation (confirmed across multiple official sources)..." |
| S2-I2-Medium | Credible source, supported but single-sourced | "A Bloomberg report indicates [single authoritative source]..." |
| S3-I3-Low | Uncertain source, limited support | "An unverified forum post suggests [requires verification]..." |
| S1-I3-Medium | Official source, but claim is poorly documented | "The vendor mentions this feature, but documentation is incomplete..." |

---

## Part 2: Source Classification

### 2.1 Five-Tier Source Taxonomy

Technical documentation exists on a reliability spectrum. This taxonomy guides source selection and weighting.

#### Tier 1 — Authoritative (Highest Trust)

**What belongs here:**
- Official vendor documentation
- OpenAPI specifications from primary sources
- Release notes and changelogs from maintainers
- Primary research papers (peer-reviewed)

**Indicators:**
- Published on vendor domain
- Version-matched to the software being evaluated
- Actively maintained with clear update history

**Trust level:** Accept unless contradicted by direct testing.

---

#### Tier 2 — Validated Community

**What belongs here:**
- Highly-voted Stack Overflow answers (50+ score, accepted)
- Peer-reviewed community documentation (MDN, Wikipedia for technical topics)
- GitHub Discussions with maintainer endorsement
- Established expert blogs with multi-year track records

**Indicators:**
- High engagement metrics
- Editorial review visible
- Author credentials verifiable

**Trust level:** Generally reliable; verify against Tier 1 when stakes are high.

---

#### Tier 3 — Curated Secondary

**What belongs here:**
- Technical tutorials from reputable platforms (official partner blogs, established learning sites)
- Conference presentations and talks
- Technical books from recognized publishers
- Maintained "awesome" lists with active curation

**Indicators:**
- Institutional backing
- Clear publication/update history
- Author identified with credentials

**Trust level:** Useful for understanding, but verify specific claims.

---

#### Tier 4 — General Community

**What belongs here:**
- Blog posts from verified developers (Medium, Dev.to, personal blogs)
- GitHub issues without maintainer verification
- Tutorials without editorial oversight
- Social media posts from identified experts

**Indicators:**
- Author profile visible
- Some engagement/discussion
- No institutional backing

**Trust level:** Treat as leads for further investigation, not authoritative sources.

---

#### Tier 5 — Unverified (Use with Caution)

**What belongs here:**
- Anonymous blog posts without credentials
- Outdated Stack Overflow answers (5+ years, no updates)
- Social media posts from unknown accounts
- AI-generated content without verification
- Anonymous forum content

**Trust level:** Do not cite without explicit qualification and independent verification.

**Critical warning about Stack Overflow:** Research indicates that approximately 58% of Stack Overflow answers are already obsolete when posted, and only 20% ever receive updates. Tags for fast-moving technologies (React, Node.js, Android) have particularly high obsolescence rates. Always check answer dates and verify against official documentation.

### 2.2 Tier Assignment Flowchart

```
Is it from the official vendor/maintainer?
    YES → Tier 1
    NO ↓

Does it have peer review OR high community validation (50+ votes)?
    YES → Tier 2
    NO ↓

Is it from an established platform with editorial oversight?
    YES → Tier 3
    NO ↓

Does the author have verifiable credentials?
    YES → Tier 4
    NO → Tier 5
```

---

## Part 3: Citation Format

### 3.1 Required Citation Fields

Every citation in Compass artifacts must include these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier (format: `cite-{artifact-id}-{NNN}`) |
| `source_url` | Yes | Primary URL for the source |
| `title` | Yes | Human-readable source title |
| `source_type` | Yes | Classification (see below) |
| `retrieved_at` | Yes | When the content was accessed (ISO 8601) |

### 3.2 Recommended Additional Fields

| Field | Description |
|-------|-------------|
| `author` | Person or organization responsible |
| `date_published` | Original publication date |
| `version` | Software/API version if applicable |
| `excerpt` | Exact quoted text supporting the citation |
| `tier` | Source tier (T1–T5) |
| `reliability` | Source reliability rating (S1–S4) |

### 3.3 Source Type Values

| Value | When to Use |
|-------|-------------|
| `api_docs` | Official API documentation |
| `vendor_docs` | Other official vendor documentation |
| `announcement` | Release notes, blog posts from vendors |
| `article` | News articles, technical publications |
| `book` | Published books |
| `paper` | Academic/research papers |
| `community` | Stack Overflow, forums, GitHub issues |
| `blog` | Personal or company blogs |
| `webpage` | Other web content |

### 3.4 Citation Schema

```json
{
  "id": "cite-RF-03-01-001",
  "source_type": "api_docs",
  "title": "Authentication API Reference",
  "source_url": "https://docs.example.com/auth",
  "author": "Example Inc.",
  "date_published": "2024-11-15",
  "retrieved_at": "2026-01-25T10:30:00Z",
  "version": "v2.3",
  "excerpt": "All API requests require Bearer token authentication",
  "tier": "T1",
  "reliability": "S1"
}
```

### 3.5 In-Document Citation Format

Within Research Findings and other artifacts, cite sources using this format:

**Inline citation:**
```markdown
All API requests require Bearer token authentication [1].
```

**Source list:**
```markdown
## Sources

1. **[T1/S1]** Example Inc. "Authentication API Reference" v2.3. 
   Retrieved 2026-01-25. https://docs.example.com/auth
   
2. **[T2/S2]** Stack Overflow. "How to implement JWT refresh tokens" (Score: 127, Accepted). 
   Retrieved 2026-01-25. https://stackoverflow.com/questions/12345
```

The `[T#/S#]` prefix immediately signals source quality to readers.

---

## Part 4: Freshness and Staleness

### 4.1 Why Freshness Matters

Information decay varies by content type, but all documentation eventually becomes stale. In technical documentation:
- APIs change and deprecate
- Best practices evolve
- Security vulnerabilities emerge
- Tools and frameworks release new versions

Failing to track freshness leads to outdated recommendations, which undermines the entire documentation system.

### 4.2 Staleness Thresholds by Content Type

| Content Type | Maximum Age Before Review | Rationale |
|--------------|---------------------------|-----------|
| Critical/compliance docs | 7 days | Regulatory requirements, security |
| API documentation | Tied to version lifecycle | Shelf life matches software version |
| Official announcements | Point-in-time (never expires) | Historical record |
| Technical tutorials | Tied to software version | Shelf life matches technology |
| Technical blog posts | 6–12 months | Technology evolution |
| Stack Overflow answers | High skepticism always | Majority obsolete when posted |
| Conceptual/evergreen content | 6+ months | Foundational knowledge decays slower |

### 4.3 Freshness Scoring

Calculate staleness ratio:

```
staleness_ratio = days_since_update / acceptable_threshold_days
```

| Staleness Ratio | Freshness Score | Status |
|-----------------|-----------------|--------|
| < 0.5 | 100 | Fresh |
| 0.5 – 1.0 | Linear decay 100→0 | Aging |
| > 1.0 | 0 | Overdue for review |

**Example:** API documentation with a 90-day threshold, last updated 60 days ago:
- Staleness ratio: 60/90 = 0.67
- Freshness score: ~66 (interpolated)
- Status: Aging, review soon

### 4.4 Freshness in Retrieval

When multiple sources are available, weight by freshness:

```
final_relevance = (semantic_relevance × 0.7) + (freshness_score × 0.3)
```

Adjust weights by content type:
- **API docs, news:** 0.4–0.5 freshness weight
- **Tutorials:** 0.2–0.3 freshness weight  
- **Conceptual content:** 0.1 freshness weight

### 4.5 Deprecation Status

Track content lifecycle explicitly:

| Status | Meaning | Action |
|--------|---------|--------|
| **Current** | Active, recommended for use | Use normally |
| **Deprecated** | Still works but superseded | Show alternatives, warn readers |
| **Obsolete** | No longer accurate | Do not use; update or remove |
| **Removed** | Content deleted or inaccessible | Archive reference, find replacement |

### 4.6 Required Freshness Metadata

Every cited source must track:

| Field | Required | Description |
|-------|----------|-------------|
| `retrieved_at` | Yes | When content was accessed |
| `date_published` | Recommended | Original publication date |
| `version` | When applicable | Software/API version context |
| `status` | Recommended | Current, deprecated, obsolete, removed |

---

## Part 5: Evidence Storage

### 5.1 Evidence Artifact Schema

For formal evidence tracking (e.g., in Research Findings), use this schema:

```json
{
  "schema_version": "1.0",
  "citation": {
    "id": "cite-RF-03-01-001",
    "type": "api_docs",
    "title": "Authentication API Reference",
    "source_url": "https://docs.example.com/auth",
    "authors": ["Example Inc."],
    "date_published": "2024-11-15",
    "retrieved_at": "2026-01-25T10:30:00Z",
    "version": "v2.3"
  },
  "content": {
    "text": "All API requests require Bearer token authentication...",
    "excerpt": "Bearer token authentication",
    "section_path": ["Authentication", "Overview"]
  },
  "quality": {
    "tier": "T1",
    "source_reliability": "S1",
    "information_quality": "I2",
    "confidence": "high",
    "freshness_score": 92
  },
  "verification": {
    "content_hash": "sha256:abc123...",
    "verified_at": "2026-01-25T11:00:00Z",
    "verified_by": "jsmith"
  },
  "metadata": {}
}
```

### 5.2 Storage Principles

**Store content hashes:** Detect when sources change after indexing. This enables alerts when cited content has been modified.

**Separate metadata from content:** Keep text payloads clean; attach quality signals as structured metadata.

**Track provenance:** Every citation must trace back to an original source. Never cite secondary sources when primary sources are available.

**Support version pinning:** Users working with specific software versions need citations matched to their context.

---

## Part 6: Implementation Guidance

### 6.1 For Research Authors

When conducting research:

1. **Start with Tier 1 sources.** Check official documentation before searching forums.

2. **Verify community content.** Cross-reference Stack Overflow answers against official docs.

3. **Check dates obsessively.** A 2019 answer about a 2019 API may be wrong for the 2026 version.

4. **Qualify uncertainty.** Use confidence language appropriately. Don't present speculation as fact.

5. **Document your methodology.** Future readers should understand how you found and evaluated sources.

### 6.2 For Reviewers

When reviewing Research Findings:

1. **Check tier assignments.** Are sources classified correctly?

2. **Verify freshness.** Are citations current enough for the claims being made?

3. **Look for missing qualifications.** Are confidence levels appropriate to the evidence?

4. **Test primary sources.** Spot-check that citations actually support the claims.

5. **Question single-sourced claims.** Important claims should have corroboration or explicit qualification.

### 6.3 For Implementation Agents

When using Research Findings:

1. **Check confidence levels.** High-confidence findings can be acted on; low-confidence findings need verification.

2. **Verify against current docs.** Research may have aged since publication.

3. **Note version context.** Findings about version X may not apply to version Y.

4. **Flag contradictions.** If implementation reveals contradictions with research, trigger reconciliation.

---

## Appendix A: Glossary

**Citation**: A reference to a source that supports a claim in documentation.

**Confidence**: Overall certainty in a claim, synthesizing source reliability, information quality, and judgment.

**Evidence artifact**: A structured record of a citation with full metadata and quality assessment.

**Freshness score**: A measure of how current a source is relative to its expected update frequency.

**Information quality**: How well-supported a specific claim is (I1–I4).

**Source reliability**: How trustworthy a source is in general (S1–S4).

**Source tier**: Classification of sources by reliability (T1–T5).

**Staleness ratio**: Days since update divided by acceptable threshold; values >1 indicate overdue review.

---

## Appendix B: Related Documents

- **STD-20-01**: Citation format specification with examples and compliance checklist
- **DD-13-01**: Artifact taxonomy (includes Research Finding templates)
- **DD-12-01**: Repository structure (where research artifacts live)
- **Compass System Definition**: System requirements for pristine context layer

---

*End of Evidence Standards for Citations and Sources (DD-20-01)*
