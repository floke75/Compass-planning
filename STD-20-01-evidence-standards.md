---
id: STD-20-01
type: standard
area: 20-evidence-standards
title: Evidence Citation Format Specification
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Specifies the required citation format, provides examples of properly formatted citations, and documents common errors to avoid
tags: [evidence, citations, format, specification, compliance]
related:
  - DD-20-01
  - DD-13-01
companion: DD-20-01
enforcement: Research Finding review checklist
---

# Evidence Citation Format Specification

## Document Purpose

This document specifies the required format for citations in Compass documentation. It is the enforceable companion to DD-20-01 (Evidence Standards for Citations and Sources).

**How to use this document:**
1. When creating Research Findings or other artifacts with citations, follow the formats specified here
2. When reviewing documents, use the compliance checklist to verify citation quality
3. Reference the common errors section to avoid typical mistakes

---

## Part 1: Citation Format Specification

### 1.1 Required Fields

Every citation MUST include these fields:

| Field | Type | Format | Example |
|-------|------|--------|---------|
| `id` | string | `cite-{artifact-id}-{NNN}` | `cite-RF-03-01-001` |
| `source_url` | string | Full URL with protocol | `https://docs.example.com/auth` |
| `title` | string | Source document title | `"Authentication API Reference"` |
| `source_type` | enum | See Section 1.3 | `api_docs` |
| `retrieved_at` | datetime | ISO 8601 with timezone | `2026-01-25T10:30:00Z` |

### 1.2 Recommended Fields

These fields SHOULD be included when available:

| Field | Type | Format | Example |
|-------|------|--------|---------|
| `author` | string | Person or organization | `"Example Inc."` |
| `date_published` | date | ISO 8601 date | `2024-11-15` |
| `version` | string | Version identifier | `v2.3` |
| `excerpt` | string | Relevant quoted text | `"All API requests require..."` |
| `tier` | enum | T1–T5 | `T1` |
| `reliability` | enum | S1–S4 | `S1` |

### 1.3 Source Type Values

Use exactly these values for `source_type`:

| Value | Description | Typical Tier |
|-------|-------------|--------------|
| `api_docs` | Official API documentation | T1 |
| `vendor_docs` | Other official vendor documentation | T1 |
| `announcement` | Release notes, vendor blog posts | T1 |
| `article` | News articles, technical publications | T2–T3 |
| `book` | Published technical books | T2–T3 |
| `paper` | Academic/research papers | T1–T2 |
| `community` | Stack Overflow, GitHub issues, forums | T2–T4 |
| `blog` | Personal or company blogs | T3–T4 |
| `webpage` | Other web content | T4–T5 |

### 1.4 Tier Values

| Value | Meaning |
|-------|---------|
| `T1` | Authoritative (official vendor sources) |
| `T2` | Validated community (high-reputation sources) |
| `T3` | Curated secondary (reputable platforms) |
| `T4` | General community (identified authors) |
| `T5` | Unverified (anonymous or unknown quality) |

### 1.5 Reliability Values

| Value | Meaning |
|-------|---------|
| `S1` | Established (verified expertise, consistent accuracy) |
| `S2` | Credible (editorial oversight, generally reliable) |
| `S3` | Uncertain (unknown track record, requires verification) |
| `S4` | Questionable (anonymous, biased, or previously inaccurate) |

---

## Part 2: JSON Schema

### 2.1 Citation Object Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Compass Citation",
  "type": "object",
  "required": ["id", "source_url", "title", "source_type", "retrieved_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^cite-[A-Z]+-[0-9]+-[0-9]+-[0-9]+$",
      "description": "Unique citation identifier"
    },
    "source_url": {
      "type": "string",
      "format": "uri",
      "description": "Full URL to the source"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "description": "Source document title"
    },
    "source_type": {
      "type": "string",
      "enum": ["api_docs", "vendor_docs", "announcement", "article", "book", "paper", "community", "blog", "webpage"],
      "description": "Classification of source type"
    },
    "retrieved_at": {
      "type": "string",
      "format": "date-time",
      "description": "When the content was accessed"
    },
    "author": {
      "type": "string",
      "description": "Person or organization responsible"
    },
    "date_published": {
      "type": "string",
      "format": "date",
      "description": "Original publication date"
    },
    "version": {
      "type": "string",
      "description": "Software/API version if applicable"
    },
    "excerpt": {
      "type": "string",
      "description": "Relevant quoted text"
    },
    "tier": {
      "type": "string",
      "enum": ["T1", "T2", "T3", "T4", "T5"],
      "description": "Source tier classification"
    },
    "reliability": {
      "type": "string",
      "enum": ["S1", "S2", "S3", "S4"],
      "description": "Source reliability rating"
    }
  }
}
```

### 2.2 Full Evidence Artifact Schema

For formal evidence storage (optional for simple citations):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Compass Evidence Artifact",
  "type": "object",
  "required": ["schema_version", "citation"],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0"
    },
    "citation": {
      "$ref": "#/definitions/citation"
    },
    "content": {
      "type": "object",
      "properties": {
        "text": { "type": "string" },
        "excerpt": { "type": "string" },
        "section_path": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "quality": {
      "type": "object",
      "properties": {
        "tier": { "type": "string", "enum": ["T1", "T2", "T3", "T4", "T5"] },
        "source_reliability": { "type": "string", "enum": ["S1", "S2", "S3", "S4"] },
        "information_quality": { "type": "string", "enum": ["I1", "I2", "I3", "I4"] },
        "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
        "freshness_score": { "type": "integer", "minimum": 0, "maximum": 100 }
      }
    },
    "verification": {
      "type": "object",
      "properties": {
        "content_hash": { "type": "string" },
        "verified_at": { "type": "string", "format": "date-time" },
        "verified_by": { "type": "string" }
      }
    },
    "metadata": {
      "type": "object"
    }
  }
}
```

---

## Part 3: In-Document Citation Format

### 3.1 Inline Citations

Reference sources using numbered citations in square brackets:

```markdown
All API requests require Bearer token authentication [1].
The recommended approach uses refresh tokens for session management [2].
```

### 3.2 Source List Format

List sources at the end of the document in the `## Sources` section:

**Format:**
```
N. **[T#/S#]** Author. "Title" Version (if applicable). 
   Published/Updated DATE. Retrieved DATE. URL
   
   Optional: Brief quality note or excerpt.
```

**Example:**
```markdown
## Sources

1. **[T1/S1]** Example Inc. "Authentication API Reference" v2.3. 
   Updated 2024-11-15. Retrieved 2026-01-25. https://docs.example.com/auth

2. **[T2/S2]** Stack Overflow. "How to implement JWT refresh tokens" (Score: 127, Accepted). 
   Posted 2023-06-12. Retrieved 2026-01-25. https://stackoverflow.com/questions/12345
   Note: Answer verified against official docs; approach still current as of v2.3.

3. **[T3/S2]** Jane Smith. "Understanding OAuth2 Flows". Tech Conference 2024. 
   Published 2024-03-20. Retrieved 2026-01-25. https://techconf.example.com/talks/oauth2
```

### 3.3 Tier/Reliability Prefix

Always include the `[T#/S#]` prefix to immediately signal source quality:

- **[T1/S1]** — Highest quality: official, verified
- **[T2/S2]** — High quality: reputable, reliable
- **[T3/S3]** — Medium quality: requires some caution
- **[T4/S4]** — Lower quality: verify before relying on
- **[T5/S4]** — Questionable: cite only with explicit warnings

---

## Part 4: Examples

### 4.1 Correct Citation Examples

#### Example 1: Official Documentation (T1/S1)

**JSON format:**
```json
{
  "id": "cite-RF-03-01-001",
  "source_url": "https://docs.anthropic.com/claude/reference/messages-api",
  "title": "Messages API Reference",
  "source_type": "api_docs",
  "retrieved_at": "2026-01-25T14:30:00Z",
  "author": "Anthropic",
  "version": "v1",
  "tier": "T1",
  "reliability": "S1"
}
```

**In-document format:**
```markdown
1. **[T1/S1]** Anthropic. "Messages API Reference" v1. 
   Retrieved 2026-01-25. https://docs.anthropic.com/claude/reference/messages-api
```

---

#### Example 2: Stack Overflow Answer (T2/S2)

**JSON format:**
```json
{
  "id": "cite-RF-03-01-002",
  "source_url": "https://stackoverflow.com/questions/67890/rate-limiting-patterns",
  "title": "Best practices for API rate limiting",
  "source_type": "community",
  "retrieved_at": "2026-01-25T14:35:00Z",
  "author": "user:jane_developer",
  "date_published": "2024-08-15",
  "excerpt": "Token bucket algorithms provide the best balance of fairness and burst handling",
  "tier": "T2",
  "reliability": "S2"
}
```

**In-document format:**
```markdown
2. **[T2/S2]** jane_developer. "Best practices for API rate limiting" (Score: 89, Accepted). 
   Posted 2024-08-15. Retrieved 2026-01-25. https://stackoverflow.com/questions/67890/rate-limiting-patterns
   Note: Verified against official documentation; approach still current.
```

---

#### Example 3: Technical Blog Post (T3/S3)

**JSON format:**
```json
{
  "id": "cite-RF-03-01-003",
  "source_url": "https://engineering.example.com/blog/memory-architecture",
  "title": "Building a Scalable Memory Layer for LLM Applications",
  "source_type": "blog",
  "retrieved_at": "2026-01-25T14:40:00Z",
  "author": "Example Engineering Team",
  "date_published": "2025-10-22",
  "tier": "T3",
  "reliability": "S3"
}
```

**In-document format:**
```markdown
3. **[T3/S3]** Example Engineering Team. "Building a Scalable Memory Layer for LLM Applications". 
   Published 2025-10-22. Retrieved 2026-01-25. https://engineering.example.com/blog/memory-architecture
   Note: Company engineering blog; specific implementation may differ from general best practices.
```

---

#### Example 4: Low-Quality Source with Warning (T5/S4)

**JSON format:**
```json
{
  "id": "cite-RF-03-01-004",
  "source_url": "https://forum.example.com/thread/12345",
  "title": "Workaround for authentication bug",
  "source_type": "community",
  "retrieved_at": "2026-01-25T14:45:00Z",
  "author": "anonymous",
  "date_published": "2023-02-10",
  "tier": "T5",
  "reliability": "S4"
}
```

**In-document format:**
```markdown
4. **[T5/S4]** Anonymous. "Workaround for authentication bug". 
   Posted 2023-02-10. Retrieved 2026-01-25. https://forum.example.com/thread/12345
   ⚠️ Warning: Anonymous source, 3 years old, not verified. Included only to document 
   that this workaround exists in community discussions; do NOT rely on without verification.
```

---

### 4.2 Version-Specific Citation

When citing documentation for a specific software version:

**JSON format:**
```json
{
  "id": "cite-RF-01-02-001",
  "source_url": "https://docs.python.org/3.11/library/asyncio.html",
  "title": "asyncio — Asynchronous I/O",
  "source_type": "api_docs",
  "retrieved_at": "2026-01-25T15:00:00Z",
  "author": "Python Software Foundation",
  "version": "Python 3.11",
  "tier": "T1",
  "reliability": "S1"
}
```

**In-document format:**
```markdown
5. **[T1/S1]** Python Software Foundation. "asyncio — Asynchronous I/O". Python 3.11 Documentation. 
   Retrieved 2026-01-25. https://docs.python.org/3.11/library/asyncio.html
   Note: Specific to Python 3.11; may differ in other versions.
```

---

## Part 5: Common Errors to Avoid

### 5.1 Missing Required Fields

❌ **Wrong:**
```markdown
See the official docs at https://docs.example.com for details.
```

✅ **Correct:**
```markdown
See the official authentication documentation [1] for details.

## Sources
1. **[T1/S1]** Example Inc. "Authentication Guide". 
   Retrieved 2026-01-25. https://docs.example.com/auth
```

**Why it matters:** Links without citation metadata cannot be evaluated for quality, tracked for staleness, or verified.

---

### 5.2 Missing Tier/Reliability Assessment

❌ **Wrong:**
```markdown
1. Stack Overflow. "How to implement caching". https://stackoverflow.com/questions/12345
```

✅ **Correct:**
```markdown
1. **[T2/S2]** Stack Overflow. "How to implement caching" (Score: 156, Accepted). 
   Posted 2024-05-10. Retrieved 2026-01-25. https://stackoverflow.com/questions/12345
```

**Why it matters:** Without tier/reliability, readers cannot judge how much to trust the source.

---

### 5.3 Missing Retrieved Date

❌ **Wrong:**
```markdown
1. **[T1/S1]** AWS. "Lambda Documentation". https://docs.aws.amazon.com/lambda
```

✅ **Correct:**
```markdown
1. **[T1/S1]** AWS. "Lambda Documentation". 
   Retrieved 2026-01-25. https://docs.aws.amazon.com/lambda
```

**Why it matters:** Documentation changes over time. Without a retrieval date, there's no way to know if the cited content is still accurate.

---

### 5.4 Citing Secondary Sources Instead of Primary

❌ **Wrong:**
```markdown
According to a blog post about the AWS announcement [1], Lambda now supports...

1. **[T3/S3]** Tech Blogger. "What's New in AWS Lambda". https://blog.example.com/aws-news
```

✅ **Correct:**
```markdown
According to the AWS announcement [1], Lambda now supports...

1. **[T1/S1]** AWS. "Announcing New Lambda Features". AWS News Blog. 
   Published 2026-01-20. Retrieved 2026-01-25. https://aws.amazon.com/blogs/aws/new-lambda-features
```

**Why it matters:** Primary sources are more reliable and less prone to misinterpretation.

---

### 5.5 Over-Trusting Stack Overflow

❌ **Wrong:**
```markdown
The standard approach is to use [implementation from Stack Overflow] [1].

1. **[T1/S1]** Stack Overflow. "How to do X". https://stackoverflow.com/questions/old-answer
```

✅ **Correct:**
```markdown
A commonly referenced approach uses [implementation] [1], though this should be verified against 
current official documentation [2].

1. **[T2/S3]** Stack Overflow. "How to do X" (Score: 45). 
   Posted 2021-03-15. Retrieved 2026-01-25. https://stackoverflow.com/questions/old-answer
   Note: Answer is 5 years old; verify before using.

2. **[T1/S1]** Vendor. "Official Implementation Guide" v3.0. 
   Updated 2025-11-01. Retrieved 2026-01-25. https://docs.vendor.com/guide
```

**Why it matters:** Stack Overflow answers are often outdated. Rating them T1/S1 is incorrect.

---

### 5.6 Missing Version Context

❌ **Wrong:**
```markdown
React supports concurrent rendering [1].

1. **[T1/S1]** React. "Concurrent Features". https://react.dev/reference/react
```

✅ **Correct:**
```markdown
React 18+ supports concurrent rendering [1].

1. **[T1/S1]** React. "Concurrent Features". React 18 Documentation. 
   Retrieved 2026-01-25. https://react.dev/reference/react
   Note: Concurrent features introduced in React 18; not available in earlier versions.
```

**Why it matters:** Features, APIs, and behaviors change between versions. Omitting version context can lead to incompatible implementations.

---

### 5.7 Failing to Qualify Low-Confidence Sources

❌ **Wrong:**
```markdown
The recommended approach is to use X [1].

1. **[T4/S3]** Random Blog. "My thoughts on X". https://blog.random.com/x
```

✅ **Correct:**
```markdown
One approach suggested in community discussions is to use X [1], though this has not been 
verified against official recommendations.

1. **[T4/S3]** Random Blog. "My thoughts on X". 
   Published 2024-07-20. Retrieved 2026-01-25. https://blog.random.com/x
   Note: Personal opinion, not official guidance. Included as one perspective.
```

**Why it matters:** Low-tier sources should inform, not dictate. The text must match the confidence level of the source.

---

## Part 6: Compliance Checklist

Use this checklist when reviewing Research Findings or other documents with citations.

### 6.1 Per-Citation Checklist

For each citation, verify:

- [ ] Has unique ID in correct format (`cite-{artifact-id}-{NNN}`)
- [ ] Has valid source URL
- [ ] Has descriptive title
- [ ] Has correct source_type value
- [ ] Has retrieved_at date in ISO 8601 format
- [ ] Has tier assignment (T1–T5)
- [ ] Has reliability rating (S1–S4)
- [ ] Tier/reliability appears in in-document citation `[T#/S#]`
- [ ] Version included (if applicable)
- [ ] Low-quality sources (T4/T5) have explicit warnings

### 6.2 Document-Level Checklist

For the document overall:

- [ ] All claims with external sources have inline citations
- [ ] Sources section exists at document end
- [ ] Sources use consistent format
- [ ] Primary sources cited when available (not just secondary)
- [ ] Stack Overflow answers have age/score noted
- [ ] Overall confidence matches weakest critical source
- [ ] No orphaned citations (cited but not in sources list)
- [ ] No orphaned sources (in list but never cited)

### 6.3 Freshness Checklist

- [ ] All retrieved_at dates are within acceptable freshness thresholds
- [ ] Old sources (>1 year) have explicit freshness notes
- [ ] API/framework documentation matches version being discussed
- [ ] No sources marked "deprecated" or "obsolete" without acknowledgment

---

## Appendix A: Quick Reference

### Citation ID Format
```
cite-{artifact-id}-{NNN}
Example: cite-RF-03-01-001
```

### Source Types
```
api_docs | vendor_docs | announcement | article | book | paper | community | blog | webpage
```

### Tier/Reliability Prefixes
```
[T1/S1] — Highest quality (official, verified)
[T2/S2] — High quality (reputable, reliable)
[T3/S3] — Medium quality (use with some caution)
[T4/S4] — Lower quality (verify before relying)
[T5/S4] — Questionable (cite only with warnings)
```

### In-Document Format
```markdown
N. **[T#/S#]** Author. "Title" Version. 
   Published/Updated DATE. Retrieved DATE. URL
   Note: Quality notes if needed.
```

---

## Appendix B: Related Documents

- **DD-20-01**: Evidence standards (definitions and rationale)
- **DD-13-01**: Artifact taxonomy (Research Finding template)
- **DD-12-01**: Repository structure (where research artifacts live)

---

*End of Evidence Citation Format Specification (STD-20-01)*
