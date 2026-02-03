---
id: ADR-06-01
type: adr
area: 06-research-tools
title: Research Tools Selection
status: proposed
created: 2026-01-28
updated: 2026-02-03
author: compass-research
summary: Selects Context7 + Firecrawl + Tavily as the research tool stack for Compass context collection
tags: [research-tools, decision, context7, firecrawl, tavily, mcp]
related:
  - RF-06-01
  - DD-20-01
  - STD-20-01
  - ADR-04-01
links:
  - rel: related
    target_id: "RF-06-01"
  - rel: related
    target_id: "DD-20-01"
  - rel: related
    target_id: "STD-20-01"
  - rel: related
    target_id: "ADR-04-01"
decision_date: null
deciders: []
supersedes: null
---

# Research Tools Selection

## Status

Proposed

## Context

Compass is an LLM-orchestrated planning, research, and documentation system. The Pristine Context Layer (Layer 5 per SYS-00) requires verified external sources with full citation metadata for evidence-based planning and implementation. Research tools must support the evidence standards defined in DD-20-01/STD-20-01, including source URL capture, retrieval timestamps, source tier classification (T1–T5), and content hashing for change detection.

The tool selection must satisfy these constraints:
- Phase 1 budget: $600/year ($50/month)
- Phase 3 budget: $2,000/year (~$167/month)
- Output compatible with Obsidian vault (Markdown with YAML frontmatter)
- MCP server availability for Claude/LLM integration
- Coverage of version-specific library documentation, general web content, and PDFs

## Options Considered

### Option 1: Context7 + Firecrawl + Tavily (Recommended)

Three specialized tools covering complementary domains: Context7 for version-specific library documentation, Firecrawl for general web scraping with JS rendering, and Tavily for RAG-optimized search with citations.

**Pros:**
- Context7 indexes 43,000+ libraries with version-specific matching
- Firecrawl produces clean Markdown with JS rendering and PDF support
- Tavily provides discovery with up to 20 aggregated sources per query
- All three have official MCP servers
- Phase 1 cost: $192/year (32% of budget)
- Phase 3 cost: $996–1,596/year (50–80% of budget)

**Cons:**
- Three tools to configure and maintain
- No single tool provides all DD-20-01 citation fields natively
- Requires transformation layer for evidence artifact generation

### Option 2: Firecrawl + Exa

Firecrawl for all web scraping, Exa for semantic search with rich metadata.

**Pros:**
- Exa provides best-in-class metadata (author, ISO 8601 dates)
- Fewer tools to maintain
- 94.9% accuracy on SimpleQA benchmark

**Cons:**
- No version-specific library documentation support
- Exa costs $5/1,000 requests (expensive at scale)
- Phase 1 cost: $192 + ~$300 Exa = $492/year
- Phase 3 cost: ~$1,800/year for adequate Exa volume

### Option 3: Perplexity API + Firecrawl

Perplexity for search with AI synthesis, Firecrawl for extraction.

**Pros:**
- Perplexity provides AI-synthesized answers with citations
- Single search tool reduces complexity

**Cons:**
- Perplexity pricing ($5–14/1k requests + tokens) expensive for systematic collection
- No version-specific documentation support
- Limited control over source selection
- Better suited for occasional complex queries than pipeline integration

### Option 4: Browserbase + Custom Scraping

Full browser automation for maximum flexibility.

**Pros:**
- Handles any JavaScript, authentication, or anti-bot protection
- Complete control over extraction logic

**Cons:**
- $20/month minimum ($240/year) exceeds simple scraping needs
- Requires custom scraping code for each site type
- Overkill for documentation and static content
- No search capability included

### Option 5: Jina Reader Only

Minimalist approach using only Jina Reader's free tier.

**Pros:**
- Zero cost (10M tokens/month free)
- Simple URL-to-Markdown conversion

**Cons:**
- No search/discovery capability
- No version-specific library support
- Limited JS rendering compared to Firecrawl
- Requires knowing exact URLs in advance

## Decision

We will use **Context7 + Firecrawl + Tavily** as the primary research tool stack.

This combination provides comprehensive coverage across all Compass evidence collection needs:

1. **Context7** (Free tier) handles version-specific library documentation—critical for researching rapidly evolving frameworks like React, Next.js, and Convex. The semantic search across 43,000+ libraries with explicit version matching prevents outdated documentation from polluting research findings.

2. **Firecrawl** (Hobby tier, $16/month) provides robust web scraping with JavaScript rendering for SPAs, PDF extraction, and clean Markdown output. The 3,000 monthly credits accommodate Phase 1 volume with headroom for bursts.

3. **Tavily** (Free tier) enables RAG-optimized search with citations, returning up to 20 sources per query. The free tier's 1,000 monthly credits cover discovery needs without additional cost.

**Secondary tools** to add as needed:
- **Exa** for semantic search precision on complex research queries
- **Jina Reader** for cost optimization on simple static pages
- **GitHub API** for repository metadata and release notes
- **Browserbase** only if authenticated content access proves necessary

## Consequences

### Positive

- All three primary tools have official MCP servers, enabling direct Claude integration
- Phase 1 annual cost ($192) is 32% of budget, leaving significant headroom
- Version-specific documentation support prevents outdated library information
- Firecrawl's Markdown quality reduces post-processing complexity
- Tool specialization allows routing queries to optimal extraction method

### Negative

- Three tools require configuration and API key management
- No tool provides all DD-20-01 citation fields natively—transformation layer required
- MCP server ecosystem is rapidly evolving; may require updates
- Context7 coverage depends on library popularity; gaps may require fallback

### Neutral

- Transformation layer for YAML frontmatter generation is needed regardless of tool selection
- Content hashing for change detection must be implemented in transformation layer
- Source tier classification (T1–T5) requires domain-based rules regardless of tool

## Implementation Notes

### Phase 1 Setup

1. **API Key Acquisition**
   - Context7: Free, no key required for MCP (uses public endpoint)
   - Firecrawl: Sign up at firecrawl.dev, obtain API key
   - Tavily: Sign up at tavily.com, obtain API key

2. **MCP Server Configuration** (claude_desktop_config.json)
   ```json
   {
     "mcpServers": {
       "context7": {
         "command": "npx",
         "args": ["-y", "@upstash/context7-mcp"]
       },
       "firecrawl": {
         "command": "npx",
         "args": ["-y", "firecrawl-mcp"],
         "env": {"FIRECRAWL_API_KEY": "fc-xxx"}
       },
       "tavily": {
         "command": "npx",
         "args": ["-y", "tavily-mcp@latest"],
         "env": {"TAVILY_API_KEY": "tvly-xxx"}
       }
     }
   }
   ```

3. **Transformation Layer**
   - Build wrapper functions for each tool
   - Inject `retrieved_at` timestamp (ISO 8601)
   - Compute SHA-256 content hash
   - Classify source tier by domain rules
   - Generate YAML frontmatter per STD-20-01
   - Store to Obsidian vault

4. **Domain Classification Rules**
   - T1: Official vendor domains (react.dev, nextjs.org, etc.)
   - T2: MDN, high-score Stack Overflow
   - T3: Curated tutorials, conference talks
   - T4: Medium, Dev.to, personal blogs
   - T5: Anonymous forums, AI-generated without verification

### Phase 3 Scaling

1. Upgrade Firecrawl to Standard tier ($83/month) for 100,000 credits
2. Add Exa allocation (~$30/month) for semantic search precision
3. Consider Tavily Bootstrap ($50/month) if search volume exceeds free tier
4. Implement freshness tracking with staleness alerts per DD-20-01 Part 4

### Fallback Positions

- **Context7 library gap**: Crawl docs site directly with Firecrawl; submit to context7.com/add-library
- **Firecrawl rate limit**: Prioritize high-value extractions; use Jina Reader for simple pages
- **Tavily depth limitation**: Use Exa for queries requiring more precision
- **Authenticated content**: Add Browserbase only when specific protected documentation needed

## Related Documents

- **RF-06-01**: Research findings supporting this decision
- **DD-20-01**: Evidence standards the tools must support
- **STD-20-01**: Citation format specification
- **ADR-04-01**: Documentation platform (Obsidian) the tools must integrate with
- **SYS-00**: System definition describing Pristine Context Layer requirements

---

*End of Research Tools Selection (ADR-06-01)*
