---
id: ADR-04-01
type: adr
area: 04-documentation
title: Documentation Platform Selection
status: proposed
created: 2026-01-26
updated: 2026-01-26
author: compass-research
summary: Selects Obsidian with Git as the documentation platform for Compass based on frontmatter preservation, backlinks, MCP support, and zero cost
tags: [documentation, platform, decision, obsidian, git]
related:
  - RF-04-01
  - DD-12-01
  - DD-13-01
decision_date: null
deciders: []
supersedes: null
---

# Documentation Platform Selection

## Status

Proposed

## Context

Compass is an LLM-orchestrated planning, research, and documentation system. Documentation is the primary output of Compass—the system produces specifications, research documents, decision records, and handoff bundles that implementation platforms consume. The documentation platform choice directly affects how effectively LLM agents can retrieve and work with artifacts, how the team collaborates on documentation, and whether the documentation remains portable over time.

The platform must support specific requirements defined in DD-12-01 (Repository Structure) and DD-13-01 (Artifact Taxonomy): YAML frontmatter with 10+ required fields per artifact, wiki-style linking between artifacts using canonical IDs, Git-based version control following GitHub Flow, and programmatic access for LLM retrieval via MCP or REST API.

Budget constraints are $50/month for Phase 1 and $150/month for Phase 3.

## Options Considered

### Option 1: Obsidian with Git

Local-first markdown editor with native wiki-links, backlinks, and graph visualization. Git integration via the Obsidian Git community plugin. LLM access via multiple mature MCP servers including cyanheads/obsidian-mcp-server.

**Pros:**
- Perfect YAML frontmatter preservation with Properties View UI
- Native wiki-link syntax (`[[artifact-id]]`) and backlinks panel
- Built-in interactive graph visualization for relationship exploration
- Multiple mature MCP servers with full CRUD, search, and frontmatter operations
- Zero cost for core workflow
- Plain markdown files with zero vendor lock-in
- Large plugin ecosystem for extensibility

**Cons:**
- No real-time collaborative editing (async via Git only)
- PR creation requires GitHub web interface
- Mobile sync has performance issues on large vaults (1000+ files)
- Requires coordination discipline around sync timing

### Option 2: GitBook

Documentation platform with bidirectional Git sync. Native MCP server and llms.txt generation on published sites. Professional collaboration UI suitable for non-technical contributors.

**Pros:**
- Truly bidirectional Git sync (edit in GitBook or GitHub)
- Native MCP server auto-generated at `{docs-url}/~gitbook/mcp`
- Auto-generates llms.txt and llms-full.txt
- Professional published documentation site included
- Good real-time collaboration features
- Fits both budget phases (~$30-95/month)

**Cons:**
- Web editor may not preserve custom YAML frontmatter fields
- No wiki-style backlinks or graph visualization
- Proprietary layer between user and git
- Medium vendor lock-in risk

### Option 3: VS Code with Foam

VS Code extension providing wiki-links, backlinks, and graph visualization for plain markdown. Maximum Git integration via VS Code's native source control and GitHub Pull Requests extension.

**Pros:**
- Most direct Git integration with full GitHub Flow in-editor
- Foam provides wiki-links, backlinks, and graph visualization
- Real-time collaboration via VS Code Live Share
- Zero cost
- Zero vendor lock-in

**Cons:**
- Requires VS Code familiarity
- Graph visualization less polished than Obsidian
- More developer-oriented experience

### Option 4: Mintlify

Developer documentation platform with excellent AI-native features including auto llms.txt, native MCP server with API execution capability, and MDX support.

**Pros:**
- Excellent MDX/frontmatter support
- Native MCP server can execute API calls from OpenAPI specs
- Auto-generates llms.txt in collaboration with Anthropic
- Professional documentation appearance

**Cons:**
- Hobby tier limits to 1 member
- Pro tier costs $300/month—double Phase 3 budget
- No wiki-links or backlinks
- Pricing eliminates this option

### Option 5: Do Nothing (Plain Markdown in GitHub)

Store markdown files in GitHub repository, edit via GitHub web interface or local editor, collaborate via pull requests.

**Pros:**
- Zero cost
- Maximum portability
- Direct Git workflow

**Cons:**
- No backlinks or graph visualization
- No structured editing experience
- GitHub web editor lacks markdown preview quality
- No MCP integration without custom development

## Decision

We will use **Obsidian with Git** because it uniquely satisfies all core Compass requirements while maintaining zero cost and zero vendor lock-in.

Obsidian is the only option that combines: perfect YAML frontmatter preservation with a structured Properties View, native wiki-links and backlinks matching Compass's cross-reference patterns, built-in graph visualization for understanding artifact relationships, and a mature MCP server ecosystem enabling LLM retrieval. The async-via-Git collaboration model is acceptable for a 2-3 person team with established coordination practices.

## Consequences

### Positive

- All DD-12-01 naming conventions and DD-13-01 frontmatter schemas work without modification
- Native backlinks enable artifact relationship discovery during planning
- Graph visualization supports understanding documentation structure
- MCP servers enable Compass agents to read, search, and modify artifacts
- Zero ongoing cost preserves budget for other infrastructure
- Plain markdown files ensure long-term portability

### Negative

- Team cannot simultaneously edit the same document in real-time
- Creating pull requests requires switching to GitHub web interface
- Mobile editing performance may be limited on large vaults
- Team must establish and follow sync discipline to avoid conflicts

### Neutral

- llms.txt requires manual creation via build script rather than auto-generation
- Published documentation site requires separate setup if needed (GitHub Pages or similar)

## Implementation Notes

### Phase 1 Setup

1. Create GitHub repository following DD-12-01 structure
2. Install Obsidian on team machines; clone repository as vault
3. Install Obsidian Git plugin with repository credentials
4. Install Local REST API plugin for MCP access
5. Configure cyanheads/obsidian-mcp-server
6. Create artifact templates per DD-13-01
7. Establish Git workflow conventions per DD-12-01 Part 5
8. Generate initial llms.txt per DD-12-01 Section 2.3

### Collaboration Protocol

- Sync on start (pull), sync on save (commit + push)
- Feature branches for major changes; direct commits for corrections
- Pull requests via GitHub when review needed
- Resolve conflicts in Obsidian editor using standard Git markers

### Fallback Position

If real-time collaboration becomes essential, migrate to GitBook with Git Sync enabled. Markdown files with frontmatter transfer directly; wiki-links require conversion to standard markdown links.

## Related Documents

- **RF-04-01**: Research findings supporting this decision
- **DD-12-01**: Repository structure conventions the platform must support
- **DD-13-01**: Artifact taxonomy and frontmatter schema the platform must preserve

---

*End of Documentation Platform Selection (ADR-04-01)*
