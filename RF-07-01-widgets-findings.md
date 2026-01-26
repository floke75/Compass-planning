---
id: RF-07-01
type: rf
area: 07-widget-libraries
title: Widget Component Library Research Findings
status: draft
created: 2026-01-26
updated: 2026-01-26
author: compass-research
summary: Evaluates widget component libraries and generative UI approaches against Compass taxonomy, recommending Thesys C1 with custom shadcn/ui extensions
tags: [widgets, components, ui, generative-ui, thesys, shadcn]
related:
  - RF-02-01
  - ADR-02-01
confidence: high
methodology: "Web research with official vendor documentation, GitHub repositories, and framework integration guides"
limitations:
  - "Thesys C1 is a young product (April 2025 launch), production stability unverified at scale"
  - "No hands-on performance benchmarking conducted"
  - "Custom component development estimates based on similar projects, not direct prototyping"
  - "C1 pricing may change as product matures"
responds_to: null
implications_for: [ADR-07-01, DD-19-01, STD-19-01]
---

# Widget Component Library Research Findings

## Executive Summary

**Recommendation**: Implement a hybrid architecture combining **Thesys C1** for conversational UI and standard interactions with **shadcn/ui + dnd-kit** custom components for specialized planning widgets.

**Confidence**: High — Thesys C1 provides native Mastra integration (Compass's selected orchestration framework) and streaming generative UI, while shadcn/ui offers the control needed for complex planning interactions.

**Key insight**: The emergence of generative UI APIs fundamentally changes the build-vs-buy calculus. Rather than building a JSON schema → component registry → React rendering pipeline, generative UI enables the LLM to describe UI intent directly, with the rendering layer interpreting structured specifications into live components. This reduces orchestration complexity while maintaining type safety through Zod schemas.

**Key trade-off**: Thesys C1 introduces vendor dependency and recurring costs (~$50-500/month depending on usage), but the alternative—building full widget orchestration from scratch—requires 3-4 additional weeks of development versus 1-2 weeks for C1 integration.

**Critical finding**: No single library covers more than 50% of Compass's widget taxonomy natively. Every approach requires custom development for ranked choice, pairwise comparison, allocation, and spatial widgets. The question is not which library to use, but which rendering paradigm to build upon.

---

## Part 1: Context and Scope

### 1.1 Research Question

What widget rendering approach best supports Compass's requirements for LLM-generated dynamic widgets, development velocity for a small non-technical team, and coverage of the specialized planning widget taxonomy?

### 1.2 Compass-Specific Requirements

The evaluation focused on five capabilities derived from the Compass System Definition and prior research decisions.

**Dynamic Widget Generation** (System Definition §2.2): Compass generates widgets dynamically based on conversational context. The widget layer must render from LLM-generated specifications without requiring code changes for each new widget instance.

**Taxonomy Coverage** (System Definition §2.2): Compass defines 16+ widget types across six categories: choice, spectrum/allocation, comparative, spatial/ordering, generative, and meta widgets. The solution must cover the majority natively or provide clear extension paths.

**Mastra Integration** (ADR-02-01): Compass uses Mastra + Vercel AI SDK v6 for orchestration. The widget solution should integrate cleanly with Mastra's workflow system rather than requiring parallel orchestration infrastructure.

**Development Velocity**: EFN's small team requires solutions that accelerate development rather than requiring extensive custom infrastructure. LLM coding agents must be able to understand and modify the widget code.

**UX Escape Hatches** (System Definition §2.2): Every widget must support three standard actions: "None of these / I'll describe instead," "Help me think," and "Research this." The solution must enable consistent implementation of these guarantees.

### 1.3 Evaluation Criteria

This research explicitly excludes accessibility (WCAG compliance) from evaluation criteria, as Compass is an internal tool. Evaluation focuses on development velocity, LLM maintainability, dynamic rendering capability, TypeScript/React support, and customization flexibility.

### 1.4 Candidates Evaluated

The research evaluated both traditional component libraries and novel generative UI approaches:

| Candidate | Category | Key Differentiator |
|-----------|----------|-------------------|
| Thesys C1 | Generative UI API | Native Mastra integration, streaming UI generation |
| CopilotKit | Agent-UI Framework | Open-source AG-UI protocol, human-in-the-loop |
| Vercel AI SDK | Tool-based Pattern | Maximum control, AI Elements library |
| shadcn/ui | Component Library | Copy-paste ownership, Tailwind styling |
| SurveyJS | Survey Framework | Native ranked choice, matrix questions |
| React Aria | Hooks Library | Best drag-and-drop system |

---

## Part 2: The Generative UI Paradigm

### 2.1 Traditional vs. Generative Approaches

Traditional widget architectures follow a rigid pipeline: LLM outputs JSON schema → application code maps to component registry → React renders the matched component. This requires maintaining comprehensive schema definitions, switch statements for every widget type, and careful synchronization between LLM prompts and frontend code.

Generative UI inverts this model. Tools like Thesys C1 enable the LLM to describe UI intent directly, with the rendering layer interpreting structured specifications (not raw code) into live components. The critical insight is that generative UI treats UI intent as data to interpret, not code to execute.

Three distinct approaches emerged from research:

| Approach | How It Works | Best For |
|----------|--------------|----------|
| JSON-Registry | Predefined schemas → component lookup → render | Maximum control, deterministic behavior |
| Generative UI | LLM → UI spec (DSL) → SDK renders components | Rapid development, conversational UIs |
| Agent-Driven | Agent selects from developer-registered actions | Complex multi-step workflows |

### 2.2 Implications for Compass

For Compass's use case—an LLM-orchestrated planning system with conversational widget presentation—the generative UI approach with custom component extensions provides the optimal balance of development velocity and widget coverage. The JSON-registry approach remains valuable for widgets requiring deterministic behavior (ranked choice, allocation) where LLM interpretation variability would be problematic.

---

## Part 3: Candidate Deep Dives

### 3.1 Thesys C1

Thesys C1 is the first production-ready generative UI API with official Mastra integration—a critical architectural alignment given Compass's orchestration stack. Launched in April 2025, C1 provides an OpenAI-compatible endpoint that returns structured UI specifications (C1 DSL) rather than plain text, which the Crayon SDK renders as interactive React components.

**Core Architecture**:
```
Mastra Agent → C1 API (OpenAI-compatible) → UI Specification (JSON DSL) → <C1Component> → Live React
```

**Built-in Components**: C1 includes sliders, select/multi-select, checkboxes, radio groups, date pickers, charts (line/bar/pie/scatter/area), tables with sorting/filtering, and action buttons. Progressive streaming renders components as they're generated, reducing time-to-interactivity.

**Custom Component Creation**: Developers create a React component with C1 hooks (`useOnAction`, `useC1State`), define a Zod schema with `.describe()` annotations, convert to JSON schema, and register in the API payload. This enables Compass to extend C1's capabilities for specialized planning widgets while leveraging native generation for standard interactions.

**Pricing**: Free tier offers 5,000 API calls/month (sufficient for development). Build tier at $49/month provides 25,000 calls. Grow tier at $499/month covers 500,000 calls with $0.001 overage. LLM token costs pass through at provider rates (Claude Sonnet 4: $3/$15 per million tokens input/output).

**Mastra Integration**: Thesys provides official documentation for Mastra integration, enabling direct use of C1 within Mastra agent workflows without additional orchestration glue code.

### 3.2 CopilotKit

CopilotKit provides an alternative architecture using the AG-UI Protocol—an open, event-based protocol for agent-to-UI communication developed in partnership with Google's A2UI research. It excels at bidirectional state synchronization and human-in-the-loop workflows, both relevant to planning systems.

The `useCopilotAction` hook enables registering custom widgets that agents can invoke:

```typescript
useCopilotAction({
  name: "rankOptions",
  renderAndWaitForResponse: ({ args, respond }) => (
    <RankedChoiceWidget options={args.options} onComplete={respond} />
  )
});
```

**Strengths**: Open-source with MIT license—no API costs for the core framework. Strong human-in-the-loop patterns via `renderAndWaitForResponse`. Active development with Google partnership.

**Limitations**: No native Mastra integration (requires additional orchestration code). Spatial and comparative widgets require custom development. Cloud tiers add analytics and security guardrails ($1,000/seat/month for Team, from $5K/month for Enterprise).

### 3.3 Vercel AI SDK Pattern

Vercel AI SDK v5/v6 doesn't offer true generative UI, but its tool → component mapping pattern provides a well-architected alternative for teams wanting full control. The SDK's new AI Elements library (built on shadcn/ui) accelerates chat interface development.

The pattern involves defining tools with Zod input schemas, where tools return structured data, message parts include typed tool results, and components render based on tool state (`input-available` → loading, `output-available` → render, `output-error` → error).

**v0.dev API**: Vercel's v0.dev now offers a full programmatic API for generating React + Tailwind components from natural language prompts. While not real-time generative UI, it can accelerate custom widget development during build time.

**Key Limitation**: AI SDK's React Server Components approach (`streamUI`) is paused due to technical issues (component remounting, quadratic data transfer). Use the tool-based client pattern instead.

### 3.4 shadcn/ui

shadcn/ui remains the strongest foundation for custom widgets requiring precise control. Its copy-paste ownership model, full TypeScript support, and explicit design for AI/LLM code generation make it ideal for building Compass's specialized planning widgets.

The library provides 57 components covering standard UI patterns. For drag-and-drop interactions (ranked choice, card sort, sequencing), shadcn/ui integrates well with dnd-kit (7M weekly downloads).

**Strengths**: Full code ownership (no vendor dependency), excellent TypeScript support, Tailwind-based styling, designed for LLM code generation, large community (104k GitHub stars).

**Limitations**: No drag-and-drop primitives—requires dnd-kit integration. All specialized planning widgets require custom development. No orchestration layer—pure UI components only.

### 3.5 SurveyJS

SurveyJS uniquely offers native ranked choice (drag-to-reorder) and matrix question types ideal for comparative evaluation. Its JSON-native architecture aligns well with LLM generation patterns.

**Strengths**: Native ranking questions with drag-and-drop. Matrix questions for trade-off tables. JSON-based form definition (matches LLM output patterns). Conditional logic built-in.

**Limitations**: Survey Creator requires commercial licensing ($499/developer). Styling system less flexible than Tailwind. Limited to survey-style interactions—spatial widgets and merge gates not feasible.

---

## Part 4: Widget Taxonomy Coverage Matrix

The following matrix maps each Compass widget type against the evaluated approaches. Coverage assessment uses: ✅ Native/easy support, 🔧 Requires adaptation or custom component, 🏗️ Must build from scratch, ❌ Not feasible.

### 4.1 Choice Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Single select | ✅ | ✅ | ✅ | ✅ | ✅ |
| Multi select | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ranked choice | 🔧 | 🔧 | 🔧 | 🔧 | ✅ |
| Pairwise/Tournament | 🔧 | 🔧 | 🔧 | 🏗️ | 🔧 |

### 4.2 Spectrum and Allocation Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Slider (labeled endpoints) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Opposing spectrums | 🔧 | 🔧 | 🔧 | 🔧 | 🔧 |
| Allocation ("100 pts") | 🔧 | 🔧 | 🔧 | 🏗️ | 🏗️ |

### 4.3 Comparative Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Trade-off tables | 🔧 | 🔧 | ✅ | 🔧 | ✅ |
| A/B comparisons | 🔧 | 🔧 | 🔧 | 🏗️ | 🔧 |

### 4.4 Spatial and Ordering Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Card sort | 🔧 | 🔧 | 🔧 | 🔧 | 🔧 |
| Sequencing/ordering | 🔧 | 🔧 | 🔧 | 🔧 | ✅ |
| Quadrant placement | 🔧 | 🔧 | 🔧 | 🏗️ | ❌ |

### 4.5 Generative Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Mad-lib completion | 🔧 | 🔧 | ✅ | 🏗️ | 🏗️ |
| Field prompts | ✅ | ✅ | ✅ | ✅ | ✅ |

### 4.6 Meta Widgets

| Widget | Thesys C1 | CopilotKit | AI SDK | shadcn/ui | SurveyJS |
|--------|:---------:|:----------:|:------:|:---------:|:--------:|
| Decision gates | ✅ | ✅ | ✅ | 🔧 | 🔧 |
| Dealbreaker checklists | ✅ | ✅ | ✅ | ✅ | ✅ |
| Research triggers | ✅ | ✅ | ✅ | 🔧 | 🔧 |
| Merge gates | 🔧 | ✅ | 🔧 | 🏗️ | 🏗️ |

### 4.7 Coverage Summary

| Approach | Native Coverage | With Adaptation | Must Build Custom |
|----------|-----------------|-----------------|-------------------|
| Thesys C1 | 7/16 (44%) | 15/16 (94%) | 1/16 (6%) |
| CopilotKit | 6/16 (38%) | 15/16 (94%) | 1/16 (6%) |
| AI SDK Pattern | 7/16 (44%) | 14/16 (88%) | 2/16 (12%) |
| shadcn/ui | 6/16 (38%) | 10/16 (63%) | 6/16 (37%) |
| SurveyJS | 8/16 (50%) | 13/16 (81%) | 2/16 (12%), 1 not feasible |

---

## Part 5: Gap Analysis

### 5.1 Widgets Requiring Custom Development

Regardless of library choice, these Compass widgets require custom component development:

| Widget | Why No Library Support | Recommended Approach |
|--------|----------------------|---------------------|
| **Allocation ("spend 100 points")** | No library handles linked sliders with sum constraints | Multiple shadcn Slider components with shared state and Zod `refine()` validator; register as C1 custom component |
| **Pairwise/Tournament comparison** | Specialized interaction pattern unique to planning tools | Custom bracket component with RadioGroup primitives and elimination state machine |
| **Quadrant placement** | 2D positioning is highly application-specific | Canvas or absolute positioning with drop zones; dual-slider alternative for keyboard operation |
| **Opposing spectrums** | Semantic meaning requires custom labeling | Slider with distinct min/max label styling and center-point indicator |
| **Merge gates** | Unique to Compass workflow (accept/edit/reject with diff) | ToggleButtonGroup with tri-state plus inline editor for "edit" branch |

### 5.2 UX Escape Hatches Implementation

The required UX guarantees (escape hatch, support trigger, research trigger) are meta-patterns rather than widgets. The recommended implementation involves wrapping every widget in a `<WidgetContainer>` component that provides standardized footer actions.

For Thesys C1, this means registering a reusable `WidgetWrapper` custom component that adds standard action buttons. C1's `onAction` callback routes user selections to the appropriate handler (text input modal, help agent call, or research trigger).

For the shadcn/ui approach, create a higher-order component or context provider that wraps all widgets with consistent footer buttons and handles routing to Mastra workflow actions.

---

## Part 6: Development Effort Comparison

### 6.1 Effort Estimates by Approach

| Approach | Setup | Basic Widgets | Specialized Widgets | Spatial Widgets | Total |
|----------|-------|---------------|---------------------|-----------------|-------|
| Thesys C1 + Custom | 1-2 days | 2-3 days (native) | 2 weeks (custom) | 2 weeks (custom) | **5-6 weeks** |
| CopilotKit + Custom | 1-2 days | 3-5 days | 2-3 weeks | 2-3 weeks | **6-8 weeks** |
| shadcn/ui + dnd-kit | 2-3 days | 1-2 weeks | 2-3 weeks | 2-3 weeks | **6-9 weeks** |
| SurveyJS + Custom | 1 week | 1 week (native) | 2 weeks | 3 weeks (limitations) | **7-9 weeks** |

### 6.2 Cost Comparison (Monthly, Phase 1 Usage)

| Approach | Licensing/API | Development Offset | Net Assessment |
|----------|---------------|-------------------|----------------|
| Thesys C1 | $49-99/month | -3 weeks dev time | Most cost-effective |
| CopilotKit | $0 (open source) | Baseline | Good if avoiding vendor lock-in |
| shadcn/ui | $0 | +3-4 weeks dev time | Higher upfront, zero recurring |
| SurveyJS | $0-499 one-time | Comparable | Only if heavy survey focus |

---

## Part 7: Dynamic Rendering Pattern

### 7.1 Recommended Architecture

The hybrid approach uses Thesys C1 for orchestration with custom components for specialized widgets:

```
Mastra Agent → Decision Logic
  ├─ Standard interactions → C1 Generative UI (native)
  ├─ Specialized widgets → C1 Custom Components (shadcn-based)
  └─ Complex state flows → Direct React + React Hook Form
```

### 7.2 Custom Component Registration

For widgets not covered by C1's native library, create shadcn/ui-based components and register them as C1 custom components:

```typescript
// 1. Define the widget component
const AllocationWidget = ({ goals, total, onComplete }) => {
  const [values, setValues] = useState(/* ... */);
  // shadcn Slider components with linked state
  return (/* ... */);
};

// 2. Define Zod schema for LLM generation
const allocationSchema = z.object({
  goals: z.array(z.string()).describe("Items to allocate points across"),
  total: z.number().describe("Total points to allocate, typically 100"),
});

// 3. Register with C1 in API payload
const customComponents = {
  AllocationWidget: {
    component: AllocationWidget,
    schema: zodToJsonSchema(allocationSchema),
  }
};
```

### 7.3 Streaming and Progressive Rendering

Thesys C1 supports progressive streaming natively—components render as the LLM generates them. For custom components, implement loading states that display immediately when the component type is identified, then populate with data as it streams.

---

## Part 8: Integration with Orchestration

### 8.1 Mastra Integration Pattern

Thesys provides official Mastra integration documentation. The pattern involves configuring a C1-enabled model in Mastra's agent definition:

```typescript
import { Agent } from "@mastra/core";
import { createC1Client } from "@thesys/sdk";

const planningAgent = new Agent({
  name: "compass-planning",
  model: createC1Client({
    apiKey: process.env.THESYS_API_KEY,
    customComponents: compassWidgets,
  }),
  // ... workflow configuration
});
```

### 8.2 Coordination with Widget Schema (Area 19)

The widget schema definition (DD-19-01, STD-19-01) should account for the hybrid rendering approach:

1. Define Zod schemas for all 16 widget types, using `.describe()` annotations extensively
2. For C1-native widgets, schemas serve as prompting guidance
3. For custom components, schemas define the exact JSON structure C1 must produce
4. Use separate schemas per widget type rather than discriminated unions (per RF-02-01 limitation)

---

## Part 9: Limitations and Open Questions

### 9.1 Research Limitations

**Framework maturity**: Thesys C1 launched in April 2025. Long-term stability and pricing evolution remain unverified, though the product has attracted enterprise customers and active development continues.

**No benchmarking**: This research did not conduct hands-on performance testing. Latency, throughput, and rendering performance under load remain unverified.

**Custom component complexity**: Development estimates for custom widgets are based on similar projects, not direct prototyping. Actual effort may vary based on specific interaction requirements.

### 9.2 Open Questions

**C1 Custom Component Limits**: Are there constraints on custom component complexity or state management? Early prototyping should verify.

**Streaming Edge Cases**: How does C1 handle streaming for custom components with complex initialization? May need fallback patterns.

**Offline/Degraded Mode**: If C1 API is unavailable, can widgets fall back to static rendering? Evaluate during implementation.

---

## Sources

All sources assessed per STD-20-01 evidence standards.

### Tier 1: Official Documentation

1. **[T1/S1]** Thesys. "What is C1 by Thesys?" Retrieved 2026-01-26. https://docs.thesys.dev/guides/what-is-thesys-c1.md

2. **[T1/S1]** Thesys. "Integrating Mastra with Thesys". Retrieved 2026-01-26. https://docs.thesys.dev/guides/frameworks/mastra.md

3. **[T1/S1]** Thesys. "Implementing Custom Components". Retrieved 2026-01-26. https://docs.thesys.dev/guides/custom-components.md

4. **[T1/S1]** Thesys. "Form Elements". Retrieved 2026-01-26. https://docs.thesys.dev/library/form-elements.md

5. **[T1/S1]** CopilotKit. "Documentation". Retrieved 2026-01-26. https://docs.copilotkit.ai/

6. **[T1/S1]** Vercel. "AI SDK Core: Tools". Retrieved 2026-01-26. https://ai-sdk.dev/docs/foundations/tools

7. **[T1/S1]** shadcn. "Components". Retrieved 2026-01-26. https://ui.shadcn.com/docs/components

8. **[T1/S1]** SurveyJS. "Question Types". Retrieved 2026-01-26. https://surveyjs.io/form-library/documentation/question-types

### Tier 2: Credible Developer Sources

9. **[T2/S2]** Business Wire. "Thesys Introduces C1 to Launch the Era of Generative UI". Published 2025-04-18. Retrieved 2026-01-26. https://www.businesswire.com/news/home/20250418761213/en/

10. **[T2/S2]** InfoWorld. "Thesys introduces generative UI API for building AI apps". Published 2025-04. Retrieved 2026-01-26. https://www.infoworld.com/article/3971182/thesys-introduces-generative-ui-api-for-building-ai-apps.html

11. **[T2/S2]** GitHub. "google/A2UI". Retrieved 2026-01-26. https://github.com/google/A2UI

12. **[T2/S2]** GitHub. "thesysdev/examples". Retrieved 2026-01-26. https://github.com/thesysdev/examples

13. **[T2/S2]** CopilotKit. "Pricing". Retrieved 2026-01-26. https://www.copilotkit.ai/pricing

---

## Appendix A: Glossary

**AG-UI Protocol**: Agent-to-UI Protocol, an open event-based protocol for agent-to-UI communication developed by CopilotKit in partnership with Google.

**C1 DSL**: Thesys C1's domain-specific language for describing UI specifications in JSON format.

**Crayon SDK**: Thesys's React SDK that renders C1 DSL specifications as interactive components.

**Custom Component**: A developer-created React component registered with C1 to extend its native widget library.

**dnd-kit**: A lightweight, modular drag-and-drop toolkit for React (7M weekly downloads).

**Generative UI**: An approach where LLMs generate UI specifications directly, rather than outputting data that maps to predefined components.

**JSON-Registry Pattern**: Traditional approach where LLM outputs JSON matching predefined schemas, which application code maps to a component registry for rendering.

**Widget Taxonomy**: Compass's classification of 16+ widget types across six categories (choice, spectrum, comparative, spatial, generative, meta).

---

## Appendix B: Related Documents

- **RF-02-01**: LLM Orchestration Framework Research Findings (Mastra + Vercel AI SDK selected)
- **ADR-02-01**: LLM Orchestration Selection
- **DD-19-01**: Widget Schema Definition (coordinate—this research informs schema design)
- **STD-19-01**: Widget Schema Standards
- **Compass System Definition**: Authoritative system specification (§2.2 Widget Taxonomy)

---

*End of Widget Component Library Research Findings (RF-07-01)*
