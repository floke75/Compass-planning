---
id: RF-06-01
type: rf
area: 06-research-tools
title: Research Tools Research Findings
status: draft
created: 2026-01-28
updated: 2026-01-28
author: compass-research
summary: Evaluates research and context collection tools for Compass evidence gathering against DD-20-01 standards
tags: [research-tools, evidence, context, web-scraping, documentation, mcp]
related:
  - DD-20-01
  - STD-20-01
  - ADR-04-01
confidence: high
methodology: "Documentation analysis, pricing verification, and evidence standards mapping"
limitations:
  - "Rate limits and pricing subject to vendor changes"
  - "MCP server ecosystem rapidly evolving"
  - "Version-specific coverage varies by library popularity"
responds_to: null
implications_for: [integration-pipeline, pristine-context-layer]
---

# Research Tools Research Findings

## Executive Summary

**Recommendation**: Deploy **Context7 + Firecrawl + Tavily** as the primary research tool stack for Compass evidence collection.

**Confidence**: High — all three tools have official MCP servers, production-grade APIs, and pricing within budget constraints.

**Key Trade-offs**:
- Context7 excels at version-specific library documentation but has no general web capability
- Firecrawl provides comprehensive web scraping with JS rendering but requires credit-based budgeting
- Tavily offers RAG-optimized search with citations but limited depth per result
- No single tool provides all DD-20-01 citation fields natively; a transformation layer is required

**Phase 1 Cost**: $192/year (Context7 Free + Firecrawl Hobby + Tavily Free)
**Phase 3 Cost**: $1,356–1,680/year depending on volume and Exa allocation

---

## Part 1: Source Coverage Matrix

### 1.1 Coverage by Content Type

| Content Type | Best Tool | Alternative | Coverage Quality |
|-------------|-----------|-------------|------------------|
| Version-specific library docs | **Context7** | Firecrawl (crawl docs site) | Excellent — 43k+ libraries indexed with version tags |
| Static documentation pages | Jina Reader | Firecrawl | Good — both produce clean Markdown |
| JavaScript-rendered SPAs | **Firecrawl** | Browserbase | Excellent — Chromium fleet handles most cases |
| PDF documents | **Firecrawl** | Jina Reader | Good — native PDF extraction |
| GitHub repositories | **GitHub API** | Firecrawl | Excellent — direct metadata access |
| npm/PyPI metadata | **Direct APIs** | Context7 | Excellent — no auth for public packages |
| General web search | **Tavily** | Exa | Good — RAG-optimized with citations |
| Complex interactions (auth) | **Browserbase** | None | Specialized — only for protected content |

### 1.2 Tool-by-Tool Coverage Assessment

**Context7** [1]
- Indexes 43,000+ libraries from official documentation sources
- Version-specific matching: explicit (`/vercel/next.js/v15.1.8`) or inferred from query
- Semantic search across code snippets and explanatory text
- Benchmark scores available (Next.js: 82.2) for quality verification
- Gap: No general web capability; library must be in index

**Firecrawl** [2]
- Full web scraping with JavaScript rendering via pre-warmed Chromium fleet
- PDF extraction, full-site crawls, and structured data extraction
- Browser actions (click, scroll, type) for complex SPAs
- waitFor strategies up to 300s timeout for slow-loading content
- Gap: No version-aware library indexing; treats docs as generic web pages

**Tavily** [3]
- Search API returns up to 20 aggregated sources per query
- Optimized for RAG pipelines with LLM-ready content formatting
- Include/exclude domain filtering for source quality control
- `raw_content` option for full page text (higher credit cost)
- Gap: Limited depth per result; discovery-focused rather than extraction-focused

**Jina Reader** [4]
- URL-to-Markdown conversion via `r.jina.ai/{url}`
- ReaderLM-v2 model (1.5B parameters) for content extraction
- JSON mode with metadata headers available
- Free tier: 10M tokens/month
- Gap: No search capability; URL must be known

**Exa** [5]
- Neural/semantic search with 94.9% accuracy on SimpleQA benchmark
- Rich metadata including author and ISO 8601 published dates
- Content extraction with highlights
- Gap: Higher cost per query than Tavily; better for precision than volume

**Perplexity API** [6]
- AI-synthesized answers with inline citations
- Multiple models available (sonar-pro, sonar-deep-research)
- Gap: Per-request pricing ($5-14/1k requests + tokens) expensive for systematic collection

**Browserbase** [7]
- Full headless browser automation with Playwright/Puppeteer
- Session persistence, CAPTCHA solving, anti-detection
- Gap: $20/month minimum; overkill for most documentation scraping

### 1.3 Coverage Gaps and Mitigations

| Gap | Mitigation |
|-----|------------|
| Context7 missing library | Submit to context7.com/add-library; fallback to Firecrawl docs crawl |
| Authenticated documentation | Browserbase for login-protected content (add only if needed) |
| Real-time news/events | Tavily search with date filters; Exa for semantic precision |
| Historical documentation versions | GitHub releases API; Wayback Machine (manual) |

---

## Part 2: Evidence Standards Fit

### 2.1 DD-20-01 Required Fields Mapping

Per DD-20-01 and STD-20-01, each citation requires:
- `id`: Unique identifier (`cite-{artifact-id}-{NNN}`)
- `source_url`: Full URL with protocol
- `title`: Source document title
- `source_type`: Enumerated type (api_docs, vendor_docs, etc.)
- `retrieved_at`: ISO 8601 timestamp with timezone

Recommended fields:
- `author`: Person or organization
- `date_published`: ISO 8601 date
- `version`: Software/API version
- `tier`: T1–T5 source classification
- `reliability`: S1–S4 rating

### 2.2 Native Field Support by Tool

| Tool | source_url | title | retrieved_at | date_published | version | content_hash |
|------|-----------|-------|--------------|----------------|---------|--------------|
| Context7 | ✅ `source` | ✅ | ❌ Add at ingestion | ❌ | ✅ Explicit | ❌ |
| Firecrawl | ✅ `sourceURL` | ✅ `metadata.title` | ❌ Add at ingestion | ❌ | ❌ | ✅ Change tracking |
| Jina Reader | ✅ Header/JSON | ✅ | ✅ JSON mode | ❌ | ❌ | ❌ |
| Tavily | ✅ `url` | ✅ `title` | ❌ Add at ingestion | Partial | ❌ | ❌ |
| Exa | ✅ `url` | ✅ `title` | ❌ Add at ingestion | ✅ ISO 8601 | ❌ | ❌ |
| Perplexity | ✅ `citations[]` | ❌ URLs only | ❌ | ❌ | ❌ | ❌ |
| GitHub API | ✅ Constructed | ✅ | ✅ Add at ingestion | ✅ `updated_at` | ✅ Tags | ✅ ETag |

**Assessment**: No tool provides all fields natively. **Exa** offers the richest metadata (author, published date in ISO 8601). **GitHub API** provides the most complete evidence artifact support including ETags for change detection.

### 2.3 Transformation Requirements

All tools require a wrapper layer to meet DD-20-01 compliance:

```javascript
// Transformation pseudocode for evidence artifact
function transformToEvidence(rawResponse, tool, sourceType) {
  return {
    schema_version: "1.0",
    citation: {
      id: generateCitationId(),
      source_url: extractUrl(rawResponse, tool),
      title: extractTitle(rawResponse, tool),
      source_type: sourceType,
      retrieved_at: new Date().toISOString(),
      author: extractAuthor(rawResponse, tool) || null,
      date_published: extractPublishedDate(rawResponse, tool) || null,
      version: extractVersion(rawResponse, tool) || null,
      tier: classifyTier(sourceUrl),
      reliability: assessReliability(sourceUrl, tool)
    },
    content: {
      text: extractContent(rawResponse, tool),
      excerpt: truncate(extractContent(rawResponse, tool), 500)
    },
    quality: {
      content_hash: computeSha256(extractContent(rawResponse, tool)),
      freshness_score: null // Computed at retrieval time
    }
  };
}
```

### 2.4 Source Tier Classification Rules

Per DD-20-01 Part 2.1, implement domain-based classification:

| Pattern | Tier | Rationale |
|---------|------|-----------|
| `react.dev`, `nextjs.org`, `docs.convex.dev` | T1 | Official vendor documentation |
| `github.com/{vendor}/*` | T1 | Official vendor repositories |
| `developer.mozilla.org` | T2 | Validated community (MDN) |
| `stackoverflow.com` (50+ score, accepted) | T2 | High community validation |
| `*.medium.com`, `dev.to` | T4 | General community |
| Unknown domains | T4 | Default until verified |
| Anonymous forums | T5 | Unverified |

### 2.5 Freshness Tracking Support

Per DD-20-01 Part 4, freshness requires:
- `retrieved_at`: All tools support via wrapper injection
- `date_published`: Exa provides; others require extraction or estimation
- `version`: Context7 provides; others require URL parsing or metadata extraction
- Change detection: Firecrawl change tracking mode; GitHub API ETags; others require hash comparison

**Staleness calculation** must be implemented in the transformation layer using content-type thresholds from DD-20-01 Part 4.2.

---

## Part 3: Output Format Assessment

### 3.1 Markdown Quality Comparison

**Firecrawl** produces the cleanest Markdown for complex pages:
- Proper header hierarchy (H1 → H2 → H3)
- Code blocks with language tags preserved
- Tables converted accurately
- Relative links maintained
- Navigation/boilerplate filtered

**Jina Reader** (ReaderLM-v2) handles most content well:
- Strong table and list conversion
- Occasional issues with complex navigation layouts
- Better for simpler documentation pages

**Context7** returns structured JSON requiring reconstruction:
- Code snippets in separate array
- Explanatory text in another array
- Useful for programmatic processing
- Requires template for human-readable output

**Tavily** returns content as text within JSON:
- `content` field: Summary text
- `raw_content` field: Full page (optional, higher cost)
- Adequate for search results; less polished than Firecrawl

### 3.2 Metadata Structure

**Context7 response structure**:
```json
{
  "library": "react",
  "version": "19.0",
  "source": "https://react.dev/reference/react/useEffect",
  "snippets": [
    {"code": "useEffect(() => {...})", "language": "jsx"},
    {"text": "useEffect is a React Hook that..."}
  ]
}
```

**Firecrawl response structure**:
```json
{
  "success": true,
  "data": {
    "markdown": "# Page Title\n\nContent...",
    "metadata": {
      "title": "Page Title",
      "sourceURL": "https://example.com/page",
      "statusCode": 200
    }
  }
}
```

**Tavily response structure**:
```json
{
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "content": "Summary text...",
      "score": 0.95,
      "raw_content": "Full page text..."
    }
  ]
}
```

### 3.3 Obsidian Compatibility

All tools require post-processing for Obsidian vault storage:

**Target format** (per ADR-04-01):
```yaml
---
source_url: "https://react.dev/reference/react/useEffect"
title: "useEffect – React"
source_type: "api_docs"
tier: "T1"
reliability: "S1"
retrieved_at: "2026-01-28T14:30:00Z"
date_published: null
version: "React 19.0"
content_hash: "sha256:a3b8c9d..."
tool: "context7"
---

# useEffect – React

[Markdown content here...]

## Sources

1. **[T1/S1]** React. "useEffect". React 19 Documentation.
   Retrieved 2026-01-28. https://react.dev/reference/react/useEffect
```

**Transformation steps**:
1. Extract raw response from tool
2. Generate YAML frontmatter with all citation fields
3. Clean Markdown body (Firecrawl/Jina output ready; Context7 requires assembly)
4. Append Sources section per STD-20-01 format
5. Write to Obsidian vault at appropriate path

---

## Part 4: Rate Limits and Pricing

### 4.1 Detailed Pricing by Tool

**Context7** [8]
| Tier | Price | Limits |
|------|-------|--------|
| Free | $0 | Unlimited queries; public libraries only |
| Pro | $7/seat/month | Private repos; priority support |

**Firecrawl** [9]
| Tier | Price | Credits/Month | Per-Credit Cost |
|------|-------|---------------|-----------------|
| Free | $0 | 500 | N/A |
| Hobby | $16/month | 3,000 | $0.0053 |
| Standard | $83/month | 100,000 | $0.00083 |
| Growth | $333/month | 500,000 | $0.00067 |

Credit consumption: 1 credit = 1 scrape (Markdown mode); 5 credits = extract mode; 50 credits = deep research

**Tavily** [10]
| Tier | Price | Credits/Month |
|------|-------|---------------|
| Free (Researcher) | $0 | 1,000 |
| Bootstrap | $50/month | 15,000 |
| Project | $150/month | 50,000 |

**Jina Reader** [11]
| Tier | Price | Tokens/Month |
|------|-------|--------------|
| Free | $0 | 10M |
| Basic | $9.90/month | 100M |

**Exa** [12]
| Operation | Cost |
|-----------|------|
| Neural search | $5/1,000 requests |
| Content extraction | $1/1,000 requests |
| Highlights | $1/1,000 requests |

**Perplexity API** [6]
| Model | Cost |
|-------|------|
| sonar | $5/1M input tokens; $15/1M output |
| sonar-pro | $3/1M input; $15/1M output |
| sonar-deep-research | $2/request |

**Browserbase** [7]
| Tier | Price | Sessions |
|------|-------|----------|
| Starter | $20/month | 1,000 |
| Developer | $100/month | 10,000 |

### 4.2 Phase 1 Cost Projections ($600/year budget)

**Estimated volume**: 10–20 requests/day = 300–600/month

| Configuration | Monthly Cost | Annual Cost | Capacity |
|--------------|--------------|-------------|----------|
| Context7 Free + Firecrawl Hobby + Tavily Free | $16 | **$192** | 3,000 scrapes + 1,000 searches |
| + Jina Free | $16 | **$192** | +10M tokens for simple pages |
| + Exa $10/month allocation | $26 | **$312** | +2,000 neural searches |

**Recommended Phase 1**: $192/year core stack, $120 Exa reserve = **$312/year** (52% of budget)

### 4.3 Phase 3 Cost Projections ($2,000/year budget)

**Estimated volume**: 50–100 requests/day = 1,500–3,000/month

| Configuration | Monthly Cost | Annual Cost | Capacity |
|--------------|--------------|-------------|----------|
| Context7 Free + Firecrawl Standard + Tavily Free | $83 | **$996** | 100k scrapes + 1k searches |
| Context7 Free + Firecrawl Standard + Tavily Bootstrap | $133 | **$1,596** | 100k scrapes + 15k searches |
| + Exa allocation ($30/month) | $163 | **$1,956** | +6,000 neural searches |

**Recommended Phase 3**: Firecrawl Standard + Tavily Free + Exa allocation = **$1,356/year** with headroom for burst usage

### 4.4 Rate Limit Considerations

| Tool | Rate Limit | Burst Handling |
|------|------------|----------------|
| Context7 | No published limit | Assumed fair use |
| Firecrawl | Based on plan tier | Credits roll over (unclear) |
| Tavily | Tier-based monthly | No rollover |
| Jina | Token-based monthly | Basic tier for burst |
| Exa | Pay-per-request | No limit beyond budget |
| GitHub API | 5,000/hour authenticated | Adequate for research |

---

## Part 5: Ingestion Pipeline Sketch

### 5.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DISCOVERY LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│  Tavily Search      →  RAG-optimized results with URLs              │
│  Exa Neural Search  →  Semantic matches for complex queries         │
│  GitHub Search API  →  Repository and code discovery                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          ROUTING LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│  URL Pattern Matching:                                               │
│  • Library docs domains → Context7                                   │
│  • github.com/*/*       → GitHub API                                 │
│  • *.pdf URLs           → Firecrawl (PDF mode)                       │
│  • Known SPAs           → Firecrawl (with actions)                   │
│  • Simple static pages  → Jina Reader (cost optimization)            │
│  • Unknown URLs         → Firecrawl (robust fallback)                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTRACTION LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│  Context7        →  Version-specific library documentation          │
│  Firecrawl       →  General web, SPAs, PDFs, full-site crawls       │
│  Jina Reader     →  Simple static pages (free tier optimization)    │
│  GitHub API      →  README, releases, code files                    │
│  npm/PyPI APIs   →  Package metadata, dependencies                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TRANSFORMATION LAYER                             │
├─────────────────────────────────────────────────────────────────────┤
│  1. Capture raw response + tool metadata                             │
│  2. Inject retrieved_at timestamp (ISO 8601)                         │
│  3. Compute content SHA-256 hash                                     │
│  4. Classify source tier (T1-T5) by domain rules                     │
│  5. Assess source reliability (S1-S4)                                │
│  6. Generate YAML frontmatter per STD-20-01                          │
│  7. Clean/normalize Markdown body                                    │
│  8. Append Sources section                                           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         STORAGE LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  Obsidian Vault (per ADR-04-01):                                     │
│  • /evidence/{date}/{source-domain}/{slug}.md                        │
│  • Git commit with retrieval metadata                                │
│  • Index update for cross-reference                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Routing Logic (Pseudocode)

```javascript
function selectTool(url, queryContext) {
  // Version-specific library documentation
  const libraryDomains = [
    'react.dev', 'nextjs.org', 'docs.convex.dev',
    'vuejs.org', 'angular.io', 'svelte.dev'
  ];
  if (libraryDomains.some(d => url.includes(d))) {
    return { tool: 'context7', reason: 'Version-aware library docs' };
  }
  
  // GitHub content
  if (url.match(/github\.com\/[\w-]+\/[\w-]+/)) {
    return { tool: 'github-api', reason: 'Direct repository access' };
  }
  
  // PDF documents
  if (url.endsWith('.pdf') || url.includes('/pdf/')) {
    return { tool: 'firecrawl', mode: 'pdf', reason: 'PDF extraction' };
  }
  
  // Known JavaScript-heavy SPAs
  const spaIndicators = ['app.', 'dashboard.', 'console.'];
  if (spaIndicators.some(i => url.includes(i))) {
    return { tool: 'firecrawl', mode: 'spa', reason: 'JS rendering required' };
  }
  
  // Simple static pages (cost optimization)
  const staticPatterns = ['docs.', 'wiki.', 'help.'];
  if (staticPatterns.some(p => url.includes(p))) {
    return { tool: 'jina', reason: 'Simple page, free tier' };
  }
  
  // Default fallback
  return { tool: 'firecrawl', mode: 'standard', reason: 'Robust fallback' };
}
```

### 5.3 MCP Server Configuration

**Claude Desktop / Claude Code configuration** (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "description": "Version-specific library documentation"
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      },
      "description": "Web scraping with JS rendering"
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY}"
      },
      "description": "RAG-optimized web search"
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "${EXA_API_KEY}"
      },
      "description": "Neural semantic search"
    }
  }
}
```

**Remote MCP endpoints** (for server-side integration):
- Context7: `https://mcp.context7.com/mcp`
- Firecrawl: `https://mcp.firecrawl.dev/{API_KEY}/v2/mcp`
- Tavily: `https://mcp.tavily.com/mcp`

---

## Part 6: Recommendation

### 6.1 Primary Tool Selection

| Role | Tool | Rationale |
|------|------|-----------|
| Library documentation | **Context7** | Version-specific indexing, 43k+ libraries, free tier adequate |
| General web scraping | **Firecrawl** | Best Markdown quality, JS rendering, PDF support, MCP ready |
| Discovery/search | **Tavily** | RAG-optimized, citations included, free tier for Phase 1 |

### 6.2 Secondary Tools (As Needed)

| Role | Tool | When to Add |
|------|------|-------------|
| Semantic search | **Exa** | Complex research queries requiring precision |
| Simple pages | **Jina Reader** | Cost optimization for known static pages |
| AI synthesis | **Perplexity API** | Occasional complex queries requiring synthesis |
| Protected content | **Browserbase** | Only if authenticated documentation access needed |

### 6.3 Implementation Priority

**Phase 1 (Immediate)**:
1. Deploy Context7 + Firecrawl + Tavily via MCP servers
2. Build transformation layer for YAML frontmatter generation
3. Implement content hashing for change detection
4. Establish domain-based tier classification rules
5. Create Obsidian vault storage structure

**Phase 2 (Scaling)**:
1. Add Exa for semantic search capabilities
2. Implement freshness tracking with staleness alerts
3. Build URL routing logic for tool selection
4. Add Jina Reader for cost optimization on simple pages

**Phase 3 (Comprehensive)**:
1. Upgrade Firecrawl tier based on volume
2. Consider Browserbase for authenticated content (if needed)
3. Implement full evidence artifact schema storage
4. Add change detection pipeline with content hash comparison

---

## Sources

1. **[T1/S1]** Upstash. "Context7 MCP: Up-to-Date Docs for Any Cursor Prompt".
   Retrieved 2026-01-28. https://upstash.com/blog/context7-mcp

2. **[T1/S1]** Firecrawl. "Firecrawl Documentation".
   Retrieved 2026-01-28. https://docs.firecrawl.dev/

3. **[T1/S1]** Tavily. "About - Tavily Docs".
   Retrieved 2026-01-28. https://docs.tavily.com/documentation/about

4. **[T2/S2]** Scrapeless. "Best Jina.ai Alternatives".
   Retrieved 2026-01-28. https://www.scrapeless.com/en/wiki/jina-ai-alternatives

5. **[T1/S1]** Exa. "Web Search API and Crawling for AI".
   Retrieved 2026-01-28. https://exa.ai/exa-api

6. **[T1/S1]** Perplexity. "Perplexity API Platform".
   Retrieved 2026-01-28. https://www.perplexity.ai/api-platform

7. **[T2/S2]** GoLogin. "Is Browserbase Any Good? Tech Expert Review".
   Retrieved 2026-01-28. https://gologin.com/blog/is-browserbase-any-good/

8. **[T1/S1]** Context7. "Plans & Pricing - Context7 MCP".
   Retrieved 2026-01-28. https://context7.com/docs/plans-pricing

9. **[T1/S1]** Firecrawl. "Firecrawl Pricing".
   Retrieved 2026-01-28. https://www.firecrawl.dev/pricing

10. **[T2/S2]** Firecrawl Blog. "Tavily Pricing: Complete Breakdown".
    Retrieved 2026-01-28. https://www.firecrawl.dev/blog/tavily-pricing

11. **[T2/S2]** Apify. "Jina AI vs. Firecrawl for web-LLM extraction".
    Retrieved 2026-01-28. https://blog.apify.com/jina-ai-vs-firecrawl/

12. **[T1/S1]** Exa Labs. "Exa MCP Server - GitHub".
    Retrieved 2026-01-28. https://github.com/exa-labs/exa-mcp-server

---

*End of Research Tools Research Findings (RF-06-01)*
