# Refactoring Plan: Migrate amplifier-app-cli to amplifier-foundation

**Status:** Draft
**Created:** 2025-12-20
**Author:** Claude Code analysis

## Executive Summary

This document evaluates how `amplifier-app-cli` could be refactored to make deeper use of `amplifier-foundation`. The analysis reveals that the CLI already uses foundation extensively for bundle operations and mentions. The remaining refactoring opportunities are primarily about **consolidation** rather than major architectural changes.

## Current State Analysis

### What amplifier-foundation Already Provides (Currently Used)

The CLI already imports and uses these foundation components:

| Component | Usage Location | Purpose |
|-----------|----------------|---------|
| `BundleRegistry` | `amplifier_app_cli/paths.py`, `amplifier_app_cli/lib/bundle_loader/` | Central bundle management |
| `Bundle`, `load_bundle`, `PreparedBundle` | `amplifier_app_cli/lib/bundle_loader/prepare.py` | Bundle loading workflow |
| `BundleModuleResolver` | `amplifier_app_cli/lib/bundle_loader/__init__.py` | Module resolution for bundles |
| `ContentDeduplicator`, `ContextFile` | `amplifier_app_cli/lib/mention_loading/` | @mention content deduplication |
| `format_directory_listing` | `amplifier_app_cli/lib/mention_loading/loader.py` | Directory listing for @mentions |
| `BaseMentionResolver` | `amplifier_app_cli/lib/mention_loading/app_resolver.py` | Bundle namespace resolution |
| `SimpleSourceResolver`, `SimpleCache` | `amplifier_app_cli/lib/bundle_loader/source_resolver.py` | URI resolution and caching |
| `DiskCache` | `amplifier_app_cli/lib/bundle_loader/source_resolver.py` | Persistent bundle cache |
| `get_amplifier_home` | `amplifier_app_cli/lib/bundle_loader/source_resolver.py` | Standard home directory |
| `check_bundle_status`, `refresh_bundle` | `amplifier_app_cli/commands/bundle.py`, `amplifier_app_cli/commands/update.py` | Bundle status management |

**Note:** These imports may fail if the installed `amplifier-foundation` version does not export all symbols. The foundation package is pinned to `main` branch which may have API drift.

### What Remains Local (Potential Migration Candidates)

| Local Code | Location | Migration Potential |
|------------|----------|---------------------|
| Text parsing (`parse_mentions`, etc.) | `amplifier_app_cli/utils/mentions.py` | Low - foundation has basic parsing but CLI needs `@~/` handling, quote exclusion, type extraction |
| App shortcuts (`@user:`, `@project:`, `@~/`) | `amplifier_app_cli/lib/mention_loading/app_resolver.py` | Low - app-layer policy by design |
| Collection resolution (deprecated) | `amplifier_app_cli/lib/mention_loading/app_resolver.py` | N/A - being removed |
| Well-known bundles registry | `amplifier_app_cli/lib/bundle_loader/discovery.py` | Low - app-layer policy |
| CLI search paths | `amplifier_app_cli/paths.py` | Low - app-layer policy |

## Refactoring Recommendations

### Phase 1: Add amplifier-foundation as Explicit Dependency

**Priority:** High
**Effort:** Low
**Risk:** Low
**Status:** COMPLETED (2025-12-20)

~~Currently, `amplifier-foundation` is used but not listed in `pyproject.toml` dependencies.~~

**UPDATE:** `amplifier-foundation` is already an explicit dependency in `pyproject.toml`:
- Line 16: Listed in `dependencies`
- Line 47: Source configured in `[tool.uv.sources]`

```toml
# pyproject.toml (current state)
dependencies = [
    # ...
    "amplifier-foundation",  # Already present
]

[tool.uv.sources]
amplifier-foundation = { git = "https://github.com/microsoft/amplifier-foundation", branch = "main" }
```

**Benefits achieved:**
- Explicit dependency management
- Version pinning capability
- Clearer architecture understanding

**Known Issue - API Drift:**
The foundation package is pinned to `main` branch, which may have API changes. The CLI code imports symbols like `BundleRegistry`, `PreparedBundle`, `check_bundle_status` that may not be exported in all versions. If tests fail with `ImportError`, verify the installed foundation version exports the expected symbols.

---

### Phase 2: Consolidate Mention Text Parsing

**Priority:** Low (was Medium)
**Effort:** Low
**Risk:** Low

**Current State:**
`utils/mentions.py` contains ~140 lines of regex-based @mention parsing:
- `parse_mentions()` - Extract @mentions from text
- `has_mentions()` - Check if text contains @mentions
- `extract_mention_path()` - Remove @ prefix
- `extract_mention_type()` - Classify mention type

**Investigation Result (2025-12-20):**
Foundation **does** have `parse_mentions()` in `amplifier_foundation.mentions.parser`, but the implementations differ:

| Feature | Foundation | CLI |
|---------|------------|-----|
| Excludes fenced code blocks (```) | ✓ | ✗ |
| Excludes inline code (`) | ✓ | ✓ |
| Excludes quoted strings | ✗ | ✓ |
| `@~/` home path handling | ✗ | ✓ |
| `has_mentions()` | ✗ | ✓ |
| `extract_mention_path()` | ✗ | ✓ |
| `extract_mention_type()` | ✗ | ✓ |
| Filters out "@mention" keyword | ✗ | ✓ |

**Recommendation:** Keep CLI's local implementation. The CLI has app-specific needs (`@~/` handling, quote exclusion, type extraction) that foundation doesn't provide. The overlap is minimal and the implementations serve different purposes.

**No migration recommended** - this is app-layer policy that should remain local.

---

### Phase 3: Evaluate AppMentionResolver Simplification

**Priority:** Low
**Effort:** Low
**Risk:** Low

**Current State:**
`AppMentionResolver` in `lib/mention_loading/app_resolver.py` (~290 lines) handles:
1. App shortcuts (`@user:`, `@project:`, `@~/`) - **App policy, keep local**
2. Bundle namespace delegation to foundation - **Already delegated**
3. Bundle mappings fallback - **Profile mode compatibility**
4. Collection resolution (deprecated) - **To be removed**
5. Relative path resolution - **App policy, keep local**

**Recommendation:**
The current design is correct per the kernel philosophy ("foundation provides mechanism, app provides policy"). The only change would be to **remove the deprecated collection resolution code** once collections are fully deprecated.

**No changes recommended** until collection deprecation is complete.

---

### Phase 4: Standardize Path Utilities

**Priority:** Low
**Effort:** Low
**Risk:** Low

**Current State:**
- `paths.py` uses `get_amplifier_home()` from foundation
- Local helpers like `_get_user_and_project_paths()` implement CLI-specific search path logic

**Investigation Required:**
Check if foundation provides:
- Standard search path patterns
- Path validation utilities
- Cross-platform path handling

**Likely Outcome:**
Most path logic is app-layer policy (search order, scope handling) and should remain local. Foundation's `get_amplifier_home()` is already the main reusable component.

---

### Phase 5: Bundle Loader Consolidation (Future)

**Priority:** Low (Dependent on Foundation Evolution)
**Effort:** High
**Risk:** Medium

**Current State:**
`lib/bundle_loader/` contains ~700 lines across 6 files:
- `discovery.py` - `AppBundleDiscovery` with well-known bundles and search paths
- `prepare.py` - Bridge functions to foundation's prepare workflow
- `source_resolver.py` - Thin wrapper around foundation's resolvers
- `resolvers.py` - App module resolver
- `user_registry.py` - User-added bundles persistence

**Analysis:**
Most of this code is **app-layer policy**:
- Well-known bundles (foundation, recipes) are CLI decisions
- Search paths are CLI decisions
- User registry is CLI-specific persistence

**Recommendation:**
Monitor foundation evolution. If foundation adds:
- Pluggable bundle discovery mechanisms
- Standard well-known bundle patterns
- User preference persistence APIs

Then revisit this code for potential migration.

---

## Implementation Order

| Phase | Description | Priority | Status |
|-------|-------------|----------|--------|
| 1 | Add explicit foundation dependency | High | **COMPLETED** (2025-12-20) |
| 2 | ~~Consolidate mention parsing~~ | ~~Low~~ | N/A - Investigation complete, no migration needed |
| 3 | Remove deprecated collection code | Low | Pending collection deprecation |
| 4 | Evaluate path utilities | Low | Pending |
| 5 | Bundle loader consolidation | Low | Pending foundation evolution |

## Architectural Principles to Preserve

The current codebase correctly follows key architectural principles that should be maintained:

### 1. Foundation Provides Mechanism, App Provides Policy
```
Foundation (mechanism):          App (policy):
- ContentDeduplicator            - Search path order
- BundleRegistry                 - Well-known bundles
- load_bundle(), prepare()       - @user:, @project: shortcuts
- BaseMentionResolver            - Collection resolution (deprecated)
```

### 2. Clean Layer Boundaries
```
┌─────────────────────────────────────────────────────────────┐
│ CLI Commands Layer (commands/)                               │
│   Uses paths.py factories to get configured components       │
├─────────────────────────────────────────────────────────────┤
│ App Policy Layer (paths.py, lib/)                           │
│   Configures foundation components with CLI-specific paths   │
├─────────────────────────────────────────────────────────────┤
│ Foundation Mechanism Layer (amplifier-foundation)            │
│   Generic, reusable components                               │
└─────────────────────────────────────────────────────────────┘
```

### 3. Dependency Injection Pattern
```python
# paths.py provides factories that inject CLI policy into foundation mechanisms
def create_bundle_registry(home: Path | None = None) -> BundleRegistry:
    """Factory injects CLI-specific configuration into foundation's BundleRegistry."""
    ...
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Foundation API breaking changes | Medium | High | Pin foundation version, run tests on upgrade |
| Over-migration (moving policy to foundation) | Low | Medium | Follow kernel philosophy strictly |
| Under-migration (duplicate code) | Low | Low | Regular audits against foundation capabilities |
| Test coverage gaps | Medium | Medium | Ensure test parity when migrating |

## Success Metrics

1. **Explicit dependency** - `amplifier-foundation` listed in `pyproject.toml`
2. **No duplicate code** - Text parsing utilities not duplicated if foundation provides them
3. **Clean boundaries** - App policy stays in app, mechanism in foundation
4. **Test parity** - All existing tests pass after migration
5. **Documentation** - Architecture decisions documented

## Open Questions

1. ~~**Does foundation provide @mention text parsing?**~~
   - **RESOLVED (2025-12-20):** Yes, foundation has `parse_mentions()` but CLI's version is more comprehensive with app-specific features (`@~/` handling, quote exclusion, type extraction). No migration needed - see Phase 2 investigation results.

2. **What's the timeline for collection deprecation?**
   - Affects when to remove collection resolution code

3. **Are there foundation APIs we're not using that we should be?**
   - Audit foundation's public API against our local implementations

## Next Steps

1. [ ] Review this plan with team
2. [x] Investigate foundation's mention parsing API (2025-12-20: Done - see Phase 2)
3. [ ] Create tracking issues for approved phases
4. [x] Implement Phase 1 (explicit dependency) - **COMPLETED** (2025-12-20: Already in pyproject.toml)
5. [x] Document findings from Phase 2 investigation (2025-12-20: Done - no migration needed)
6. [ ] Resolve foundation API drift (BundleRegistry import failures)

---

## Appendix A: Current Foundation Import Map

```
amplifier_app_cli/
├── commands/
│   ├── bundle.py
│   │   └── imports: BundleStatus, check_bundle_status, refresh_bundle
│   └── update.py
│       └── imports: BundleStatus, check_bundle_status, refresh_bundle
├── lib/
│   ├── bundle_loader/
│   │   ├── __init__.py
│   │   │   └── imports: Bundle, BundleRegistry, load_bundle, BundleModuleResolver, PreparedBundle
│   │   ├── discovery.py
│   │   │   └── imports: BundleRegistry
│   │   ├── prepare.py
│   │   │   └── imports: Bundle, load_bundle, PreparedBundle
│   │   └── source_resolver.py
│   │       └── imports: SimpleCache, SimpleSourceResolver, get_amplifier_home, DiskCache
│   └── mention_loading/
│       ├── __init__.py
│       │   └── imports: ContentDeduplicator, ContextFile
│       ├── app_resolver.py
│       │   └── imports: BaseMentionResolver (TYPE_CHECKING)
│       └── loader.py
│           └── imports: ContentDeduplicator, ContextFile, format_directory_listing
├── paths.py
│   └── imports: BundleRegistry
├── main.py
│   └── imports: PreparedBundle (TYPE_CHECKING)
├── runtime/config.py
│   └── imports: BundleRegistry, PreparedBundle (TYPE_CHECKING)
└── session_spawner.py
    └── imports: ContentDeduplicator
```

## Appendix B: Lines of Code Analysis

| Component | Lines | Foundation Usage | Migration Potential |
|-----------|-------|------------------|---------------------|
| `amplifier_app_cli/utils/mentions.py` | 140 | None | Low (CLI has app-specific needs) |
| `amplifier_app_cli/lib/mention_loading/loader.py` | 178 | High | Low (already using foundation) |
| `amplifier_app_cli/lib/mention_loading/app_resolver.py` | 288 | Medium | Low (app policy) |
| `amplifier_app_cli/lib/bundle_loader/discovery.py` | 384 | Medium | Low (app policy) |
| `amplifier_app_cli/lib/bundle_loader/prepare.py` | 182 | High | Low (thin wrapper) |
| `amplifier_app_cli/lib/bundle_loader/source_resolver.py` | 81 | High | Low (thin wrapper) |
| `amplifier_app_cli/paths.py` | 704 | Low | Low (app policy) |
| `amplifier_app_cli/main.py` | 2109 | Low | N/A (CLI entry) |
| `amplifier_app_cli/session_store.py` | 479 | None | N/A (filesystem only) |
| `amplifier_app_cli/session_spawner.py` | 355 | Medium | Low (uses core) |
| `amplifier_app_cli/commands/` (total) | 6120 | Low | N/A (CLI commands) |
