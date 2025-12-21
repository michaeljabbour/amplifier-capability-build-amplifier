---
bundle:
  name: dev
  version: 1.0.0
  description: Development overlay - adds debug settings

includes:
  - ./base.md

providers:
  - module: provider-anthropic
    config:
      debug: true
      raw_debug: true
      temperature: 0.7
---

Development mode enabled. You have access to verbose debugging output.
