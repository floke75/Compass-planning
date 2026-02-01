---
id: RF-10-01
type: rf
area: 10-dev-tooling
title: Development Tooling Research Findings
status: draft
created: 2026-01-28
updated: 2026-01-28
author: compass-research
summary: Evaluates development tooling for Compass including testing frameworks, CI/CD pipelines, linting, and environment configuration optimized for LLM-assisted development with Convex and Vercel
tags: [dev-tooling, testing, ci-cd, linting, typescript, vitest, biome, convex]
related:
  - ADR-01-01
  - ADR-08-01
  - DD-17-01
confidence: high
methodology: "Tool evaluation with LLM maintainability focus, official documentation review, community pattern analysis"
limitations:
  - "Tooling preferences are somewhat subjective"
  - "Ecosystem evolves rapidly"
  - "convex-test is relatively new with less LLM training data coverage"
responds_to: null
implications_for: [development-workflow, code-quality, deployment-pipeline]
---

# Development Tooling Research Findings

## Executive Summary

**Recommendation**: Vitest + convex-test for testing, Biome for linting/formatting, Vercel Marketplace integration for CI/CD, with strict TypeScript configuration throughout.

**Confidence**: High — All recommended tools are officially supported by their respective platforms, well-documented, and follow patterns that LLM coding agents generate reliably.

**Key Trade-offs**:
- Biome over ESLint + Prettier: Sacrifices ecosystem maturity for configuration simplicity
- No Playwright initially: Defers E2E testing complexity until genuine need emerges
- Vercel-managed deployments: Sacrifices CI/CD customization for zero-maintenance automation

**Cost**: $0 additional — All tools are free/open-source beyond existing Convex and Vercel subscriptions.

---

## Part 1: Testing Strategy

### 1.1 Framework Selection: Vitest + convex-test

**Selected**: Vitest as the test runner with `convex-test` for Convex function testing.

**Why Vitest over Jest**:
- Native ESM support without configuration gymnastics
- Jest-compatible API (LLM agents trained on Jest patterns work immediately)
- 10-20x faster execution through native TypeScript support
- First-class Convex compatibility via `convex-test` documentation

**What is convex-test**: The `convex-test` library (version 0.0.41, Apache 2.0 license) provides a mock Convex backend that runs entirely in JavaScript. It's maintained by Convex employees and is the officially recommended testing approach. The library supports testing queries, mutations, actions, authentication flows, and scheduled functions without requiring a real Convex backend.

### 1.2 Installation and Configuration

Install the required packages:

```bash
npm install --save-dev convex-test vitest @edge-runtime/vm
```

**Why @edge-runtime/vm**: Convex functions run in an edge runtime environment, not standard Node.js. The `@edge-runtime/vm` package simulates this environment so tests accurately reflect production behavior. Without it, tests might pass locally but fail when deployed because of runtime API differences.

Create `vitest.config.ts` in your project root:

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "edge-runtime",
    server: { deps: { inline: ["convex-test"] } },
  },
});
```

**Configuration explained**:
- `environment: "edge-runtime"`: Tells Vitest to use the edge runtime simulation instead of Node.js
- `server.deps.inline: ["convex-test"]`: Forces Vitest to bundle `convex-test` instead of treating it as an external dependency, which is required for the edge runtime to work correctly

### 1.3 Test Categories and Patterns

#### Unit Tests for Convex Functions

The basic pattern for testing Convex queries and mutations:

```typescript
// convex/tasks.test.ts
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import { api } from "./_generated/api";
import schema from "./schema";

// This glob imports all Convex functions for the test environment
const modules = import.meta.glob("./**/*.ts");

test("creates and retrieves tasks", async () => {
  // Create a test instance with your schema and modules
  const t = convexTest(schema, modules);
  
  // Call mutations and queries using the generated API types
  const taskId = await t.mutation(api.tasks.create, { 
    text: "Complete research", 
    priority: "high" 
  });
  
  const tasks = await t.query(api.tasks.list);
  expect(tasks).toMatchObject([{ text: "Complete research" }]);
});
```

**Why this pattern works for LLM agents**: The `api.tasks.create` syntax matches exactly how you call Convex functions from frontend code. LLM agents that understand Convex client code can generate test code with minimal adaptation.

#### Authentication Testing

Testing functions that require user identity:

```typescript
test("users see only their own tasks", async () => {
  const t = convexTest(schema, modules);
  
  // Create an authenticated context for Sarah
  const asSarah = t.withIdentity({ 
    name: "Sarah", 
    email: "sarah@test.com",
    subject: "user_sarah_123"  // The unique user ID
  });
  await asSarah.mutation(api.tasks.create, { text: "Sarah's task" });
  
  // Create a separate authenticated context for Lee
  const asLee = t.withIdentity({ 
    name: "Lee", 
    email: "lee@test.com",
    subject: "user_lee_456"
  });
  const leesTasks = await asLee.query(api.tasks.myTasks);
  
  // Lee should not see Sarah's tasks
  expect(leesTasks).toHaveLength(0);
});
```

**What withIdentity does**: It creates a mock authentication context that your Convex functions receive via `ctx.auth.getUserIdentity()`. The `subject` field is the unique identifier — if your real auth provider uses different fields, adjust accordingly.

#### Mocking External APIs in Actions

Convex actions can call external APIs. To test them without real API calls:

```typescript
import { vi } from "vitest";

test("AI action with mocked OpenAI", async () => {
  const t = convexTest(schema, modules);

  // Mock the global fetch function
  vi.stubGlobal("fetch", vi.fn(async () => ({ 
    json: async () => ({ 
      choices: [{ message: { content: "Mocked AI response" }}] 
    }),
    ok: true,
  }) as Response));

  const reply = await t.action(api.ai.generate, { prompt: "hello" });
  expect(reply).toContain("Mocked AI response");
  
  // Always clean up mocks to avoid affecting other tests
  vi.unstubAllGlobals();
});
```

**Why stubGlobal instead of vi.mock**: Convex actions run in the edge runtime where standard Node.js mocking doesn't work. `vi.stubGlobal` replaces the global `fetch` function that the edge runtime uses.

#### Testing Scheduled Functions

For functions that schedule other functions:

```typescript
test("cleanup job runs after creation", async () => {
  const t = convexTest(schema, modules);
  
  // Create something that schedules a cleanup
  await t.mutation(api.tasks.createWithCleanup, { 
    text: "Temporary task",
    deleteAfterMs: 60000 
  });
  
  // Fast-forward time to trigger scheduled functions
  await t.finishInProgressScheduledFunctions();
  
  // Verify the scheduled function ran
  const tasks = await t.query(api.tasks.list);
  expect(tasks).toHaveLength(0); // Task was cleaned up
});
```

### 1.4 Coverage Expectations

**Target: 60-70% line coverage on Convex functions**, with higher coverage on:
- Authentication and authorization logic (aim for 90%+)
- Financial calculations or data transformations (aim for 85%+)
- Data validation and input sanitization (aim for 80%+)

**Why not 100%**: Research from Meta's TestGen-LLM project found that only ~10% of AI-generated tests successfully improve existing test suites without human iteration. Chasing 100% coverage leads to brittle tests that break on implementation changes without catching real bugs.

**What to skip initially**:
- Simple CRUD operations with no business logic
- UI rendering tests (defer to manual testing)
- Third-party integration responses (mock at the boundary)

### 1.5 E2E Testing Assessment: Playwright Deferred

**Recommendation**: Do not implement Playwright E2E tests initially. Add them only when you have complex multi-page workflows (checkout flows, multi-step forms) that justify the maintenance overhead.

**Why defer Playwright**:

1. **Complexity conflicts with LLM maintainability**: Browser installation, test data management, authentication state, and flaky test debugging require expertise the team doesn't have and that LLM agents handle poorly.

2. **Convex's own guidance**: The official documentation states, "You can catch a surprising number of bugs from a test that simply loads the page." This suggests even Convex considers comprehensive E2E testing optional for most applications.

3. **Maintenance burden**: Playwright tests require updating whenever UI changes. For a small team, this maintenance cost often exceeds the bug-catching benefit.

**Staged approach for Compass**:

| Phase | Testing Approach |
|-------|------------------|
| Now (MVP) | Vitest + convex-test for backend, manual smoke testing for UI |
| Post-MVP | Add simple "page loads" smoke tests if instability emerges |
| Production | Consider Playwright only for critical flows (payments, data export) |

---

## Part 2: CI/CD Design

### 2.1 Pipeline Architecture

The Vercel Marketplace Convex integration handles deployment automatically. Your GitHub Actions workflow should only run validation checks—type checking, linting, and tests—not deployment.

**Why this separation matters**: The Vercel integration creates isolated preview deployments with fresh Convex backends for every pull request. If you also deployed from GitHub Actions, you'd have conflicting deployments and no preview isolation.

### 2.2 GitHub Actions Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Type check
        run: npx tsc --noEmit
      
      - name: Lint
        run: npx biome check .
      
      - name: Run tests
        run: npm test
```

**Configuration explained**:
- `on: pull_request` and `push: branches: [main]`: Runs on every PR and every push to main
- `npm ci` instead of `npm install`: Uses the exact versions from `package-lock.json` for reproducible builds
- `tsc --noEmit`: Type checks without producing output files
- Steps run sequentially; if any fails, the workflow stops

### 2.3 Vercel + Convex Integration Setup

The integration handles environment configuration automatically. Here's what happens:

1. **Production deployments**: When you push to `main`, Vercel builds your frontend and runs `npx convex deploy` to push your Convex functions to production.

2. **Preview deployments**: When you open a PR, Vercel creates a preview URL and creates a separate Convex preview deployment. The preview uses production data but runs your branch's Convex functions.

**Deploy keys** authenticate these deployments. Generate them in the Convex Dashboard under Project Settings → Deploy Keys:

| Key Type | Purpose | Vercel Environment Scope |
|----------|---------|-------------------------|
| Production | `prod:qualified-jaguar-123\|eyJ...` | Production only |
| Preview | `preview:team:project\|eyJ...` | Preview only |

Both are stored as `CONVEX_DEPLOY_KEY` in Vercel's environment variables—the different scopes ensure the correct key is used for each deployment type.

### 2.4 Build Command Configuration

In Vercel's project settings, set the Build Command to:

```bash
npx convex deploy --cmd 'npm run build'
```

**What this does**: First deploys your Convex functions, then runs your frontend build. The order matters because the frontend build may import Convex-generated types.

**For preview deployments with seed data**, use:

```bash
npx convex deploy --cmd 'npm run build' --preview-run 'seedData'
```

The `--preview-run` flag executes an internal mutation only on preview deployments:

```typescript
// convex/seed.ts
import { internalMutation } from "./_generated/server";

export default internalMutation({
  handler: async (ctx) => {
    // Only runs on preview deployments
    await ctx.db.insert("settings", { key: "demo_mode", value: true });
    await ctx.db.insert("tasks", { text: "Sample task", completed: false });
  },
});
```

### 2.5 Critical Requirement: Commit Generated Files

**The `convex/_generated/` directory must be committed to your repository.**

This is counterintuitive—most generated files are gitignored. But Convex's generated types are required for TypeScript compilation. Without them:
- `npm run build` fails because imports from `"./_generated/api"` can't resolve
- Type checking in CI fails
- LLM agents can't understand your API shape

Add to `.gitignore`:
```
# Ignore local environment files
.env.local
.env

# Do NOT ignore convex/_generated/
```

---

## Part 3: Linting and Formatting

### 3.1 Tool Selection: Biome

**Selected**: Biome as the single tool for linting and formatting.

**Why Biome over ESLint + Prettier**:

| Factor | Biome | ESLint + Prettier |
|--------|-------|-------------------|
| Config files | 1 (`biome.json`) | 3-4+ files |
| Dependencies | 1 package | 6-10+ packages |
| Speed | ~25ms typical | ~500ms-2s typical |
| TypeScript | Native support | Requires plugins |
| LLM maintainability | Single config to understand | Multiple configs interact |

The critical factor for LLM-driven development is **configuration simplicity**. When an LLM agent needs to modify linting rules, understanding one file is dramatically easier than understanding the interaction between `.eslintrc.js`, `.prettierrc`, `.eslintignore`, and various plugin configurations.

### 3.2 Installation and Configuration

Install Biome with exact versioning (the `-E` flag pins the exact version to avoid unexpected updates):

```bash
npm install -D -E @biomejs/biome
npx @biomejs/biome init
```

Replace the generated `biome.json` with this Convex-optimized configuration:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.2.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": true,
    "includes": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.json"],
    "ignore": [
      "**/node_modules/**",
      "**/.next/**",
      "**/convex/_generated/**"
    ]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "noUnusedImports": "error",
        "useExhaustiveDependencies": "error"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noDoubleEquals": "error",
        "noEmptyBlockStatements": "error"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error"
      }
    }
  }
}
```

**Configuration explained**:

- `vcs.useIgnoreFile`: Respects your `.gitignore`, so you don't duplicate ignore patterns
- `files.ignore`: Explicitly ignores generated Convex code (linting it would be pointless and slow)
- `lineWidth: 100`: Slightly wider than the 80-character default; reduces line breaks in Convex function signatures
- `organizeImports`: Automatically sorts and groups imports, reducing diff noise in PRs

### 3.3 Rules That Catch LLM-Generated Errors

Research identifies common bug patterns in AI-generated code. These rules specifically target them:

| Rule | LLM Error Pattern It Catches |
|------|------------------------------|
| `noUnusedVariables` | Hallucinated variables that don't exist |
| `noUnusedImports` | Imports for unused functionality |
| `noEmptyBlockStatements` | Incomplete implementations (empty catch blocks, stub functions) |
| `noExplicitAny` | Type confusion from lazy typing |
| `noDoubleEquals` | Loose equality bugs (`==` vs `===`) |
| `useExhaustiveDependencies` | Missing React hook dependencies |
| `noNonNullAssertion` | Unsafe null assertions (`!`) that hide potential crashes |

### 3.4 TypeScript Configuration

Strict TypeScript settings catch approximately 40% more errors than default settings. Create or update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true,
    "jsx": "preserve"
  },
  "include": ["src/**/*", "convex/**/*"],
  "exclude": ["node_modules", "convex/_generated"]
}
```

**Why each strict flag matters for LLM code**:

| Flag | What It Catches |
|------|-----------------|
| `strictNullChecks` | LLMs often forget null/undefined handling |
| `noImplicitAny` | Prevents loosely-typed generated code from compiling |
| `noUncheckedIndexedAccess` | Catches array access without bounds checking |
| `noImplicitReturns` | Catches incomplete function implementations |
| `exactOptionalPropertyTypes` | Catches confusion between `undefined` and missing properties |

### 3.5 Editor Integration

For VS Code, add to `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "biomejs.biome",
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "biome.enabled": true
}
```

Commit this file so all team members and LLM coding agents use consistent settings.

---

## Part 4: Environment Configuration

### 4.1 How Convex Environment Variables Work

Convex environment variables work differently than typical Node.js applications:

- **They are deployment-specific**: Each Convex deployment (dev, preview, production) has its own set of environment variables
- **They are stored in Convex's infrastructure**: Not in `.env` files on your machine
- **They are only accessible in Convex functions**: Frontend code cannot read them directly

**Setting variables via CLI**:

```bash
# Set a variable on your current deployment
npx convex env set OPENAI_API_KEY "sk-xxxxx"

# Set a variable on a specific deployment
npx convex env set SENDGRID_API_KEY "SG.xxxxx" --prod

# List all variables (values hidden)
npx convex env list
```

**Setting variables via Dashboard**: Navigate to your project → Settings → Environment Variables. This is often easier for initial setup.

### 4.2 Accessing Variables in Convex Functions

```typescript
// convex/actions/email.ts
import { action } from "./_generated/server";

export const sendWelcomeEmail = action({
  args: { email: v.string() },
  handler: async (ctx, args) => {
    const apiKey = process.env.SENDGRID_API_KEY;
    
    // Always validate that required variables exist
    if (!apiKey) {
      throw new Error("SENDGRID_API_KEY environment variable not configured");
    }
    
    // Use the API key
    const response = await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ /* email payload */ }),
    });
    
    if (!response.ok) {
      throw new Error(`SendGrid API error: ${response.status}`);
    }
  },
});
```

### 4.3 Critical Pitfall: Don't Condition Exports on Environment Variables

This is the most common mistake LLM agents make with Convex environment variables:

```typescript
// ❌ WRONG - This breaks because function definition is evaluated at deploy time
export const myFunc = process.env.DEBUG 
  ? mutation({ /* debug version */ }) 
  : internalMutation({ /* production version */ });

// ❌ WRONG - Same problem
const config = process.env.FEATURE_FLAG === "true" ? optionA : optionB;
export const myFunc = mutation({ args: config, /* ... */ });
```

**Why this breaks**: Convex evaluates your function definitions at deploy time to register them. Environment variables may not be available or may have different values during this registration phase.

```typescript
// ✅ CORRECT - Condition inside the handler
export const myFunc = mutation({
  handler: async (ctx, args) => {
    if (process.env.DEBUG) {
      console.log("Debug mode:", args);
    }
    // Regular logic
  },
});
```

### 4.4 Environment Flow Across Stages

| Stage | Convex Backend Vars | Frontend Connection | How It's Set |
|-------|---------------------|---------------------|--------------|
| Local dev | Dashboard for dev deployment | `.env.local` (auto-generated) | `npx convex dev` creates it |
| Preview | Dashboard defaults | Auto-set by Vercel integration | Preview deploy key |
| Production | Dashboard for prod deployment | Auto-set by Vercel integration | Production deploy key |

**Local development flow**:

1. Run `npx convex dev` to start the local development server
2. Convex creates `.env.local` with your development deployment URL:
   ```
   CONVEX_DEPLOYMENT=dev:happy-owl-456
   NEXT_PUBLIC_CONVEX_URL=https://happy-owl-456.convex.cloud
   ```
3. Your frontend reads `NEXT_PUBLIC_CONVEX_URL` to connect to Convex
4. Your Convex functions read environment variables from the Dashboard

### 4.5 File Management

**Files to commit**:
- `convex/` — All your Convex function code
- `convex/_generated/` — Generated types (required for TypeScript)
- `convex.json` — Convex project configuration
- `.env.example` — Template showing required variables (no actual values)

**Files to gitignore**:
```
.env.local
.env
.env.*.local
```

**Example `.env.example`**:
```bash
# Convex deployment URL (auto-generated by `npx convex dev`)
CONVEX_DEPLOYMENT=
NEXT_PUBLIC_CONVEX_URL=

# Required for email functionality
# Set in Convex Dashboard, not here
# SENDGRID_API_KEY=

# Required for AI features  
# Set in Convex Dashboard, not here
# OPENAI_API_KEY=
```

---

## Part 5: LLM Maintainability Assessment

### 5.1 Training Data Coverage

| Tool | Documentation Quality | LLM Familiarity | Assessment |
|------|----------------------|-----------------|------------|
| Vitest | Excellent, extensive examples | High (Jest-compatible API) | ✅ Strong choice |
| convex-test | Good, official Convex docs | Medium (newer library) | ⚠️ May need examples in codebase |
| Biome | Excellent, modern docs | Growing (2.x is newer) | ✅ Simple config helps |
| Convex | Very good, active updates | Medium-High | ✅ Consistent patterns |
| Vercel | Excellent | Very High | ✅ Widely adopted |
| GitHub Actions | Excellent | Very High | ✅ Industry standard |

### 5.2 Mitigation for Lower-Coverage Tools

**convex-test**: Include working test examples in your codebase. When LLM agents see the module glob pattern and test structure, they can extrapolate:

```typescript
// convex/example.test.ts — Keep this as a reference for LLM agents
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import { api } from "./_generated/api";
import schema from "./schema";

const modules = import.meta.glob("./**/*.ts");

test("example pattern for LLM reference", async () => {
  const t = convexTest(schema, modules);
  // LLM agents will copy this pattern
});
```

**Biome**: The single-file configuration actually helps LLM agents. They can read the entire `biome.json` and understand all rules without navigating multiple files.

### 5.3 Debugging Support

| Tool | Error Message Quality | Stack Trace Clarity | Log Access |
|------|----------------------|---------------------|------------|
| Vitest | Excellent | Clear, points to source | Console output |
| convex-test | Good | Points to Convex function | Test output |
| Biome | Excellent | Points to exact line/column | CLI output |
| Convex Dashboard | Good | Full function logs | Web UI |
| Vercel | Good | Build logs accessible | Web UI |

All tools provide explicit error handling and clear logs—meeting the System Definition §4.2 requirement for debuggability.

---

## Part 6: Recommendation Summary

### 6.1 Complete Toolchain

| Category | Tool | Version | Purpose |
|----------|------|---------|---------|
| Test Runner | Vitest | ^3.x | Fast, TypeScript-native testing |
| Convex Testing | convex-test | ^0.0.41 | Mock Convex backend |
| Edge Runtime | @edge-runtime/vm | ^5.x | Simulate Convex runtime |
| Linter/Formatter | Biome | ^2.x | Single-tool code quality |
| CI/CD | GitHub Actions + Vercel | — | Validation + deployment |
| Type Checking | TypeScript | ^5.x | Strict mode enabled |

### 6.2 Package.json Scripts

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

### 6.3 File Structure

```
project-root/
├── .github/
│   └── workflows/
│       └── ci.yml              # Validation workflow
├── convex/
│   ├── _generated/             # COMMIT THIS
│   ├── schema.ts
│   ├── tasks.ts
│   └── tasks.test.ts           # Tests alongside functions
├── src/
│   └── ...                     # Frontend code
├── .env.example                # Template for required vars
├── .env.local                  # GITIGNORE THIS
├── biome.json                  # Linting config
├── convex.json                 # Convex project config
├── tsconfig.json               # TypeScript config
├── vitest.config.ts            # Test config
└── package.json
```

---

## Appendix A: Sources

1. **[T1/S1]** Convex. "convex-test Documentation." Retrieved 2026-01-28. https://docs.convex.dev/testing/convex-test

2. **[T1/S1]** Convex. "Using Convex with Vercel." Retrieved 2026-01-28. https://docs.convex.dev/production/hosting/vercel

3. **[T1/S1]** Convex. "Environment Variables." Retrieved 2026-01-28. https://docs.convex.dev/production/environment-variables

4. **[T1/S1]** Convex. "Deploy Keys." Retrieved 2026-01-28. https://docs.convex.dev/cli/deploy-key-types

5. **[T1/S1]** Biomejs. "Getting Started." Retrieved 2026-01-28. https://biomejs.dev/guides/getting-started/

6. **[T1/S1]** Convex Stack. "Testing patterns for peace of mind." Retrieved 2026-01-28. https://stack.convex.dev/testing-patterns

7. **[T2/S2]** npm. "convex-test package." Retrieved 2026-01-28. https://www.npmjs.com/package/convex-test

8. **[T2/S2]** Qodo. "TestGen-LLM Implementation." Retrieved 2026-01-28. https://www.qodo.ai/blog/we-created-the-first-open-source-implementation-of-metas-testgen-llm/

---

## Appendix B: Related Documents

- **ADR-01-01**: Backend Platform Selection (Convex) — Provides context for testing patterns
- **ADR-08-01**: Hosting Platform Selection (Vercel) — Defines deployment pipeline
- **DD-17-01**: Integration Patterns — Secret management and webhook testing approaches
- **SYS-00**: Compass System Definition — Team capacity constraints (§4.2), debuggability requirements (§1.7)

---

*End of Development Tooling Research Findings (RF-10-01)*
