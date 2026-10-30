# Build with Amplifier

Add the capability. Keep the architecture clear.

Watch the [70-second film](https://michaeljabbour.github.io/amplifier-skill-build-amplifier/#film): a copied conductor that cancel cannot stop, and how the skill finds the right seam before it builds. The example in it is fictional.

A working guide for people extending Amplifier. Find the right home for a feature, build one useful slice, and check that it behaves correctly inside the host you actually use.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-build-amplifier/) · [Read the method](skills/build-amplifier/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Choose the right seam.** Separate application interaction, reusable bundle wiring, callable tools, hooks and providers before adding code.
- **Keep the useful context.** Six substantial reference topics cover Core, Foundation, module authoring, application integration, routing and work across repositories.
- **Hand over a working slice.** Make inputs, errors, cancellation and cleanup explicit, with commands someone else can repeat.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-build-amplifier.git
cd amplifier-skill-build-amplifier
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/build-amplifier` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Build with Amplifier to inspect this repository. I want a progress panel for a long-running tool. Decide where the feature belongs, identify the actual event contract, and propose one slice with cancellation and cleanup checks.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Inspect the host.** Read its manifests, installed contracts and a neighboring implementation. Record what version the advice applies to.
2. **Build the smallest slice.** Agree the observable behavior and ownership, then implement through the seam that already owns it.
3. **Prove and hand over.** Check registration, success, invalid input, cancellation and cleanup; record installation and rollback.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional slice: import progress
UI owns: display and user cancellation
Core owns: tool execution
Contract: current host event schema, inspected revision recorded
Checks: success, error, cancel, listener cleanup
Open evidence: real-host run pending
```

## What is checked

The six-topic reference mirror, isolated helper regressions and complete portable installation are checked. These checks establish retained content and software behavior; a new extension still needs validation in its actual host. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

The current public source branch (`4beb46c…`) was merged normally into this candidate after the first local extraction. All six topics remain substantial, independently loadable references: [router](skills/build-amplifier/references/upstream-suite/amplifier-skill/METHOD.md), [Core concepts](skills/build-amplifier/references/upstream-suite/amplifier-core-concepts/METHOD.md), [module/bundle authoring](skills/build-amplifier/references/upstream-suite/amplifier-module-and-bundle-development/METHOD.md), [Foundation examples](skills/build-amplifier/references/upstream-suite/amplifier-foundation-reference/METHOD.md), [app integration](skills/build-amplifier/references/upstream-suite/amplifier-app-integration/METHOD.md), and [cross-repo workflow](skills/build-amplifier/references/upstream-suite/amplifier-cross-repo-workflows/METHOD.md). A generated source/output hash check prevents guide loss. [Current contract caveats](skills/build-amplifier/references/current-contracts.md) identify historical API/lifecycle claims that need installed-host verification.

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

## Repository migration

This repository was renamed from `amplifier-skill-build-amplifier` to `amplifier-capability-build-amplifier`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
