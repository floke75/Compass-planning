---
id: DD-22-01
type: definition
area: 22-llm-implementability
title: LLM-Implementability Evaluation Framework
status: draft
created: 2026-02-06
updated: 2026-02-06
author: compass-research
summary: Defines six LLM-Implementability criteria (LI-1 through LI-6), a 0-3 scoring rubric, threshold and weighting rules, and evidence mapping for evaluating technology choices when the primary developer is an LLM coding agent rather than a human
tags: [llm-implementability, evaluation, methodology, scoring, technology-selection, agent-development]
related:
  - DD-20-01
  - STD-20-01
  - DD-13-01
  - DD-14-01
  - SYS-00
  - RF-03-02
links:
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "DD-13-01"
  - rel: related
    target_id: "DD-14-01"
  - rel: related
    target_id: "SYS-00"
  - rel: informed_by
    target_id: "RF-03-02"
companion: STD-22-01
---

# LLM-Implementability Evaluation Framework

## Document Purpose

This document defines the evaluation framework for assessing how well a technology, library, or service supports implementation by LLM coding agents. It introduces six criteria (LI-1 through LI-6), a standardized scoring rubric, threshold rules for flagging risk, and weighting guidance for the Compass context.

**Why this matters**: Compass is built by LLM coding agents, not human developers (SYS-00 §1.1). This changes what "good" means for a technology choice. A library with excellent human documentation but unpredictable API surfaces may score poorly because LLMs hallucinate when patterns are ambiguous. A less-known library with a tight, type-safe API and machine-readable docs may score higher because LLMs generate correct code from it reliably. Traditional evaluation criteria—developer experience, learning curve, community size—are proxies for the wrong thing when the developer is an LLM. This framework provides the right proxies.

**Origin**: The RF-03-02 research session (Advanced Memory and Context Engineering) surfaced this need explicitly. When memory architecture alternatives were re-evaluated through an LLM-implementability lens, the selection calculus changed materially. Graphiti's Docker-based MCP setup scored better than alternatives with superior human documentation but worse structural predictability. This pattern generalizes: every technology evaluation in Compass should include an LLM-implementability assessment.

**Audience**: Anyone conducting technology research, creating Research Findings, writing ADR decision rationale, or reviewing technology selections for Compass.

**Companion document**: STD-22-01 (planned) will make this framework enforceable by requiring LI assessments in all RF documents and ADR rationale.

---

## Part 1: The Conceptual Shift

### 1.1 Why Traditional Evaluation Criteria Are Insufficient

Technology evaluation has historically optimized for human developers. Criteria like "developer experience," "learning curve," and "time to first working prototype" assume a human brain that learns, remembers, gets frustrated, and works limited hours. These assumptions are baked into Research Findings, ADR rationale, and the System Definition itself.

When the developer is an LLM coding agent, the relevant dimensions shift:

| Dimension | Human Developer Lens | LLM Agent Lens |
|-----------|---------------------|----------------|
| **Timeline** | Calendar duration ("2-3 weeks") | Irrelevant as a unit. What matters is *complexity*—the number of concepts, integration points, and iteration cycles required. |
| **Documentation quality** | Subjective ("well-documented") | Can the LLM parse and act on the docs? Is there `llms.txt`? An MCP docs server? Structured examples? |
| **API design** | "Good developer experience" | API surface area (smaller = fewer hallucination vectors), naming predictability, type safety at compile time |
| **Learning curve** | "How long to learn" | LLM familiarity—is the library well-represented in training data? Are patterns conventional? |
| **Code quality** | "Clean code, good practices" | Structural quality for *generation*—can an LLM produce correct code from a specification? |
| **Ecosystem** | "Large community" | MCP tool availability, Claude Code compatibility, machine-readable documentation |
| **Cost** | Developer hours × hourly rate | Token cost × complexity. A harder-to-implement solution costs more tokens, not more weeks. |
| **Risk** | "Framework maturity" | Hallucination risk—unfamiliar libraries produce more incorrect code. Verification difficulty. |

This is not a cosmetic relabeling. It changes which technology wins an evaluation. A library with 50,000 GitHub stars but a sprawling, permissive API may lose to a library with 5,000 stars but a tight, type-safe surface that LLMs consistently get right.

### 1.2 What LLM-Implementability Measures

LLM-implementability is the probability that an LLM coding agent will produce correct, production-quality code for a given technology choice, given a well-written specification. It is a composite property influenced by six factors:

1. **Documentation quality for LLM consumption** (LI-1): Can the LLM access and parse the library's documentation effectively?
2. **MCP tool availability** (LI-2): Can the LLM interact with the library's documentation and APIs through the Model Context Protocol?
3. **Code complexity and structural quality** (LI-3): Does the API design minimize opportunities for the LLM to generate plausible but incorrect code?
4. **Testability and self-verification** (LI-4): Can the LLM verify its own output through automated testing?
5. **LLM familiarity from training data** (LI-5): Is the library well-represented in the LLM's training corpus?
6. **Hallucination risk profile** (LI-6): How many ways can the LLM generate plausible but wrong code, and how detectable are such errors?

These six criteria are defined in detail in Part 2.

### 1.3 Relationship to Functional Evaluation

LLM-implementability does not replace functional evaluation. A technology must still meet functional requirements (capability, performance, cost, security). LLM-implementability is an additional dimension that captures *implementation feasibility when the builder is an LLM*.

The evaluation sequence is:

1. **Functional fit**: Does the technology meet Compass requirements? (Existing RF methodology)
2. **LLM-implementability**: Can an LLM agent implement it correctly? (This framework)
3. **Combined assessment**: Functional fit × implementability = selection recommendation

A technology with perfect functional fit but an LI score below threshold (§3.3) should be flagged as high-risk. A technology with adequate functional fit and a high LI score may be preferred over a functionally superior but harder-to-implement alternative.

### 1.4 Scope and Boundaries

**In scope**: Evaluation of libraries, frameworks, services, and tools that LLM coding agents will use to build Compass. This includes backend platforms, orchestration frameworks, widget libraries, hosting providers, and development tooling.

**Out of scope**: Evaluation of the LLM models themselves (covered by RF-09-01 and ADR-09-01). Evaluation of content produced by Compass for human consumption (covered by DD-18-01 and DD-19-01). General software quality metrics unrelated to LLM code generation.

---

## Part 2: The Six LI Criteria

### 2.1 LI-1: Documentation Quality for LLM Consumption

Documentation quality for LLM consumption measures how effectively an LLM can access, parse, and act on a library's documentation to produce correct code. This is distinct from human-readable documentation quality: a beautifully designed documentation site with interactive examples may score poorly if the content is not machine-parseable, while a plain `llms.txt` file may score excellently.

**Assessment questions**:

1. Does the library provide an `llms.txt` file? (`llms.txt` is a standardized format for exposing documentation to LLM agents, analogous to `robots.txt` for search engines.)
2. Is there an MCP documentation server (e.g., `@mastra/mcp-docs-server`)? This allows LLMs to query documentation programmatically rather than relying on training data.
3. Are code examples complete and copy-pasteable? Pseudocode and incomplete snippets force the LLM to fill gaps, increasing hallucination risk.
4. Is documentation structured with clear headings and sections rather than narrative prose? LLMs extract information more reliably from structured content.
5. Are API references machine-readable (TypeDoc, JSDoc, OpenAPI spec)? These formats are parsed more reliably than prose descriptions.
6. Is there a single canonical source of truth for the API, or are there multiple conflicting documentation versions?

**Signal hierarchy** (strongest evidence first):

| Signal | Strength | Rationale |
|--------|----------|-----------|
| `llms.txt` with full + lite variants | Very strong | Purpose-built for LLM consumption |
| MCP documentation server | Very strong | Enables real-time, version-specific queries |
| OpenAPI / TypeDoc / JSDoc specs | Strong | Machine-parseable API definitions |
| Structured docs with complete examples | Moderate | Reduces gap-filling hallucination |
| Prose-heavy docs without structured API reference | Weak | LLMs struggle to extract precise API details from narrative |
| No public documentation | Absent | LLM must rely entirely on training data |

### 2.2 LI-2: MCP Tool Availability

MCP (Model Context Protocol) tool availability measures whether the LLM can interact with the library through standardized tool interfaces. MCP tools are the primary mechanism by which LLM agents access external capabilities; a library with an MCP server is fundamentally more accessible to an LLM than one without.

**Assessment questions**:

1. Does the library have an official MCP server? This is the highest-value signal because it provides a structured, versioned interface that the LLM can invoke directly.
2. Can Claude Code or similar agents access the library's documentation via MCP? This enables the agent to look up API details in real time rather than relying on potentially stale training data.
3. Are there Claude-specific integration guides (`CLAUDE.md`, Cursor rules, `.cursorrules`)? These provide agent-specific configuration and conventions.
4. Is there a Context7 entry for version-specific documentation? Context7 provides MCP-accessible, version-pinned documentation for popular libraries.
5. Does the library expose its functionality through well-defined tool schemas (JSON Schema, Zod schemas) that an LLM can invoke?

**Signal hierarchy**:

| Signal | Strength | Rationale |
|--------|----------|-----------|
| Official MCP server with documented tools | Very strong | Direct LLM invocation path |
| Context7 entry with version-pinned docs | Strong | Real-time version-specific doc access via MCP |
| `CLAUDE.md` or equivalent agent integration guide | Strong | Agent-specific conventions reduce configuration errors |
| Unofficial/community MCP server | Moderate | Available but may lack maintenance guarantees |
| Well-defined JSON Schema / Zod tool schemas | Moderate | Enables tool-use patterns even without MCP |
| No MCP presence | Absent | LLM must rely on code generation from training data only |

### 2.3 LI-3: Code Complexity and Structural Quality

Code complexity and structural quality measure how many ways an LLM can go wrong when generating code for this library. This is the most nuanced criterion because it combines API design, type system strength, naming conventions, and pattern conventionality.

**Assessment questions**:

1. **API surface area**: How many concepts must the LLM hold simultaneously to produce correct code? A library requiring 5 concepts (create client, call method, handle response, handle error, clean up) is more implementable than one requiring 20 (configure provider, register middleware, define schemas, set up interceptors, manage connection pools, etc.).
2. **Naming predictability**: Do method names follow conventions the LLM knows? A library using `createUser`, `getUser`, `updateUser`, `deleteUser` is more predictable than one using `fabricateEntity`, `resolveIdentity`, `mutateRecord`, `decommissionAgent`.
3. **Type safety**: Does the type system catch mistakes at compile time? TypeScript with strict mode and Zod validation catches errors that would otherwise become runtime failures. This is critical because an LLM cannot "debug by running and observing" as naturally as a human—it relies on type-checker feedback.
4. **Boilerplate ratio**: How much repetitive setup code is needed? High boilerplate means more tokens spent on low-value code that must be correct but is tedious to generate consistently.
5. **Pattern conventionality**: Does the library follow patterns common in LLM training data? Express-like middleware patterns, React-like component patterns, and REST-like resource patterns are deeply embedded in LLM training. Libraries using these patterns benefit from transfer learning.
6. **Configuration complexity**: Are there many configuration options with subtle interactions? Each configuration knob is a potential hallucination point.

**The "concept count" heuristic**: As a practical shortcut, count the number of distinct concepts an LLM must correctly combine to complete a typical task. Libraries requiring fewer than 10 concepts per task tend to score well; those requiring 20+ tend to score poorly.

**Signal hierarchy**:

| Signal | Strength | Rationale |
|--------|----------|-----------|
| TypeScript-native with strict types and Zod schemas | Very strong | Compile-time error catching eliminates a class of LLM mistakes |
| Small, predictable API surface (< 10 concepts per task) | Very strong | Fewer concepts = fewer hallucination opportunities |
| Conventional patterns (Express-like, React-like) | Strong | Training data transfer learning |
| Single way to do things (opinionated API) | Strong | Eliminates choice points where LLMs pick wrong options |
| Large, permissive API with many optional parameters | Weak | Many correct-looking but wrong combinations |
| Custom DSL or novel patterns | Weak | Not in training data; requires extensive in-context learning |

### 2.4 LI-4: Testability and Self-Verification

Testability measures whether an LLM can verify its own generated code through automated testing. This is the feedback loop that transforms "generate and hope" into "generate, test, iterate." An LLM that can run tests after generating code and interpret failures to fix them is dramatically more effective than one generating code blindly.

**Assessment questions**:

1. Can the LLM run tests after generating code? This requires the test framework to be installable and executable in the LLM's environment (e.g., Vitest, Jest, or the library's own test utilities).
2. Is there a test framework with clear assertion patterns? `expect(result).toBe(expected)` is more interpretable by an LLM than custom assertion DSLs.
3. Can tests run without external dependencies? If testing requires a running database, external API, or network access, the feedback loop breaks. Libraries with in-memory test modes, mock backends, or test utilities (e.g., `convex-test`) score higher.
4. Is the feedback loop tight? Does a failing test clearly indicate *what* went wrong and *where*? Stack traces pointing to the exact assertion with a clear diff ("expected 'foo', got 'bar'") are more useful to an LLM than cryptic error codes or timeout failures.
5. Are there example tests in the documentation? LLMs learn testing patterns from examples more reliably than from prose descriptions.

**Signal hierarchy**:

| Signal | Strength | Rationale |
|--------|----------|-----------|
| Dedicated test utilities with in-memory backends | Very strong | Self-contained test loop; no external dependencies |
| Well-documented test patterns with examples | Strong | LLM can follow existing patterns |
| Standard test framework support (Vitest, Jest) | Strong | Deeply embedded in training data |
| Tests require external services (databases, APIs) | Weak | Breaks the fast feedback loop |
| No testing guidance or utilities | Absent | LLM must invent testing approach; high error rate |

### 2.5 LI-5: LLM Familiarity (Training Data Representation)

LLM familiarity measures how well the library is represented in the LLM's training data. Libraries that appeared frequently in training corpora (code repositories, documentation, tutorials, Stack Overflow) are more reliably generated by LLMs because the model has seen many correct usage examples. This is a pragmatic criterion: newer or less popular libraries are inherently riskier for LLM implementation regardless of their technical quality.

**Assessment questions**:

1. **Popularity metrics**: What are the npm weekly downloads, GitHub stars, and fork count? These serve as rough proxies for training data presence. A library with 20 million weekly npm downloads is almost certainly well-represented; one with 200 weekly downloads almost certainly is not.
2. **Library age**: When was the library first released? Libraries that existed before the LLM's training data cutoff (typically 2024-2025 for current models) are better known than those released after. A library that has been stable since 2020 is more reliably generated than one released in January 2026.
3. **Tutorial and blog coverage**: Are there many tutorials, blog posts, and Stack Overflow answers? Each of these is a potential training example. High coverage means the LLM has seen the library used correctly in many contexts.
4. **Pattern transferability**: Even if the specific library is unfamiliar, are similar patterns from well-known libraries transferable? A new library that uses Express-like patterns benefits from the LLM's deep familiarity with Express, even though it has never seen the new library specifically.
5. **Version stability**: Has the API been stable across versions, or are there major breaking changes? If the LLM was trained on v2 but the project uses v3 with a different API, familiarity becomes a liability (see LI-6).

**Proxy metrics and their reliability**:

| Metric | Reliability as Training Data Proxy | Notes |
|--------|-----------------------------------|-------|
| npm weekly downloads > 1M | High | Almost certainly in training data |
| npm weekly downloads 100K-1M | Moderate | Likely in training data |
| npm weekly downloads < 100K | Low | May or may not be in training data |
| GitHub stars > 10K | High | Major libraries; extensive coverage |
| GitHub stars 1K-10K | Moderate | Known but coverage may be thin |
| GitHub stars < 1K | Low | Limited training data presence |
| First release before 2023 | High | Pre-dates most training cutoffs |
| First release 2024-2025 | Moderate | May be in training data; coverage varies |
| First release 2026+ | Low | Almost certainly not in training data |

**Important caveat**: Familiarity metrics are proxies, not guarantees. A highly popular library with frequent breaking changes may have *misleading* training data (the LLM generates v2 code when v3 is needed). Version awareness interacts with LI-6 (hallucination risk).

### 2.6 LI-6: Hallucination Risk Profile

Hallucination risk profile measures how likely an LLM is to generate plausible but incorrect code for this library, and how difficult such errors are to detect and fix. This is the "failure mode" criterion: all LLMs hallucinate sometimes, but some libraries make hallucination more likely and harder to catch.

**Assessment questions**:

1. **Known gotchas**: Does the library have common pitfalls that LLMs consistently get wrong? For example, libraries that require specific initialization ordering, have methods that look similar but behave differently, or have silent failure modes where incorrect code compiles but produces wrong results.
2. **Version confusion**: Are there multiple library versions with different APIs in the LLM's training data? If v2 and v3 have incompatible APIs and the LLM has seen both, it may generate code mixing v2 and v3 patterns—syntactically valid but semantically broken.
3. **API consistency**: Does the library offer one way to do things (opinionated) or many ways (permissive)? Permissive APIs increase hallucination risk because the LLM may choose a valid-looking but wrong approach. For example, a library that offers callbacks, promises, and async/await for the same operation has three potential code paths; an LLM may mix them.
4. **Error message diagnostics**: When the LLM generates incorrect code, are error messages diagnostic enough for it to self-correct? Messages like "TypeError: Cannot read property 'foo' of undefined at line 42" are actionable; messages like "Error code 500" are not.
5. **Silent failure modes**: Can incorrect code pass type checking and even basic tests but fail at runtime or produce subtly wrong results? These are the most dangerous hallucination outcomes because they pass automated verification.
6. **Recovery cost**: If the LLM makes a mistake, how expensive (in tokens and iteration cycles) is the fix? A library where errors are localized (fix one function) has lower recovery cost than one where errors cascade (a wrong configuration affects the entire application).

**Risk profiles**:

| Profile | Description | Example |
|---------|-------------|---------|
| **Low risk** | Opinionated API, strong types, diagnostic errors, no version confusion | A TypeScript-native library with a single stable API version and compile-time validation |
| **Medium risk** | Some ambiguity, adequate types, reasonable errors, minor version differences | A well-known library with 2-3 API patterns and occasional breaking changes |
| **High risk** | Permissive API, weak types, opaque errors, significant version confusion | A library with many configuration options, JavaScript-only (no TypeScript types), and major API differences between widely-used versions |
| **Very high risk** | Novel patterns, no types, silent failures, extensive version divergence | A new library using custom DSLs with no TypeScript support and breaking changes every minor version |

---

## Part 3: Scoring Rubric

### 3.1 The 0-3 Scale

Each LI criterion is scored on a 0-3 integer scale. Half-point increments (0.5, 1.5, 2.5) are permitted when evidence supports an intermediate assessment.

| Score | Label | Definition | Practical Meaning |
|-------|-------|------------|-------------------|
| **0** | Absent | The capability is absent or actively hostile to LLM implementation. | The LLM will almost certainly fail to produce correct code for this aspect. Using this library requires extensive prompt engineering or manual intervention. |
| **1** | Limited | The capability is present but limited. The LLM will struggle without significant prompt engineering or supplementary context. | The LLM can produce code but will require multiple iteration cycles, detailed specifications, and careful review. Expect 40-60% first-attempt correctness. |
| **2** | Good | The capability is well-supported. The LLM can implement correctly with a well-written specification. | The LLM will produce substantially correct code from a clear spec. Expect 70-85% first-attempt correctness with standard iteration to resolve edge cases. |
| **3** | Excellent | The capability is outstanding. The LLM will produce correct code from minimal guidance. | The LLM generates correct code with high confidence. Expect 85-95% first-attempt correctness. Minimal iteration needed. |

**Calibration guidance**: The percentages above are approximate and serve as calibration anchors, not measured values. Assessors should use their judgment informed by the evidence signals defined in Part 2 for each criterion.

### 3.2 Scoring Procedure

For each technology being evaluated:

1. **Collect evidence** for each LI criterion using the assessment questions and signal hierarchies defined in Part 2.
2. **Assign a raw score** (0-3) for each criterion based on the evidence. Document the primary evidence supporting each score.
3. **Calculate the raw total** by summing all six scores (maximum 18).
4. **Apply weighting** if context-specific weighting rules apply (see §4.1).
5. **Compare against thresholds** (see §3.3) to determine risk classification.
6. **Document the assessment** using the template in §3.4.

### 3.3 Thresholds

| Total Score | Classification | Implication |
|-------------|---------------|-------------|
| **14-18** | Low risk | LLM implementation is well-supported. Standard development practices apply. |
| **8-13** | Moderate risk | LLM implementation is feasible but requires additional measures: detailed specifications, supplementary documentation in agent context, more iteration budget, and careful review. |
| **4-7** | High risk | LLM implementation will be difficult. Flag for review. Consider alternatives. If no alternatives exist, plan for extensive prompt engineering, manual code review, and higher token budgets. |
| **0-3** | Exclusion zone | LLM implementation is impractical. Do not select unless no alternative exists and the capability is absolutely required. Require explicit risk acceptance in the ADR. |

**Threshold interpretation**: These thresholds are guidelines, not hard gates. A technology scoring 7 with all scores distributed evenly (roughly 1.2 per criterion) presents different risk than one scoring 7 with three 0s and three 2+ (concentrated weakness). Assessors should consider the distribution of scores, not just the total.

### 3.4 Assessment Template

Research Findings documents should include an LI assessment using this format:

```markdown
### LLM-Implementability Assessment

| Criterion | Score | Primary Evidence |
|-----------|-------|-----------------|
| LI-1: Documentation Quality | X/3 | [key evidence] |
| LI-2: MCP Tool Availability | X/3 | [key evidence] |
| LI-3: Code Complexity | X/3 | [key evidence] |
| LI-4: Testability | X/3 | [key evidence] |
| LI-5: LLM Familiarity | X/3 | [key evidence] |
| LI-6: Hallucination Risk | X/3 | [key evidence] |
| **Raw Total** | **XX/18** | |
| **Weighted Total** | **XX/YY** | [if weighting applies] |
| **Risk Classification** | [Low/Moderate/High/Exclusion] | |

**Assessment notes**: [Any qualitative observations about score distribution,
concentrated weaknesses, or mitigating factors.]
```

When comparing multiple technologies, present scores side by side:

```markdown
### Comparative LLM-Implementability Assessment

| Criterion | Technology A | Technology B | Technology C |
|-----------|-------------|-------------|-------------|
| LI-1: Documentation Quality | X/3 | X/3 | X/3 |
| LI-2: MCP Tool Availability | X/3 | X/3 | X/3 |
| LI-3: Code Complexity | X/3 | X/3 | X/3 |
| LI-4: Testability | X/3 | X/3 | X/3 |
| LI-5: LLM Familiarity | X/3 | X/3 | X/3 |
| LI-6: Hallucination Risk | X/3 | X/3 | X/3 |
| **Raw Total** | **XX/18** | **XX/18** | **XX/18** |
| **Risk Classification** | [class] | [class] | [class] |
```

---

## Part 4: Weighting and Context-Specific Application

### 4.1 Compass-Specific Weighting

For Compass technology evaluations specifically, LI-1 (Documentation Quality) and LI-3 (Code Complexity) carry 1.5× weight. This reflects two empirical observations:

1. **Documentation quality is the primary determinant of first-attempt correctness**: When an LLM has access to accurate, structured documentation (via `llms.txt` or MCP), its code generation accuracy improves dramatically. Without good documentation, even a familiar, well-typed library produces unreliable output because the LLM falls back on potentially stale training data.

2. **Code complexity is the primary determinant of iteration cost**: When a library has a large API surface or ambiguous patterns, each iteration cycle requires more tokens and more LLM reasoning to resolve. This compounds: a library that requires 5 iteration cycles instead of 2 doesn't cost 2.5× more—it costs more because each cycle builds on potentially flawed output from the previous cycle.

**Weighted calculation for Compass**:

```
Weighted Total = (LI-1 × 1.5) + LI-2 + (LI-3 × 1.5) + LI-4 + LI-5 + LI-6
Maximum possible = 4.5 + 3 + 4.5 + 3 + 3 + 3 = 21
```

**Weighted thresholds**:

| Weighted Score | Classification |
|----------------|---------------|
| 16-21 | Low risk |
| 9-15 | Moderate risk |
| 5-8 | High risk |
| 0-4 | Exclusion zone |

### 4.2 When to Use Weighted vs. Raw Scores

Use **weighted scores** when:
- Evaluating technologies for Compass implementation (the default case)
- The implementation context has a clear LLM-agent-first constraint
- Documentation quality and code complexity are known primary risk factors

Use **raw scores** when:
- Comparing technologies in a general context without specific weighting rationale
- All six criteria are equally important to the decision
- The evaluation is preliminary and weighting decisions have not been made

### 4.3 Custom Weighting for Other Contexts

Other projects in the EFN ecosystem may define their own weighting rules. The six LI criteria and the 0-3 scale remain fixed; only the multipliers change. Custom weighting must be documented in the relevant RF or ADR and must state the rationale for each weight adjustment.

---

## Part 5: Evidence Mapping

### 5.1 Connecting LI Evidence to the DD-20-01 Framework

The evidence standards in DD-20-01 (Source Reliability S1-S4, Information Quality I1-I4, Confidence levels) apply to LLM-implementability evidence. This section maps common LI evidence types to the DD-20-01 grading framework.

| LI Evidence Type | DD-20-01 Source Tier | Source Reliability | Notes |
|-----------------|---------------------|-------------------|-------|
| Library's own `llms.txt` file | T1 (Authoritative) | S1 | First-party documentation; definitive for LI-1 |
| Official MCP server listing in vendor docs | T1 (Authoritative) | S1 | First-party tool availability; definitive for LI-2 |
| TypeDoc/JSDoc API reference | T1 (Authoritative) | S1 | Machine-generated from source; definitive for LI-3 type safety |
| npm weekly download count | T1 (Authoritative) | S2 | Objective metric, but only a proxy for training data presence (LI-5) |
| GitHub star count | T1 (Authoritative) | S2 | Objective metric, rough proxy for popularity and training data |
| Context7 listing | T2 (Validated Community) | S2 | Third-party aggregation; strong evidence for LI-2 |
| Library author's blog post on LLM support | T2 (Validated Community) | S2 | Credible but potentially biased toward positive framing |
| Community MCP server (unofficial) | T4 (General Community) | S3 | Useful but may lack maintenance; uncertain reliability |
| Stack Overflow answer about library gotchas | T2-T4 (varies) | S2-S3 | Useful for LI-6 hallucination risk; check recency and votes |
| Personal experience report on LLM code generation | T4 (General Community) | S3-S4 | Anecdotal; useful for LI-6 but requires corroboration |
| Benchmark results for LLM code generation accuracy | T1-T2 (if peer-reviewed) | S1-S2 | Strongest evidence for LI overall; rare |

### 5.2 Minimum Evidence Requirements

For a score of 2 or 3 on any LI criterion, at least one piece of T1 or T2 evidence should support the assessment. Scores of 0 or 1 can be assigned based on absence of evidence (a library with no `llms.txt` scores 0 on that LI-1 sub-signal regardless of other evidence).

For the overall LI assessment to carry High confidence (per DD-20-01 §1.4), at least four of the six criteria should have T1 or T2 evidence. Assessments with fewer than four evidenced criteria should be marked Medium confidence.

---

## Part 6: Implementation Guidance

### 6.1 For Research Authors

When creating or updating Research Findings (RF documents):

1. **Include an LI assessment for every evaluated technology.** Use the template from §3.4. For comparative evaluations, use the side-by-side format.

2. **Collect LI evidence during research, not after.** Check for `llms.txt`, MCP servers, and Context7 entries as part of the initial research sweep. These take seconds to verify and provide high-value signals.

3. **Use the assessment questions.** Each criterion in Part 2 provides specific questions. Work through them systematically rather than estimating from general impressions.

4. **Document the primary evidence for each score.** A score without evidence is an opinion. Reference specific URLs, metrics, or test results.

5. **Note concentrated weaknesses.** A technology scoring 12/18 with a 0 on LI-4 (testability) has a specific, addressable problem. Call it out rather than letting it hide in the total.

6. **Replace timeline estimates with complexity profiles.** Instead of "estimated 2-3 weeks," write: "Requires implementing ~8 distinct concepts (client setup, agent definition, tool registration, state management, persistence, error handling, testing, deployment). Moderate concept count with conventional patterns (LI-3: 2/3) and good test utilities (LI-4: 2/3) suggests moderate iteration budget."

### 6.2 For ADR Authors

When writing or updating Architecture Decision Records:

1. **Reference LI scores in decision rationale.** If a technology was selected partly because of superior LLM-implementability, state this explicitly and cite the scores.

2. **Address LI risks in the Consequences section.** If the selected technology has a concentrated weakness (e.g., low LI-6 due to version confusion), document the mitigation strategy.

3. **Compare LI scores when rejecting alternatives.** "Technology B was rejected despite functional parity because its LI score (6/18, High Risk) indicated significantly higher implementation difficulty than Technology A (14/18, Low Risk)."

### 6.3 For Reviewers

When reviewing RF or ADR documents:

1. **Verify evidence for high scores.** A score of 3/3 on LI-1 without citing `llms.txt` or an MCP docs server should be questioned.

2. **Check for missing criteria.** All six criteria must be scored. A missing criterion is a gap, not an implicit 0.

3. **Question threshold-crossing decisions.** If a technology scores below 8/18 but is still selected, the ADR must explain why no better alternative exists and what mitigations are planned.

4. **Look for stale familiarity assumptions.** LI-5 scores based on npm downloads from 6+ months ago may not reflect current training data. Check that metrics are recent.

### 6.4 For Implementation Agents

When using LI assessments to plan implementation:

1. **Budget more iterations for low-scoring criteria.** A technology scoring 1/3 on LI-4 (testability) means the test-fix loop will be slower. Plan accordingly.

2. **Front-load documentation retrieval.** If LI-1 is high (good `llms.txt` or MCP docs), use those resources before generating code. If LI-1 is low, gather supplementary documentation into the context window manually.

3. **Flag hallucination risks early.** If LI-6 flags version confusion, pin the exact version in the specification and include version-specific examples in the prompt.

4. **Prefer libraries with high LI-3 for early implementation.** When sequencing work, start with libraries that have small, predictable APIs. Build confidence before tackling libraries with lower LI-3 scores.

---

## Part 7: Replacing Timeline Estimates with Complexity Profiles

### 7.1 The Problem with Calendar Timelines

Calendar-based estimates ("2-3 weeks with 1-2 developers") encode assumptions about human work patterns: 40-hour weeks, context-switching overhead, learning curves, meetings, and weekend breaks. None of these apply to LLM coding agents. An LLM works 24/7, has no meetings, and doesn't learn gradually—it either has the knowledge or it doesn't.

Calendar timelines are also difficult to verify or compare. "2 weeks" means different things depending on developer skill, interruption frequency, and definition of "done."

### 7.2 Complexity Profiles

A complexity profile replaces a timeline estimate with a structural description of the implementation challenge:

| Dimension | What It Measures | How to Assess |
|-----------|-----------------|---------------|
| **Concept count** | Number of distinct concepts the LLM must correctly implement | Count: client setup, schemas, handlers, integrations, etc. |
| **Integration points** | Number of subsystem boundaries the implementation crosses | Count: API connections, database interactions, external services |
| **Pattern conventionality** | How closely the required patterns match LLM training data | Reference LI-3 and LI-5 scores |
| **Test coverage feasibility** | How much of the implementation can be verified through automated testing | Reference LI-4 score; estimate percentage of testable vs. manual-verification code |
| **Expected iteration cycles** | How many generate-test-fix loops before correctness | Estimate based on LI-3 (complexity) and LI-4 (testability): low complexity + high testability = 2-3 cycles; high complexity + low testability = 8-12 cycles |
| **Token budget estimate** | Rough order-of-magnitude token consumption | Concept count × iteration cycles × average tokens per iteration (typically 2K-10K tokens per concept per cycle) |

**Example complexity profile** (replacing a "2-3 weeks" estimate):

> Mastra integration requires implementing ~8 distinct concepts (project setup, agent definitions, tool registration, workflow state machine, persistence adapter, error handling, test harness, deployment configuration). The framework uses conventional TypeScript patterns (LI-3: 2/3) and provides test utilities (LI-4: 2/3). With 3-4 integration points (Convex backend, LLM provider, widget renderer, MCP tools) and moderate concept count, expect 3-5 iteration cycles. Estimated token budget: 150K-400K tokens across all implementation tasks.

---

## Appendix A: Glossary

**API surface area**: The total set of methods, types, configuration options, and patterns that a developer (human or LLM) must understand to use a library correctly.

**Complexity profile**: A structured description of an implementation challenge in terms of concept count, integration points, testability, and iteration expectations. Replaces calendar-based timeline estimates.

**Concept count**: The number of distinct concepts an LLM must correctly combine to implement a feature. Lower counts correlate with higher implementation reliability.

**Hallucination**: When an LLM generates plausible but incorrect code, typically because of incomplete training data, version confusion, or ambiguous API patterns.

**Iteration cycle**: One pass through the generate → test → interpret-failure → fix loop. Each cycle consumes tokens and adds latency.

**LI-1 through LI-6**: The six LLM-Implementability criteria defined in this document. See Part 2 for full definitions.

**LLM-implementability**: The probability that an LLM coding agent will produce correct, production-quality code for a given technology choice, given a well-written specification.

**`llms.txt`**: A standardized text file (similar to `robots.txt`) that libraries publish to provide LLM-friendly documentation. Defined by the llmstxt.org specification.

**MCP (Model Context Protocol)**: A protocol standard for connecting LLM agents to external tools and data sources. MCP servers expose structured tool interfaces that LLMs can invoke programmatically.

**Pattern conventionality**: The degree to which a library's patterns match those commonly found in LLM training data. Conventional patterns (Express-like, React-like) are more reliably generated.

**Recovery cost**: The token and iteration expense of fixing an LLM-generated error. Localized errors (fix one function) have lower recovery cost than cascading errors (wrong configuration affects everything).

**Token budget**: The estimated total token consumption for an implementation task, calculated from concept count × iteration cycles × tokens per iteration.

**Training data representation**: How frequently a library appears in the LLM's training corpus. Higher representation generally correlates with more reliable code generation.

**Version confusion**: A hallucination failure mode where the LLM generates code mixing API patterns from different library versions.

---

## Appendix B: Related Documents

- **STD-22-01** (planned): Enforceable standards making the LI framework mandatory for RF and ADR documents
- **DD-20-01**: Evidence grading framework (S1-S4, I1-I4, Confidence) — LI evidence maps to this framework per §5.1
- **STD-20-01**: Citation format specification — LI evidence citations follow this format
- **DD-13-01**: Artifact taxonomy — defines RF and ADR artifact types that must include LI assessments
- **DD-14-01**: EFN ecosystem definitions — LI criteria apply when evaluating new ecosystem tools
- **SYS-00**: System definition — establishes that Compass is built by LLM coding agents (§1.1)
- **RF-03-02**: Advanced Memory and Context Engineering — the research session that surfaced the need for this framework
- **RF-01-01**: Backend Platform Research — contains an early LLM-maintainability assessment that predates this framework
- **RF-02-01**: Orchestration Framework Research — contains a 14-point LLM-maintainability rubric, the closest predecessor to this framework

---

## Appendix C: Mapping from Prior LLM-Maintainability Rubrics

Several existing RF documents contain LLM-maintainability assessments that predate this framework. This appendix maps their criteria to the LI-1 through LI-6 framework to facilitate updates.

### RF-01-01 Backend Platform Assessment

| RF-01-01 Criterion | Maps to LI Criterion |
|--------------------|-----------------------|
| MCP Server | LI-2 (MCP Tool Availability) |
| `llms.txt` | LI-1 (Documentation Quality) |
| Cursor Rules | LI-2 (MCP Tool Availability) |
| TypeScript Types | LI-3 (Code Complexity — type safety) |
| LLM Error Prevention | LI-6 (Hallucination Risk — error diagnostics) |

### RF-02-01 Orchestration Framework Assessment

| RF-02-01 Criterion | Maps to LI Criterion |
|--------------------|-----------------------|
| Documentation quality | LI-1 (Documentation Quality) |
| TypeScript-first design | LI-3 (Code Complexity — type safety) |
| Common patterns vs DSL | LI-3 (Code Complexity — pattern conventionality) |
| LLM-specific support | LI-1 + LI-2 (combined Documentation + MCP) |
| Error message quality | LI-6 (Hallucination Risk — error diagnostics) |
| Community knowledge | LI-5 (LLM Familiarity) |
| Single-page quickstart | LI-1 (Documentation Quality — complete examples) |

These mappings are provided for convenience. When updating existing RFs, assessors should re-evaluate using the full LI framework rather than mechanically translating old scores.

---

*End of LLM-Implementability Evaluation Framework (DD-22-01)*
