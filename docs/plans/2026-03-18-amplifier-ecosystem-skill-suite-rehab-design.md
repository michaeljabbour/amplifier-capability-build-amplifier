# Amplifier Ecosystem Skill Suite Rehab Design

## Goal
Rehab the `amplifier-skill` repo from a single delegation-focused skill into a router-first, ecosystem-aware skill suite that quickly routes users to the right repo, docs, examples, workflow, and expert guidance across the Amplifier ecosystem.

## Background
The current repo is small and centered on a single skill at `amplifier-skill/SKILL.md`. Today it mainly covers deliberate Amplifier delegation, CLI preflight, runtime discovery, session inspection, and sandbox-safe fallbacks. That is useful, but it leaves major gaps in the broader ecosystem story.

The main missing areas are:
- core concepts and contracts
- Foundation examples and reusable patterns
- `amplifier-app-cli` as the real end-to-end validation surface
- recipes, bundles, and module taxonomy
- safe cross-repo workflows and testing order across `amplifier`, `amplifier-core`, `amplifier-foundation`, and `amplifier-app-cli`

The repo also likely still has README and install-path drift after the move into the `amplifier-skill/` subdirectory. The rehab therefore needs to cover both content and repo/package cleanup.

This suite must serve three audiences:
- Amplifier maintainers
- application builders embedding Amplifier
- bundle, agent, and module authors

## Approach
Use **Option 1: a router-first hybrid suite**.

The new repo should have one lean top-level skill plus focused companion skills. The priority order is:
1. **fast routing**
2. **safe execution workflow**
3. **conceptual teaching**

Most companion skills should be moderate depth. One heavier companion should focus on Foundation docs and examples.

The central design rule is:
- **embed stable guidance in the skills**
- **route volatile details to authoritative docs and expert agents**

This keeps the top-level experience fast and usable while avoiding a giant reference blob that will drift as the ecosystem changes.

## Architecture
The top-level skill is a **router and decision aid**. Its job is to identify:
- which repo is involved
- which layer is involved
- what kind of task the user has
- which docs, examples, companion skill, and expert agent are appropriate
- what the safe workflow is

The suite should be organized around **canonical-source awareness**, not around copying everything into one place. The skills should teach which source is canonical for each decision.

### Canonical source model
The design must explicitly encode and route around these mandatory canonical sources:
- `/Users/michaeljabbour/dev/amplifier/docs/MODULES.md`
- module development guidance from the Amplifier ecosystem
- bundle development guidance from Amplifier Foundation
- `/Users/michaeljabbour/dev/amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`
- `/Users/michaeljabbour/dev/amplifier/docs`
- `/Users/michaeljabbour/dev/amplifier-foundation/docs`
- `/Users/michaeljabbour/dev/amplifier-foundation/examples`

The suite should also explicitly teach cross-repo workflow guidance spanning:
- `amplifier`
- `amplifier-core`
- `amplifier-foundation`
- `amplifier-app-cli`

`amplifier-app-cli` should be treated as the true end-to-end validation surface for the stack.

## Components
### `amplifier-ecosystem-router`
Front door for the suite.

Responsibilities:
- classify the task by repo, layer, and intent
- route to the right companion skill
- route to the right canonical docs and examples
- point to the right expert agent when details are volatile or authoritative clarification is needed
- give the safe next-step workflow instead of only providing references

### `amplifier-cross-repo-workflows`
Cross-repo execution companion.

Responsibilities:
- explain dependency hierarchy and repo roles
- cover development order and push order across repos
- cover testing ladder and validation order
- explain local override vs shadow workflows
- teach why `amplifier-app-cli` is the real end-to-end validation surface

### `amplifier-core-concepts`
Core ecosystem concepts companion.

Responsibilities:
- explain kernel ideas
- cover the five module types
- explain orchestrators as the main engine
- explain session lifecycle
- explain hooks and events
- explain tool-vs-hook distinction
- explain kernel-vs-module philosophy

### `amplifier-module-and-bundle-development`
Mandatory authoring companion.

Responsibilities:
- distill `/Users/michaeljabbour/dev/amplifier/docs/MODULES.md`
- distill module development guidance from the Amplifier ecosystem
- distill bundle development guidance from Amplifier Foundation
- explain module vs bundle vs agent vs behavior distinctions
- cover common authoring pitfalls and when to consult expert agents

This companion is the canonical home for module and bundle authoring guidance in the suite.

### `amplifier-foundation-reference`
Heavier Foundation-focused reference companion.

Responsibilities:
- absorb the most important stable material from `/Users/michaeljabbour/dev/amplifier-foundation/docs`
- absorb the strongest example-driven material from `/Users/michaeljabbour/dev/amplifier-foundation/examples`
- distill the most important lessons from `/Users/michaeljabbour/dev/amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`
- become the main example-driven teaching asset in the suite

### `amplifier-app-integration`
Application embedding and integration companion.

Responsibilities:
- explain how to build applications on top of Amplifier
- use `APPLICATION_INTEGRATION_GUIDE.md` as a canonical anchor
- explain when validation must happen through real CLI and app flows
- connect app-building guidance back to `amplifier-app-cli` as the practical proof surface

## Data Flow
1. A user starts at `amplifier-ecosystem-router`.
2. The router classifies the request by:
   - repo
   - layer
   - intent
3. The router sends the user to the appropriate companion skill, canonical docs, examples, and expert agent.
4. The selected companion skill provides:
   - distilled stable concepts
   - the relevant workflow or checklist
   - source-of-truth pointers for volatile details
   - common mistakes to avoid
5. If the task spans multiple repos, `amplifier-cross-repo-workflows` provides the safe change order, testing order, and validation path.
6. If the task needs practical stack validation, the workflow ends at `amplifier-app-cli` rather than stopping at library-level checks.

The suite should therefore teach **source selection and safe workflow execution**, not just isolated facts.

## Error Handling
The main failure mode for this repo is stale or misallocated knowledge. The rehab should handle that by design.

Key rules:
- keep the router lean so it remains usable and current
- keep companion skills focused by domain
- embed stable mental models, not volatile implementation trivia
- route volatile details to authoritative docs and expert agents
- explicitly teach which source is canonical for which decision

Operationally, every skill should consistently state:
- what the skill is for
- when to use it
- what docs it distills
- what expert agents to consult
- what workflow or checklist applies
- what common mistakes to avoid

Repo-level errors should also be addressed during rehab:
- fix README and install-path drift
- align docs and package references with the actual repo layout
- add lightweight validation and sanity checks for helper scripts and router paths

## Testing Strategy
Validation for this rehab should cover both content and repo coherence.

Minimum validation:
- README and install instructions updated to match the repo after the `amplifier-skill/` restructure
- repo structure clearly matches the new suite architecture
- helper scripts receive lightweight repeatable validation or sanity checks
- router paths are sanity-checked against real task types

The router should be verified against at least these task classes:
- repo discovery and governance questions
- module work
- bundle and agent work
- app integration work
- cross-repo workflow decisions

## Acceptance Criteria
- A user can start from the router skill and reach the right companion quickly.
- Mandatory sources are explicitly covered:
  - `/Users/michaeljabbour/dev/amplifier/docs/MODULES.md`
  - module development guidance from the Amplifier ecosystem
  - bundle development guidance from Amplifier Foundation
  - `/Users/michaeljabbour/dev/amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`
- The suite teaches safe cross-repo execution, not just concepts.
- `amplifier-app-cli` is treated as the end-to-end validation surface.
- The heavier Foundation/examples companion becomes the main example-driven teaching asset.
- README, install-path, and docs cleanup are included in scope.
- Helper-script validation is included in scope.
- The repo no longer has packaging or documentation drift relative to the implemented suite structure.

## Open Questions
No blocking product or scope questions remain from the validated design. Exact file layout, naming details, and validation command choices can be finalized during implementation planning as long as they preserve this architecture, source-of-truth model, and acceptance criteria.
