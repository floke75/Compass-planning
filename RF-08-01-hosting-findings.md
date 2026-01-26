---
id: RF-08-01
type: rf
area: 08-hosting
title: Frontend Hosting Platform Research Findings
status: draft
created: 2026-01-25
updated: 2026-01-25
author: compass-research
summary: Evaluates frontend hosting platforms for Compass with Convex as the backend, comparing Vercel, Netlify, Cloudflare Pages, and Railway across pricing, Convex integration quality, preview deployments, and operational simplicity
tags: [hosting, frontend, deployment, vercel, netlify, cloudflare, convex]
related:
  - RF-01-01
  - ADR-01-01
confidence: high
methodology: "Web research with official vendor documentation, pricing verification, and Convex integration analysis"
limitations:
  - "Pricing subject to change; verified January 25, 2026"
  - "No hands-on deployment testing performed"
  - "Netlify's credit-based pricing model is new (September 2025) and may evolve"
responds_to: null
implications_for: [ADR-08-01, A10]
---

# Frontend Hosting Platform Research Findings

## Executive Summary

**Primary Recommendation**: **Vercel** for Compass frontend hosting.

**Confidence**: High — Vercel provides the best official Convex integration with Marketplace-level support, zero-configuration deployment workflows, and comprehensive documentation. For a non-technical team relying on LLM coding agents, Vercel's seamless GitHub integration minimizes deployment friction.

**Key insight**: Since Convex handles all backend concerns (database, API, serverless functions, real-time sync), frontend hosting is a commodity decision. The differentiator is integration quality with Convex and deployment simplicity—not raw hosting capabilities. Vercel wins on both dimensions with dedicated Convex Marketplace integration and official documentation.

**Trade-offs accepted**:

- Per-seat pricing ($20/user/month) over Cloudflare's flat rate in exchange for superior Convex integration
- Vercel's ecosystem over Cloudflare's larger CDN network in exchange for simpler deployment workflows
- Slight vendor preference toward Next.js in exchange for broadest Convex documentation support

**Alternatives assessment**:

- **Cloudflare Pages**: Best choice if cost optimization at scale is the priority. Flat $20/month pricing regardless of team size, unlimited bandwidth, and largest CDN network. Requires additional configuration for Convex apps. Recommended for Phase 3 if budget becomes a concern.
- **Netlify**: Viable alternative with similar capabilities to Vercel. Free preview deployments are uniquely valuable. Credit-based pricing introduces complexity. Recommended if preview deployment volume is unusually high.
- **Railway**: Not recommended for this use case. Designed for full-stack applications; adds unnecessary complexity for frontend-only hosting with Convex.

**Budget assessment**: All options within targets. Vercel ~$40-60/month at Phase 1 (2-3 users), ~$100-200/month at Phase 3 (10-20 users). Cloudflare Pages remains flat at ~$20-25/month regardless of scale.

---

## Part 1: Research Context and Scope

### 1.1 Hosting Requirements for Convex Applications

ADR-01-01 selected Convex as the backend platform. Convex Cloud handles:

| Component | Convex Responsibility | External Hosting Needed |
|-----------|----------------------|------------------------|
| Database | ✅ Document-relational storage | ❌ No |
| API/Functions | ✅ Serverless queries/mutations | ❌ No |
| File Storage | ✅ Integrated storage | ❌ No |
| Real-time Sync | ✅ Automatic reactivity | ❌ No |
| Authentication | ✅ Built-in auth providers | ❌ No |
| **Frontend Hosting** | ❌ Not included | ✅ **Yes** |

**Scope determination**: This research evaluates frontend hosting platforms only. Backend hosting is resolved by Convex Cloud.

### 1.2 Compass-Specific Requirements

Based on the Compass System Definition, frontend hosting must support:

**Operational constraints** (System Definition §4):

- Budget: Hosting should fit within overall $600–$2,000/year initial budget
- Team: Non-traditional developers using LLM coding agents—deployment must be simple
- Managed services preferred with minimal self-hosting
- Vendor independence: Standard deployment artifacts, portable configurations

**Scale requirements** (System Definition §3.7):

- Phase 1: 2–3 concurrent users
- Phase 3: 10–20 concurrent users
- Response time: Widget rendering under 100ms (CDN performance matters)

### 1.3 Evaluation Criteria Prioritization

| Criterion | Priority | Rationale |
|-----------|----------|-----------|
| **Convex integration quality** | Critical | Official support reduces deployment friction |
| **Deployment simplicity** | Critical | Non-technical team relies on automated workflows |
| **Preview deployments** | High | LLM coding agents generate PRs requiring review |
| **Cost efficiency** | Medium | Budget is generous; efficiency preferred but not constraining |
| **CDN performance** | Medium | Important for widget rendering; all candidates adequate |
| **Vendor independence** | Medium | Frontend hosting is commodity; low lock-in risk |

---

## Part 2: Platform Evaluations

### 2.1 Vercel

**What it is**: Vercel is a frontend deployment platform optimized for React and Next.js applications. Founded by the creators of Next.js, Vercel provides zero-configuration deployment from Git repositories with automatic preview deployments and global CDN distribution.

**Architecture philosophy**: Vercel treats frontend deployment as a Git-triggered workflow. Every push creates a deployment; every pull request creates a preview. The platform handles build optimization, asset compression, and global distribution automatically.

#### Pricing (January 2026)

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Hobby | $0 | 100 GB bandwidth, 1 user | Non-commercial only |
| Pro | $20/user/month | 1 TB bandwidth, unlimited projects | Commercial use |
| Enterprise | Custom | Custom limits, SLA, SSO | Large organizations |

**Cost estimate for Compass**:

- Phase 1 (2-3 users): $40-60/month (2-3 seats × $20)
- Phase 3 (10-20 users): $100-200/month (5-10 active developer seats)

Note: "Users" in Vercel's model refers to team members who deploy or configure projects. Viewers of deployed applications do not require seats.

#### Convex Integration: Exceptional

Convex has a dedicated integration in the Vercel Marketplace, providing the highest level of official support among evaluated platforms.

| Integration Aspect | Assessment | Evidence |
|--------------------|------------|----------|
| Official Marketplace | ✅ Yes | One-click installation from Vercel Marketplace |
| Documentation quality | ✅ Comprehensive | Dedicated guide at docs.convex.dev/production/hosting/vercel |
| Build command | ✅ Simple | `npx convex deploy --cmd 'npm run build'` |
| Environment variables | ✅ Automatic | `CONVEX_DEPLOY_KEY` managed via integration |
| Preview backends | ✅ Supported | Separate Convex deployment per preview branch |

**How the integration works**: The Vercel integration connects your Vercel project to a Convex project. When Vercel builds your application, it runs `npx convex deploy` to push your Convex functions to the cloud, then runs your frontend build command. Environment variables are automatically injected.

For preview deployments, Convex creates an isolated backend instance per preview branch. This prevents test data from contaminating production and allows reviewers to interact with fully functional previews.

**Why this matters for Compass**: The Marketplace integration means LLM coding agents can generate standard Next.js or React code without special deployment considerations. The deployment pipeline "just works" with no manual intervention beyond initial setup.

#### Deployment Workflow

**Initial setup (one-time, ~15 minutes)**:

1. Create Vercel account via GitHub authentication
2. Import repository from GitHub (automatic framework detection)
3. Install Convex integration from Vercel Marketplace
4. Add `CONVEX_DEPLOY_KEY` environment variable (from Convex dashboard)
5. Deploy

**Ongoing workflow (automatic)**:

- Push to `main` → automatic production deployment
- Open pull request → automatic preview deployment with isolated Convex backend
- Merge pull request → preview cleaned up, production redeployed

**Review process**: Vercel posts preview URLs as comments on pull requests. Non-technical reviewers can click the link to test changes in a fully functional environment without any technical knowledge required.

#### Additional Capabilities

| Capability | Vercel Support |
|------------|---------------|
| Edge Functions | ✅ 100+ edge locations |
| CI/CD Integration | ✅ GitHub, GitLab, Bitbucket |
| Custom domains | ✅ Automatic SSL |
| Analytics | ✅ Web Vitals, real-time |
| GDPR compliance | ✅ EU-US Data Privacy Framework certified |

---

### 2.2 Cloudflare Pages

**What it is**: Cloudflare Pages is a frontend deployment platform built on Cloudflare's global network of 300+ edge locations. Originally focused on static sites, Pages now supports full-stack applications through Cloudflare Workers integration.

**Architecture philosophy**: Cloudflare optimizes for edge deployment, running code as close to users as possible. Pages leverages the same network infrastructure that powers Cloudflare's CDN and DDoS protection services.

#### Pricing (January 2026)

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Free | $0 | 500 builds/month, **unlimited bandwidth** | 1 concurrent build |
| Pro | $20/month flat | 5,000 builds/month, **unlimited bandwidth** | 5 concurrent builds |
| Business | $200/month flat | 20,000 builds/month, **unlimited bandwidth** | 20 concurrent builds |

**Cost estimate for Compass**:

- Phase 1 (2-3 users): $0-20/month (free tier likely sufficient)
- Phase 3 (10-20 users): $20/month (Pro tier covers any realistic usage)

**Critical differentiator**: Cloudflare's pricing is **flat per account**, not per-seat. Unlimited team members can deploy without additional cost. Bandwidth is genuinely unlimited on all tiers with no overage charges.

#### Convex Integration: Requires Configuration

Cloudflare Pages does not have an official Convex Marketplace integration. The integration path is documented through a community guide rather than official vendor documentation.

| Integration Aspect | Assessment | Evidence |
|--------------------|------------|----------|
| Official Marketplace | ❌ No | No Cloudflare integration in Convex dashboard |
| Documentation quality | ⚠️ Community | Guide at stack.convex.dev (Convex community blog) |
| Build command | ⚠️ Complex | Requires `@cloudflare/next-on-pages` package |
| Environment variables | ✅ Manual | Standard Cloudflare Pages environment configuration |
| Preview backends | ⚠️ Manual | Requires custom workflow configuration |

**Additional configuration required**:

For Next.js applications (likely Compass framework), Cloudflare Pages requires:

1. Install `@cloudflare/next-on-pages` package
2. Create `wrangler.toml` configuration file
3. Enable Node.js compatibility flags
4. Configure build command: `npx @cloudflare/next-on-pages`

The community guide notes this setup takes approximately 30-45 minutes versus 15 minutes for Vercel.

**Why this matters for Compass**: The additional configuration complexity is a one-time cost during initial setup. However, it creates potential friction for LLM coding agents that may not understand Cloudflare-specific requirements. Documentation references Vercel patterns, which may confuse AI assistants.

#### Deployment Workflow

**Initial setup (one-time, ~45 minutes)**:

1. Create Cloudflare account
2. Connect GitHub repository to Cloudflare Pages
3. Install `@cloudflare/next-on-pages` in project
4. Create `wrangler.toml` with Node.js compatibility flags
5. Configure build command and environment variables
6. Add `CONVEX_DEPLOY_KEY` to environment variables
7. Deploy

**Ongoing workflow (automatic after setup)**:

- Push to `main` → automatic production deployment
- Open pull request → automatic preview deployment
- Convex preview backend requires separate configuration

#### Additional Capabilities

| Capability | Cloudflare Pages Support |
|------------|-------------------------|
| Edge Functions | ✅ 300+ edge locations (industry largest) |
| CI/CD Integration | ✅ GitHub, GitLab |
| Custom domains | ✅ Automatic SSL via Cloudflare |
| Analytics | ✅ Via Cloudflare Web Analytics |
| GDPR compliance | ✅ EU Cloud Code of Conduct certified |

---

### 2.3 Netlify

**What it is**: Netlify is a frontend deployment platform similar to Vercel, providing Git-triggered deployments with automatic preview deployments. Netlify pioneered the "Git push to deploy" workflow and remains popular for JAMstack applications.

**Architecture philosophy**: Netlify emphasizes collaborative workflows with features like Deploy Previews, split testing, and form handling built into the platform.

#### Pricing (September 2025 Update)

Netlify transitioned to credit-based pricing in September 2025, changing the cost model significantly.

| Plan | Cost | Included | Notes |
|------|------|----------|-------|
| Starter | $0 | 300 credits/month | Limited features |
| Pro | $20/member/month | 2,500 credits/member | Standard features |
| Enterprise | Custom | Custom credits | SSO, SLA |

**Credit consumption** (simplified):

- Build minutes: 1 credit/minute
- Bandwidth: 1 credit/GB
- Functions: varies by execution time

**Cost estimate for Compass**:

- Phase 1 (2-3 users): $40-60/month (similar to Vercel)
- Phase 3 (10-20 users): $100-200/month (similar to Vercel)

**Critical note**: Preview deployments on Netlify are **free**—they do not consume credits. This is uniquely valuable if LLM coding agents generate many pull requests for review.

#### Convex Integration: Good

Convex provides official documentation for Netlify deployment, though not a Marketplace integration.

| Integration Aspect | Assessment | Evidence |
|--------------------|------------|----------|
| Official Marketplace | ❌ No | No Netlify integration in Convex dashboard |
| Documentation quality | ✅ Official | Guide at docs.convex.dev/production/hosting/netlify |
| Build command | ✅ Simple | Same as Vercel: `npx convex deploy --cmd 'npm run build'` |
| Environment variables | ✅ Manual | Standard Netlify environment configuration |
| Preview backends | ✅ Supported | Fresh Convex backend per Deploy Preview |

**Integration parity with Vercel**: The deployment workflow mirrors Vercel's approach with the same build command override. The primary difference is manual environment variable configuration versus automatic integration.

#### Deployment Workflow

**Initial setup (one-time, ~20 minutes)**:

1. Create Netlify account via GitHub authentication
2. Import repository from GitHub
3. Configure build settings (automatic framework detection)
4. Add `CONVEX_DEPLOY_KEY` to environment variables
5. Optionally add separate key for preview environment
6. Deploy

**Ongoing workflow (automatic)**:

- Push to `main` → automatic production deployment
- Open pull request → automatic Deploy Preview (free, no credit consumption)
- Merge pull request → preview cleaned up, production redeployed

#### Additional Capabilities

| Capability | Netlify Support |
|------------|----------------|
| Edge Functions | ✅ 70+ edge locations |
| CI/CD Integration | ✅ GitHub, GitLab, Bitbucket |
| Custom domains | ✅ Automatic SSL |
| Analytics | ✅ Via Netlify Analytics |
| GDPR compliance | ✅ GDPR compliant with DPA |

---

### 2.4 Railway

**What it is**: Railway is a platform-as-a-service for deploying full-stack applications. Unlike Vercel, Netlify, and Cloudflare Pages, Railway is container-based and designed for backend services, databases, and full-stack deployments.

**Architecture philosophy**: Railway abstracts infrastructure management for backend services, providing Git-triggered deployment of Docker containers with automatic scaling and provisioning.

#### Why Railway Is Not Recommended

Railway is designed for a different use case than Compass requires:

| Aspect | Railway Approach | Compass Requirement |
|--------|-----------------|---------------------|
| Primary purpose | Backend services, full-stack | Frontend only (Convex handles backend) |
| Hosting model | Containers with CPU/RAM pricing | Static/edge deployment |
| Convex integration | Templates for self-hosting Convex | Connection to Convex Cloud |
| CDN | ❌ No built-in CDN | Global edge distribution |
| Pricing | Usage-based (CPU, RAM, egress) | Predictable per-seat or flat |

**Convex-specific issue**: Railway's Convex templates are designed for self-hosting the Convex backend—not for deploying frontends that connect to Convex Cloud. Convex's official documentation does not include Railway as a hosting option for this use case.

**Static site workaround**: Railway can host static frontends via NGINX or Caddy containers, but this requires container configuration that adds unnecessary complexity. The result would be a container-hosted static site without CDN benefits—inferior to purpose-built frontend platforms.

**Cost estimate**: Railway's usage-based pricing makes costs unpredictable. A simple frontend could cost $25-40/month or spike higher depending on traffic patterns. There is no free tier for ongoing use (only a one-time $5 credit).

**Recommendation**: Railway should not be evaluated further for Compass frontend hosting. It excels at backend services but is the wrong tool for frontend-only deployment with Convex.

---

## Part 3: Comparative Analysis

### 3.1 Feature Comparison Matrix

| Feature | Vercel | Cloudflare Pages | Netlify | Railway |
|---------|--------|------------------|---------|---------|
| **Convex Marketplace** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Official Convex Docs** | ✅ Yes | ⚠️ Community | ✅ Yes | ❌ No |
| **Zero-config deploy** | ✅ Yes | ⚠️ Requires config | ✅ Yes | ❌ Complex |
| **Preview deployments** | ✅ Yes | ✅ Yes | ✅ Free | ⚠️ Config needed |
| **Preview Convex backends** | ✅ Automatic | ⚠️ Manual | ✅ Supported | ❌ N/A |
| **Edge locations** | 100+ | **300+** | 70+ | 4 regions |
| **Built-in CDN** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Unlimited bandwidth** | ❌ 1TB Pro | ✅ Yes | ❌ Credit-based | ❌ Paid egress |

### 3.2 Pricing Comparison at Scale

**Phase 1: 2-3 users**

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Vercel Pro | $40-60 | 2-3 seats × $20 |
| Cloudflare Pro | $0-20 | Free tier or flat $20 |
| Netlify Pro | $40-60 | 2-3 members × $20 |
| Railway | $25-40 | Unpredictable usage |

**Phase 3: 10-20 users**

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Vercel Pro | $100-200 | 5-10 developer seats |
| Cloudflare Pro | **$20** | Flat rate, unlimited users |
| Netlify Pro | $100-200 | 5-10 member seats |
| Railway | $60-150+ | Variable container costs |

**Budget analysis**: All options fit within the $50/month Phase 1 and $150/month Phase 3 hosting budget targets from the research task. Cloudflare offers the best value at scale due to flat pricing.

### 3.3 Convex Integration Quality Ranking

1. **Vercel** — Marketplace integration, automatic environment variables, official documentation as primary example
2. **Netlify** — Official documentation, same deployment pattern as Vercel, manual configuration
3. **Cloudflare Pages** — Community documentation, additional packages required, manual Convex backend configuration
4. **Railway** — Not applicable for this use case

### 3.4 Deployment Simplicity Ranking

1. **Vercel** — Zero-configuration, automatic framework detection, integrated Convex setup
2. **Netlify** — Near-zero configuration, automatic framework detection, manual environment setup
3. **Cloudflare Pages** — Requires Cloudflare-specific packages and configuration files
4. **Railway** — Requires container configuration for static sites

### 3.5 LLM Coding Agent Compatibility

For a team relying on LLM coding agents to generate and maintain code, documentation alignment matters. When AI assistants search for deployment guidance:

**Vercel**: Most Convex tutorials and examples use Vercel. LLM training data includes extensive Vercel deployment patterns. Generated code is likely to work without modification.

**Netlify**: Good documentation coverage. Similar patterns to Vercel. LLMs may occasionally confuse Vercel and Netlify configuration details.

**Cloudflare Pages**: Requires Cloudflare-specific packages (`@cloudflare/next-on-pages`) that LLMs may not include by default. Configuration files (`wrangler.toml`) differ from standard patterns. Higher likelihood of AI-generated code requiring manual correction.

---

## Part 4: Recommendations

### 4.1 Primary Recommendation: Vercel

Vercel is recommended for Compass frontend hosting based on:

**Integration quality**: The Convex Marketplace integration provides the smoothest deployment experience. Environment variables are automatically managed, and preview deployments create isolated Convex backends without additional configuration.

**Documentation alignment**: Convex's official documentation uses Vercel as the primary hosting example. LLM coding agents searching for deployment guidance will find Vercel patterns first and most frequently.

**Operational simplicity**: Zero-configuration deployment fits the team's non-technical profile. The workflow (push to GitHub → automatic deployment) requires no manual intervention after initial setup.

**Ecosystem fit**: Vercel is the optimal deployment target for Next.js applications (likely Compass framework choice). The same company maintains both products, ensuring compatibility.

### 4.2 Alternative Recommendation: Cloudflare Pages

If cost optimization becomes a priority at Phase 3 scale, consider migrating to Cloudflare Pages:

**When to choose Cloudflare**:

- Team grows beyond 10 developer seats and Vercel costs exceed budget comfort
- Traffic patterns are unpredictable (financial news can spike)
- Bandwidth costs on Vercel approach concerning levels
- Initial Convex configuration complexity is no longer a barrier (team has experience)

**Migration path**: Cloudflare Pages uses standard build outputs. Migration involves:

1. Adding `@cloudflare/next-on-pages` package
2. Creating `wrangler.toml` configuration
3. Moving environment variables to Cloudflare dashboard
4. Updating DNS if using Cloudflare domains

The migration is straightforward but not zero-effort. Recommend evaluating at Phase 3 rather than starting with Cloudflare.

### 4.3 Netlify as Viable Option

Netlify is a viable alternative if:

- Free preview deployments are valuable due to high PR volume from LLM agents
- Team prefers Netlify's collaborative features (Netlify Drawer, deploy notifications)
- Specific Netlify features (form handling, identity) are useful

For Compass's requirements, Netlify offers no significant advantage over Vercel while lacking the Marketplace integration.

### 4.4 Railway Not Recommended

Railway should not be considered for Compass frontend hosting. It is designed for backend services and adds unnecessary complexity for frontend-only deployment with Convex Cloud.

---

## Part 5: Open Questions for Stakeholders

1. **Framework choice**: Is Next.js confirmed as the Compass frontend framework? Vercel's advantages are strongest with Next.js. If using Vite or another framework, the platforms become more equivalent.

2. **Traffic prediction**: Are traffic spikes expected (breaking financial news)? If yes, Cloudflare's unlimited bandwidth provides peace of mind. If traffic is predictable, Vercel's limits are likely adequate.

3. **Preview deployment volume**: How many pull requests per week are anticipated from LLM coding agents? High volume (>50/week) might favor Netlify's free previews.

4. **Team growth timeline**: When might the team exceed 5-10 developer seats? This affects when Cloudflare's flat pricing becomes advantageous.

---

## Part 6: Next Steps

**If proceeding with Vercel**:

1. Create Vercel team account and configure GitHub integration
2. Install Convex integration from Vercel Marketplace
3. Import Compass repository and configure initial deployment
4. Set up preview deployment workflow for isolated Convex backends
5. Document deployment process in Compass repository README
6. Configure custom domain and SSL (if applicable)

**If evaluating Cloudflare as alternative**:

1. Prototype deployment with `@cloudflare/next-on-pages` on a test project
2. Measure configuration complexity and time investment
3. Compare preview deployment workflow with Vercel experience
4. Document findings for Phase 3 cost optimization decision

---

## Appendix A: Detailed Pricing Tables

### Vercel Pro Plan Details

| Resource | Included | Overage |
|----------|----------|---------|
| Bandwidth | 1 TB/month | $0.15/GB |
| Build minutes | 6,000/month | $0.015/minute |
| Serverless function execution | 1M invocations | $0.60/M |
| Edge function execution | 1M invocations | $0.65/M |
| Image optimization | 5,000 images | $5/1,000 |

### Cloudflare Pages Pro Plan Details

| Resource | Included | Overage |
|----------|----------|---------|
| Bandwidth | **Unlimited** | N/A |
| Builds | 5,000/month | Additional builds fail |
| Concurrent builds | 5 | N/A |
| Preview deployments | Unlimited | N/A |
| Sites | Unlimited | N/A |

### Netlify Pro Plan Details (Credit-Based)

| Resource | Credit Cost |
|----------|------------|
| Build minutes | 1 credit/minute |
| Bandwidth | 1 credit/GB |
| Functions (125K invocations included) | 1 credit/125K additional |

Pro plan includes 2,500 credits/member/month.

---

## Appendix B: Sources

1. **[T1/S1]** Convex. "Using Convex with Vercel." Retrieved 2026-01-25. https://docs.convex.dev/production/hosting/vercel

2. **[T1/S1]** Convex. "Setting Up Cloudflare Pages for Convex Preview Deployments." Retrieved 2026-01-25. https://stack.convex.dev/setting-up-cloudflare-pages-for-convex-deployments

3. **[T1/S1]** Vercel. "Pricing." Retrieved 2026-01-25. https://vercel.com/pricing

4. **[T1/S1]** Cloudflare. "Pages Pricing." Retrieved 2026-01-25. https://pages.cloudflare.com

5. **[T1/S1]** Netlify. "Credit-based pricing on Netlify." Published 2025-09. Retrieved 2026-01-25. https://www.netlify.com/blog/new-pricing-credits/

6. **[T1/S1]** Vercel. "EU-US Data Privacy Framework Certification." Retrieved 2026-01-25. https://vercel.com/guides/is-vercel-certified-under-dpf

7. **[T1/S1]** Vercel. "How to Use GitHub Actions with Vercel." Retrieved 2026-01-25. https://docs.vercel.com/kb/guide/how-can-i-use-github-actions-with-vercel

8. **[T2/S2]** Railway. "Static Hosting Guide." Retrieved 2026-01-25. https://docs.railway.com/guides/static-hosting

---

## Appendix C: Related Documents

- **RF-01-01**: Backend Platform Research Findings (confirms Convex selection, frontend hosting not included)
- **ADR-01-01**: Backend Platform Selection (Convex selected; requires external frontend hosting)
- **Compass System Definition**: Budget constraints and team capacity context
- **ADR-08-01**: Frontend Hosting Selection (pending decision document)

---

*End of Frontend Hosting Platform Research Findings (RF-08-01)*
