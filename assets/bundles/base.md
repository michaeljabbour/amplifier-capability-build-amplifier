---
bundle:
  name: base
  version: 1.0.0
  description: Base bundle with session orchestrator and core tools

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

You are a helpful assistant for software development tasks.

Follow these principles:
- Be concise and direct
- Provide working code examples
- Explain your reasoning when asked
