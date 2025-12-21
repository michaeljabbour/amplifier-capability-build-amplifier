---
bundle:
  name: prod
  version: 1.0.0
  description: Production overlay - optimized settings

includes:
  - ./base.md
  - ./assets/bundles/base.md

providers:
  - module: provider-anthropic
    config:
      debug: false
      temperature: 0.3
      timeout: 60
---

Production mode. Responses optimized for reliability and consistency.
