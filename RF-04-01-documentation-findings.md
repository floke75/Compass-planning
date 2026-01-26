---
id: RF-04-01
type: rf
area: 04-documentation
title: Documentation Platform Research Findings
status: draft
created: 2026-01-26
updated: 2026-01-26
author: compass-research
summary: Evaluates documentation platforms for Compass against requirements for YAML frontmatter, Git integration, backlinks, and LLM retrieval
tags: [documentation, knowledge-management, platform, obsidian, gitbook, mcp]
related:
  - DD-12-01
  - DD-13-01
confidence: high
methodology: "Web research with feature comparison across 7 candidates, pricing verification, MCP ecosystem assessment"
limitations:
  - "Real-time collaboration assessment based on documentation rather than hands-on testing"
  - "Mobile sync performance claims not independently verified"
responds_to: null
implications_for: [A06]
---

# Documentation Platform Research Findings

## Executive Summary

**Primary Recommendation**: Obsidian with Git

**Confidence Level**: High for core documentation requirements; Medium for team collaboration workflows

**Key Trade-offs**:
- Obsidian delivers perfect YAML frontmatter preservation, native backlinks, mature MCP servers, and zero cost
- No real-time collaborative editing (async via Git only)
- PR workflow requires GitHub web interface rather than in-app

**Alternative**: GitBook when prioritizing native llms.txt generation, polished collaboration UI, and professional documentation appearance over wiki-style backlinks. Budget ~$30-95/month depending on tier.

The documentation platform landscape underwent significant transformation in 2024-2025 with MCP (Model Context Protocol) adoption across major platforms. Anthropic donated MCP to the Linux Foundation in December 2025, and it is now supported by OpenAI, Google DeepMind, and over 2,000 MCP servers exist in the ecosystem. This fundamentally changes how LLM agents access documentation—native MCP support is now a realistic selection criterion rather than a nice-to-have.

---

## Part 1: Capability Matrix

### 1.1 Full Comparison

| Capability | Obsidian + Git | VS Code + Foam | Docusaurus | Mintlify | GitBook | Outline | Notion |
|------------|----------------|----------------|------------|----------|---------|---------|--------|
| **YAML Frontmatter (10+ fields)** | ✅ Excellent | ✅ Excellent | ⚠️ Good | ✅ Excellent | ⚠️ Good* | ❌ Not native | ❌ Properties instead |
| **Git Integration** | ✅ Good | ✅ Excellent | ✅ Good | ✅ Excellent | ✅ Excellent | ❌ None | ❌ Fragile tools |
| **Wiki-links** | ✅ Native | ✅ Foam | ❌ No | ❌ No | ❌ No | ⚠️ @mentions | ⚠️ @mentions |
| **Backlinks** | ✅ Native | ✅ Foam | ❌ No | ❌ No | ❌ No | ✅ Native | ✅ Native |
| **Graph Visualization** | ✅ Built-in | ✅ Foam | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **MCP Server** | ✅ Multiple mature | ✅ Filesystem | ⚠️ None | ✅ Native auto | ✅ Native auto | ✅ Community | ✅ Official |
| **llms.txt** | ⚠️ Manual | ⚠️ Manual | ⚠️ Build-time | ✅ Auto | ✅ Auto | ⚠️ Manual | ⚠️ Manual |
| **Real-time Collaboration** | ❌ Limited | ✅ Live Share | ❌ PR-only | ❌ PR-only | ✅ Good | ✅ Excellent | ✅ Excellent |
| **Vendor Lock-in** | ✅ None | ✅ None | ⚠️ Low | ⚠️ Low | ⚠️ Medium | ✅ Low | ⚠️ High |
| **Phase 1 Budget (<$50)** | ✅ $0 | ✅ $0 | ✅ $0 | ❌ $0/1 user | ✅ ~$30 | ✅ $10 | ✅ $20-30 |
| **Phase 3 Budget (<$150)** | ✅ $0 | ✅ $0 | ✅ $0 | ❌ $300 | ✅ ~$95-125 | ✅ $10-79 | ✅ $40-60 |

*GitBook preserves frontmatter via Git Sync but web editor edits may strip custom fields

### 1.2 Requirement Coverage by Candidate

**Obsidian + Git**: Meets all core requirements. Perfect frontmatter preservation with Properties View UI. Native wiki-links (`[[artifact-id]]`) and backlinks panel. Built-in graph visualization. Multiple mature MCP servers available. Zero cost for core workflow.

**VS Code + Foam**: Meets all core requirements through extension ecosystem. Most direct Git integration via VS Code's built-in source control. Foam provides wiki-links, backlinks, and graph visualization. Real-time collaboration via Live Share. Zero cost.

**GitBook**: Strong on Git integration (truly bidirectional sync) and native MCP/llms.txt generation. Weaker on wiki-links and graph visualization. Web editor may not preserve custom frontmatter fields—Git-first editing required. Moderate cost fits both budget phases.

**Mintlify**: Excellent MDX/frontmatter support and AI-native features including auto llms.txt and MCP with API execution. Pricing creates insurmountable barrier: Hobby tier limits to 1 member, Pro tier costs $300/month—double the Phase 3 budget.

**Outline**: Excellent real-time collaboration. Stores content in internal format rather than raw markdown with YAML frontmatter. No Git integration. Community MCP servers available. Very low cost ($10/month starter).

**Notion**: Rich collaboration features and official MCP server. Uses database properties instead of YAML frontmatter—requires transformation for Compass compatibility. Git sync tools exist but are fragile. Moderate cost.

**Docusaurus**: Open-source static site generator. Good frontmatter support at build time. No editing experience, backlinks, or graph visualization. MCP servers not available. Free but requires developer setup.

---

## Part 2: Format Compatibility

### 2.1 YAML Frontmatter Handling

**Obsidian** preserves all YAML frontmatter fields without modification and provides a built-in Properties View (since v1.4) for viewing and editing frontmatter as structured properties. This is the cleanest solution for Compass's 10+ required fields per DD-13-01.

**VS Code with plain markdown** naturally preserves frontmatter since files are never transformed. Extensions like Foam can parse and utilize frontmatter for navigation and organization.

**GitBook's web editor** uses an internal content model rather than raw markdown frontmatter. When editing through Git Sync, frontmatter is preserved, but editing through the web interface may not maintain custom fields—only documented fields survive the round-trip reliably. Recommendation: establish Git as primary editing path.

**Mintlify** keeps true MDX files in your git repository. The platform reads specific fields (title, description, sidebarTitle) but does not strip unknown custom fields. Your files remain standard MDX with frontmatter.

**Notion lacks frontmatter entirely** but database properties serve as a robust alternative. All 10+ Compass fields map cleanly to property types: id (auto), type (select), area (select), title (title), status (select), created/updated (dates auto), author (person), summary (rich_text), tags (multi-select), related (relation). The limitation: properties do not export to YAML frontmatter natively without tools like notion-to-md.

**Outline stores content in its internal format**, not raw markdown with YAML frontmatter. Document metadata (title, author, timestamps) is database-stored. Custom fields would require structured templates in document bodies or API automation.

### 2.2 Naming Convention Support

All git-backed platforms (Obsidian, VS Code/Foam, GitBook, Mintlify, Docusaurus) support Compass naming conventions defined in DD-12-01:
- Prefix patterns: `SPEC-`, `ADR-`, `RF-`, `DD-`, `STD-`, `HANDOFF-`, `IDX-`
- kebab-case file naming
- Area codes in filenames

Notion and Outline use page titles rather than filenames, requiring convention enforcement through templates or automation.

---

## Part 3: Git Integration Workflow

### 3.1 Obsidian with Obsidian Git Plugin

**Workflow**: Automatic commit-and-sync cycles with pull-on-startup, Source Control View, and line-by-line diff viewing. The workflow supports feature branches, but PR creation requires GitHub's web interface—the plugin focuses on sync rather than full GitHub Flow.

**Conflict handling**: Uses standard git conflict markers with manual resolution in editor.

**Mobile sync**: Uses isomorphic-git JavaScript implementation with known performance issues on large vaults (1000+ files). Desktop reliability is excellent using native git.

**Strengths**: Familiar git workflow for developers. Full history preserved. Branch switching supported.

**Limitations**: No in-app PR creation or review. Mobile performance concerns for large vaults.

### 3.2 Plain Markdown with VS Code

**Workflow**: Most complete GitHub Flow support through VS Code's built-in source control plus the GitHub Pull Requests extension for creating, reviewing, and merging PRs directly in the editor. GitLens enhances blame and history. Foam adds wiki-links and backlinks on top of this git-native foundation.

**This approach treats git as the true source of truth with zero abstraction layer.**

**Strengths**: Full GitHub Flow in-editor. No sync abstraction. Maximum portability.

**Limitations**: Requires VS Code familiarity. Graph visualization less polished than Obsidian.

### 3.3 GitBook

**Workflow**: Truly bidirectional sync—edit in GitBook and changes commit to GitHub, or commit in GitHub and changes appear in GitBook. Initial sync direction is configurable. GitBook has its own change request system that integrates with Git PRs, providing a documentation-native workflow on top of git.

**Branch protection and merge rules work as expected.**

**Strengths**: Professional collaboration UI. Non-technical users can contribute. Published documentation site included.

**Limitations**: Web editor may not preserve custom frontmatter. Proprietary layer between user and git.

### 3.4 Mintlify

**Workflow**: Uses a GitHub App for automatic sync: push changes to GitHub and Mintlify deploys; edit in Mintlify's web editor and it commits to your repository. Your Git repository remains the source of truth.

**Feature branches and branch protection are fully supported. Preview deployments require the Pro plan.**

**Strengths**: Git remains source of truth. Preview deployments (Pro tier).

**Limitations**: Pro tier required for full features. $300/month exceeds budget.

---

## Part 4: LLM Retrieval Assessment

### 4.1 MCP Server Ecosystem

**Obsidian MCP ecosystem has matured significantly** with multiple production-ready servers:

- **cyanheads/obsidian-mcp-server**: Requires the Local REST API plugin. Offers full CRUD operations on notes, search (text and regex), frontmatter management, and directory listing. Most comprehensive option.

- **obsidian-mcp-tools** by jacksteamdev: Runs as a native Obsidian plugin with semantic search and Templater integration—no external REST API needed.

- **obsidian-semantic-mcp**: Consolidates 20+ tools into 5 AI-optimized semantic operations for cleaner agent interactions.

**Notion has the most mature MCP implementation** with an official hosted server from Notion themselves (`@notionhq/notion-mcp-server`). It provides OAuth flow, returns Notion-flavored Markdown for token efficiency, and supports full read/write operations including database queries. The hosted option means zero local setup.

**GitBook and Mintlify provide native, automatic MCP servers** on every published site. GitBook's server lives at `{docs-url}/~gitbook/mcp`; Mintlify's at `{docs-url}/mcp`. Both auto-generate llms.txt and llms-full.txt files. Mintlify's MCP server can execute API calls when you provide an OpenAPI spec—a unique capability for API documentation.

**Outline has multiple community MCP servers** including RAG-based implementations with semantic search and document summarization. The **Vortiago/mcp-outline** server supports full CRUD, collections, comments, and rate limiting.

**For plain markdown files**, the official MCP reference implementation includes a filesystem server with configurable access controls. **library-mcp** by Will Larson specifically handles markdown knowledge bases with YAML frontmatter, offering tag-based and date-range retrieval—well-suited for Compass's artifact structure.

### 4.2 llms.txt Support

**Native auto-generation**: GitBook, Mintlify, Fern

**Build-time generation**: Docusaurus (via plugin)

**Manual creation required**: Obsidian, VS Code/Foam, Outline, Notion

For Obsidian and VS Code workflows, llms.txt can be generated via a simple build script that enumerates markdown files with frontmatter. DD-12-01 already defines the llms.txt structure for Compass.

### 4.3 API Quality Assessment

| Platform | API Type | Quality | Notes |
|----------|----------|---------|-------|
| Obsidian | REST (plugin) | Good | Via Local REST API plugin; full vault access |
| GitBook | REST | Excellent | Well-documented, comprehensive endpoints |
| Mintlify | REST | Good | Primarily for docs management |
| Notion | REST | Excellent | Official, comprehensive, well-maintained |
| Outline | REST | Good | Full CRUD, collections, comments |

---

## Part 5: Pricing Analysis

### 5.1 Detailed Cost Comparison (January 2026)

| Platform | Phase 1 (<$50/mo) | Phase 3 (<$150/mo) | Notes |
|----------|-------------------|-------------------|-------|
| **Obsidian + Git** | ✅ $0 | ✅ $0 | Core app FREE; Sync optional at $4-5/mo per user |
| **VS Code + Foam + GitHub** | ✅ $0-12 | ✅ $0-12 | GitHub Team $4/user for protected branches |
| **Docusaurus** | ✅ $0 | ✅ $0 | Open source; hosting via GitHub Pages free |
| **GitBook** | ✅ ~$30 | ✅ ~$95-125 | Free site + Plus users $10/user; Premium site $65 |
| **Mintlify** | ❌ $0 (1 user only) | ❌ $300 | Hobby free but single-member; Pro way over budget |
| **Outline Cloud** | ✅ $10 | ✅ $10-79 | Starter 1-10 users flat $10; Team 11-100 at $79 |
| **Outline Self-hosted** | ✅ ~$5-10 | ✅ ~$10-20 | BSL license free; VPS + setup time |
| **Notion** | ✅ $20-30 | ✅ $40-60 | Plus $10/user; Business $20/user for AI |

### 5.2 Budget Fit Analysis

**Mintlify's pricing creates a cliff**: Hobby tier works for solo use but limits to 1 member. Pro jumps to $300/month—double the Phase 3 budget. This eliminates Mintlify despite its excellent AI-native features.

**GitBook fits both budget phases** with careful tier selection. Free site + 3 Plus users costs ~$30/month. Premium site ($65) + Pro users reaches ~$95-125/month for Phase 3.

**Obsidian and VS Code/Foam are essentially free** for the core documentation workflow. Optional Obsidian Sync adds $4-5/month per user but is not required if using Git for synchronization.

---

## Part 6: Recommendation

### 6.1 Primary Choice: Obsidian with Git

Obsidian with the Obsidian Git plugin best satisfies Compass's requirements as defined in DD-12-01 and DD-13-01:

| Requirement | How Obsidian Meets It |
|-------------|----------------------|
| YAML frontmatter (10+ fields) | Perfect preservation with Properties View UI |
| Git integration | Good support via plugin; feature branches work |
| Backlinks | Native wiki-link syntax with backlinks panel |
| Graph visualization | Built-in interactive graph view |
| MCP servers | Multiple mature implementations available |
| llms.txt | Manual creation via build script |
| Cost | $0 for core workflow |
| Portability | Plain markdown files, zero vendor lock-in |

### 6.2 Trade-offs to Accept

- No real-time collaborative editing (async via Git only)
- PR workflow requires leaving Obsidian for GitHub web interface
- Mobile sync has performance limitations on large vaults (1000+ files)
- Team collaboration requires coordination discipline around sync timing

### 6.3 Alternative: GitBook

Choose GitBook when:
- Native llms.txt generation is important
- Team includes non-technical contributors who need polished UI
- Published documentation site is required
- Wiki-style backlinks are not essential

Budget: ~$30/month Phase 1, ~$95-125/month Phase 3

**Critical requirement**: Ensure Git Sync is enabled and establish Git as primary editing path to preserve custom frontmatter fields.

### 6.4 Alternative: VS Code with Foam

Choose VS Code + Foam when:
- Team is already embedded in VS Code workflows
- Most direct Git integration is desired
- Real-time collaboration via Live Share is valuable

Foam provides wiki-links, backlinks, and graph visualization on top of VS Code's native Git support. This is the most git-native approach with zero abstraction layer.

---

## Part 7: Implementation Path

### 7.1 Phase 1 Setup (Obsidian + Git)

1. Create GitHub repository for Compass documentation following DD-12-01 structure
2. Install Obsidian (free) on all team machines
3. Clone repository; open as Obsidian vault
4. Install Obsidian Git plugin, configure with repository credentials
5. Install Local REST API plugin for MCP access
6. Configure cyanheads/obsidian-mcp-server for LLM agent integration
7. Create document templates matching DD-13-01 artifact types
8. Define Git workflow conventions (commit frequency, branch naming per DD-12-01 Part 5)
9. Generate initial llms.txt following DD-12-01 Section 2.3 format

### 7.2 Collaboration Workflow

- Each team member has local vault synced via Git
- Feature branches (`docs/{type}/{topic}`) for major documentation changes
- Direct commits to main for quick updates and corrections
- Pull requests via GitHub web interface when review is needed
- Conflict resolution through standard Git merge in editor

### 7.3 LLM Integration

- MCP server exposes vault contents to Claude, Cursor, or custom Compass agents
- Frontmatter searchable and filterable via MCP tools
- llms.txt maintained via build script; regenerate when adding major sections

---

## Sources

1. **[T1/S3]** GitHub. "Vinzent03/obsidian-git". Retrieved 2026-01-26. https://github.com/Vinzent03/obsidian-git

2. **[T1/S2]** Luegm. "Leveraging Obsidian with GitHub for Collaborative Documentation". Retrieved 2026-01-26. https://luegm.dev/posts/obsidiangit/

3. **[T1/S4]** Cogit8. "Obsidian and Git: A Quick Setup Guide for Developers". Retrieved 2026-01-26. https://rob.cogit8.org/posts/2025-03-25-obsidian-git-quick-setup-for-developers/

4. **[T1/S1]** Foam. "What is Foam?". Retrieved 2026-01-26. https://foambubble.github.io/foam/

5. **[T1/S2]** GitHub. "cyanheads/obsidian-mcp-server". Retrieved 2026-01-26. https://github.com/cyanheads/obsidian-mcp-server

6. **[T1/S3]** LobeHub. "Obsidian MCP Server". Retrieved 2026-01-26. https://lobehub.com/mcp/cyanheads-obsidian-mcp-server

7. **[T1/S2]** GitHub. "jacksteamdev/obsidian-mcp-tools". Retrieved 2026-01-26. https://github.com/jacksteamdev/obsidian-mcp-tools

8. **[T1/S3]** GitHub. "aaronsb/obsidian-semantic-mcp". Retrieved 2026-01-26. https://github.com/aaronsb/obsidian-semantic-mcp

9. **[T1/S1]** Notion. "Notion MCP – Connect Notion to your favorite AI tools". Retrieved 2026-01-26. https://developers.notion.com/docs/mcp

10. **[T1/S2]** GitBook. "MCP servers for published docs". Retrieved 2026-01-26. https://gitbook.com/docs/publishing-documentation/mcp-servers-for-published-docs

11. **[T1/S2]** Glama. "Outline Wiki MCP Server by huiseo". Retrieved 2026-01-26. https://glama.ai/mcp/servers/@huiseo/outline-wiki-mcp

12. **[T1/S2]** Playbooks. "Markdown Library MCP server for AI agents". Retrieved 2026-01-26. https://playbooks.com/mcp/lethain-markdown-library

13. **[T1/S1]** Mintlify. "Pricing". Retrieved 2026-01-26. https://www.mintlify.com/pricing

14. **[T1/S1]** Obsidian. "Pricing". Retrieved 2026-01-26. https://obsidian.md/pricing

15. **[T1/S2]** OpenAI. "Model Context Protocol". Retrieved 2026-01-26. https://developers.openai.com/codex/mcp/

---

*End of Documentation Platform Research Findings (RF-04-01)*
