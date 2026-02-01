---
id: ADR-10-01
type: adr
area: 10-dev-tooling
title: Development Tooling Selection
status: proposed
created: 2026-01-28
updated: 2026-01-28
author: compass-research
summary: Selects Vitest + convex-test for testing, Biome for linting/formatting, GitHub Actions for CI validation, and Vercel-managed deployment as the development tooling stack for Compass
tags: [dev-tooling, decision, testing, linting, ci-cd, vitest, biome]
related:
  - RF-10-01
  - ADR-01-01
  - ADR-08-01
decision_date: null
deciders: []
supersedes: null
---

# Development Tooling Selection

## Status

**Proposed** — Awaiting stakeholder review based on RF-10-01 research findings.

---

## Context

ADR-01-01 selected Convex as the backend platform, and ADR-08-01 selected Vercel as the frontend hosting platform. Development tooling must integrate seamlessly with this stack while prioritizing LLM maintainability—the ability for AI coding agents like Claude Code to generate correct code using these tools.

The Compass System Definition (§4.2) establishes that EFN's builders are a non-traditional development team who rely on LLM coding agents as their primary development method. They do not have SQL familiarity or traditional software engineering backgrounds. This context makes tool selection critical: complex configuration, fragmented documentation, or unfamiliar patterns will degrade AI code generation quality.

The System Definition (§1.7) also emphasizes debuggability—explicit error handling, clear logs, and observable workflows. Development tooling must provide actionable error messages that both humans and AI agents can interpret.

Budget constraints (System Definition §4.1) allocate $600–$2,000/year for external services. All recommended tools are free/open-source, adding no cost beyond existing Convex and Vercel subscriptions.

---

## Decision

We will use the following development tooling stack for Compass:

### Testing

**Vitest + convex-test** as the testing framework.

- **Vitest** (^3.x): Modern test runner with native TypeScript support and Jest-compatible API
- **convex-test** (^0.0.41): Official Convex testing library providing mock backend
- **@edge-runtime/vm** (^5.x): Runtime simulation for accurate Convex function testing

### Linting and Formatting

**Biome** (^2.x) as the single tool for both linting and formatting.

Biome replaces the traditional ESLint + Prettier combination with a single configuration file and dependency.

### CI/CD

**GitHub Actions for validation only**; deployment handled by Vercel Marketplace integration.

GitHub Actions runs type checking, linting, and tests. Vercel handles all deployment logic including preview deployments with isolated Convex backends.

### TypeScript

**TypeScript 5.x with strict mode enabled** for maximum error detection in LLM-generated code.

### Environment Configuration

**Convex Dashboard for secrets**; `.env.local` for frontend connection URLs only.

Convex environment variables are deployment-specific and managed through the Convex Dashboard or CLI, not through local `.env` files.

---

## Options Considered

### Option 1: Vitest + convex-test (Selected)

**Testing**: Vitest with convex-test for Convex function testing.

**Pros:**
- Official Convex testing approach with maintained library
- Jest-compatible API leverages existing LLM training data
- 10-20x faster than Jest due to native ESM support
- Full support for testing queries, mutations, actions, and authentication

**Cons:**
- convex-test is relatively new (v0.0.41) with less community coverage
- Requires @edge-runtime/vm dependency for accurate simulation

### Option 2: Jest + Custom Mocks

**Testing**: Jest with manually built Convex mocking.

**Pros:**
- Jest is extremely well-documented and familiar to LLMs
- Maximum flexibility in test structure

**Cons:**
- Would require building mock infrastructure that convex-test provides
- No official Convex documentation for Jest patterns
- Slower execution due to CommonJS overhead
- Manual mock maintenance burden

### Option 3: Biome (Selected)

**Linting/Formatting**: Biome as single tool.

**Pros:**
- Single configuration file (`biome.json`) vs 3-4+ for ESLint + Prettier
- 10-25x faster execution
- Native TypeScript support without plugins
- Single dependency vs 6-10 packages

**Cons:**
- Younger ecosystem than ESLint
- Some ESLint rules don't have Biome equivalents
- Lower LLM training data coverage (mitigated by simple config)

### Option 4: ESLint + Prettier

**Linting/Formatting**: Traditional ESLint and Prettier combination.

**Pros:**
- Industry standard with maximum documentation
- Highest LLM familiarity
- Largest rule ecosystem

**Cons:**
- Multiple configuration files create maintenance burden
- Plugin interactions can be confusing
- Slower execution
- Configuration complexity degrades LLM code generation

### Option 5: Playwright for E2E Testing (Deferred)

**E2E Testing**: Playwright browser automation.

**Pros:**
- Catches integration bugs that unit tests miss
- Visual testing capabilities
- Cross-browser support

**Cons:**
- High maintenance overhead for small team
- Browser installation and test data management complexity
- Flaky test debugging requires visual context LLMs lack
- Convex documentation suggests this is optional

**Decision**: Defer Playwright until post-MVP when complex multi-page workflows justify the overhead.

### Option 6: GitHub Actions for Deployment

**CI/CD**: Full deployment via GitHub Actions.

**Pros:**
- Complete control over deployment pipeline
- No dependency on Vercel-specific features

**Cons:**
- Would conflict with Vercel Marketplace integration
- Loses automatic preview deployments with isolated Convex backends
- Requires manual environment variable management

**Decision**: Let Vercel handle deployments; GitHub Actions runs validation only.

---

## Consequences

### Positive

**LLM maintainability is maximized** through simple, well-documented tools. Vitest uses Jest-compatible syntax that LLMs generate reliably. Biome's single-file configuration is easier for AI agents to understand and modify than multi-file ESLint setups.

**Zero additional cost** beyond existing subscriptions. All selected tools are free and open-source.

**Debugging is straightforward** with clear error messages from all tools. Vitest provides excellent stack traces, Biome points to exact line/column positions, and Convex Dashboard shows full function logs.

**Operational simplicity** through Vercel-managed deployments. No deployment scripts to maintain, no environment variable synchronization, no preview deployment configuration.

**Testing covers the critical layer**. Convex functions are the core of Compass's functionality; thorough backend testing with convex-test catches the most important bugs.

### Negative

**convex-test has lower LLM training data coverage** than established testing libraries. Mitigation: Include example test files in the codebase that LLM agents can reference.

**Biome's rule ecosystem is smaller** than ESLint's. Some specialized rules may not exist. Mitigation: The rules that exist cover the most common LLM error patterns; specialized rules can be added later.

**No E2E testing initially** means some integration bugs may reach production. Mitigation: Manual smoke testing during development; staged Playwright introduction post-MVP.

**TypeScript strict mode may initially frustrate** by flagging more errors. Mitigation: This is desirable—it catches LLM errors before runtime.

### Neutral

**GitHub Actions runs validation but not deployment.** This is a deliberate separation of concerns, not a limitation.

**convex/_generated/ must be committed** to the repository for TypeScript compilation in CI. This is a Convex requirement regardless of tooling choices.

---

## Implementation Notes

### Initial Setup

Install development dependencies:

```bash
npm install --save-dev vitest convex-test @edge-runtime/vm @biomejs/biome
```

Create configuration files:
- `vitest.config.ts` — Test runner configuration with edge-runtime environment
- `biome.json` — Linting and formatting rules
- `tsconfig.json` — TypeScript strict mode settings
- `.github/workflows/ci.yml` — Validation workflow

Create example test file as LLM reference:
- `convex/example.test.ts` — Shows convex-test patterns for AI agents to follow

### CI/CD Setup

1. Create GitHub Actions workflow at `.github/workflows/ci.yml`
2. Verify Vercel Marketplace Convex integration is enabled
3. Generate deploy keys in Convex Dashboard
4. Add `CONVEX_DEPLOY_KEY` to Vercel environment variables (separate production/preview scopes)
5. Set Vercel build command: `npx convex deploy --cmd 'npm run build'`

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "npm-run-all --parallel dev:frontend dev:backend",
    "dev:frontend": "next dev",
    "dev:backend": "convex dev",
    "build": "next build",
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "validate": "npm run typecheck && npm run lint && npm run test"
  }
}
```

### Test Coverage Targets

| Code Area | Target Coverage | Rationale |
|-----------|-----------------|-----------|
| Authentication logic | 90%+ | Security-critical |
| Data validation | 80%+ | Prevents bad data |
| Business logic | 70%+ | Core functionality |
| Simple CRUD | Skip initially | Low bug density |

### Future Considerations

**Playwright addition** (Phase 2+): When complex multi-step workflows exist, add targeted E2E tests for those flows only.

**Testing for @convex-dev/agent**: When implementing planning sessions, test thread persistence, tool execution, and human-in-the-loop flows.

**Biome rule expansion**: As common error patterns emerge, add specific rules to catch them.

---

## Related Documents

**Research foundation**: RF-10-01 provides the comprehensive research findings that informed this decision, including detailed tool evaluations and configuration examples.

**Backend context**: ADR-01-01 documents the Convex selection that establishes testing patterns and environment variable management.

**Hosting context**: ADR-08-01 documents the Vercel selection that defines the deployment pipeline and preview deployment workflow.

**Integration patterns**: DD-17-01 defines webhook testing approaches and secret management patterns that integrate with this tooling.

**System requirements**: SYS-00 Compass System Definition provides the team capacity constraints (§4.2), debuggability requirements (§1.7), and budget constraints (§4.1) that shaped this decision.

---

*End of Development Tooling Selection (ADR-10-01)*
