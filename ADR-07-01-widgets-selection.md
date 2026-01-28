---
id: ADR-07-01
type: adr
area: 07-widget-libraries
title: Widget Component Library Selection
status: proposed
created: 2026-01-26
updated: 2026-01-26
author: compass-research
summary: Selects Thesys C1 with custom shadcn/ui components as the widget rendering approach for Compass
tags: [widgets, components, decision, generative-ui, thesys]
related:
  - RF-07-01
  - ADR-02-01
  - DD-19-01
decision_date: null
deciders: []
supersedes: null
---

# Widget Component Library Selection

## Decision

Adopt a **hybrid widget rendering architecture** combining Thesys C1 for generative UI with custom shadcn/ui + dnd-kit components for specialized planning widgets.

**Primary rendering layer**: Thesys C1 for conversational UI, standard form elements, and dynamic widget generation.

**Custom component layer**: shadcn/ui + dnd-kit for approximately 8 specialized widgets not covered by C1's native component library.

**Form state management**: React Hook Form with Zod validation for complex multi-field widgets.

---

## Status

Proposed — pending team review and C1 integration prototype.

---

## Context

Compass requires dynamic widgets for structured input during LLM-orchestrated planning conversations. The Compass System Definition (§2.2) specifies a taxonomy of 16 widget types across six categories: choice widgets, spectrum/allocation widgets, comparative widgets, spatial/ordering widgets, generative widgets, and meta widgets. Every widget must support three UX guarantees: escape hatch, help trigger, and research trigger.

The orchestration layer (Mastra + Vercel AI SDK v6, per ADR-02-01) generates widget specifications as Zod-validated JSON. The widget layer must render these specifications as interactive React components, support progressive streaming during LLM generation, and enable custom extension for Compass-specific interactions.

---

## Options Considered

### Option 1: Thesys C1 with Custom Components (Selected)

Use Thesys C1's generative UI API as the primary rendering layer, with custom shadcn/ui + dnd-kit components registered as C1 custom components for specialized widgets.

**Strengths**: Native Mastra integration eliminates orchestration glue code. Streaming support reduces time-to-interactivity. Clear custom component pattern enables taxonomy extension. OpenAI-compatible API simplifies integration. Reasonable pricing at $49-499/month for projected usage.

**Weaknesses**: New product (April 2025) with unverified long-term stability. Requires learning C1 DSL patterns. Vendor dependency for core rendering.

**Development estimate**: 5-6 weeks for complete taxonomy coverage.

### Option 2: CopilotKit with Custom Components

Use CopilotKit's AG-UI protocol for agent-to-UI communication, with custom shadcn/ui components for specialized widgets.

**Strengths**: Open-source core with MIT license. Strong human-in-the-loop patterns via `useCopilotAction`. Google A2UI partnership suggests ecosystem momentum.

**Weaknesses**: No native Mastra integration (requires custom glue code). More complex setup than C1. Enterprise features require $1,000+/seat/month.

**Development estimate**: 6-8 weeks for complete taxonomy coverage.

### Option 3: shadcn/ui + dnd-kit with JSON Registry

Build a custom JSON-to-component registry using shadcn/ui primitives and dnd-kit for drag-and-drop interactions.

**Strengths**: Maximum control over rendering behavior. Full code ownership. No vendor dependency for core rendering. Excellent TypeScript support and LLM maintainability.

**Weaknesses**: Requires building and maintaining registry infrastructure. No turnkey streaming support. Higher development overhead for orchestration integration.

**Development estimate**: 6-9 weeks for complete taxonomy coverage.

### Option 4: SurveyJS with Custom Extensions

Use SurveyJS Form Library for survey-style widgets with custom components for spatial and comparison widgets.

**Strengths**: Native ranked choice and matrix widgets. JSON-first architecture aligns with LLM generation. Mature product with stable API.

**Weaknesses**: Less flexible styling than Tailwind. Survey Creator licensing costs (€499-€1,998/developer). Limited ecosystem integration with Mastra/Vercel stack.

**Development estimate**: 7-9 weeks for complete taxonomy coverage.

---

## Decision Rationale

### Why Thesys C1 with Custom Components

The selection prioritizes **development velocity** and **architectural alignment** with the existing Mastra + Vercel AI SDK stack. Thesys C1 provides native Mastra integration, eliminating the need for custom orchestration glue code that all other options require. This directly addresses the constraint that EFN has a small, non-technical team without traditional development resources.

The generative UI paradigm fundamentally changes the build-versus-buy calculus. Rather than maintaining comprehensive Zod schemas, component registries, and switch statements synchronized with LLM prompts, C1 enables the LLM to describe UI intent directly through structured specifications that the SDK interprets. This reduces the surface area for orchestration bugs and simplifies maintenance.

C1's custom component system provides an escape valve for Compass-specific widgets. By building approximately 8 custom components using shadcn/ui + dnd-kit and registering them with C1, the hybrid approach achieves complete taxonomy coverage while leveraging native generation for standard interactions.

### Why Not CopilotKit

CopilotKit's open-source core is appealing, but the lack of native Mastra integration adds integration complexity that offsets the licensing benefit. The AG-UI protocol is architecturally sound but introduces concepts (bidirectional state sync, action registration) that duplicate functionality already present in Mastra's thread-based memory system.

### Why Not Pure shadcn/ui

A custom JSON registry provides maximum control but requires significant additional development to achieve feature parity with C1's streaming and orchestration integration. The 3-4 week development time difference represents meaningful velocity impact for initial delivery.

### Why Not SurveyJS

SurveyJS's native ranking and matrix widgets are valuable, but its styling constraints and limited ecosystem integration create friction with the Tailwind/Mastra/Vercel stack. The licensing costs for Survey Creator are comparable to C1's Grow tier without providing the generative UI benefits.

---

## Custom Component Scope

The following widgets require custom development using shadcn/ui + dnd-kit, registered as C1 custom components:

| Widget | Implementation Approach | Estimated Effort |
|--------|------------------------|------------------|
| RankedChoice | shadcn Card + dnd-kit Sortable | 3-4 days |
| PairwiseComparison | shadcn Card + RadioGroup + state machine | 4-5 days |
| AllocationSlider | shadcn Slider + shared state + Zod refine | 3-4 days |
| OpposingSpectrum | shadcn Slider + custom labels | 1-2 days |
| TradeoffTable | shadcn DataTable + inline inputs | 3-4 days |
| CardSort | shadcn Card + dnd-kit multiple zones | 3-4 days |
| Sequencer | shadcn + dnd-kit Sortable | 2-3 days |
| QuadrantPlacer | Custom positioning + shadcn styling | 4-5 days |

Total custom development: approximately 24-31 days (5-6 weeks with integration and testing).

---

## Cost Analysis

### Thesys C1 Costs

| Tier | API Calls/Month | Monthly Cost | Use Case |
|------|-----------------|--------------|----------|
| Free | 5,000 | $0 | Development |
| Build | 25,000 | $49 | Phase 1 production |
| Grow | 500,000 | $499 | Phase 3 production |

LLM token costs pass through at provider rates (Claude Sonnet 4: $3/$15 per MTok).

### Projected Monthly Costs

| Phase | C1 Tier | C1 Cost | LLM Passthrough | Total Widget Layer |
|-------|---------|---------|-----------------|-------------------|
| Phase 1 | Build | $49 | ~$10-20 | ~$60-70/month |
| Phase 3 | Grow | $499 | ~$50-100 | ~$550-600/month |

These costs fit within the budget targets established in the Compass System Definition (§4.1).

---

## Consequences

### Positive Consequences

**Faster initial delivery**: Native Mastra integration and built-in components reduce time to working prototype by 2-3 weeks versus custom registry approaches.

**Reduced maintenance burden**: Generative UI pattern eliminates the need to maintain synchronization between Zod schemas, component registry, and LLM prompts.

**Streaming support**: Native progressive rendering improves user experience during LLM generation without custom implementation.

**Clear extension path**: Custom component registration provides structured approach for adding Compass-specific widgets.

### Negative Consequences

**Vendor dependency**: Core rendering depends on Thesys C1 availability and API stability.

**Learning curve**: Team must learn C1 DSL patterns and custom component registration.

**Cost scaling**: C1 costs scale with usage; high-volume Phase 3 scenarios may require cost monitoring.

### Mitigation Strategies

**Vendor dependency**: Maintain abstraction layer between Mastra workflows and C1 rendering. Document fallback to pure shadcn/ui registry if C1 becomes unavailable.

**Learning curve**: Invest in prototype development during Phase 1 to build team familiarity before scaling.

**Cost scaling**: Monitor API call patterns; optimize batching and caching for high-frequency interactions.

---

## Implementation Notes

### Integration Pattern

```
Mastra Agent → Decision Logic
  ├─ Standard interactions → C1 Generative UI (native)
  ├─ Specialized widgets → C1 Custom Components (shadcn-based)
  └─ Complex state flows → Direct React + React Hook Form
```

### Widget Wrapper for UX Guarantees

All widgets must be wrapped with a `WidgetWrapper` component that provides standardized footer actions for escape hatch, help trigger, and research trigger. Register this as a C1 custom component that other widgets compose.

### Schema Implications for Area 19

Widget schemas (Area 19) should use separate Zod schemas per widget type rather than discriminated unions. Include a `meta` field for UX guarantee configuration. Schema-component registration manifests serve as the single source of truth for widget capabilities.

---

## Related Decisions

**ADR-02-01 (Orchestration Selection)**: Mastra + Vercel AI SDK v6 selection directly informs this decision—C1's native Mastra integration is a primary selection factor.

**Area 19 (Widget Schema)**: This decision establishes constraints for widget schema design, particularly the need for separate schemas per type and custom component registration patterns.

**Area 18 (Questioning Arc)**: Widget rendering integrates with questioning arc state management via Mastra workflow suspension and C1 action callbacks.

---

## Review Triggers

This decision should be reconsidered if:

- Thesys C1 pricing increases significantly beyond projected costs
- C1 API stability issues impact production reliability
- Custom component requirements exceed 50% of total widget interactions
- Mastra integration patterns change in ways that break C1 compatibility
- Alternative generative UI solutions emerge with superior Mastra integration

---

*End of Widget Component Library Selection (ADR-07-01)*
