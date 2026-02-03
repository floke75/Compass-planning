---
id: ADR-08-01
type: adr
area: 08-hosting
title: Frontend Hosting Platform Selection
status: proposed
created: 2026-01-25
updated: 2026-02-03
author: compass-research
summary: Selects Vercel as the frontend hosting platform for Compass based on official Convex Marketplace integration, zero-configuration deployment workflows, and optimal documentation alignment for LLM coding agents
tags: [hosting, frontend, deployment, vercel, convex, decision]
related:
  - RF-08-01
  - ADR-01-01
links:
  - rel: related
    target_id: "RF-08-01"
  - rel: related
    target_id: "ADR-01-01"
decision_date: null
deciders: []
supersedes: null
---

# Frontend Hosting Platform Selection

## Status

**Proposed** — Awaiting stakeholder review based on RF-08-01 research findings.

---

## Context

ADR-01-01 selected Convex as the backend platform for Compass. Convex Cloud handles database storage, serverless functions, file storage, real-time synchronization, and authentication. However, Convex does not include frontend hosting—the web application that users interact with must be deployed separately.

The Compass System Definition (§4.2) emphasizes that operational simplicity is essential for EFN's non-traditional development team. The team relies on LLM coding agents as their primary development method and does not maintain infrastructure manually. Frontend hosting must integrate seamlessly with the Convex backend and require minimal configuration.

The hosting platform must also support preview deployments. LLM coding agents generate pull requests that require review before merging to production. Preview deployments allow reviewers to test changes in a fully functional environment with an isolated Convex backend, ensuring test data does not contaminate production.

Budget constraints (System Definition §4.1) allocate a portion of the $600–$2,000/year initial budget to hosting. The research task specified $50/month for Phase 1 and $150/month for Phase 3 as hosting budget targets.

---

## Options Considered

### Option 1: Vercel

Vercel is a frontend deployment platform optimized for React and Next.js applications. Founded by the creators of Next.js, Vercel provides zero-configuration deployment from Git repositories with automatic preview deployments and global CDN distribution across 100+ edge locations.

**Pros:**

Vercel offers the highest-quality Convex integration among evaluated platforms. Convex has a dedicated integration in the Vercel Marketplace, enabling one-click installation with automatic environment variable management. When Vercel builds the application, it automatically runs Convex deployment and injects the necessary configuration without manual intervention.

The deployment workflow is fully automated. Every push to the main branch triggers a production deployment. Every pull request triggers a preview deployment with an isolated Convex backend. Preview URLs are posted as comments on pull requests, allowing non-technical reviewers to test changes by clicking a link.

Convex's official documentation uses Vercel as the primary hosting example. LLM coding agents searching for deployment guidance will find Vercel patterns first and most frequently. This documentation alignment reduces the likelihood of AI-generated code requiring manual correction.

**Cons:**

Vercel uses per-seat pricing at $20/user/month. At Phase 3 scale with 10-20 users, costs could reach $100-200/month depending on how many team members require deployment access. This is within budget targets but higher than Cloudflare's flat-rate alternative.

Vercel has a slight preference toward Next.js in its feature set and documentation. While other frameworks are fully supported, the optimal experience is with Next.js applications. This creates mild lock-in toward the Vercel/Next.js ecosystem.

---

### Option 2: Cloudflare Pages

Cloudflare Pages is a frontend deployment platform built on Cloudflare's global network of 300+ edge locations—the largest CDN in the industry. Pages supports static sites and full-stack applications through Cloudflare Workers integration.

**Pros:**

Cloudflare uses flat-rate pricing: $20/month for the Pro plan regardless of team size. Bandwidth is genuinely unlimited on all tiers with no overage charges. At Phase 3 scale with 10-20 users, Cloudflare would cost $20/month versus $100-200/month on Vercel—a significant difference.

The CDN network is the largest in the industry, with over 300 points of presence globally *(as_of: 2026-01-25)*. For a financial news broadcaster where breaking stories can cause sudden traffic surges, unlimited bandwidth eliminates billing anxiety entirely.

**Cons:**

Cloudflare Pages does not have an official Convex Marketplace integration. Deploying a Convex application requires additional configuration: installing the `@cloudflare/next-on-pages` package, creating a `wrangler.toml` configuration file, and enabling Node.js compatibility flags. This setup takes approximately 30-45 minutes versus 15 minutes for Vercel.

The Convex integration is documented through a community guide on Convex's Stack blog rather than official vendor documentation. This creates potential friction for LLM coding agents that may not understand Cloudflare-specific requirements. Configuration files differ from standard patterns found in most tutorials and training data.

---

### Option 3: Netlify

Netlify is a frontend deployment platform similar to Vercel, providing Git-triggered deployments with automatic preview deployments. Netlify pioneered the "Git push to deploy" workflow and remains popular for JAMstack applications.

**Pros:**

Netlify's preview deployments (called Deploy Previews) are genuinely free—they do not consume credits or count against plan limits. For a workflow generating many pull requests from LLM coding agents, this provides unlimited testing without cost concerns.

Convex provides official documentation for Netlify deployment with the same build command pattern as Vercel: `npx convex deploy --cmd 'npm run build'`. The setup process mirrors Vercel's approach with only manual environment variable configuration as the difference.

**Cons:**

Netlify transitioned to credit-based pricing in September 2025, adding complexity to cost estimation. Non-technical users may find credit consumption confusing compared to Vercel's straightforward per-seat model.

No Marketplace integration exists. While documentation is official, the integration requires manual configuration of environment variables and does not provide the automatic setup that Vercel's Marketplace integration offers.

---

### Option 4: Railway

Railway is a platform-as-a-service for deploying full-stack applications using container-based infrastructure.

**Pros:**

Railway excels at backend service deployment with automatic scaling and provisioning.

**Cons:**

Railway is designed for a fundamentally different use case. It hosts containerized applications, not static frontends with CDN distribution. For frontend-only hosting with Convex Cloud, Railway would require configuring NGINX or Caddy containers to serve static files—unnecessary complexity that defeats the purpose of a managed hosting platform.

Railway's Convex templates are designed for self-hosting the Convex backend, not for deploying frontends that connect to Convex Cloud. Convex's official documentation does not include Railway as a hosting option for this use case.

Railway lacks a built-in CDN. Global content delivery would require additional Cloudflare integration, adding complexity and infrastructure to manage.

---

### Option 5: Do Nothing (Defer Decision)

Defer the hosting decision to allow more evaluation time.

**Pros:**

No immediate implementation effort. Additional research could surface new options.

**Cons:**

Compass cannot be deployed without frontend hosting. This decision does not block research phases but does block any practical testing or demonstration of Compass functionality. The evaluated platforms (Vercel, Cloudflare, Netlify) represent the leading options for React/Next.js frontend deployment. Waiting for hypothetical better options provides no concrete benefit.

---

## Decision

We will use **Vercel** as the frontend hosting platform for Compass.

The decision is driven by three factors that align with EFN's specific context:

**Factor 1: Convex Integration Quality**. The Vercel Marketplace integration provides the smoothest deployment experience for Convex applications. Environment variables are automatically managed, preview deployments create isolated Convex backends without additional configuration, and the entire workflow requires no manual intervention after initial 15-minute setup. For a non-technical team relying on automated workflows, this friction reduction is significant.

**Factor 2: Documentation Alignment for LLM Agents**. The team relies on LLM coding agents as their primary development method. Convex's official documentation uses Vercel as the primary hosting example. Most tutorials, examples, and community resources assume Vercel deployment. When AI assistants generate deployment code, it will most likely match Vercel's expected patterns without requiring manual correction.

**Factor 3: Operational Simplicity**. The System Definition emphasizes managed services with minimal self-hosting. Vercel's zero-configuration deployment (push to GitHub → automatic deployment) fits this requirement exactly. No infrastructure configuration, no build scripts to maintain, no container orchestration. The workflow is simple enough that even non-technical stakeholders can understand the deployment pipeline.

The cost trade-off has been evaluated and accepted. Vercel's per-seat pricing will cost approximately $40-60/month at Phase 1 (2-3 users) and $100-200/month at Phase 3 (10-20 users). This is within budget targets and justified by the integration quality advantages. If costs become a concern at scale, migration to Cloudflare Pages is straightforward.

---

## Consequences

### Positive

The Convex Marketplace integration accelerates Compass deployment by eliminating manual configuration. Initial setup requires approximately 15 minutes: connect GitHub, install integration, deploy. No environment variable management, no build command configuration, no preview deployment setup.

Automatic preview deployments with isolated Convex backends enable safe review of LLM-generated pull requests. Reviewers can test changes in fully functional environments without risking production data contamination.

Documentation alignment with LLM training data improves AI coding assistant effectiveness. Generated deployment code is more likely to work correctly on first attempt, reducing debugging time for the non-technical team.

The global CDN with 100+ edge locations provides adequate performance for widget rendering under 100ms as specified in the System Definition's performance targets.

### Negative

Per-seat pricing creates predictable but potentially significant costs at scale. If the team grows to 10-15 developers with Vercel access, monthly costs could reach $200-300/month. This remains within the proven-value budget tier but exceeds the initial budget target if Compass is the only service consuming that allocation.

Slight ecosystem preference toward Next.js may influence framework decisions. While Vercel supports all major frameworks, the optimal experience and deepest integration is with Next.js. This creates mild pressure toward the Vercel/Next.js ecosystem.

Bandwidth limits (1 TB/month on Pro plan) could become relevant if traffic spikes significantly during breaking financial news. Overages cost $0.15/GB. For perspective, 1 TB handles approximately 10 million page views of typical frontend assets.

### Neutral

Migration to Cloudflare Pages remains straightforward if cost optimization becomes necessary. Both platforms deploy standard build outputs from Git repositories. Migration involves adding Cloudflare-specific configuration files and moving environment variables—a task measured in hours, not weeks.

Preview deployment retention differs between platforms (Vercel retains for 5-14 days, Netlify for 90 days). The shorter Vercel retention is unlikely to affect Compass workflows where pull requests are reviewed within days.

---

## Implementation Notes

### Initial Setup

Create a Vercel team account using GitHub authentication. Team accounts enable collaboration features and shared billing.

Import the Compass repository from GitHub. Vercel's automatic framework detection will identify the project type and configure appropriate build settings.

Install the Convex integration from the Vercel Marketplace. This connects the Vercel project to the Compass Convex project and configures environment variable management.

Configure the build command override if needed: `npx convex deploy --cmd 'npm run build'`. The Convex integration may set this automatically.

Add separate `CONVEX_DEPLOY_KEY` values for production and preview environments. This enables isolated Convex backends per preview deployment.

Deploy the initial version and verify the deployment URL is accessible.

### Ongoing Operations

No ongoing operations required. Vercel handles deployment automatically on every Git push.

Monitor bandwidth usage through Vercel's dashboard. If usage approaches 1 TB/month, evaluate traffic patterns and consider Cloudflare migration.

Review Vercel invoices monthly to track cost trajectory as the team grows.

### Cost Optimization Path

If Vercel costs exceed comfort levels at Phase 3 scale, migrate to Cloudflare Pages:

1. Add `@cloudflare/next-on-pages` package to the project
2. Create `wrangler.toml` configuration file with Node.js compatibility flags
3. Move environment variables to Cloudflare Pages dashboard
4. Test preview deployment workflow with Convex
5. Update DNS to point to Cloudflare Pages deployment
6. Decommission Vercel project

This migration can be completed in a single work session and poses minimal risk since both platforms deploy standard build outputs.

---

## Related Documents

**Research foundation**: RF-08-01 provides the comprehensive research findings that informed this decision, including detailed platform evaluations, comparative analysis, and pricing projections.

**Backend context**: ADR-01-01 documents the Convex selection that establishes the requirement for external frontend hosting.

**Informs downstream research**: Area 10 (Dev Tooling—research pending) should incorporate Vercel deployment patterns into the development workflow specification.

**System requirements**: The Compass System Definition provides the operational constraints, budget targets, and team capacity context that shaped this decision.

---

*End of Frontend Hosting Platform Selection (ADR-08-01)*
