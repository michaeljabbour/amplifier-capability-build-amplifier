# Build with Amplifier

Build the extension in the right place, against the current contracts.

People building Amplifier applications, bundles, tools, hooks, and providers. Use when adding an Amplifier capability, composing a client, or debugging the boundary between Foundation and Core.

## Install the portable method

```sh
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

Keep the complete `skills/build-amplifier` folder together. Installation copies only that method, references, and license; it starts no service and installs no runtime. Use a different skills-parent path for your host.

## Choose the mode

- **Place** — A request could become configuration, bundle, tool, hook, provider, or app code. A seam decision with inspected contracts and a smallest working slice.
- **Build** — The host and extension seam are known. A native implementation with cleanup, failure behavior, and contract checks.
- **Delegate** — The user explicitly asks to run work through Amplifier. A bounded runtime request and an attributed result; never implicit delegation.

## What was consolidated

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the local site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

Open `_site/index.html` or serve `_site` with a local static server. The downloadable ZIP is built from canonical method bytes. The fictional before/after example illustrates intended judgment; it is not a measured improvement. Nothing has been published or renamed remotely.
